# -*- coding: utf-8 -*-
import multiprocessing
import os
import sys
import time
import arcpy

# python3不需要下面两行
# reload(sys)
# sys.setdefaultencoding('utf-8')

####  arcpy相关设置
country = 'Athen'
# type = 'walk'                                         ###  hgv   car  walk  cycling
typeList = ['hgv', 'car', 'walk', 'cycling']  # ,
resolution = 500
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True
inputFileRoot = r'G:\project\osm\overlay' + '\\' + country
arcpy.env.workspace = inputFileRoot


def MakeFolder_shp(inputFileRoot):
    path = inputFileRoot + '\\' + 'shapefile' + '_' + str(resolution)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

    for type in typeList:
        if type == "walk":
            for i in [type + '_fifteen' + '_' + str(resolution), type + '_thirty' + '_' + str(resolution),
                      type + '_sixty' + '_' + str(resolution), 'temp']:
                isExists = os.path.exists(path + '\\' + i)
                if not isExists:
                    os.makedirs(path + '\\' + i)
        else:
            for i in [type + '_fifteen' + '_' + str(resolution), type + '_thirty' + '_' + str(resolution),
                      type + '_sixty' + '_' + str(resolution), 'temp']:
                isExists = os.path.exists(path + '\\' + i)
                if not isExists:
                    os.makedirs(path + '\\' + i)


def MakeFolder_raster(inputFileRoot):
    path = inputFileRoot + '\\' + 'raster' + '_' + str(resolution)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

    for type in typeList:
        if type == "walk":
            for i in [type + '_fifteen' + '_' + str(resolution), type + '_thirty' + '_' + str(resolution),
                      type + '_sixty' + '_' + str(resolution), type + '_finalResult' + '_' + str(resolution), 'temp']:
                isExists = os.path.exists(path + '\\' + i)
                if not isExists:
                    os.makedirs(path + '\\' + i)
        else:
            for i in [type + '_fifteen' + '_' + str(resolution), type + '_thirty' + '_' + str(resolution),
                      type + '_sixty' + '_' + str(resolution), type + '_finalResult' + '_' + str(resolution), 'temp']:
                isExists = os.path.exists(path + '\\' + i)
                if not isExists:
                    os.makedirs(path + '\\' + i)


####json 转 shp###########
def JsonToShp(fileRoot, item, type, timeItem):
    arcpy.JSONToFeatures_conversion(
        fileRoot + '\\' + 'json' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
            resolution) + '\\' + item,
        fileRoot + '\\' + 'shapefile' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
            resolution) + '\\' + item.split('.')[0] + '_' + str(resolution) + '.shp')


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
def ShpFixGeometry(fileRoot, item, newTempDir, timeItem, type):
    ###检查几何
    arcpy.env.scratchWorkspace = newTempDir
    out_table = newTempDir + '\\' + 'outputTable'
    arcpy.CheckGeometry_management(
        fileRoot + '\\' + 'shapefile' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
            resolution) + '\\' + item, out_table)

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
def ShpToRaster(fileRoot, item, timeItem, type):
    arcpy.PolygonToRaster_conversion(
        fileRoot + '\\' + 'shapefile' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
            resolution) + '\\' + item, "FID",
        fileRoot + '\\' + 'raster' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
            resolution) + '\\' + item.split('.')[0] + '.tif', cellsize=0.00054)


if __name__ == '__main__':
    ################运行前删除shapefile 和 raster下的temp文件夹#########

    ###创建文件夹
    MakeFolder_shp(inputFileRoot)  # , type)
    MakeFolder_raster(inputFileRoot)  # , type)

    print("CPU_Number", str(multiprocessing.cpu_count()))
    multiprocessing.freeze_support()

    print('JsonToShp')
    MyGPpool = multiprocessing.Pool()  # 进程池
    time1 = time.time()
    for type in typeList:
        if type == "walk":
            timeList = ['fifteen', 'thirty', 'sixty']
        else:
            timeList = ['fifteen', 'thirty', 'sixty']

        for timeItem in timeList:
            files = os.listdir(
                inputFileRoot + '\\' + 'json' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
                    resolution))  ####获取该文件下的所有文件
            for item in files:
                result = MyGPpool.apply_async(JsonToShp, args=(inputFileRoot, item, type, timeItem,))  ##多进程处理
    MyGPpool.close()
    MyGPpool.join()
    time2 = time.time()
    print(u"JsonToShp need time:", (time2 - time1) / 60, '\n')

    print('ShpFixGeometry')
    time1 = time.time()
    MyGPpool = multiprocessing.Pool()  # 进程池
    for type in typeList:
        if type == "walk":
            timeList = ['fifteen', 'thirty', 'sixty']
        else:
            timeList = ['fifteen', 'thirty', 'sixty']

        for timeItem in timeList:
            files = os.listdir(
                inputFileRoot + '\\' + 'shapefile' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
                    resolution))
            for item in files:
                if item[-4:] == '.shp':
                    newTempDir = inputFileRoot + '\\' + 'shapefile' + '_' + str(
                        resolution) + '\\' + 'temp' + '\\' + type + '_' + timeItem + '_' + str(resolution) + '\\' + \
                                 item.split('.')[0]
                    os.makedirs(newTempDir)

                    result = MyGPpool.apply_async(ShpFixGeometry,
                                                  args=(inputFileRoot, item, newTempDir, timeItem, type,))  ##多进程处理
    MyGPpool.close()
    MyGPpool.join()
    time2 = time.time()
    print("ShpFixGeometry need time:", (time2 - time1) / 60, '\n')

    print('ShpToRaster')
    time1 = time.time()
    results = []
    MyGPpool = multiprocessing.Pool()
    for type in typeList:
        if type == "walk":
            timeList = ['fifteen', 'thirty', 'sixty']
        else:
            timeList = ['fifteen', 'thirty', 'sixty']
        for timeItem in timeList:
            files = os.listdir(
                inputFileRoot + '\\' + 'shapefile' + '_' + str(resolution) + '\\' + type + '_' + timeItem + '_' + str(
                    resolution))
            for item in files:
                if item[-4:] == '.shp':
                    result = MyGPpool.apply_async(ShpToRaster, args=(inputFileRoot, item, timeItem, type,))
    MyGPpool.close()
    MyGPpool.join()
    time2 = time.time()
    print('ShpToRaster need time', (time2 - time1) / 60, '\n')
