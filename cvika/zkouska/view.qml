import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import OskPlugin 1.0

Rectangle {
    id: root
    width: 1024
    height: 633

    ListModel {
        id: personalData
        ListElement { dataLabel: "Firstname";  dataValue: "Herbert"; }
        ListElement { dataLabel: "Lastname"; dataValue: "Roth"; }
        ListElement { dataLabel: "Plays"; dataValue: "Guitar"; }
        ListElement { dataLabel: "Age"; dataValue: "65";}
        ListElement { dataLabel: "Hobby"; dataValue: "Walking"; }
        ListElement { dataLabel: "Birthday"; dataValue: "14.12.1926"; }
        ListElement {  dataLabel: "City";dataValue: "Suhl"; }
        ListElement { dataLabel: "Country"; dataValue: "Germany"; }
    }
   
    ScrollView {
        anchors.fill: parent

        ListView {
            id: listView
            anchors.fill: parent
            clip: true
            model: personalData
            focus: true

            delegate: FocusScope {
                x: rectangle.x;
                y: rectangle.y
                width: rectangle.width;
                height: rectangle.height

                Rectangle {
                    id: rectangle
                    height: 66
                    width: 500
                    border.color: "grey"
                    border.width: 2
                    TextInput {
                        anchors.centerIn: parent
                        text: dataValue
                        font.pixelSize: 24
                        focus: true
                        activeFocusOnTab: true
                        onActiveFocusChanged: if(activeFocus) { listView.currentIndex = index }
                    }
                }
            }
        }
    }
}