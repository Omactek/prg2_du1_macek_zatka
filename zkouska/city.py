from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal, QTimer, QAbstractListModel, QByteArray, QRegExp
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
import sys
import json
import typing
from enum import Enum

VIEW_URL = "view.qml"
SEZNAM_OBCI = "obce.geojson"

class ObceModel(QAbstractListModel):
    
    class Roles(Enum):
        LOC = QtCore.Qt.UserRole+0
        POP = QtCore.Qt.UserRole+1
        AREA = QtCore.Qt.UserRole+2
        DISTRICT = QtCore.Qt.UserRole+3
        REGION = QtCore.Qt.UserRole+4
        IS_CITY = QtCore.Qt.UserRole+5
        
    def __init__(self, filename=None):
        QAbstractListModel.__init__(self)
        self.seznam_obci = []
        if filename:
            self.load_from_json(filename)

    def load_from_json(self, filename):
        with open (filename, encoding = "utf-8") as file:
            self.seznam_obci = json.load(file)

            for entry in self.seznam_obci["features"]:
                lon = entry["geometry"]["coordinates"][0]
                lat = entry["geometry"]["coordinates"][1]
                entry["geometry"]["coordinates"] = QGeoCoordinate(float(lat), float(lon))
    
    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.seznam_obci["features"])

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            return self.seznam_obci["features"][index.row()]["properties"]["NAZ_OBEC"]
        elif role == self.Roles.LOC.value: 
            return self.seznam_obci["features"][index.row()]["geometry"]["coordinates"]
        elif role == self.Roles.POP.value:
            return self.seznam_obci["features"][index.row()]["properties"]["POCET_OBYV"]
        elif role == self.Roles.AREA.value:
            return round(self.seznam_obci["features"][index.row()]["properties"]["area"],2)
        elif role == self.Roles.DISTRICT.value:
            return self.seznam_obci["features"][index.row()]["properties"]["NAZ_OKRES"]
        elif role == self.Roles.REGION.value:
            return self.seznam_obci["features"][index.row()]["properties"]["NAZ_KRAJ"]
        elif role == self.Roles.IS_CITY.value:
            if self.seznam_obci["features"][index.row()]["properties"]["is_city"] == "TRUE":
                return "Město"
            else:
                return "Vesnice" 
            #return self.seznam_obci["features"][index.row()]["properties"]["is_city"]

    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.LOC.value] = QByteArray(b'location')
        roles[self.Roles.POP.value] = QByteArray(b'population')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.DISTRICT.value] = QByteArray(b'district')
        roles[self.Roles.REGION.value] = QByteArray(b'region')
        roles[self.Roles.IS_CITY.value] = QByteArray(b'township')
        print(roles)
        return roles

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
obce_model = ObceModel(SEZNAM_OBCI)

kraje_proxy = QtCore.QSortFilterProxyModel()
kraje_proxy.setSourceModel(obce_model)
kraje_proxy.setFilterRole(3)
kraje_proxy.setFilterRegExp(QRegExp("Olomoucký kraj", QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))

ctxt = view.rootContext()
ctxt.setContextProperty("ObceModel", obce_model)
ctxt.setContextProperty("KrajeProxy", kraje_proxy)
view.setSource(url)
view.show()
app.exec_()