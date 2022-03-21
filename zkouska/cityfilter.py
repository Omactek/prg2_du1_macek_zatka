from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray, QRegExp

from prg2_du1_macek_zatka.city import VIEW_URL

mesta_filter_string = "" # "Město" or "Vesnice"
obce_filter_string = "" # "Město" or "Vesnice"
kraje_filer_string = ""
okresy_filer_string = ""

kraj_filter_string = ""

mesta_proxy = QtCore.QSortFilterProxyModel()
mesta_proxy.setSourceModel(obce_model)
mesta_proxy.setFilterRole(obce_model.Roles.IS_CITY.value)
mesta_proxy.setFilterRegExp(QRegExp(kraj_filter_string, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))

obce_proxy = QtCore.QSortFilterProxyModel()
obce_proxy.setSourceModel(mesta_proxy)
obce_proxy.setFilterRole(obce_model.Roles.IS_CITY.value)
obce_proxy.setFilterRegExp(QRegExp(obce_filter_string, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))

kraje_proxy = QtCore.QSortFilterProxyModel()
kraje_proxy.setSourceModel(obce_proxy)
kraje_proxy.setFilterRole(obce_model.Roles.DISTRICT.value)
kraje_proxy.setFilterRegExp(QRegExp(kraje_filer_string, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))

okresy_proxy = QtCore.QSortFilterProxyModel()
okresy_proxy.setSourceModel(kraje_proxy)
okresy_proxy.setFilterRole(obce_model.Roles.REGION.value)
okresy_proxy.setFilterRegExp(QRegExp(okresy_filer_string, QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))


ctxt.setContextProperty("KrajeProxy", kraje_proxy)