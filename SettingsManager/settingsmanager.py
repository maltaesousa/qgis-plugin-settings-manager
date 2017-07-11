# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SettingsManager
                                 A QGIS plugin
 Settings Manager
                              -------------------
        begin                : 2014-03-05
        copyright            : (C) 2014 by Rémi Bovard
        email                : remi.bovard@nyon.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import resources_rc
from settingsmanagerdialog import SettingsManagerDialog
import os.path

class SettingsManager:

    PLUGIN_VERSION = u"2.18.2"
    GEODATA_PATH = os.path.normpath("Q:\\")
    PROJECTION = u"EPSG:21781"

    settings = QSettings()

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(
            self.plugin_dir, "i18n", "settingsmanager_{}.qm" . format(locale)
        )

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        self.dlg = SettingsManagerDialog()

    def initGui(self):
        self.action = QAction(
            QIcon(":/plugins/settingsmanager/icon.png"), u"Settings Manager",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Settings Manager", self.action)

    def unload(self):
        self.iface.removePluginMenu(u"&Settings Manager", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.dlg.show()
        result = self.dlg.exec_()

        if result == 1:
            self.__set_options()
            self.__set_toolbars_visibility()
            self.__set_paths()
            self.__set_browser()
            self.__set_wms_connections()
            self.__set_postgis_connections()
            self.__set_plugins()

            self.iface.messageBar().pushMessage(
                u"Installation",
                u"Paramètres SIT importés (version " + self.PLUGIN_VERSION + "), " +
                u"redémarrer QGIS pour terminer l'installation.",
                level = QgsMessageBar.INFO
            )

    def __set_options(self):

        settings = self.settings

        # General
        settings.setValue("Qgis/showTips218", False)
        settings.setValue("Qgis/checkVersion", False)
        # settings.setValue("Qgis/newProjectDefault", True)

        # System
        # settings.setValue(
        #     "svg/searchPathsForSVG",
        #     os.path.join(self.GEODATA_PATH, "Impression\Symboles")
        # )

        # Data sources
        settings.setValue("Qgis/nullValue", "")
        settings.setValue("Qgis/addPostgisDC", True)

        # Map tools
        settings.setValue("Map/identifyMode", 3)
        settings.setValue("Map/identifyAutoFeatureForm", True)
        settings.setValue(
            "Map/scales",
            u"1:100000,1:50000,1:25000,1:10000,1:5000,1:2500,1:1000,1:500," +
            u"1:250,1:100"
        )

        # Composer
        settings.setValue("Composer/defaultFont", u"Arial Narrow")
        settings.setValue(
            "Composer/searchPathsForTemplates",
            os.path.join(self.GEODATA_PATH, "01_Maps/014_QuantumGIS/Insets")
        )

        # Digitizing
        settings.setValue(
            "Qgis/digitizing/default_snap_mode", u"to vertex and segment"
        )
        settings.setValue("Qgis/digitizing/default_snapping_tolerance", 5)
        settings.setValue("Qgis/digitizing/default_snapping_tolerance_unit", 1)

        # CRS 21781
        settings.setvalue("Projections/EPSG:2056/EPSG:21781_destTransform", 100001)
        settings.setvalue("Projections/EPSG:2056/EPSG:21781_srcTransform", -1)
        settings.setvalue("Projections/EPSG:21781/EPSG:2056_destTransform", -1)
        settings.setvalue("Projections/EPSG:21781/EPSG:2056_srcTransform", 100001)
        settings.setValue("Projections/defaultBehaviour", u"useGlobal")
        settings.setValue("Projections/layerDefaultCrs", self.PROJECTION)
        settings.setValue("Projections/otfTransformAutoEnable", False)
        settings.setValue("Projections/otfTransformEnabled", False)
        settings.setValue("Projections/projectDefaultCrs", self.PROJECTION)

        settings.setValue("UI/recentProjectionsAuthId", self.PROJECTION)
        settings.setValue("UI/recentProjections", [47,1919]) # EPSG: 2056,21781

        # Network
        settings.setValue("proxy/proxyEnabled", True)
        settings.setValue("proxy/proxyType", u"DefaultProxy")

    def __set_toolbars_visibility(self):

        iface = self.iface

        # Visible
        iface.attributesToolBar().setVisible(True)
        iface.digitizeToolBar().setVisible(True)
        iface.fileToolBar().setVisible(True)
        iface.layerToolBar().setVisible(True)
        iface.mapNavToolToolBar().setVisible(True)

        # Hidden
        iface.advancedDigitizeToolBar().setVisible(False)
        iface.databaseToolBar().setVisible(False)
        iface.helpToolBar().setVisible(False)
        iface.mainWindow().findChild(
            QToolBar, "mLabelToolBar"
        ).setVisible(False)
        iface.pluginToolBar().setVisible(False)
        iface.rasterToolBar().setVisible(False)
        iface.vectorToolBar().setVisible(False)
        iface.webToolBar().setVisible(False)

    def __set_paths(self):

        settings = self.settings

        # Last paths
        settings.setValue(
            "UI/lastProjectDir",
            os.path.join(self.GEODATA_PATH, "01_Maps/014_QuantumGIS")
        )
        settings.setValue(
            "UI/lastVectorFileFilterDir",
            os.path.join(self.GEODATA_PATH, "02_Geodata")
        )
        settings.setValue(
            "UI/lastRasterFileFilterDir",
            os.path.join(self.GEODATA_PATH, "02_Geodata/02_20_PhotosAeriennes")
        )
        settings.setValue(
            "Qgis/last_embedded_project_path",
            os.path.join(self.GEODATA_PATH, "01_Maps/014_QuantumGIS")
        )

        # File filter
        settings.setValue(
            "UI/lastVectorFileFilter", "ESRI Shapefiles (*.shp *.SHP)"
        )

    def __set_browser(self):

        settings = self.settings

        # Favourites
        settings.setValue(
            "browser/favourites",[os.path.join(
                self.GEODATA_PATH, "01_Maps/014_QuantumGIS"
            ),os.path.join(self.GEODATA_PATH, "02_Geodata")])

    def __set_wms_connections(self):

        settings = self.settings

        # ASIT VD
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/url",
            u"https://ows.asitvd.ch/wmts"
        )
        settings.setValue(
            "Qgis/WMS/ASIT VD/authcfg", u"asitvd1"
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/smoothPixmapTransform", True
        )

        # GeoPlaNet
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/url",
            u"http://www.geo.vd.ch/main/wsgi/mapserv_proxy"
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/smoothPixmapTransform", True
        )

        # SITNyon
        settings.setValue(
            "Qgis/connections-wms/mapnv/url",
            u"https://mapnv.ch/main/wsgi/mapserv_proxy"
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv/smoothPixmapTransform", True
        )

        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/url",
            u"https://mapnv.ch/main/tiles/1.0.0/WMTSCapabilities.xml"
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/mapnv (WMTS)/smoothPixmapTransform", True
        )

        # Swisstopo
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/url",
            u"https://wms.geo.admin.ch/?lang=fr"
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/smoothPixmapTransform", True
        )

        # Vaud
        settings.setValue(
            "Qgis/connections-wms/Vaud/url",
            u"http://wms.vd.ch/public/services/wmsVD/Mapserver/Wmsserver"
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/smoothPixmapTransform", True
        )

    def __set_postgis_connections(self):

        settings = self.settings

        settings.setValue("PostgreSQL/connections/selected", u"srvsit2")

        # yverdon_main
        settings.setValue(
            "PostgreSQL/connections/srvsit2/host", u"srvsit2"
        )
        settings.setValue(
            "PostgreSQL/connections/srvsit2/port", 5433
        )
        settings.setValue(
            "PostgreSQL/connections/srvsit2/database", u"yvedon_main"
        )
        settings.setValue(
            "PostgreSQL/connections/srvsit2/sslmode", 0
        )
        settings.setValue(
            "PostgreSQL/connections/srvsit2/geometryColumnsOnly", False
        )

    def __set_plugins(self):

        settings = self.settings

        # Settings
        settings.setValue("Qgis/plugin-installer/checkOnStart", True)
        settings.setValue("Qgis/plugin-installer/checkOnStartInterval", 7)
        settings.setValue(
            "Qgis/plugin-installer/allowExperimental", True
        ) # Allows experimental plugins but doesn't check the checkbox...

        # Enable plugins
        settings.setValue("Plugins/libspatialqueryplugin", True)

        # Disable plugins
        settings.setValue("Plugins/libgrassplugin7", False)
        settings.setValue("Plugins/libroadgraphplugin", False)
        settings.setValue("PythonPlugins/SettingsManager", False)

#        # Plugin ProjectLauncher
#        self.__set_plugin_project_launcher()

        # Plugin QuickFinder
        self.__set_plugin_quick_finder()

#    def __set_plugin_project_launcher(self):
#
#        settings = self.settings
#
#        # Enable plugin
#        settings.setValue("PythonPlugins/ProjectLauncher", True)
#
#        # Settings
#        settings.setValue(
#            "Plugins/ProjectLauncher/projects_list",
#            os.path.join(self.GEODATA_PATH, "Projets\projects.ini")
#        )

    def __set_plugin_quick_finder(self):

        settings = self.settings

        # Enable plugin
        settings.setValue("PythonPlugins/quickfinder", True)

        # Settings
        settings.setValue("Plugins/quickfinder_plugin/geomapfish", True)
        settings.setValue(
            "Plugins/quickfinder_plugin/geomapfishUrl",
            u"https://mapnv.ch/main/wsgi/fulltextsearch"
        )
        settings.setValue(
            "Plugins/quickfinder_plugin/geomapfishCrs", self.PROJECTION
        )
        settings.setValue("Plugins/quickfinder_plugin/osm", False)
