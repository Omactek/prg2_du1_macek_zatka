from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray, QRegExp

from prg2_du1_macek_zatka.city import VIEW_URL
obce_proxy = QtCore.QSortFilterProxyModel()
obce_proxy.setSourceModel(citylist_model)
obce_proxy.setFilterRegExp(QRegExp("Adamov", QtCore.Qt.CaseSensitivity.CaseInsensitive,
                                    QRegExp.FixedString))

"""               
VIEW
proxy 6
proxy 5
...
model_obec
"""