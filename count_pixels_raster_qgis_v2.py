from os import path
import struct
from osgeo import gdal

# change path file to save
pathfile = 'pytest.txt'

def countRasterValue(val):

    layer = iface.activeLayer()
    provider = layer.dataProvider()

    fmttypes = {'Byte':'B', 'UInt16':'H', 'Int16':'h', 'UInt32':'I', 'Int32':'i', 'Float32':'f', 'Float64':'d'}

    my_path = provider.dataSourceUri()

    (root, filename) = path.split(my_path)

    dataset = gdal.Open(my_path)

    band = dataset.GetRasterBand(1)

    print "\nrows = %d columns = %d" % (band.YSize, band.XSize)
    with open(pathfile, 'a') as the_file:
        the_file.write("\nrows = %d columns = %d\n" % (band.YSize, band.XSize))
   
    BandType = gdal.GetDataTypeName(band.DataType)

   # print "Data type = ", BandType
   # with open('pytest.txt', 'a') as the_file:
   #     the_file.write("Data type = ", BandType)

    print "Executing for %s" % filename
    with open(pathfile, 'a') as the_file:
        the_file.write("Executing for %s\n" % filename)
    
    print "in %s" % root
    with open(pathfile, 'a') as the_file:
        the_file.write("in %s\n" % root)

    count_value = 0

    for y in range(band.YSize):

        scanline = band.ReadRaster(0, y, band.XSize, 1, band.XSize, 1, band.DataType)
        values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)

        for value in values:
            if value == val:
                count_value += 1

    print "Raster count = %d of %d" % (count_value, val)
    
    with open(pathfile, 'a') as the_file:
        the_file.write("Raster count = %d of %d\n" % (count_value, val))
        
    dataset = None
    
    return count_value

count = 0
for i in range(1,20):
    count = count + countRasterValue(i)
    
print "\nAmount of pixels in image is %d" % (count)

with open(pathfile, 'a') as the_file:
    the_file.write("\nAmount of pixels in image is %d\n\n\n" % (count))

