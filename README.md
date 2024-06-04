## Kuidas kasutada?
Kontrolli, et arvutis oleks Python ja Mavproxy.

Installi `requirements.txt`, avades CMDs mavlink-telemeetria kausta ning sisestades käsu:
```
pip install -r requirements.txt
```
Aktiveeri _virtual environment_. Sisestage
```
venv\Scripts\activate
```
**Kontrolli config.ini failis olevad parameetrid.**

Jooksuta `main.py` kasutades käsku
```
python main.py
```
Jooskuta command promptis
```
mavproxy --master=COMx --out 127.0.0.1:14550
```
`x` asendada pordi numbriga, millesse raadio on ühendatud (vt Device Managerist).

Kui MAVPROXY saab MAVLINKi ühenduse kätte, peaks antennisuunaja tööle hakkama.
