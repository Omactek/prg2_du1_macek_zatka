# Vývojářská dokumentace

Následující aplikace byla vytvořena v prostředí PySide2 a QtQuick. Pomocí pluginu byl přidán mapový podklad - OpenStreetMaps.

### Vstupní data
Na vstupu pracujeme se souborem obce.geojson, který uchovává data o jednotlivých obcích. Konkrétně jsou to: Název obce, název okresu, název kraje, boolovskou hodnotu zda jde o město, počet obyvatel a rozloha.

### Grafické rozhraní
Základem aplikace je RowLayout, který se skládá ze dvou sloupců (Columns) a mapového pole. V prvním sloupci (vlevo) se nachází filtrovací funkce - 2x CheckBox - města, vesnice; RangeSlider - filtrování dle počtu obyvatel sídla; Rozklikávací boxy s nabídkou krajů a okresů.

### 
