# Script for generate Grafana dashboard based on Astra config

Before it you must read https://radiosintetica.ru/2018/03/20/astra-grafana/

Requirements:
- Python 3
- Grafana 5.3.4 (Only on this was tested)
- Astra 5.64

---

For generate dashboard:

Place your astra config into config_from_astra.json and run:

```./generate.py config_from_astra.json``` 

Will generate source into `out.json` in same directory. After it you must import it in Grafana. In process script will ask you for dashboard name and for datasource name in Grafana.

---

In `./grafana` found separated template, you can customize/change it.

Result looks like this:
![Grafana](/preview.png)

---
P.S.: For now it was made for myself and not have presentative look, because have little of time, but it works. Also, for now you can`t change grid properties quickly (size, count of graphs per row, etc.).