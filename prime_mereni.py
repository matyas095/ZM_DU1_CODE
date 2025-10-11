import json, math;
from pathlib import Path
import numpy as np;

ABSOLUTE_PATH = Path(__file__).parent.resolve();

def findFile(name):
    source_dir = Path(ABSOLUTE_PATH);

    for file in source_dir.rglob(name):
        return file;

def rounding(numero):
    numero = str(numero)
    passedDot = False;
    for i in range(0, len(numero)):
        if(numero[i] == "."): passedDot = True;
        if (numero[i].isdigit() and numero[i] == "0") or numero[i] == "." or passedDot == False: continue;
        if(int(i) > 4):
            numero = numero[:i - 1] + str(int(numero[i - 1]) + 1);
        else:
            numero = numero[:i + 1];
        break;
    return float(numero);

with open(findFile("input.json")) as f:
    jThingys = json.load(f);
    hodnoty = jThingys["hodnoty"];
    velicina = jThingys["velicina"]; # Čísla ze kterých mám hodnoty měření

def aritmetr_prumer(arr):
    prumer = 0;
    for i in range(0, len(arr)):
        prumer += arr[i];
    return prumer * (1 / len(arr));

def odchylka_prumerova(prumer, hodnota_x):
    return prumer - hodnota_x;

prumer = aritmetr_prumer(hodnoty);
odchylky = [];
for i in range(0, len(hodnoty)):
    odchylky.append(odchylka_prumerova(hodnoty[i], prumer));


def stredni_kvadraticka_chyba(arr, prumer):
    hodnota_s = 0;
    for i in range(0, len(arr)):
        hodnota_s += (arr[i] - prumer) ** 2;
    return math.sqrt(hodnota_s / (len(arr) * (len(arr) - 1)));
    return "{:.1f}".format(math.sqrt(hodnota_s / (len(arr) * (len(arr) - 1))));

stredni_chyba_kvadraticka = stredni_kvadraticka_chyba(hodnoty, prumer);
# prumer = "{:.1f}".format(prumer);

data = {
    "prumer": rounding(prumer),
    "odchylky": [],
    "stredni_kvadraticka_chyba": rounding(stredni_chyba_kvadraticka),

    "velicina": velicina
};

for i in range(0, len(hodnoty)):
    odchylka = data["prumer"] - hodnoty[i];
    data["odchylky"].append(odchylka)

with open(findFile("output.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4);