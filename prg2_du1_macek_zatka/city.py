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
    districts = [["VŠE"],["Praha"],[ "České Budějovice","Český Krumlov", "Jindřichův Hradec", "Písek",                            "Prachatice",                            "Strakonice",                            "Tábor"],        [ "Blansko",                                "Brno-město",                                "Brno-venkov",                                "Břeclav",                                "Hodonín",                                "Vyškov",                                "Znojmo"],[ "Cheb",                            "Karlovy Vary",                            "Sokolov"],[ "Havlíčkův Brod",                            "Jihlava",                            "Pelhřimov",                            "Třebíč",                            "Žďár nad Sázavou"],[ "Hradec Králové",                                "Jičín",                                "Náchod",                                "Rychnov nad Kněžnou",                                "Trutnov"],[ "Česká Lípa",                        "Jablonec nad Nisou",                        "Liberec",                        "Semily"],[ "Bruntál",                                "Frýdek-Místek",                                "Karviná",                                "Nový Jičín",                                "Opava",                                "Ostrava-město"],[ "Jeseník",                        "Olomouc",                        "Prostějov",                        "Přerov",                        "Šumperk"],[ "Chrudim",                            "Pardubice",                            "Svitavy",                            "Ústí nad Orlicí"],[ "Domažlice",                        "Klatovy",                        "Plzeň-jih",                        "Plzeň-město",                        "Plzeň-sever",                        "Rokycany",                        "Tachov"],[ "Benešov",                            "Beroun",                            "Kladno",                            "Kolín",                            "Kutná Hora",                            "Mělník",                            "Mladá Boleslav",                            "Nymburk",                            "Praha-východ",                            "Praha-západ",                            "Příbram",                            "Rakovník"],[ "Děčín",                        "Chomutov",                        "Litoměřice",                        "Louny",                        "Most",                        "Teplice",                        "Ústí nad Labem"],[ "Kroměříž",                        "Uherské Hradiště",                        "Vsetín",                        "Zlín"]]
    if int(index) == 0:
        merged = []
        for i in range(0,14):
                merged = merged + districts[i]
        merged.sort()
        merged.append("VŠE")
        return merged
    
    di = districts[int(index)]
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
        self._area = ""
        self._districts = []
        self._district = ""
        self._zobrazit_mesta = True
        self._zobrazit_vesnice = True
        self.is_city = "" #"Vesnice" or ""
        self.is_vesnice = "" #"Město" or ""
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
    
    def set_mesta(self, new_val):
        if new_val != self._zobrazit_mesta:
            self._zobrazit_mesta = new_val
            self.filtr_checkbox_city()

    def set_zobrazit_vesnice(self, new_val):
        if new_val != self._zobrazit_vesnice:
            self._zobrazit_vesnice = new_val
            self.filtr_checkbox_obec()

    def set_area(self, new_val):
        if new_val != self._area:
            self._area = new_val
            self.area_changed.emit(self._area)
            self.filtruj_kraje()
            self.set_districts(choose_district(self.area))

    def set_districts(self, new_val): #filters districts based on selected area
        if new_val != self._districts:
            self._districts = new_val
            print(self._districts)
            ctxt.setContextProperty("dist", self._districts)

    def set_district(self, new_val):
        if new_val != self._district:
            self._district = new_val
            print("toto je self._districts: ")
            self.district_changed.emit(self._district)
            print(self._district)
            self.filtruj_okresy()

  
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


    zobrazit_mesta_changed = Signal()
    zobrazit_vesnice_changed = Signal()
    kraj_change = Signal()
    area_changed = Signal(str)
    district_changed = Signal(str)

    zobrazit_mesta = Property(bool, lambda self: self._zobrazit_mesta, set_mesta, notify = zobrazit_mesta_changed)
    zobrazit_vesnice = Property(bool, lambda self: self._zobrazit_vesnice, set_zobrazit_vesnice, notify = zobrazit_vesnice_changed)
    area = Property(str, lambda self: self._area, set_area, notify=area_changed)
    district = Property(str,lambda self: self._district, set_district, notify=district_changed)
    
    def filtr_checkbox_city(self):
        if self._zobrazit_mesta:
            self.is_city = ""
        elif not self._zobrazit_mesta: 
            self.is_city = "Vesnice"
        mesta_proxy.setFilterRegExp(QRegExp(obce_model.is_city, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))
        print("konec")

    def filtr_checkbox_obec(self):
        if self._zobrazit_vesnice:
            self.is_vesnice= ""
        elif not self._zobrazit_vesnice: 
            self.is_vesnice = "Město"
        obce_proxy.setFilterRegExp(QRegExp(obce_model.is_vesnice, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))

    def filtruj_kraje(self):
        sz = ["VŠE", "Hlavní město Praha","Jihočeský kraj","Jihomoravský kraj","Karlovarský kraj","Kraj Vysočina","Královéhradecký kraj","Liberecký kraj","Moravskoslezský kraj","Olomoucký kraj","Pardubický kraj","Plzeňský kraj","Středočeský kraj","Ústecký kraj","Zlínský kraj"]
        kraje_str = sz[int(obce_model._area)]
        if kraje_str == "VŠE":
            kraje_str = ""
        kraje_proxy.setFilterRegExp(QRegExp(kraje_str, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))
        print(obce_model._area)

    def filtruj_okresy(self):
        okresy_str = self._district
        if okresy_str == "VŠE":
            okresy_str = ""
        print(okresy_str)
        okresy_proxy.setFilterRegExp(QRegExp(okresy_str, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
obce_model = ObceModel(SEZNAM_OBCI)

mesta_proxy = QtCore.QSortFilterProxyModel()
mesta_proxy.setSourceModel(obce_model)
mesta_proxy.setFilterRole(obce_model.Roles.IS_CITY.value)

obce_proxy = QtCore.QSortFilterProxyModel()
obce_proxy.setSourceModel(mesta_proxy)
obce_proxy.setFilterRole(obce_model.Roles.IS_CITY.value)

kraje_proxy = QtCore.QSortFilterProxyModel()
kraje_proxy.setSourceModel(obce_proxy)
kraje_proxy.setFilterRole(obce_model.Roles.REGION.value)

okresy_proxy = QtCore.QSortFilterProxyModel()
okresy_proxy.setSourceModel(kraje_proxy)
okresy_proxy.setFilterRole(obce_model.Roles.DISTRICT.value)

ctxt = view.rootContext()
ctxt.setContextProperty("ObceModel", obce_model)
ctxt.setContextProperty("FinalProxy", okresy_proxy)


view.setSource(url)
view.show()
app.exec_()