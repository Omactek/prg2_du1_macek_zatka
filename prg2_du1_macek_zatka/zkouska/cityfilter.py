from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray, QRegExp
obce_proxy = QtCore.QSortFilterProxyModel()
obce_proxy.setSourceModel(citylist_model)
obce_proxy.setFilterRegExp(QRegExp("Adamov", QtCore.Qt.CaseSensitivity.CaseInsensitive,
                                    QRegExp.FixedString))

                            