import csv

schueler_path = r"C:\Users\hp-laptop-info\Downloads\Benutzer_kant-gymnasium.de_21.02.2023.csv"
kurswahl_path = r"C:\Users\hp-laptop-info\Downloads\Klasse7 Wahlen der Wahlpflichtfächer 2022_23 - 21.02.2023.csv"

output_path = r"C:\Users\hp-laptop-info\Desktop\output.csv"


with open(schueler_path, "r", encoding="utf-8") as schueler_file, open(kurswahl_path, "r", encoding="ansi") as kurswahl_file, open(output_path, "w+", encoding="utf-8") as output_file:
    schueler_reader = csv.reader(schueler_file, delimiter=";", quotechar='"', lineterminator="\n")
    kurswahl_reader = csv.reader(kurswahl_file, delimiter=";", quotechar='"', lineterminator="\n")
    output_writer = csv.writer(output_file, delimiter=";", quotechar='"', lineterminator="\n")

    schueler_namen = dict()
    kurswahlen = dict()

    # Frau Seltmann taucht natürlich nicht in der Schülerliste auf
    schueler_namen["74709b00a5f4433b49ecfb9c105427c8"] = ("J.", "Seltmann")

    cols = next(schueler_reader)

    schueler_id_index = cols.index("Import-ID")
    schueler_firstname_index = cols.index("Vorname")
    schueler_lastname_index = cols.index("Nachname")

    cols = next(kurswahl_reader)

    kurswahl_id_index = cols.index("Import-ID")
    kurswahl_klasse_index = cols.index("Zusätzliche Informationen")
    kurswahl_wgruppe_index = cols.index("Wahlgruppe")
    kurswahl_option_id_index = cols.index("ID")
    kurswahl_option_index = cols.index("Option")
    kurswahl_datum_index = cols.index("Hinzugefügt")

    output_cols = ["ID", "Vorname", "Nachname", "Klasse", "Datum"]

    wahl_gruppen = list()

    for row in schueler_reader:
        schueler_namen[row[schueler_id_index]] = (row[schueler_firstname_index], row[schueler_lastname_index])
    
    for row in kurswahl_reader:
        if row[kurswahl_wgruppe_index] not in wahl_gruppen:
            wahl_gruppen.append(row[kurswahl_wgruppe_index])

        schueler_id = row[kurswahl_id_index]

        if schueler_id not in kurswahlen:
            kurswahlen[schueler_id] = [schueler_namen[schueler_id][0], schueler_namen[schueler_id][1], row[kurswahl_klasse_index], row[kurswahl_datum_index], {}]
        
        kurswahlen[schueler_id][4][row[kurswahl_wgruppe_index]] = (row[kurswahl_option_id_index], row[kurswahl_option_index])
    
    for wahl_gruppe in wahl_gruppen:
        output_cols.append(wahl_gruppe)
        output_cols.append("Gewählter " + wahl_gruppe + " Kurs")

    output_writer.writerow(output_cols)
    print(output_cols)
    
    for kurswahl in kurswahlen:
        l = kurswahlen[kurswahl]
        out_row = [kurswahl] + l[:4]
        wahlen = l[4]

        for gruppe in wahl_gruppen:
            if gruppe not in wahlen:
                out_row.append("")
                out_row.append("")
            else:
                wahl = wahlen[gruppe]
                out_row.append(wahl[0])
                out_row.append(wahl[1])
        
        print(out_row)
        output_writer.writerow(out_row)
