import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14
import QtQuick.Layouts 1.1


RowLayout {
    anchors.fill: parent

    property var currentModelItem;

    Column {
        id: first_column
        anchors.fill: parent
        Layout.minimumWidth: 210

        CheckBox {
            id: check_city
            text: "Města"
            checked: true
            Binding {
                target: ObceModel
                property: "zobrazit_mesta"
                value: check_city.checked
            }
        }

        CheckBox {
            id: check_obec
            text: "Obce"
            checked: true
            Binding {
                target: ObceModel
                property: "zobrazit_vesnice"
                value: check_obec.checked
            }
        }

        Rectangle {
            id: slide_rec
            anchors.top: check_obec.bottom
            anchors.left: check_obec.left
            anchors.topMargin: 10

            Text {
                text: "Počet obyvatel"
                anchors.horizontalCenter: slide.horizontalCenter
                anchors.bottom: slide.top
            }

            RangeSlider {
                id: slide
                from: 1
                to: 1500000
                first.value: 1
                second.value: 1500000
                stepSize: 1000 //zatím nechávám na 1000, jinak to neházi integery
                snapMode: RangeSlider.SnapAlways
            }

            Text {
                text: slide.first.value + " obyvatel"
                anchors.top: slide.bottom
                anchors.left: slide.left
            }

            Text {
                text: slide.second.value + " obyvatel"
                anchors.top: slide.bottom
                anchors.right: slide.right
            }
        }

        Rectangle{
            id: combo_rec
            anchors.top: slide_rec.bottom
            anchors.left: slide_rec.left
            anchors.topMargin: 60 //velice neelegantní rešení

            Column{
                spacing: 5
                Text{
                    id: combo_kraj_label
                    text: "Kraj:"
                }

                ComboBox {
                    id: combo_kraj
                    model: ["VŠE","Hlavní město Praha","Jihočeský kraj","Jihomoravský kraj","Karlovarský kraj",
                    "Kraj Vysočina","Královéhradecký kraj","Liberecký kraj","Moravskoslezský kraj","Olomoucký kraj",
                    "Pardubický kraj","Plzeňský kraj","Středočeský kraj","Ústecký kraj","Zlínský kraj"]
                }
                Binding{
                    target: ObceModel
                    property: "area"
                    value: combo_kraj.currentIndex
                }

                Text{
                    id: combo_okres_label
                    text: "Okres:"
                }

                ComboBox {
                    id: combo_okres
                    model: dist
                }
                Binding{
                    target: ObceModel
                    property: "district"
                    value: combo_okres.currentText
                }
            }
        }

        Rectangle {
            id: filter_rec
            anchors.top: combo_rec.bottom
            anchors.left: combo_rec.left
            anchors.topMargin: 140

            Button {
                text: "Filtrovat"
            }
        }
    }
    
    ListView {
        id: seznamObci
        Layout.minimumWidth: 210 //this could be changed to item in component width
        Layout.fillWidth: false
        Layout.fillHeight: true
        focus: true

        Component {
            id: settlementListDelegate
            Item {
                width: childrenRect.width
                height: childrenRect.height
                Text {
                        text: model.display + '<br>Rozloha: ' + model.area + ' km<sup>2</sup>' + '<br>Počet obyvatel: ' + model.population + '<br>'
                        textFormat: Text.RichText
                        color: {
                            if (model.township == "Město")
                                color = "red"
                            if (model.township == "Vesnice")
                                color = "black"

                        }
                        font.bold: {
                            if (model.township == "Město")
                                font.bold = true
                            if (model.township == "Vesnice")
                                font.bold = false

                        }
                    }
                MouseArea {
                    anchors.fill: parent
                    onClicked: seznamObci.currentIndex = index
                }
            }
        }

        model: DelegateModel {
            id: settlementListDelegateModel
            model: FinalProxy
            delegate: settlementListDelegate
        }

        onCurrentItemChanged: currentModelItem = settlementListDelegateModel.items.get(seznamObci.currentIndex).model

        highlight: Rectangle {
            color: "lightsteelblue"
        }
    }

    Plugin {
        id: mapPlugin
        name: "osm" // We want OpenStreetMap map provider
        PluginParameter {
             name:"https://tile.openstreetmap.org"
             value:"https://a.tile.openstreetmap.de/${z}/${x}/${y}.png" // We want custom tile server for tiles without labels
        }
    }

    Map { //mapa zatím nefuguje ale alespoň je tam vídět rozměr
        id: map
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.alignment: Qt.AlignRight

        plugin: mapPlugin
        activeMapType: supportedMapTypes[supportedMapTypes.length - 1] // Use our custom tile server

        center: currentModelItem.location // Center to the selected city
        zoomLevel: 10

        MapItemView {
            model: FinalProxy
            delegate: MapQuickItem {
                coordinate: model.location
                sourceItem: Loader{
                    sourceComponent:
                        if (township == "Město")
                            return idCityText
                        else if (township == "Vesnice")
                            return idNotcityText
                }
                visible: slide.first.value <= model.population && slide.second.value >= model.population //hides settlements outside of slideranger range
                
                Component{
                    id: idCityText
                    Text {
                        text: model.display
                        color: "red"
                        font.bold: true
                        x: 13
                        y: -13
                    }
                }
                Component{
                    id: idNotcityText
                    Text {
                        text: model.display
                        color: "black"
                        x: 10
                        y: -10
                    }
                }
            }
        }

        MapItemView {
            id: main_map
            model: FinalProxy
            delegate: MapQuickItem {
                coordinate: model.location
                sourceItem: Loader{
                    sourceComponent:
                        if (township == "Město")
                            return idCity
                        else if (township == "Vesnice")
                            return idNotcity
                }
                visible: slide.first.value <= model.population && slide.second.value >= model.population
                
                Component{
                    id: idCity
                    Rectangle {
                        width: 15
                        height: width
                        color: "red"
                        border.color: "black"
                        border.width: 1
                        radius: width*0.5
                    }
                }
                Component{
                    id: idNotcity
                    Rectangle {
                        width: 10
                        height: width
                        color: "black"
                        border.color: "black"
                        border.width: 1
                        radius: width*0.5
                    }
                }
            }
        }
    }
}