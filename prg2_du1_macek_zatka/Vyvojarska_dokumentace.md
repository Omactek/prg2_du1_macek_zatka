# Vývojářská dokumentace

Následující aplikace byla vytvořena v prostředí PySide2 a QtQuick. Pomocí pluginu byl přidán mapový podklad - OpenStreetMaps.

### Vstupní data
Na vstupu pracujeme se souborem obce.geojson, který uchovává data o jednotlivých obcích. Konkrétně jsou to: Název obce, název okresu, název kraje, boolovskou hodnotu zda jde o město, počet obyvatel a rozloha.

### Grafické rozhraní
Základem aplikace je RowLayout, který se skládá ze dvou sloupců (Columns) a mapového pole. V prvním sloupci (vlevo) se nachází filtrovací funkce - 2x CheckBox - města, vesnice; RangeSlider - filtrování dle počtu obyvatel sídla; Rozklikávací boxy s nabídkou krajů a okresů.

### Průběh filtrování
Při každé změně nastavení filtrů probíhá filtrování dle daného parametru. Filtrovaní zajišťují proxy modely volané v setterech při každé změně v parametrech filtrů.
Výjimkou je filtrování dle počtu ubyvatel, které není filtrováním v pravém slova smyslu, ale probíhá v qml.

### Modely
Využíváme 5 modelů nad sebou a jednoho přídavného (dist), který je využíván k získání listu okresů dle zvoleného kraje.
