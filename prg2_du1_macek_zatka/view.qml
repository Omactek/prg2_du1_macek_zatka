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
        Column {
            id: slide_item
            anchors.top: parent.bottom
            anchors.left: parent.left
            Text {
                text: "Počet obyvatel"
                anchors.horizontalCenter: slide.horizontalCenter
                anchors.bottom: slide.top
            }
            Slider {
                id: slide
                from: 1
                to: 1000000
            }
            Text {
                text: "1 obyvatel"
                anchors.top: slide.bottom
                anchors.left: slide.left
            }
            Text {
                text: "1 000 000 obyvatel"
                anchors.top: slide.bottom
                anchors.right: slide.right
            }
        }
        Text{
            text: "něco"
            anchors.top: slide_item.bottom
            anchors.left: slide_item.left
        }
    }
}