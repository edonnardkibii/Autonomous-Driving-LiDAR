# **Bachelorarbeit**

## **Steuerung eines Kleinfahrzeugs mit einem Laserscanner**
**Betreuer (Owner): Prof. Dr. Hartmut Gimpel (Fakultät MA) <br/>**
**Studenten (Developers): James Kibii, EIB ; Manuel Greiter, EIB <br/>**

In diesem Projekt wird ein Maker-Kleinfahrzeug um einen industriellen Laserscanner
(2D-LiDar) ergänzt. 
Mit dem integrierten Raspberry-Pi 4 Einplatinencomputer werden die Punktwolken-Daten
des Laserscanners ausgelesen. Damit wird eine autonome Steuerung des Fahrzeugs umgesetzt. <br/>

Die folgenden Komponenten werden für dieses Projekt verwendet: <br/>
1. Raspberry Pi 4 2GB RAM
2. SICK TIM310-1030000S01 2D-Laserscanner
3. Sunfounder Smart Sensor Car Kit
4. DC-DC Step-Up Spannungsregler
5. 2x 18650 Akkumulatoren

Das Projekt wird mit der Programmiersprache Python durchgeführt. Der Kern dieses Projekts ist die Implementierung der
Bibliothek pyusb [PyPi](https://pypi.org/project/pyusb/), [Github](https://github.com/pyusb/pyusb) zum
Auslesen der Daten über Endpoints.<br/>
Zum besseren Verständnis des 2D-LiDar kann man sich das folgende Youtube-Video [LiDar Tutorial](https://www.youtube.com/watch?v=wKrJ0fx648A&ab_channel=SICKSensorIntelligence.)
der Firma SICK ansehen. <br/>
Ein Tutorial zu Data-Telegrammen finden Sie auch hier 
[Telegramms Tutorial](https://www.youtube.com/watch?v=cTy66J6B8WY&ab_channel=SICKSensorIntelligence.). <br/>

### **Nützliche Links**
* [Operating Instructions](https://www.sick.com/media/pdf/4/04/604/IM0044604.PDF)
* [TiM-Serie, TiM3xx, Produktfamilienübersicht](https://cdn.sick.com/media/familyoverview/1/51/751/familyOverview_TiM3xx_g205751_de.pdf)
* [SOPAS Software](https://www.sick.com/de/de/sopas-engineering-tool-2020/p/p367244)
