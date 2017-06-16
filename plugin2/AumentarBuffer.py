# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AumentarBuffer
                                 A QGIS plugin
 Añade aleros a una construcción catastral
                              -------------------
        begin                : 2017-04-03
        git sha              : $Format:%H$
        copyright            : (C) 2017 by seresco
        email                : pablo.cuadrado@seresco.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
#"""
#from qgis.core import *
#from PyQt4 import QtCore
#from PyQt4 import QtGui
#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon

#from PyQt4.QtGui import *
#from PyQt4.QtCore import pyqtSignal, pyqtSlot
from qgis.core import *
import qgis.utils
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
import processing
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from math import *
from processing import *
from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.outputs import OutputVector
from processing.tools import *
from shapely.geometry import *
from qgis.gui import QgsMessageBar






# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from AumentarBuffer_dialog import AumentarBufferDialog
import os.path


class AumentarBuffer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AumentarBuffer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&AumentarBuffer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AumentarBuffer')
        self.toolbar.setObjectName(u'AumentarBuffer')
        
        #esto lo he anadido para las senales
    def showDialog(self):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        self.gui = AumentarbufferDialog(self.iface.mainWindow(),  flags)
        self.gui.initGui()
        self.gui.show()
        QObject.connect(self.gui, SIGNAL("unsetTool()"), self.unsetTool)
        QObject.connect(self.gui, SIGNAL("moveSide()"), self.moveSide)
  

    
    
    
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AumentarBuffer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = AumentarBufferDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
#        """Create the menu entries and toolbar icons inside the QGIS GUI."""

#        icon_path = ':/plugins/AumentarBuffer/icon.png'
#        self.add_action(
#            icon_path,
#            text=self.tr(u'Aumenta un alero a una construcción catastral'),
#            callback=self.run,
#            parent=self.iface.mainWindow())


        self.action = QtGui.QAction(QtGui.QIcon(":/plugins/AumentarBuffer/icon.png"),QtCore.QCoreApplication.translate("AumentarBuffer", "Aumenta un alero a una construcción catastral"),  self.iface.mainWindow())
        self.action.setEnabled(False)
        # connect to signals for button behavior
        self.action.triggered.connect(self.run)
        self.iface.currentLayerChanged["QgsMapLayer *"].connect(self.toggle)
        self.canvas.selectionChanged.connect(self.toggle)

        # Add toolbar button and menu item
        self.toolbar.addAction(self.action)
        #self.iface.AumentarBuffer().addAction(self.action)
        
        
        
        
        #anadido
      # function to activate or deactivate the plugin buttons
    def toggle(self):
        # get current active layer 
        layer = self.canvas.currentLayer()
        
        if layer and layer.type() == layer.VectorLayer:
            # disconnect all previously connect signals in current layer
            try:
                layer.editingStarted.disconnect(self.toggle)
            except:
                pass
            try:
                layer.editingStopped.disconnect(self.toggle)
            except:
                pass
            
            # check if current layer is editable and has selected features
            # and decide whether the plugin button should be enable or disable
            if layer.isEditable():
                if layer.selectedFeatureCount() > 0:
                    self.action.setEnabled(True)
                else:
                    self.action.setEnabled(False)
                layer.editingStopped.connect(self.toggle)
            # layer is not editable    
            else:
                self.action.setEnabled(False)
                layer.editingStarted.connect(self.toggle)
        else:
            self.action.setEnabled(False)
            
    
    
    
    
    
    
    
    
    
    
    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AumentarBuffer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        #linea anadida
        self.dlg =AumentarBufferDialog()
        
        
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
                        canvas = self.iface.mapCanvas()
                        layer = self.iface.activeLayer()
                        selection = layer.selectedFeatures()
                        if len(selection) < 1:
                            iface.messageBar().pushMessage("ERROR:", "Para poder ejecutar la herramienta debe tener seleccionado un bloque", level=QgsMessageBar.CRITICAL)
                            #sys.exit()
                        else:
                            pass
                        dist = float(self.dlg.DistancelineEdit.text() )
                        for feature in selection:
                            buff = feature.geometry().buffer(dist, 0, 2, 2, 1.5)
                        global buff    
                        
                        #creo capa en memoria para recoger el buffer y hacer que no se salga del universo
                        epsg = 32719
                        uri= "Polygon?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
                        mem_layer=QgsVectorLayer(uri,
                                                   'temporal',
                                                   'memory')
                        mem_pr=mem_layer.dataProvider()
                        mem_layer.startEditing()
                        fet=QgsFeature()
                        fet.setGeometry(buff)
                        mem_pr.addFeatures([fet])
                        mem_layer.commitChanges()
                        QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
                        mem_layer.selectAll()
                        #me refiero a la capa de parcelas 
                        JA003_Parcela = None
                        for i in QgsMapLayerRegistry.instance().mapLayers().values():
                            if i.name() == "JA003_Parcela":
                                JA003_Parcela = i
#                        feats1=[feature for feature in mem_layer.selectedFeatures()]
#                        feats2=[feature for feature in JA003_Parcela.getFeatures()]
#                        n_feats1=len(feats1)
#                        n_feats2=len(feats2)
#                        geom3 = [ feats1[i].geometry().intersection(feats2[j].geometry()).exportToWkt()
#                                  for i in range(n_feats1)
#                                  for j in range(n_feats2)
#                                  if feats1[i].geometry().intersects(feats2[j].geometry()) ]
#                        geom_insertar=QgsGeometry.fromWkt(geom3[0])
                        #selecciono por localizacion la parcela que intersecta con el bloque en edicion
                        #primero hago el centroide de la capa en memoria
                    
                        epsg = 32719
                        uri = "Point?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
                        centroide = QgsVectorLayer(uri,
                                                   'point',
                                                   'memory')
                        prov = centroide.dataProvider()
                        i= 0
                        for f in mem_layer.getFeatures():
                            feat = QgsFeature()
                            pt = f.geometry().centroid().asPoint()
                            print pt
                            feat.setGeometry(QgsGeometry.fromPoint(pt))
                            prov.addFeatures([feat])
                            i += 1
                        QgsMapLayerRegistry.instance().addMapLayer(centroide)
                        #hago una extraccion por localizacion para quedarme con la parcela en la que esta el bloque
                        parcelaclip = processing.runalg("qgis:extractbylocation",JA003_Parcela,centroide,['contains'],0,None)
                        parcelaclip= parcelaclip['OUTPUT']
                        parcelacliplayer = QgsVectorLayer(parcelaclip,"parcelacliplayer","ogr")
                        #parcelacliplayer_=QgsMapLayerRegistry.instance().addMapLayers([parcelacliplayer])
                        #hago el clip
                        clip = processing.runalg("qgis:clip",mem_layer,parcelacliplayer,None)
                        clipoutput = clip['OUTPUT']
                        cliplayer=QgsVectorLayer(clipoutput, "recorte_temporal","ogr")
                        cliplayer_=QgsMapLayerRegistry.instance().addMapLayers([cliplayer])
                        for i in cliplayer.getFeatures():
                            geom_insertar=i.geometry()
                        #debo eliminar los poligonos que se superpongan a otros bloques
                        
                        
                        
                        layer.invertSelection()
                        geometria_fin=processing.runalg("saga:difference",cliplayer,layer,True,None)
                        geometria_fin= geometria_fin['RESULT']
                        geometria_finlayer=QgsVectorLayer(geometria_fin,"geometria_finlayer","ogr")
                        #geometria_finlayer_=QgsMapLayerRegistry.instance().addMapLayers([geometria_finlayer])
                        for l in geometria_finlayer.getFeatures():
                            geom_insertar2=l.geometry()
                        #y en el paso final actualizo la geometria de la capa principal   
                        layer.invertSelection #para volver a tener la seleccion original
                        layer.beginEditCommand("Feature update")
                        #layer.startEditing()
                        for feature in selection:
                            fid= int(feature.id())
                        if fid==0:
                            layer.destroyEditCommand()
                            return
                        else:
                            #lyr=layer.dataProvider()
                            #lyr.changeGeometryValues({ fid : buff })
                            layer.changeGeometry(fid, geom_insertar2)
                        #layer.commitChanges()
                        #layer.updateExtents()
                        #me quito toda la chasca de capas temporales
                        QgsMapLayerRegistry.instance().removeMapLayers( [mem_layer, cliplayer, parcelacliplayer, centroide, geometria_finlayer] )
                        layer.setSelectedFeatures([])
                        layer.endEditCommand()
                        self.canvas.refresh()
                        pass
 
 
 
 #todo esto es para la sesñal		
    def enable(self):
        self.tr.setEnabled(False)		
        layer = self.iface.activeLayer()
        if layer <> None:
            if layer.type() == QgsMapLayer.VectorLayer:
                # only for polygon layers
                if layer.geometryType() == 2:
                    # enable if editable
                    self.tr.setEnabled(layer.isEditable())
                    try:
                        layer.editingStarted.disconnect(self.enable) # disconnect, will be reconnected
                    except:
                        pass
                    try:
                        layer.editingStopped.disconnect(self.enable) # when it becomes active layer again
                    except:
                        pass
            layer.editingStarted.connect(self.enable)
            layer.editingStopped.connect(self.enable)