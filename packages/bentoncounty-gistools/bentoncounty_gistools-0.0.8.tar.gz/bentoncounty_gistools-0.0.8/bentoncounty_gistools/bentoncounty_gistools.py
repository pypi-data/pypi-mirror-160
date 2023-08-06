import random
import string
from arcgis.mapping import MapServiceLayer
from arcgis.mapping import MapFeatureLayer
from arcgis.mapping import MapImageLayer
from arcgis.mapping import MapRasterLayer
import bentoncounty_gistools.urls as urls


def test_map_group(project_map, layers, template, urls, group, stub):
    """
    Build test map of the target layers.

    :param project_map: Web map to update with target layers.
    :type project_map: Web Map
    :param template: Web map template for feature layer info.
    :type template: Dictionary
    :return: Updates web map to include the target layers.
    :rtype: None
    """
    basemap = group_layer("Base")
    layers(basemap, template, urls, group, stub)
    map_def = project_map.get_data()
    map_def["operationalLayers"].append(basemap)
    project_map.update({"text": str(map_def)})


def define_layer_names(urls, stub):
    names = []
    for i in range(0, len(urls)):
        names.append(stub + "_" + str(i))
    return names


def aerial_imagery(group_lyr):
    """
    Append aerial imagery layers to group layer.

    :param group_lyr: Group layer to update with target layers.
    :type group_lyr: Group layer
    :return: Updates group layer to include the target layers.
    :rtype: None
    """
    basemap = group_layer("Aerial Imagery")
    basemap["layers"].append(urls.corvallis_image_2019)
    basemap["layers"].append(urls.corvallis_image_2021)
    basemap["layers"].append(urls.esri_image_def)
    group_lyr["layers"].append(basemap)


def test_map_image(project_map, layer_def):
    """
    Build test map of the target layers.

    :param project_map: Web map to update with target layers.
    :type project_map: Web Map
    :param template: Web map template for feature layer info.
    :type template: Dictionary
    :return: Updates web map to include the target layers.
    :rtype: None
    """
    basemap = group_layer("Base")
    make_image_layer(basemap, layer_def)
    map_def = project_map.get_data()
    map_def["operationalLayers"].append(basemap)
    project_map.update({"text": str(map_def)})


def make_image_layer(trunk, layer_def):
    trunk["layers"].append(layer_def)


def define_layers(trunk, template, urls, group, stub):
    branch = group_layer(group)
    names = define_layer_names(urls, stub)
    for i in range(0, len(urls)):
        lyr = MapImageLayer(urls[i])
        fc = feature_class(lyr, 0.5)
        fc.update({"visibility": False})
        # fc.update({'popupInfo': template[names[i] + '_popup']})
        # fc.update({'layerDefinition': template[names[i] + '_label']})
        branch["layers"].append(fc)
    trunk["layers"].append(branch)


def environment_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "hydric_soils",
        "natural_soils",
        "natural_wetlands",
        "nwi_wetlands",
        "bc_eq_slope",
        "bc_landslide",
        "shpo_buff",
        "rip_buff",
        "big_game",
        "earthquake_faults",
        "hydro_lines",
        "hydro_polys",
        "hydro_hucs",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("environment_" + lyr + post)
    return layer_name


def environment_layers(group_lyr, template):
    """
    Add layers for topographic contours to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    name_stub = environment_layer_names("")
    url_list = urls.environment_urls
    parent_group = group_layer("Environment")
    parent_group.update({"visibility": False})

    fema_layers(parent_group)

    branch = group_layer("Soil")
    branch.update({"visibility": False})
    add_single_layer(name_stub[0], url_list[0], branch, template, "Hydric Soils (NRCS)")
    add_single_layer(name_stub[1], url_list[1], branch, template)
    parent_group["layers"].append(branch)

    contour_layers(parent_group, template)

    add_single_layer(
        name_stub[6], url_list[6], parent_group, template, "SHPO Buffer", False
    )
    add_single_layer(
        name_stub[7],
        url_list[7],
        parent_group,
        template,
        "County Riparian Buffer",
        False,
    )
    add_single_layer(
        name_stub[4], url_list[4], parent_group, template, "County Slope", False
    )
    add_single_layer(
        name_stub[5],
        url_list[5],
        parent_group,
        template,
        "County Landslide Risk",
        False,
    )
    add_single_layer(
        name_stub[9],
        url_list[9],
        parent_group,
        template,
        "Earthquake Faults (advisory only)",
        False,
    )
    add_single_layer(
        name_stub[8], url_list[8], parent_group, template, "Big Game Range", False
    )

    hcp_butterfly_layers(parent_group, template)

    branch = group_layer("Corvallis Natural Features Inventory")
    nfi_hazard_layers(branch, template)
    nfi_features_layers(branch, template)
    parent_group["layers"].append(branch)

    branch = group_layer("Wetland")
    branch.update({"visibility": False})
    add_single_layer(
        name_stub[2],
        url_list[2],
        branch,
        template,
        "Wetlands - NWI (County Backup)",
        False,
    )
    add_single_layer(
        name_stub[3], url_list[3], branch, template, "Wetlands - NWI (USFWS)"
    )
    parent_group["layers"].append(branch)

    branch = group_layer("Water")
    branch.update({"visibility": False})
    add_single_layer(name_stub[10], url_list[10], branch, template, "Rivers & Streams")
    add_single_layer(name_stub[11], url_list[11], branch, template, "Water bodies")
    add_single_layer(name_stub[12], url_list[12], branch, template, "Boundaries")
    parent_group["layers"].append(branch)

    group_lyr["layers"].append(parent_group)


def hcp_butterfly_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "surveyed",
        "nectar",
        "blue_zone",
        "blue_zone_ugb",
        "kincaid",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("hcp_butterfly_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def hcp_butterfly_layers(group_lyr, template):
    """
    Add layers for topographic contours to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    popup_names = hcp_butterfly_layer_names("_popup")
    label_names = hcp_butterfly_layer_names("_label")
    url_list = urls.HCP_BUTTERFLY_URLS
    parent_group = group_layer("HCP Butterfly")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        if fc["title"] == "SurveyedAreas":
            fc.update({"title": "Surveyed Areas"})
        if fc["title"] == "NectarZone":
            fc.update({"title": "Nectar Zone"})
        if fc["title"] == "FendersBlueZone - Official":
            fc.update({"title": "Fenders Blue Zone - Official"})
        if fc["title"] == "FendersBlueZones UGB_USFWS":
            fc.update({"title": "Fenders Blue Zone - UGB (USFWS)"})
        if fc["title"] == "KincaidLupinesZone":
            fc.update({"title": "Kincaid Lupines"})
        fc.update({"popupInfo": template[popup_names[i]]})
        fc.update({"layerDefinition": template[label_names[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def contour_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "100ft",
        "20ft",
        "10ft",
        "2ft",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("contours_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def contour_layers(group_lyr, template):
    """
    Add layers for topographic contours to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    popup_names = contour_layer_names("_popup")
    label_names = contour_layer_names("_label")
    url_list = urls.TOPO_CONTOURS_URLS
    parent_group = group_layer("Topographic Contours")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        # add_single_layer(contour_names[i], url_list[i], parent_group, template)
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        if fc["title"] == "contours100ft":
            fc.update({"title": "100-ft Contours"})
        if fc["title"] == "contours20ft":
            fc.update({"title": "20-ft Contours"})
        if fc["title"] == "contours10ft":
            fc.update({"title": "10-ft Contours"})
        if fc["title"] == "contours2ft":
            fc.update({"title": "2-ft Contours"})
        fc.update({"popupInfo": template[popup_names[i]]})
        fc.update({"layerDefinition": template[label_names[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def nfi_hazard_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "closed_channel",
        "open_channel",
        "landslide",
        "slope",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("nfi_hazard_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def nfi_hazard_layers(group_lyr, template):
    """
    Add layers for nfi hazards to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    url_list = urls.NFI_HAZARD_URLS
    parent_group = group_layer("Hazards")
    parent_group.update({"visibility": False})

    branch = group_layer("Percent Slope")
    add_single_layer("nfi_hazard_slope", url_list[0], branch, template)
    parent_group["layers"].append(branch)

    branch = group_layer("Landslide Risk")
    add_single_layer("nfi_hazard_landslide", url_list[1], branch, template)
    parent_group["layers"].append(branch)

    branch = group_layer("Landslide Debris Runout Areas")
    add_single_layer("nfi_hazard_open_channel", url_list[2], branch, template)
    add_single_layer("nfi_hazard_closed_channel", url_list[3], branch, template)
    parent_group["layers"].append(branch)

    nfi_flood_layers(parent_group, template)

    group_lyr["layers"].append(parent_group)


def nfi_flood_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "0.2_floodway",
        "willamette",
        "dixon",
        "dunawi",
        "jackson",
        "lewisburg",
        "oak_creek",
        "sequoia",
        "village",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("nfi_flood" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def nfi_flood_layers(group_lyr, template):
    """
    Add layers for nfi flooding hazards to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    layer_name = nfi_flood_layer_names("_label")
    popup_name = nfi_flood_layer_names("_popup")
    url_list = urls.NFI_FLOOD_URLS
    parent_group = group_layer("Flooding")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[layer_name[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def nfi_features_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "oak_savanna",
        "wetlands_critical",
        "wetlands_dsl",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("nfi_features_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def add_single_layer(key_name, url, group_lyr, template, title=None, visibility=None):
    """
    Add single feature layer to parent group layer.

    :param key_name: Base name for template definition reference.
    :type key_name: Text string
    :param url: Url address of feature service layer to add.
    :type url: Text string (must be valid url).
    :param group_lyr: Group layer definition target for layers.
    :type group_lyr: Dictionary
    :param template: Template dictionary holding layer definitions for the map.
    :type template: Dictionary
    :param title: Optional title to assign to the added layer.
    :type title: Text string
    :param visibility: Optional level of transparency to assign to new layer.
    :type visibility: Float ranging from 0-1.
    :return: Updates group layer definition with new layer.
    """
    popup_name = key_name + "_popup"
    label_name = key_name + "_label"
    lyr = MapServiceLayer(url)
    fc = feature_class(lyr, 0.5, title)
    if visibility != None:
        fc.update({"visibility": visibility})
    fc.update({"popupInfo": template[popup_name]})
    fc.update({"layerDefinition": template[label_name]})
    group_lyr["layers"].append(fc)


def fema_layers(group_lyr):
    """
    Add layers for FEMA flood zone to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    url_list = urls.FEMA_NFHL_URLS
    parent_group = group_layer("FEMA Flood Hazard")
    parent_group.update({"visibility": True})

    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"visibility": False})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def nfi_features_layers(group_lyr, template):
    """
    Add layers for riparian areas to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    url_list = urls.FEATURES_URLS
    parent_group = group_layer("Features")
    parent_group.update({"visibility": False})

    branch = group_layer("Other Wetlands")
    add_single_layer("nfi_features_wetlands_dsl", url_list[0], branch, template)
    parent_group["layers"].append(branch)

    branch = group_layer("Systems-Critical Wetlands")
    add_single_layer(
        "nfi_features_wetlands_critical",
        urls.nfi_lsw,
        branch,
        template,
        "Locally Significant Wetlands",
    )
    parent_group["layers"].append(branch)

    riparian_layers(parent_group, template)

    branch = group_layer("Significant Vegetation")
    ppsv_layers(branch, template)
    hpsv_layers(branch, template)
    add_single_layer("nfi_features_oak_savanna", url_list[2], branch, template)
    parent_group["layers"].append(branch)

    group_lyr["layers"].append(parent_group)


def riparian_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "50foot_buffers",
        "75foot_buffers",
        "100foot_buffers",
        "120foot_buffers",
        "downtown",
        "wetlands",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("riparian_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def riparian_layers(group_lyr, template):
    """
    Add layers for riparian areas to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    layer_name = riparian_layer_names("_label")
    popup_name = riparian_layer_names("_popup")
    url_list = urls.RIPARIAN_URLS
    parent_group = group_layer("Riparian Areas")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        if i == 0:
            fc = fc_from_fl(map_lyr, 0.5)
            fc.update({"title": "Wetlands Within RAAs"})
        elif i == 3:
            fc = fc_from_fl(map_lyr, 0.5)
            fc.update({"title": "100-Foot TOB Buffers"})
        else:
            fc = feature_class(map_lyr, 0.5)

        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[layer_name[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def ppsv_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "connecting_corridors",
        "native_tree_dominated",
        "mitigation_tree_groves",
        "isolated_tree_groves",
        "top_third_ugb",
        "top_11_ugb",
        "native_tree_vegetation",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("ppsv_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def ppsv_layers(group_lyr, template):
    """
    Add layers for high protection incentive vegetation to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    popup_name = ppsv_layer_names("_popup")
    label_name = ppsv_layer_names("_label")
    url_list = urls.NFI_PPSV_URLS
    parent_group = group_layer("Partial Protection (PPSV)")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapFeatureLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[label_name[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def hpsv_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "connecting_corridors",
        "native_tree_dominated",
        "mitigation_tree_groves",
        "top_third_ugb",
        "top_11_ugb",
        "native_tree_timber",
        "native_tree_vegetation",
        "douglas_fir_chip_ross",
        "oak_savanna",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("hpsv_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def hpsv_layers(group_lyr, template):
    """
    Add layers for high protection incentive vegetation to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    popup_name = hpsv_layer_names("_popup")
    label_name = hpsv_layer_names("_label")
    url_list = urls.NFI_HPSV_URLS
    parent_group = group_layer("High Protection (HPSV)")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapFeatureLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[label_name[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def taxlot_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "corners",
        "water_lines",
        "taxlots",
        "tax_code_areas",
        "plss_lines",
        "reference_lines",
        "tax_code_lines",
        "fire_districts",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("taxlot_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def taxlot_layers(group_lyr, template):
    """
    Add layers for BC taxlots to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    layer_name = taxlot_layer_names("_label")
    url_list = urls.TAXLOT_URLS
    taxlot_group = group_layer("Taxlot Maps")
    # taxlot_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"visibility": False})

        # customize layer data
        if fc["title"] != "Corner - Above":
            fc.update({"layerDefinition": template[layer_name[i]]})
        if fc["title"] == "FireDistricts":
            fc.update({"title": "Fire Districts"})

        if fc["title"] == "TaxCodeLines - Below":
            fc.update({"title": "Tax Code Lines"})

        if fc["title"] == "ReferenceLines - Above":
            fc.update({"title": "Reference Lines"})

        if fc["title"] == "PLSSLines - Above":
            fc.update({"title": "PLSS Lines"})

        if fc["title"] == "WaterLines - Above":
            fc.update({"title": "Water Lines"})

        if fc["title"] == "Corner - Above":
            fc.update({"title": "Corners"})

        taxlot_group["layers"].append(fc)

    group_lyr["layers"].append(taxlot_group)


def anno_0050_layers_info(template):
    """
    Build dictionary of layer info.

    :param template: Web map template for layer fields.
    :return: Dictionary of short keys and layer definitions.
    """
    ref_data = template.get_data()
    ref_list = ref_data["operationalLayers"][0]["layers"][0]["layers"]
    new_data = {}
    zoning_current_popup = ref_list[0]["popupInfo"]
    zoning_current_labels = ref_list[0]["layerDefinition"]
    new_data.update({"zoning_current_popup": zoning_current_popup})
    new_data.update({"zoning_current_labels": zoning_current_labels})
    return new_data


def anno_0050_names(post):
    """
    Create list of key names for layer definition data.
    """
    stub = "anno_0020_"
    stubs = []
    for i in range(0, 36):
        stubs.append(stub + str(i) + post)
    return stubs


def anno_0050_layers(group_lyr, template):
    """
    Add layers for BC taxlot anno 0050 to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    popup_name = anno_0050_names("_popup")
    label_name = anno_0050_names("_label")
    url_list = urls.ANNO_0050_URLS
    parent_group = group_layer("Anno 0050")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapImageLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        # fc.update({"popupInfo": template[popup_name[i]]})
        # fc.update({"layerDefinition": template[label_name[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def anno_0020_layers_info(template):
    """
    Build dictionary of layer info.

    :param template: Web map template for layer fields.
    :return: Dictionary of short keys and layer definitions.
    """
    ref_data = template.get_data()
    ref_list = ref_data["operationalLayers"][0]["layers"][0]["layers"]
    new_data = {}
    zoning_current_popup = ref_list[0]["popupInfo"]
    zoning_current_labels = ref_list[0]["layerDefinition"]
    new_data.update({"zoning_current_popup": zoning_current_popup})
    new_data.update({"zoning_current_labels": zoning_current_labels})
    return new_data


def anno_0020_layers(group_lyr, template):
    """
    Add layers for BC taxlot anno 0020 to group layer.

    :param group_lyr: Group layer definition target for layers.
    :return: Updates group layer definition with layers.
    """
    anno_group = group_layer("Anno 0020")
    # for lyr in urls.ANNO_0020_URLS:
    # map_lyr = MapServiceLayer(lyr)
    # fc = feature_class(map_lyr)
    # fc.update({"visibility": False})
    # anno_group["layers"].append(fc)
    lyr = MapServiceLayer(urls.ANNO_0020_URLS[0])
    fc = feature_class(lyr)
    anno_group["layers"].append(fc)

    group_lyr["layers"].append(anno_group)


def zoning_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "ugb_corvallis",
        "ugb_philomath",
        "greenway",
        "overlays",
        "airport",
        "current",
        "flood",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("zoning_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def zoning_layers(group_lyr, template):
    """
    Add zoning layers to definition of a group layer.

    :param group_lyr: Group layer to update with zoning layers.
    :param template: Web map template for feature layer info.
    :return: Updates group layer definition with zoning' layers.
    """
    popup_name = zoning_layer_names("_popup")
    label_name = zoning_layer_names("_label")
    url_list = urls.ZONING_URLS_DRAFT
    parent_group = group_layer("Zoning")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[label_name[i]]})
        if fc["title"] == "ugb_corvallis_draft_jan2022":
            fc.update({"title": "UGB Corvallis"})
        if fc["title"] == "philomath_ugb_draft":
            fc.update({"title": "UGB Philomath"})
        if fc["title"] == "Willamette Greenway Area":
            fc.update({"title": "Willamette Greenway"})
        if fc["title"] == "Official Zoning Overlays":
            fc.update({"title": "Overlays"})
        if fc["title"] == "Airport Overlay Zone":
            fc.update({"title": "Airport Overlay"})
        if fc["title"] == "Zoning - current":
            fc.update({"title": "Zoning"})
        if fc["title"] == "FEMA_floodplain":
            fc.update({"title": "FEMA Floodplain (County backup)"})
            fc.update({"visibility": False})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def address_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "county",
        "corvallis",
        "driveways",
        "buildings",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("address_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def address_layers(group_lyr, template):
    """
    Add address layers to definition of a group layer.

    :param group_lyr: Group layer to update with address layers.
    :param template: Web map template for feature layer info.
    :return: Updates group layer definition with address layers.
    """
    popup_name = address_layer_names("_popup")
    label_name = address_layer_names("_label")
    url_list = urls.ADDRESS_URLS
    parent_group = group_layer("Addresses")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[label_name[i]]})
        if fc["title"] == "County_Addresses":
            fc.update({"title": "County"})
        if fc["title"] == "Structure_AddressCorvallis":
            fc.update({"title": "Corvallis"})
        if i in [0, 1]:
            fc.update({"visibility": False})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def survey_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "benchmarks",
        "geodetic_control",
        "section_corners",
        "section_polygons",
        "dlc_corners",
        "dlc",
        "survey_index",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("survey_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def test_map_layers(project_map, layers, template):
    """
    Build test map of the target layers.

    :param project_map: Web map to update with target layers.
    :type project_map: Web Map
    :param template: Web map template for feature layer info.
    :type template: Dictionary
    :return: Updates web map to include the target layers.
    :rtype: None
    """
    basemap = group_layer("Base")
    layers(basemap, template)
    map_def = project_map.get_data()
    map_def["operationalLayers"].append(basemap)
    project_map.update({"text": str(map_def)})


def survey_layers(group_lyr, template):
    popup_name = survey_layer_names("_popup")
    label_name = survey_layer_names("_label")
    url_list = urls.SURVEY_URLS
    parent_group = group_layer("Survey")
    # parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"visibility": False})
        fc.update({"popupInfo": template[popup_name[i]]})
        fc.update({"layerDefinition": template[label_name[i]]})
        if fc["title"] == "DLC_corner_index":
            fc.update({"title": "DLC Corners"})
        if fc["title"] == "Section_corner_index":
            fc.update({"title": "Section Corners"})
        if fc["title"] == "Section polygons":
            fc.update({"title": "Sections"})
        if fc["title"] == "Donationlandclaims":
            fc.update({"title": "Donation Land Claims"})
        if fc["title"] == "survey_index":
            fc.update({"title": "Survey Index"})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def transport_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "railroads",
        "centerlines",
        "roads",
        "road_surface",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("transport_" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def transport_layers(group_lyr, template):
    """
    Append transportation layers to web map group layer.

    :param group_lyr: Group layer definition to append with layers.
    :return: Group layer definition with transportation layers appended.
    :rtype: None.
    """
    label_name = transport_layer_names("_label")
    url_list = urls.TRANSPORT_URLS
    parent_group = group_layer("Transportation")
    parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"layerDefinition": template[label_name[i]]})
        if i in [0, 2]:
            # road surface, centerlines
            fc.update({"visibility": False})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def boundary_layer_names(post):
    """
    Create list of key names for layer definition data.
    """
    layer_stub = [
        "cities",
        "county",
        "precincts",
        "parks",
        "zip_codes",
        "school_districts",
        "fire_districts",
    ]
    layer_name = []
    for lyr in layer_stub:
        layer_name.append("boundary" + lyr + post)
    # layer order is reversed from menu order
    layer_name.reverse()
    return layer_name


def county_boundaries(group_lyr, template):
    """
    Add boundaries layers to group for web map.
    Layers include cities and places, counties, precincts, parks, zip codes, school districts and fire districts.

    :param group_lyr: Group layer definition to append with boundary layers.
    :return: Group layer definition with boundary layers appended.
    :rtype: None.
    """
    label_name = boundary_layer_names("_label")
    popup_name = boundary_layer_names("_popup")
    url_list = urls.BOUNDARY_URLS
    parent_group = group_layer("Boundaries")
    # parent_group.update({"visibility": False})
    for i in range(0, len(url_list)):
        map_lyr = MapServiceLayer(url_list[i])
        fc = feature_class(map_lyr, 0.5)
        fc.update({"visibility": False})
        if fc["title"] not in ["County Parks"]:
            fc.update({"layerDefinition": template[label_name[i]]})
        if fc["title"] in ["Zip Codes"]:
            fc.update({"popupInfo": template[popup_name[i]]})
        parent_group["layers"].append(fc)

    group_lyr["layers"].append(parent_group)


def county_basemap(project_map, template):
    """
    Add common reference layers to web map.
    Layers are taxlots, roads, railroads, section lines and section numbers.

    :param project_map: Web map to update with reference layers.
    :return: Updates the web map, adding reference layers.
    :rtype: None.
    """
    basemap = group_layer("County Planning Maps")
    aerial_imagery(basemap)
    environment_layers(basemap, template)
    zoning_layers(basemap, template)
    address_layers(basemap, template)
    taxlot_layers(basemap, template)
    transport_layers(basemap, template)
    county_boundaries(basemap, template)
    survey_layers(basemap, template)
    map_def = project_map.get_data()
    map_def["operationalLayers"].append(basemap)
    project_map.update({"text": str(map_def)})


def layer_urls(item):
    """List service layer urls.

    :param item: Service with target layers.
    :type kind: ArcGISFeatureLayer
    :return: A list of urls for layers in the service.
    :rtype: list[str]

    >>> import bentoncounty_gistools from bentoncounty_gistools as bc
    >>> gis = GIS()
    >>> # load natural features inventory feature collection service
    >>> nfi_fs = gis.content.search(
    >>>     "NaturalFeaturesInventoryService2022_DRAFT",
    >>>     item_type="Feature Layer Collection",
    >>> )[0]
    >>> urls = bc.layer_urls(nfi_fs)
    >>> urls[0]
    "https://services5.arcgis.com/U7TbEknoCzTtNGz4/arcgis/rest/services/NaturalFeaturesInventoryService2022_DRAFT/FeatureServer/0"
    >>> urls[1]
    "https://services5.arcgis.com/U7TbEknoCzTtNGz4/arcgis/rest/services/NaturalFeaturesInventoryService2022_DRAFT/FeatureServer/3"
    """
    urls = []
    for lyr in item.layers:
        urls.append(lyr.url)
    return urls


def create_layer_id(layerIndex):
    """
    Generate random ids for layers. Copied verbatim from https://community.esri.com/t5/arcgis-api-for-python-questions/python-api-add-group-layer-to-webmap/td-p/1112126.

    To build a web map from a published service, we generate feature layers pointed to each service. Each feature layer requires a unique layer id, produced by this function.

    :param layerIndex: Layer index number.
    :return: A randomized string to serve as a unique id.
    :rtype: str
    """
    return (
        "".join(random.choices(string.ascii_lowercase + string.digits, k=11))
        + "-layer-"
        + str(layerIndex)
    )


def fc_from_fl(layer, opacity=1.0):
    fc_dict = {}
    fc_dict.update({"id": create_layer_id(random.randint(10000, 99999))})
    fc_dict.update({"url": layer.url})
    fc_dict.update({"layerType": "ArcGISFeatureLayer"})
    fc_dict.update({"opacity": opacity})
    return fc_dict


def feature_class(layer, opacity=1.0, title=None):
    """
    Generic feature class wrapper for layer data.

    :param layer: Source for feature layer.
    :type layer: MapServiceLayer
    :param opacity: Opacity of feature layer.
    :type opacity: float
    :return: Feature layer data for map service layer.

    >>> import bentoncounty_gistools from bentoncounty_gistools as bc
    >>> gis = GIS()
    >>> # load natural features inventory feature collection service
    >>> nfi_fs = gis.content.search(
    >>>     "NaturalFeaturesInventoryService2022_DRAFT",
    >>>     item_type="Feature Layer Collection",
    >>> )[0]
    >>> urls = bc.layer_urls(nfi_fs)
    >>> streams = MapServiceLayer(urls[0])
    >>> stream = bc.fc_gen(streams)
    >>> stream["url"]
    "https://services5.arcgis.com/U7TbEknoCzTtNGz4/arcgis/rest/services/NaturalFeaturesInventoryService2022_DRAFT/FeatureServer/0"
    >>> stream["title"]
    "STREAMS"
    >>> stream["layerType"]
    "ArcGISFeatureLayer"
    """
    fc_dict = {}
    fc_dict.update({"id": create_layer_id(random.randint(10000, 99999))})
    fc_dict.update({"url": layer.url})
    if title != None:
        fc_dict.update({"title": title})
    else:
        fc_dict.update({"title": layer.properties.name})
    fc_dict.update({"layerType": "ArcGISFeatureLayer"})
    fc_dict.update({"opacity": opacity})
    return fc_dict


def group_layer(title):
    """
    Generates an empty group layer with a specified title.

    :param title: The title of the layer as shown in the legend.
    :return: A json dictionary for a group layer.
    """
    group_dict = {}
    group_dict.update({"id": create_layer_id(random.randint(10000, 99999))})
    group_dict.update({"layers": []})
    group_dict.update({"layerType": "GroupLayer"})
    group_dict.update({"title": title})
    return group_dict


if __name__ == "__main__":
    import doctest

    doctest.testmod()
