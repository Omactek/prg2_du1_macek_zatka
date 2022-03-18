import QtQuick 2.14
import QtQuick.Controls 2.14


Row {
    width: 800
    height: 500

    Column {
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
                    model: ["First", "Second", "Third"]
                }

                Text{
                    id: combo_okres_label
                    text: "Okres:"
                }

                ComboBox {
                    id: combo_okres
                    model: ["First", "Second", "Third"]
                }
            }
        }
    }
}