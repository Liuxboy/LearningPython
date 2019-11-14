#coding=utf-8
import arcpy
import sys
import time
import os
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')

def MakeFolder_raster(inputFileRoot):
    path = inputFileRoot + '\\' + 'raster'
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    for i in ['fifteen', 'thirty', 'sixty','finalResult','temp']:
        isExists = os.path.exists(path + '\\' + i)
        if not isExists:
            os.makedirs(path + '\\' + i)

country = 'Mexico'
arcpy.CheckOutExtension('Spatial')
desc = arcpy.Describe(r'G:\project\osm\overlay' + '\\' + country + '\\' + country + '.shp')
lyrVecPath = os.path.join(desc.path, "{0}.shp".format(country))
arcpy.env.extent = lyrVecPath  ##处理范围
arcpy.env.mask = lyrVecPath  ##掩膜
arcpy.env.overwriteOutput = True
inputFileRoot = r'G:\project\osm\overlay' + '\\' + country
arcpy.env.workspace = inputFileRoot


MakeFolder_raster(inputFileRoot)

#################制作栅格模板
def MakeRasterTemplate(fileRoot, item, newTempDir, timeItem):
    arcpy.env.scratchWorkspace = newTempDir

    outIsNull = arcpy.sa.IsNull(fileRoot + "\\" + 'raster' + '\\' + timeItem + '\\' + item)
    outCon = arcpy.sa.Con(outIsNull == 0, 1, 0)
    outCon.save(fileRoot + '\\' + 'raster' + '\\' + timeItem + '\\' + 'finalResult''\\' + item.split('.')[0] + 'all.tif')#'finalResult1_initial.tif')

if __name__ == '__main__':
    ################运行前删除raster下的temp文件夹!!!!!!!!!!!!#########
    print("CPU_Number", str(multiprocessing.cpu_count()))
    multiprocessing.freeze_support()

    print 'MakeRasterTemplate'
    time1 = time.time()
    results = []
    MyGPpool = multiprocessing.Pool()

    time1 = time.time()
    for timeItem in ['fifteen', 'thirty', 'sixty']:
        files = os.listdir(inputFileRoot + '\\' + 'raster' + '\\' + timeItem)
        count = 0
        for item in files:
            if item[-4:] == '.tif':
                count = count + 1
                if count == 1:
                    newTempDir = inputFileRoot + '\\' + 'raster' + '\\' + 'temp' + '\\' + timeItem + '\\' + item.split('.')[0]
                    os.makedirs(newTempDir)

                    result = MyGPpool.apply_async(MakeRasterTemplate, args=(inputFileRoot, item, newTempDir, timeItem,))
                    results.append(result)
                elif count == 5:
                    break
    MyGPpool.close()
    MyGPpool.join()
    time2 = time.time()
    print('MakeRasterTemplate need time', (time2 - time1) / 60, '\n')