import pandas as pd
import json


def ciselnikJSON(file_name):
    """
    Na základě vstupních dat vygeneruje JSON strukturu číselníku pro Otevřená data (OD).

    Z názvu nahraného souboru vytvoří název pro výstupní soubor (ve formátu - malá písmena, s diakritikou, spojená pomlčkou).
    Propisuje se také do iri datové sady i jendotlivých položek. Dále vytvoří prázdný dict s přednastavenou hlavičkou a částí
    "položky", která se iterativně naplní daty ze zdrojového souboru.


    Parameters
    ----------
    file_name (str): název souboru (musí odpovídat názvu datové sady v OD), kde jsou vstupní data.
                     Struktura - Kód, Název, Popis.

    Returns
    -------
    JSON file (file): výstupní soubor ve formátu JSON
    ciselnik_dict (dict): dict se strukturou číselníku, slouží hlavně k zobrazení výsledku

    """

    df = pd.read_excel(file_name)

    name = file_name.split('.')[0]  # název bez přípony (např. xlsx)

    json_file_name = '-'.join(name.lower().split(' ')) + '.json'  # název spojený pomlčkami, malá písmena

    iri = 'https://www.tacr.cz/opendata/číselníky/' + json_file_name

    # základní struktura dict
    # předvyplněná hlavička
    ciselnik_dict = {
        "@context": "https://ofn.gov.cz/číselníky/2022-02-08/kontexty/číselník.jsonld",
        "typ": "Číselník",
        "iri": iri,
        "název": {
            "cs": name
        },
        "položky": []
    }

    # naplnění části dict "položky"
    for i in range(len(df)):
        # data k naplnění
        kod = df.iloc[i, 0]
        nazev = df.iloc[i, 1]
        popis = df.iloc[i, 2]

        # naplnění dat
        child_dict = {
            "typ": "Položka",
            "iri": iri + '/' + str(kod),
            "kód": str(kod),
            "název": {
                "cs": nazev
            },
            "popis": {
                "cs": popis
            }
        }

        ciselnik_dict['položky'].append(child_dict)

    # vytvoření JSON souboru
    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(ciselnik_dict, f, ensure_ascii=False)

    return ciselnik_dict


def ciselnikCSV(file_name):
    """
    Na základě vstupních dat vygeneruje CSV strukturu číselníku pro Otevřená data (OD).

    Z názvu nahraného souboru vytvoří název pro výstupní soubor (ve formátu - malá písmena, s diakritikou, spojená pomlčkou).
    Propisuje se také do iri datové sady i jendotlivých položek. Dále vytvoří DataFrame s přednastavenou hlavičkou a částmi
    které se iterativně naplní daty ze zdrojového souboru.


    Parameters
    ----------
    file_name (str): název souboru (musí odpovídat názvu datové sady v OD), kde jsou vstupní data.
                     Struktura - Kód, Název, Popis.

    Returns
    -------
    CSV file (file): výstupní soubor ve formátu CSV
    ciselnik_df (DataFrame): DataFrame se strukturou číselníku, slouží hlavně k zobrazení výsledku

    """

    df = pd.read_excel(file_name)

    name = file_name.split('.')[0]  # název bez přípony (např. xlsx)

    csv_file_name = '-'.join(name.lower().split(' ')) + '.csv'  # název spojený pomlčkami, malá písmena

    iri = 'https://www.tacr.cz/opendata/číselníky/' + csv_file_name

    # standardizované názvy sloupců
    cols = ['číselník', 'číselník_název_cs', 'číselník_položka'
        , 'číselník_položka_kód', 'číselník_položka_název_cs', 'číselník_položka_popis_cs']

    ciselnik_list = []

    for i in range(len(df)):
        kod = int(df.iloc[i, 0])
        nazev = df.iloc[i, 1]
        popis = df.iloc[i, 2]

        iri_polozka = iri + '/' + str(kod)

        ciselnik_list.append([iri, name, iri_polozka, kod, nazev, popis])

    ciselnik_df = pd.DataFrame(ciselnik_list, columns=cols)
    ciselnik_df.to_csv(csv_file_name, encoding='utf-8', index=False)

    return ciselnik_df