import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14
import QtQuick.Layouts 1.1


Row{
    width: 1000
    height: 500

    Column {
        id: first_column
        width: parent.width/4
        height: parent.height

        CheckBox {
            id: check_city
            text: "Města"
        }

        CheckBox {
            id: check_obec
            text: "Obce"
        }

        Rectangle {
            id: slide_rec
            height: fill
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
                to: 1000000
                first.value: 1
                second.value: 1000000
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
                    currentIndex: -1
                    model: ["First", "Second", "Third"]
                }

                Text{
                    id: combo_okres_label
                    text: "Okres:"
                }

                ComboBox {
                    currentIndex: -1
                    id: combo_okres
                    model: ["First", "Second", "Third"]
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

    Plugin {
        id: mapPlugin
        name: "osm" // We want OpenStreetMap map provider
        PluginParameter {
             name:"osm.mapping.custom.host"
             value:"https://maps.wikimedia.org/osm/" // We want custom tile server for tiles without labels
        }
    }

    Map { //mapa zatím nefuguje ale alespoň je tam vídět rozměr
        id: map
        width: parent.width/2
        height: parent.height

        plugin: mapPlugin
        activeMapType: supportedMapTypes[supportedMapTypes.length - 1] // Use our custom tile server

        center: currentModelItem.location // Center to the selected city
        zoomLevel: 10

        MapItemView {
            model: cityListModel
            delegate: MapQuickItem {
                coordinate: model.location
                sourceItem: Text{
                    text: model.display
                }
            }
        }
    }

    Rectangle {
        id: third_column
        width: parent.width/4
        height: parent.height

        ListView{
            id: list_display
            model: ContactModel {}
            delegate: Text {
                text: name + ": " + number
            }
        }
    }
}