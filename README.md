## Kuidas kasutada?
- Kontrolli, et arvutis oleks Python. Seejärel installi `requirements.txt` kasutades käsku `pip install -r requirements.txt `
- Kontrolli config.txt failis olevad parameetrid.
- Jooksuta `main.py`.
- Kui pole, installi mavproxy.
- Jooskuta command promptis `mavproxy --master=COMx --out 127.0.0.1:14550`. `x` asendada pordi numbriga, millesse raadio on ühendatud (vt Device Managerist).
- Kui MAVPROXY saab MAVLINKi ühenduse kätte, peaks antennisuunaja tööle hakkama.
