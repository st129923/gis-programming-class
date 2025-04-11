ds_st = QgsProject.instance().mapLayersByName("stations")[0]
ds_dtr = QgsProject.instance().mapLayersByName("districts")[0]

b_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', "station_copy", "memory")
prov = b_layer.dataProvider()
prov.addAttributes(ds_st.fields())
b_layer.updateFields()
for feature in ds_st.getFeatures():
    val = feature["random_1"]
    b_d = val * 25
    n_f = QgsFeature()
    n_f.setGeometry(QgsGeometry.fromPointXY(feature.geometry().asPoint()).buffer(b_d, 8))
    n_f.setAttributes(feature.attributes())
    prov.addFeature(n_f)
    station.updateExtents()
#QgsProject.instance().addMapLayer(b_layer)

fid = []
for b in b_layer.getFeatures():
    for d in ds_dtr.getFeatures():
        if b.geometry().intersects(d.geometry()) and b["colour"] == "blue":
            fid.append(d.id())
ds_dtr.select(fid)




