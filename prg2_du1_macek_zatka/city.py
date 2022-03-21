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

def choose_district(index):
    districts = [["Praha"],[ "České Budějovice","Český Krumlov", "Jindřichův Hradec", "Písek",                            "Prachatice",                            "Strakonice",                            "Tábor"],        [ "Blansko",                                "Brno-město",                                "Brno-venkov",                                "Břeclav",                                "Hodonín",                                "Vyškov",                                "Znojmo"],[ "Cheb",                            "Karlovy Vary",                            "Sokolov"],[ "Havlíčkův Brod",                            "Jihlava",                            "Pelhřimov",                            "Třebíč",                            "Žďár nad Sázavou"],[ "Hradec Králové",                                "Jičín",                                "Náchod",                                "Rychnov nad Kněžnou",                                "Trutnov"],[ "Česká Lípa",                        "Jablonec nad Nisou",                        "Liberec",                        "Semily"],[ "Bruntál",                                "Frýdek-Místek",                                "Karviná",                                "Nový Jičín",                                "Opava",                                "Ostrava-město"],[ "Jeseník",                        "Olomouc",                        "Prostějov",                        "Přerov",                        "Šumperk"],[ "Chrudim",                            "Pardubice",                            "Svitavy",                            "Ústí nad Orlicí"],[ "Domažlice",                        "Klatovy",                        "Plzeň-jih",                        "Plzeň-město",                        "Plzeň-sever",                        "Rokycany",                        "Tachov"],[ "Benešov",                            "Beroun",                            "Kladno",                            "Kolín",                            "Kutná Hora",                            "Mělník",                            "Mladá Boleslav",                            "Nymburk",                            "Praha-východ",                            "Praha-západ",                            "Příbram",                            "Rakovník"],[ "Děčín",                        "Chomutov",                        "Litoměřice",                        "Louny",                        "Most",                        "Teplice",                        "Ústí nad Labem"],[ "Kroměříž",                        "Uherské Hradiště",                        "Vsetín",                        "Zlín"]]
    if int(index) == 0:
        merged = []
        for i in range(0,14):
                merged = merged + districts[i]
        merged.sort()
        merged.append("VŠE")
        return merged
    
    di = districts[int(index)-1]
    a = ['VŠE']
    dist = a + di
    return dist

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
        self._area = "Zlínský kraj"
        self._districts = ["VŠE", "Kroměříž", "Uherské Hradiště", "Vsetín", "Zlín"]
        self._district = "Zlín"
        self._zobrazit_mesta = ""
        self.kraj_filter_string = "Město" # "Město" or "Vesnice" or ""
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


    def set_area(self, new_val):
        if new_val != self._area:
            self._area = new_val
            self.area_changed.emit(self._area)
            print("Filter area:", self._area)
            self.set_districts(choose_district(self.area))
    
    def set_mesta(self, new_val):
        if new_val != self._zobrazit_mesta:
            self._zobrazit_mesta = new_val
            #self.zobrazit_mesta.emit(self._zobrazit_mesta)
            print("zobrazit_mesta: ", self._zobrazit_mesta)

    def set_districts(self, new_val):
        if new_val != self._districts:
            self._districts = new_val
            print("Filter districts:", self._districts)
            ctxt.setContextProperty("dist", self._districts)

    def set_district(self, new_val):
        if new_val != self._district:
            self._district = new_val
            self.district_changed.emit(self._district)
            print("Filter final district:", self._district)

  
    def get_district(self):
        return self._districts

    def get_zobrazit_mesta(self):
        return self.zobrazit_mesta    
    def get_zobrazit_vesnice(self):
        return self.zobrazit_vesnice
    def get_min_slider(self):
        return self.get_min_slider
    def get_max_slider(self):
        return self.get_max_slider


    kraj_change = Signal()
    area_changed = Signal(str)
    district_changed = Signal(str)

    zobrazit_vesnice = Property(bool, get_zobrazit_vesnice)
    
    min_slider = Property(int, get_min_slider)
    max_slider = Property(int, get_max_slider)

    area = Property(str, lambda self: self._area, set_area, notify=area_changed)
    district = Property(str, get_district, set_district, notify=district_changed)

    zobrazit_mesta_changed = Signal()
    zobrazit_mesta = Property(bool, lambda self: self._area, set_mesta, notify = zobrazit_mesta_changed)

    @Slot()
    def filtr_checkboxy(self):
        if self._zobrazit_mesta == False:
            self.kraj_filter_string = "Vesnice"
            mesta_proxy.setFilterRegExp(QRegExp(obce_model.kraj_filter_string, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))
        else:
            self.kraj_filter_string = "Vesnice"


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
obce_model = ObceModel(SEZNAM_OBCI)

mesta_proxy = QtCore.QSortFilterProxyModel()
mesta_proxy.setSourceModel(obce_model)
mesta_proxy.setFilterRole(obce_model.Roles.IS_CITY.value)
ctxt = view.rootContext()
ctxt.setContextProperty("ObceModel", obce_model)
ctxt.setContextProperty("FinalProxy", mesta_proxy)

#ctxt.setContextProperty("FinalProxy", mesta_proxy)

view.setSource(url)
view.show()
app.exec_()