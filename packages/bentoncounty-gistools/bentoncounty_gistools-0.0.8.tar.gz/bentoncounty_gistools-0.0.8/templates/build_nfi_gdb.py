# Import system modules
import os
import sys
import arcpy

# creates a new gdb and loads the layers for natural features inventory

# Set local variables
out_path = "S:\\maps\\ZONING\\natural_features_redraft"
out_name = "NaturalFeaturesInventory2022.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_path, out_name)

out_gdb = "S:\\maps\\ZONING\\natural_features_redraft\\NaturalFeaturesInventory2022.gdb"


# from bcc 88.050.8a
# mapped areas are divided into three categories:
# Protected Prairie and Savanna;
# High Protection Significant Vegetation (HPSV);
# and Partial Protection Significant Vegetation (PPSV)

# workspace for oak savanna
arcpy.env.workspace = "S:\\maps\\ZONING\\Natural_Features_Inventory\\Features"

# shapefiles to copy to gdb
layers = [
    "Brainard_Listed_Top_Upland_Prairies_and_Oak_Savanna.shp",
    "Local_Streams_50ft_TOB_Buffer.shp",
    "Local_Streams_75ft_TOB_Buffer.shp",
    "Local_Streams_100ft_TOB_Buffer.shp",
    "Riparian_Corridor_Downtown.shp",
]

# copy files to gdb
arcpy.FeatureClassToGeodatabase_conversion(layers, out_gdb)

# workspace for high protection incentive vegetation
arcpy.env.workspace = "S:\\maps\\ZONING\\natural_features_redraft\\incveg\\incveg_high"

# file gdb location
out_gdb = "S:\\maps\\ZONING\\natural_features_redraft\\NaturalFeaturesInventory2022.gdb"

# vector of file names to copy to gdb
high_protection = [
    "incveg_high_1of9.shp",
    "incveg_high_2of9.shp",
    "incveg_high_3of9.shp",
    "incveg_high_4of9.shp",
    "incveg_high_5of9.shp",
    "incveg_high_6of9.shp",
    "incveg_high_7of9.shp",
    "incveg_high_8of9.shp",
    "incveg_high_9of9.shp",
]

# copy files to gdb
arcpy.FeatureClassToGeodatabase_conversion(high_protection, out_gdb)

# Set workspace to partial protection incentive vegetation
arcpy.env.workspace = "S:\\maps\\ZONING\\natural_features_redraft\\incveg\\incveg_part"

# vector of file names to copy to gdb
partial_protection = [
    "incveg_part_1of7.shp",
    "incveg_part_2of7.shp",
    "incveg_part_3of7.shp",
    "incveg_part_4of7.shp",
    "incveg_part_5of7.shp",
    "incveg_part_6of7.shp",
    "incveg_part_7of7.shp",
]

# copy files to gdb
arcpy.FeatureClassToGeodatabase_conversion(partial_protection, out_gdb)


arcpy.env.workspace = (
    "S:\\maps\\ZONING\\Natural_Features_Inventory\\NaturalFeaturesInventory2021"
)
layers = [
    "riparian_buffer_120ft.shp",
    "riparian_wetlands.shp",
    "locally_significant_wetlands.shp",
    "local_wetland_inventory.shp",
    "landslide_risk.shp",
]
arcpy.FeatureClassToGeodatabase_conversion(layers, out_gdb)


arcpy.env.workspace = "S:\\maps\\ZONING\\Natural_Features_Inventory\\Hazards"
layers = [
    "2tenthsft_Floodway.shp",
    "Dixon_flooding.shp",
    "Dunawi_Flooding.shp",
    "Jackson_Frazier.shp",
    "Lewisburg_flood.shp",
    "Oak_Creek_flooding.shp",
    "Sequoia_Flooding.shp",
    "Village_Green_Flooding.shp",
    "Fema_100yr_Will-Mary.shp",
    "Open_Channel_Landslide.shp",
    "Confined_Channel_Landslide.shp",
    "Steep_Slopes.shp",
    "Streams.shp",
]
arcpy.FeatureClassToGeodatabase_conversion(layers, out_gdb)
