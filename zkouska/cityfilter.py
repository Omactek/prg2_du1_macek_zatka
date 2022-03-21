from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray, QRegExp

from prg2_du1_macek_zatka.city import VIEW_URL


kraje_proxy = QtCore.QSortFilterProxyModel()
kraje_proxy.setSourceModel(obce_model)
kraje_proxy.setFilterRole(obce_model.Roles.REGION.value) #works with argument 0 and name of settlement as argument on next line
kraje_proxy.setFilterRegExp(QRegExp("", QtCore.Qt.CaseSensitivity.CaseInsensitive, QRegExp.FixedString))





ctxt.setContextProperty("KrajeProxy", kraje_proxy)