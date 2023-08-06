from arcgis.gis import GIS
from arcgis.mapping import WebMap
from bentoncounty_gistools import bentoncounty_gistools as bc
from bentoncounty_gistools import template as tp
import os
from dotenv import load_dotenv

# import json

# load user name, password and template directory from .env
load_dotenv()
ARCGIS_USERNAME = os.getenv("ARCGIS_USERNAME")
ARCGIS_PASSWORD = os.getenv("ARCGIS_PASSWORD")
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR")

TEST_AERIAL_IMAGERY_MAP = "11cb9fbee4524770949d6a4b4db5f080"
TEST_ADDRESS_MAP = "a08fb19797cb4e61b1536fbc4961cce6"
TEST_ANNO_0020_MAP = "63d113c5b06940bd9acd82eaa740ff31"
TEST_ANNO_0050_MAP = "39be32a0a607428cb19affee732c64f9"
TEST_BOUNDARIES_MAP = "3c1a1c04eeb2404380365b00d7d2ecb6"
TEST_CONTOURS_MAP = "0b7ae5ebff5f4859b6c4696b556ebb47"
TEST_COUNTY_BASEMAP = "50ef97f3f25742fe9f8954948ad18b63"
TEST_ENVIRONMENT_MAP = "313f8d220cbe4c40b052a69c942e9bcc"
TEST_HCP_BUTTERFY_MAP = "9cd23c96be10410ba85c1c9329bd292d"
TEST_HPSV_MAP = "6c2e1b71533d4755a0b455fef2264fd6"
TEST_NATURAL_LAYERS_MAP = "9b3770d8ef684e529690f3956cc19e1a"
TEST_NFI_FEATURES_MAP = "d2608a049bed4d4b8b29c87608110137"
TEST_NFI_FLOOD_MAP = "23020f6d205c4e27bd28ae183adef5a7"
TEST_NFI_HAZARD_MAP = "692cf8d0949b40e380decdc2b7ad3b54"
TEST_NFI_MAP = "df21a6eb07ea439c80092ddcb2cf7108"
TEST_PPSV_MAP = "2a2bd64af0c747cdafcacf54f94c6e65"
TEST_RIPARIAN_MAP = "6dc956a2be7847b5a031df1973245f96"
TEST_SURVEY_MAP = "7ff1b1363e204b0396f56c6270c1bfbc"
TEST_TAXLOT_MAP = "c98a7f2f24974e09ac1a44017aa5774a"
TEST_TRANSPORTATION_MAP = "cb212d30a70a468d850a83eb4cc6bc08"
TEST_ZONING_MAP = "224f58c8813840da82b59cf3f8a58678"

# load map template
# template_name = "template.json"
# file_name = os.path.join(TEMPLATE_DIR, template_name)
# with open(file_name) as json_file:
#     template = json.load(json_file)


def planning_map():
    """
    Builds the County Planning Map.
    """
    gis = GIS(
        "https://bentoncountygis.maps.arcgis.com/", ARCGIS_USERNAME, ARCGIS_PASSWORD
    )
    template = tp.build_template()
    map_item = gis.content.get(TEST_COUNTY_BASEMAP)
    clear(map_item)
    bc.county_basemap(map_item, template)


def clear(item):
    map_item = WebMap(item)
    map_layers = map_item.layers
    for lyr in map_layers:
        map_item.remove_layer(lyr)
    map_item.update()
