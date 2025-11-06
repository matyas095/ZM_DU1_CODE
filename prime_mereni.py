import json, math;
from pathlib import Path;
import numpy as np;

from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt;

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

bins = np.arange(np.floor(min(hodnoty)), np.ceil(max(hodnoty)) + 1, 1)

plt.hist(hodnoty, bins=bins, edgecolor="black", density=False)
plt.xlabel("Proud [mA]")
plt.ylabel("Četnost měření")
plt.title("Histogram měření")
plt.grid(axis="y", alpha=0.3)

# popisky osy X jen pro celá čísla
plt.gca().xaxis.set_major_locator(MultipleLocator(1))

plt.savefig("storager/histogram.png");
plt.show();

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
    data["odchylky"].append(odchylka);

with open(findFile("output.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4);