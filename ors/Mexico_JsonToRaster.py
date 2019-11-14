# coding=utf-8
import arcpy
import sys
import time
import os
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf-8')


def MakeFolder_shp(inputFileRoot):
	path = inputFileRoot + '\\' + 'shapefile'
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
	for i in ['fifteen', 'thirty', 'sixty', 'allTime', 'temp']:
		isExists = os.path.exists(path + '\\' + i)
		if not isExists:
			os.makedirs(path + '\\' + i)


def MakeFolder_raster(inputFileRoot):
	path = inputFileRoot + '\\' + 'raster'
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
	for i in ['fifteen', 'thirty', 'sixty', 'finalResult', 'temp']:
		isExists = os.path.exists(path + '\\' + i)
		if not isExists:
			os.makedirs(path + '\\' + i)


####  arcpy相关设置
country = 'Mexico'
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True
inputFileRoot = r'G:\project\osm\overlay' + '\\' + country
arcpy.env.workspace = inputFileRoot

###创建文件夹
MakeFolder_shp(inputFileRoot)
MakeFolder_raster(inputFileRoot)


####json 转 shp###########
def JsonToShp(fileRoot, item):
	arcpy.JSONToFeatures_conversion(fileRoot + '\\' + 'json' + '\\' + item,
	                                fileRoot + '\\' + 'shapefile' + '\\' + 'allTime' + '\\' + item.split('.')[
		                                0] + '.shp')


#####拆分shp
def SplitShp(fileRoot, item):
	arcpy.FeatureClassToFeatureClass_conversion(fileRoot + '\\' + 'shapefile' + '\\' + 'allTime' + '\\' + item,
	                                            fileRoot + '\\' + 'shapefile' + '\\' + 'fifteen', \
	                                            item.split('.')[0] + '_15.shp', where_clause="Time_Mins = 15")

	arcpy.FeatureClassToFeatureClass_conversion(fileRoot + '\\' + 'shapefile' + '\\' + 'allTime' + '\\' + item,
	                                            fileRoot + '\\' + 'shapefile' + '\\' + 'thirty', \
	                                            item.split('.')[0] + '_30.shp', where_clause="Time_Mins = 30")

	arcpy.FeatureClassToFeatureClass_conversion(fileRoot + '\\' + 'shapefile' + '\\' + 'allTime' + '\\' + item,
	                                            fileRoot + '\\' + 'shapefile' + '\\' + 'sixty', \
	                                            item.split('.')[0] + '_60.shp', where_clause="Time_Mins = 60")


#####修复shp中的问题
def ShpFixGeometry(fileRoot, item, newTempDir, timeItem):
	###检查几何
	arcpy.env.scratchWorkspace = newTempDir
	out_table = newTempDir + '\\' + 'outputTable'
	arcpy.CheckGeometry_management(fileRoot + '\\' + 'shapefile' + '\\' + timeItem + '\\' + item, out_table)

	###修复几何
	fcs = []
	for row in arcpy.da.SearchCursor(out_table, ("CLASS")):
		if not row[0] in fcs:
			fcs.append(row[0])
	for fc in fcs:
		# print("Processing " + fc)
		lyr = 'temporary_layer'
		if arcpy.Exists(lyr):
			arcpy.Delete_management(lyr)

		tv = "cg_table_view"
		if arcpy.Exists(tv):
			arcpy.Delete_management(tv)

		arcpy.MakeTableView_management(out_table, tv, ("\"CLASS\" = '%s'" % fc))
		arcpy.MakeFeatureLayer_management(fc, lyr)
		arcpy.AddJoin_management(lyr, arcpy.Describe(lyr).OIDFieldName, tv, "FEATURE_ID")
		arcpy.RemoveJoin_management(lyr, os.path.basename(out_table))
		arcpy.RepairGeometry_management(lyr)


#########shp转栅格
def ShpToRaster(fileRoot, item, timeItem):
	arcpy.PolygonToRaster_conversion(fileRoot + '\\' + 'shapefile' + '\\' + timeItem + '\\' + item, "FID",
	                                 fileRoot + '\\' + 'raster' + '\\' + timeItem + '\\' + item.split('.')[0] + '.tif',
	                                 cellsize=0.0003)


if __name__ == '__main__':
	################运行前删除raster下的temp文件夹#########
	print("CPU_Number", str(multiprocessing.cpu_count()))
	multiprocessing.freeze_support()

	print('JsonToShp')
	time1 = time.time()
	results = []
	MyGPpool = multiprocessing.Pool()  # 进程池
	files = os.listdir(inputFileRoot + '\\' + 'json')  ####获取该文件下的所有文件
	for item in files:
		result = MyGPpool.apply_async(JsonToShp, args=(inputFileRoot, item,))  ##多进程处理
		results.append(result)
	MyGPpool.close()
	MyGPpool.join()
	time2 = time.time()
	print(u"JsonToShp need time:", (time2 - time1) / 60, '\n')

	print('SplitShp')
	time1 = time.time()
	results = []
	MyGPpool = multiprocessing.Pool()  # 进程池
	files = os.listdir(inputFileRoot + '\\' + 'shapefile' + '\\' + 'allTime')
	for item in files:
		if item[-4:] == '.shp':
			result = MyGPpool.apply_async(SplitShp, args=(inputFileRoot, item,))  ##多进程处理
			results.append(result)
	MyGPpool.close()
	MyGPpool.join()
	time2 = time.time()
	print("SplitShp need time:", (time2 - time1) / 60, '\n')

	print('ShpFixGeometry')
	time1 = time.time()
	results = []
	MyGPpool = multiprocessing.Pool()  # 进程池

	for timeItem in ['fifteen', 'thirty', 'sixty']:
		files = os.listdir(inputFileRoot + '\\' + 'shapefile' + '\\' + timeItem)
		for item in files:
			if item[-4:] == '.shp':
				newTempDir = inputFileRoot + '\\' + 'shapefile' + '\\' + 'temp' + '\\' + timeItem + '\\' + \
				             item.split('.')[0]
				os.makedirs(newTempDir)

				result = MyGPpool.apply_async(ShpFixGeometry,
				                              args=(inputFileRoot, item, newTempDir, timeItem,))  ##多进程处理
				results.append(result)
	MyGPpool.close()
	MyGPpool.join()
	time2 = time.time()
	print("ShpFixGeometry need time:", (time2 - time1) / 60, '\n')

	print('ShpToRaster')
	time1 = time.time()
	results = []
	MyGPpool = multiprocessing.Pool()
	for timeItem in ['fifteen', 'thirty', 'sixty']:
		count = 0
		files = os.listdir(inputFileRoot + '\\' + 'shapefile' + '\\' + timeItem)
		for item in files:
			if item[-4:] == '.shp':
				result = MyGPpool.apply_async(ShpToRaster, args=(inputFileRoot, item, timeItem,))
				results.append(result)
	MyGPpool.close()
	MyGPpool.join()
	time2 = time.time()
	print('RasterToDat need time', (time2 - time1) / 60, '\n')
