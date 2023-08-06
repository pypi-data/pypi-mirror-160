import os
import sys
import arcpy

# creates a new gdb and loads the layers for county zoning

# Set local variables
out_path = "S:/maps/ZONING/ZoningRemap2018"
out_name = "BentonZoning2022_DRAFT.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_path, out_name)

out_gdb = "S:/maps/ZONING/ZoningRemap2018/BentonZoning2022_DRAFT.gdb"


in_gdb = "S:/maps/BentonCountyGIS/Zoning_Information/Zoning.gdb"
arcpy.env.workspace = in_gdb

# features in gdb
fcs = arcpy.ListFeatureClasses()

# keep airport, floodplain, greenway, zoning 2020
del fcs[11]
del fcs[2:9]


# Copy shapefiles to a file geodatabase
for fc in fcs:
    arcpy.CopyFeatures_management(fc, os.path.join(out_gdb, os.path.splitext(fc)[0]))

arcpy.env.workspace = "S:/maps/ZONING/ZoningRemap2018/zoning_jan2022/ugb_draft"

layers = ["philomath_ugb_draft.shp",
          "ugb_draft_apr2022.shp",
          "ugb_draft_dec2021.shp",
          ]

arcpy.FeatureClassToGeodatabase_conversion(layers, out_gdb)

arcpy.env.workspace = "P:\\ArcGIS"
aprx = arcpy.mp.ArcGISProject("CURRENT")
map = aprx.listMaps()[0]
arcpy.CreateVectorTilePackage_management(map, 'nfi_draft.vtpk', "ONLINE", "", "INDEXED")


