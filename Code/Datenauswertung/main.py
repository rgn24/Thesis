import os
import pandas as pd

class Messreihe:
    def __init__(self, directory_path):
        self.path = directory_path
        self.name = os.path.basename(directory_path)
        self.length = 0

    def preprocess(self):
        # Liste aller CSV-Dateien im angegebenen Verzeichnis
        csv_files = [f for f in os.listdir(self.path) if f.endswith('.csv')]

        # Alle CSV-Dateien im Verzeichnis einlesen und in einer Liste speichern
        data_frames = []
        for file in csv_files:
            data_frames.append(pd.read_csv(os.path.join(self.path, file)))

        # Alle DataFrames in der Liste zu einem DataFrame zusammenfügen
        merged_df = pd.concat(data_frames, axis=0, ignore_index=True)

        # Doppelte Spalten entfernen
        merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

        # Anzahl der Zeilen festlegen
        self.length = len(merged_df)

        # Zusammengeführten DataFrame in eine neue CSV-Datei schreiben
        merged_df.to_csv(os.path.join(self.path, "combined_data.csv"), index=False)

    def get_info(self):
        return {"name": self.name, "length": self.length}

def main():
    # Angabe des übergeordneten Verzeichnisses, das alle Messreihen enthält
    base_directory = "Messreihen/"

    # Alle Unterordner (Messreihen) finden
    all_directories = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    print(all_directories)

    messreihen = []
    for directory in all_directories:
        m = Messreihe(directory)
        m.preprocess()
        messreihen.append(m)

    # Infos aller Messreihen anzeigen
    for m in messreihen:
        print(m.get_info())

if __name__ == '__main__':
    main()
