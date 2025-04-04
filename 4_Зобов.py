from osgeo import gdal
from qgis.core import QgsProject

input_raster_path = r'C:/Users/st129923/Downloads/2.tif'
output_raster_path = r'C:/Users/st129923/DownLoads/out_2.tif'

footprint_path = r'C:/Users/st129923/Downloads/footprint_2.geojson'

f = gdal.Open(input_raster_path)

bands = []
for i in range(1, f.RasterCount+1):
    band = f.GetRasterBand(i)
    bands.append(band.ReadAsArray().astype(float))
    
driver = gdal.GetDriverByName('GTiff')
copy = driver.Create(
    output_raster_path, 
    f.RasterXSize,
    f.RasterYSize, 
    f.RasterCount,
    gdal.GDT_Float32
)

#print(bands)

for i in range(len(bands)):
    copy.GetRasterBand(i+1).WriteArray(bands[i])
  
footprint_layer = QgsProject.instance().addMapLayer(QgsVectorLayer(footprint_path, 'footprint_2', 'ogr'))
feature = footprint_layer.getFeature(0)
geometry = feature.geometry().asPolygon()[0]

copy.SetProjection(footprint_layer.crs().toWkt())

coords = []
for i in geometry[:4]:
    coords.append((i.x(), i.y()))
gcp = []
width = copy.RasterXSize
height = copy.RasterYSize
gcp.append(gdal.GCP(coords[0][0], coords[0][1], 0, 0, 0))
gcp.append(gdal.GCP(coords[1][0], coords[1][1], 0, width - 1, 0))
gcp.append(gdal.GCP(coords[2][0], coords[2][1], 0, width - 1, height - 1))
gcp.append(gdal.GCP(coords[3][0], coords[3][1], 0, 0, height - 1))

copy.SetGCPs(gcp,footprint_layer.crs().toWkt())
copy.FlushCache()


                                                                                  