=====
Basic Use
=====

When constructing a web map from a published service, it is possible to customize the viewing experience by changing the layer style, labeling and other aspects.  Once the viewing experience is configured correctly, you will likely want these changes to persist when referencing the source layers on future maps.  For instance, the county zoning and taxlot maps share several common sources.  It would be repetitive and error-prone to repeat the server-side configuration independently for every new map, but it is not always possible to include all the necessary information for building the map in the service definitions of the source layers.  The solution employed by this package is to use template web maps to define the server-specific view settings associated with each layer.

Template web maps serve as a reference for building future web maps.  Each template map is devoted to a single group layer, whereas maps used by staff for planning typically combine several group layers together.  In the legend, group layers are named categories that include several features or layers.  Clicking on a group layer in the legend, or the expansion carrot adjacent to the legend name, will show the list of included layers, but the group layer itself does not hold its own data, merely references to child data.

Template Maps
-------------
The package function `build_template()` reads layers information from the template map and stores this info in a local file called `template.json`, which it references for future builds.  The ``json`` format is a widely used standard for storing nested key-value pairs, and under the hood all ArcGIS web maps are essentially ``json`` files telling the server where to find the source data and how to construct the visual representation.  Group layers add a level of nesting to the key-value pairs stored in the ``json`` document, and so in order to use a single function for reading data from multiple template files, the level of nesting in each template file has to be the same.  Therefore, every template map has a parent category (arbitrarily called `Base`), and then a single group category holding the layers specific to the template.  The package does not support template maps that deviate from this structure.

::

        Why is a parent "Base" layer necessary?  In order to make maps more composable, the package
        functions for adding layers insert the desired group into the parent group of a web map.
        Typically the parent group is named after the map's overarching purpose, such as "Benton
        County Zoning Map", or "Benton County Taxlot Map".  Template maps provide the "Base" layer
        as a trunk onto which the package functions attach other groups as branches.

The standard process for updating the visual representation of a map layer is to open the corresponding template and modify the settings in the ArcGIS Online GUI, then run the `build_template()` function to record the changes for later use.  The following table lists the name and description for each of the current template maps, and clicking on the name of the map will open the corresponding template in ArcGIS Online:

Table of Templates
^^^^^^^^^^^^^^^^^^
+------------------------------+----------------------------------------------------------------+
|Name                          |Description                                                     |
+==============================+================================================================+
|template_address_map_         | Addresses for County and City of Corvallis.                    |
+------------------------------+----------------------------------------------------------------+
|template_aerial_imagery_map_  | County and ESRI high resolution orthography.                   |
+------------------------------+----------------------------------------------------------------+
|template_boundaries_map_      | Layers from the Benton County boundaries service.              |
+------------------------------+----------------------------------------------------------------+
|template_contours_map_        | Topographic contour layers.                                    |
+------------------------------+----------------------------------------------------------------+
|template_environment_map_     | General water, soils and wetlands layers.                      |
+------------------------------+----------------------------------------------------------------+
|template_hpc_butterfly_map_   | Fender Blue Butterfly layers.                                  |
+------------------------------+----------------------------------------------------------------+
|template_hpsv_map_            | High protection significant vegetation from Corvallis NFI.     |
+------------------------------+----------------------------------------------------------------+
|template_nfi_features_map_    | Oak Savanna, Critical-Systems Wetlands and DSL Wetland layers. |
+------------------------------+----------------------------------------------------------------+
|template_nfi_flood_map_       | Flooding layers from Corvallis NFI hazards.                    |
+------------------------------+----------------------------------------------------------------+
|template_nfi_hazard_map_      | Confined/Open Channel, landslide risk and slope layers.        |
+------------------------------+----------------------------------------------------------------+
|template_ppsv_map_            | Partial protection significant vegetation from Corvallis NFI.  |
+------------------------------+----------------------------------------------------------------+
|template_riparian_map_        | Riparian buffers from the Corvallis NFI.                       |
+------------------------------+----------------------------------------------------------------+
|template_survey_map_          | Layers from the Benton County survey service.                  |
+------------------------------+----------------------------------------------------------------+
|template_taxlot_map_          | Layers from the Benton County taxlot service.                  |
+------------------------------+----------------------------------------------------------------+
|template_transportation_map_  | Layers from the Benton County transportation service.          |
+------------------------------+----------------------------------------------------------------+
|template_zoning_map_          | Layers from the Benton County zoning service.                  |
+------------------------------+----------------------------------------------------------------+

.. _template_address_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=5c507b0f03084f33b8da587cbd4b830b
.. _template_aerial_imagery_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=4cb460dcb6464724b2e99ba696d5dd77
.. _template_boundaries_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=c8595e39c1fe4971819d74e7318d1dbd
.. _template_contours_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=1e0e9975687741a897e2ff4c7dd3b8e0
.. _template_environment_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=a2612a21ccf3458e945ac971390cf5dc
.. _template_hpc_butterfly_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=6f3467fcdeea4d839d01bff403a5e891
.. _template_hpsv_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=d9b5d23af3044405afe06e8d488d8b64
.. _template_nfi_features_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=4b01743efdb94a3fa54e0f542aad987a
.. _template_nfi_flood_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=ee08f36f69b24f2599bea34563215a17
.. _template_nfi_hazard_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=9db5a09c12454347871a522f6af851d8
.. _template_ppsv_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=a0e7e1cb85c54fd39b95eed20d1aded9
.. _template_riparian_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=dbeaf45e240a41178879f64751d6954d
.. _template_survey_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=28cbe6fcdc7c49cba8f95666644b7fda
.. _template_taxlot_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=a409c55c9e0440488c4ab3ce5e10659d
.. _template_transportation_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=8cd34cff9a43406dae69c69fa42829b9
.. _template_zoning_map: https://bentoncountygis.maps.arcgis.com/home/item.html?id=1f417e7ca2c54a8e99ffb7b373c3c229

Updating a Template
^^^^^^^^^^^^^^^^^^^

The first step is to locate the specific layer of interest in the list of template maps.  Since county planning maps can include more than a hundred layers, it can take time to become familiar with all the different layers.  Once you have located the template map that contains the layer of interest, then you can adjust the color, style, label etc. using the ArcGIS Online GUI.  After making changes, you will need to save the changes to the template by clicking on the folder icon in the left sidebar menu and selecting "Save" from the available options.


Using the Package
-----------------


Logging Into ArcGIS Online
^^^^^^^^^^^^^^^^^^^^^^^^^^

When accessing ArcGIS online from the browser, a security check-in will prompt you to enter the username and password associated with your account.  When using this package to modify or build maps, entry of a valid username and password is still required, but the process is automated, and the package needs to accommodate different users.  How do you enter your credentials?  The solution this package employs is to use *environmental variables*, which are named references to information that are accessible to the package, but not defined in the package itself.  In this case, the relevant variables are called **ARCGIS_USERNAME** and **ARCGIS_PASSWORD**, and they are stored in a file called ``.env``.  When the package runs, it will open the ``.env`` file and read the contents, allowing the user to specify their credentials without leaking this private data.

The package will look for the ``.env`` file in the working directory of your project, and will not exist until you create it!  The good news is that you can create a ``.env`` file using any text editor.  Begin with a new blank document and enter the following:

::

        ARCGIS_USERNAME = "my_username"
        ARCGIS_PASSWORD = "my_password"
        TEMPLATE_DIR = "/path/to/my/project"

Be sure to replace *my_username* and *my_password* with your actual username and password.  Single or double quotes surrounding the username and password are required, as they specify the information as text strings, instead of variable names.  Likewise, replace */path/to/my/project* with the directory path to your project.  This is where the package will store and update the *template.json* file that describes how to build your maps.  Once these changes are complete, save the file in your working directory as *.env*.  Make sure to include the dot before *env*.  If the text editor sneakily adds a ".txt" or some other extension on the end of the file name, rename the file as ".env" and ignore any cautionary warnings about changing the file type.

Importing the Package
^^^^^^^^^^^^^^^^^^^^^

The Benton County GIS Tools package is accessible for download on Python Packaging Index (PYPI).  The easiest way to use Python within an ArcGIS project is to use the Python window.  From the ArcGIS Pro documentation_:

.. _documentation: https://pro.arcgis.com/en/pro-app/2.8/arcpy/get-started/python-window.htm

::

        To open the Python window, on the Analysis tab, in the Geoprocessing group, click the drop-down
        menu under the Python button and click the Python window button.


In order for the running instance of Python to access the functions within the package, the package must first be installed (see :doc:`Installation`), which only needs to be done once on a given machine, and then *imported*.  The import statement is a line of code that tells Python which package you are using, and optionally supplied a nickname for referring to the package in later code.  An example import statement looks like this:

::

        import bentoncounty_gistools as bc

The statement "import bentoncounty_gistools" is necessary.  The optional addition of "as bc" assigns *bc* as a nickname for the package.  Instead of typing the full name of the package "bentoncounty_gistools", you can access functions contained in the package using the shorthand "bc".  Feel free to assign a different nickname to suit your taste.

Storing Template Data
^^^^^^^^^^^^^^^^^^^^^

The template web maps store server-side information about how to display the layers in a web map.  Once you have saved changes to the template maps, the package needs to read these template maps and record the changes in its ``template.json`` file.  The function *build_template()* will read any changes to the template web maps and store this information in the ``template.json`` file.  All the functions contained in the package are accessible using package name, or the nickname specified using the "as" syntax in the import statement, and then the function name, separated by a period (in this context called a dot operator).  For instance, using the import statement above, we can access the *build_template()* function using the following statement:

::

        bc.build_template()

This is equivalent to typing "bentoncounty_gistools.build_template()".  This function only needs to be run once after making changes to a template web map.  Once the changes are saved in the ``template.json`` file, the package will reference this file for future builds.  If you save changes to a template web mab on the server, and do not run this function, then the changes will not show up in map builds, because the package will be referencing the previous configuration, and will not know about your changes.

Building the Planning Map
^^^^^^^^^^^^^^^^^^^^^^^^^

The Planning Map is a bit of a catch-all map, intended to contain any and all layers that planners may use while working with new permit applications.  Because it is a monolithic map containing more than hundred layers and many nested groups, constructing the map from scratch is a complex process, and producing this map is a primary function on this package.  Therefore the package provides a convenience function to build this map using a single line of code, as follows:

::

        bc.planning_map()

Because the map is large, this command will take a significant amount of time to finish executing.  Normal wait times run from 20-30 minutes, but if the ArcGIS server is experiencing a larger than normal workload, the execution can take longer.  The longest build time I have personally encountered is 2 hours and 38 minutes!  Since the processing is being done a remote server (ArcGIS Online), the bottleneck is not occurring on your local machine, or the local network, and you cannot mitigate this problem by upgrading to a better machine, or switching from WiFi to a broadband connection.

On my machine, the console prints an alarming amount of warning messages, including "deprecation" warnings related to specific packages or functions, which you can safely ignore.  The warnings do not originate from the code in this package, but rather its dependencies, or packages that this tools package relies on to perform some of the low level work of the application.  Updating and correcting these warnings are the responsibility of these other package developers.  All of the dependencies our package rely on are mainstream packages that support a number of professional uses, and are actively updated and maintained by their developers.  Since a number of professional projects rely on these packages, we can be confident that their developers will update their code as the language evolves, and that our code will continue to work over time.

Troubleshooting
^^^^^^^^^^^^^^^

If the map fails to build, or if any layers than you adjusted in a template map fail to display properly, this is typically frustrating but fixable.  As you are adjusting the style of layers in a web template, you may note that ArcGIS warns the user that not all style features are stable.  This means that the map might *look correct*, but might now draw properly when you try to build a new map based on the template.  The first impulse as a user is to conclude that the package does not work as intended (this was *my* first reaction to encountering this problem).  However, since the map was building correctly before you made the change to the template, chances are that the new style or label you have specified is producing a *malformed layer definition*.  This essentially means that the server cannot pull enough information, or the right kind of information, from the template file in order to construct a new map from the template.

::

        The first time I encountered this error was changing a hatched symbol to a solid color. To
        resolve the error, I had to change the layer style explicity to Basic Polygon Fill, and then
        specify the desired solid color from the GUI menu.  There are often multiple ways of changing
        the color or style of layers within the ArcGIS Online browser, and you may have to experiment
        with different combinations to find one that is stable between builds.

To avoid a situation where the map is no longer building and you do not know why, it is safest to make small, incremental changes to a template map, rebuilding the map between changes to ensure that the new features are propagating through to the final map the way you want.  If you make dozens of changes to a template map at once, it becomes hard to determine in retrospect which change caused the build to fail, and this can lead to wasted time isolating the error.

If a particular style choice is problematic, causing the build to fail or the layer to draw incorrectly, try exploring alternate ways of setting the style using the ArcGIS Online GUI.  Some style choices are simple unstable or unsupported, and you may consider using an alternative style choice that is more stable.  ArcGIS Online is still rapidly expanding the types of styles that they support, and we can expect the situation to improve in the future.
