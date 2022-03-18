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
            id: check_obce
            text: "Obce"
        }
        Item {
            id: slide_item
            anchors.top: parent.bottom
            anchors.left: parent.left
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
                stepSize: 1.0
                snapMode: slide.SnapAlways
            }
            Text {
                text: slide.first.value + " obyvatel"
                anchors.top: slide.bottom
                anchors.left: slide.left
            }
            Text {
                text: slide.second.value + "obyvatel"
                anchors.top: slide.bottom
                anchors.right: slide.right
            }
        }
        Text{
            text: "něco"
        }
    }
}