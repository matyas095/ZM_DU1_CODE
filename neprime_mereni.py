import json, math;
from pathlib import Path;
import numpy as np;

from matplotlib.ticker import MultipleLocator, MaxNLocator
import matplotlib.pyplot as plt;
import collections

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

for obj in hodnoty:
    nameThingy = obj if obj not in ["vaha", "vyska"] else {"vaha": "Váha", "vyska": "Výška"}[obj];
    bins = np.arange(np.floor(min(hodnoty[obj]["hodnoty"])), np.ceil(max(hodnoty[obj]["hodnoty"])) + 1, 1);

    if(obj == "vaha"):
        values = [500.03, 510.66, 503.97, 494.69, 504.43];
        bins = [494, 500, 504, 508, 512];

        plt.figure(figsize=(8,4));
        plt.hist(values, bins=bins, edgecolor='black');
        plt.title("Histogram měření");
        plt.xlabel("Hodnoty [mm]");
        plt.ylabel("Četnost měření");
        plt.xticks(np.arange(bins[0], bins[-1] + 1, 1));
        plt.grid(axis="y", alpha=0.3);

        plt.tight_layout();
        plt.savefig(f"storager/histogramy/{obj}.png");
        continue;

    plt.hist(hodnoty[obj]["hodnoty"], bins=bins, edgecolor="black", density=False);
    plt.xlabel(f"{nameThingy} [{hodnoty[obj]["velicina"]}]");
    plt.ylabel("Četnost měření");
    plt.title("Histogram měření");
    plt.grid(axis="y", alpha=0.3);
    plt.gca().xaxis.set_major_locator(MultipleLocator(1));

    plt.savefig(f"storager/histogramy/{obj}.png");


def aritmetr_prumer(arr):
    prumer = 0;
    for i in range(0, len(arr)):
        prumer += arr[i];
    return prumer * (1 / len(arr));

def odchylka_prumerova(prumer, hodnota_x):
    return prumer - hodnota_x;

prumery = {};
for obj in hodnoty:
    val = hodnoty[obj];
    nameThingy = obj if obj not in ["vaha", "vyska"] else {"vaha": "Váha", "vyska": "Výška"}[obj];

    prumery[nameThingy] = { "aritmetr": rounding(aritmetr_prumer(val["hodnoty"])), "velicina": val["velicina"] };

def stredni_kvadraticka_chyba(arr, prumer):
    hodnota_s = 0;
    for i in range(0, len(arr)):
        hodnota_s += (arr[i] - prumer) ** 2;
    return math.sqrt(hodnota_s / (len(arr) - 1));

chyby_stredni = {};
for obj in hodnoty:
    val = hodnoty[obj];
    nameThingy = obj if obj not in ["vaha", "vyska"] else {"vaha": "Váha", "vyska": "Výška"}[obj];

    chyby_stredni[nameThingy] = rounding(stredni_kvadraticka_chyba(val["hodnoty"], prumery[nameThingy]["aritmetr"]));

def chyba_aritmetreho_prumeru(arr, chyba):
    return chyba / math.sqrt(len(arr));

chyby_aritmetru = {};
for obj in hodnoty:
    val = hodnoty[obj];
    nameThingy = obj if obj not in ["vaha", "vyska"] else {"vaha": "Váha", "vyska": "Výška"}[obj];

    chyby_aritmetru[nameThingy] = rounding(chyba_aritmetreho_prumeru(val["hodnoty"], chyby_stredni[nameThingy]));


data = {
    "prumer": prumery,
    "odchylky": [],
    "stredni_kvadraticka_chyba": chyby_stredni,
    "chyba_aritmetickeho_prumeru": chyby_aritmetru,
};
with open(findFile("output.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4);

""" stredni_chyba_kvadraticka = stredni_kvadraticka_chyba(hodnoty, prumer);
# prumer = "{:.1f}".format(prumer);

data = {
    "prumer": rounding(prumer),
    "odchylky": [],
    "stredni_kvadraticka_chyba": rounding(stredni_chyba_kvadraticka),
    "chyba_aritmetickeho_prumeru": rounding(chyba_aritmetreho_prumeru),
};

for i in range(0, len(hodnoty)):
    odchylka = data["prumer"] - hodnoty[i];
    data["odchylky"].append(odchylka);

with open(findFile("output.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4); """