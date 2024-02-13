import pandas as pd
import numpy as np
import warnings
from cechy import *
warnings.filterwarnings('ignore')
import os

folder_path =  "C:/Users/micha/OneDrive/Pulpit/cechy/fifth-run/new"


for filename in os.listdir(folder_path):
    if "Features" in filename:  # filtrowanie plikow csv
        file_path = os.path.join(folder_path, filename)
        newName = filename.replace("Features", "Featuresseg")
        df = pd.read_csv(file_path)
        segList = [df]


    try:
        for idx, seg in enumerate(segList):
            windows = []
            seg = seg[['time', 'x', 'y', 'z']]
            df_len = len(seg)

            # wybranie dlugosci początkowego i końcowego odcięcia
            head = 5
            tail = 5

            # ustalenie wielkosci okien 500 = 5 sekundowe okna czasowe
            windowslen = 500
            range_df = seg.iloc[head*100:df_len-tail*100]
            adj = len(range_df)%windowslen
            
            for i in range(df_len-tail*100-adj):
                if i % windowslen == 0:    
                    currSeg = range_df.iloc[i:i+windowslen+1].reset_index(False).drop(columns = ['index'])
                    window_feat = feats_df(currSeg)
                    windows.append(window_feat)

            currDf = pd.concat(windows)
            if idx == 0:
                currDf.to_csv(f"./{newName}")

    except:
        continue
        
# Tworzenie jednego pliku zawierającego wszystkie pliki csv połączone w jeden plik
csv_files = [file for file in os.listdir("C:/Users/micha/OneDrive/Pulpit/cechy/fifth-run") if "FeaturesAccelerometer" in file]
merged_data = pd.DataFrame()

for file in csv_files:
    data = pd.read_csv("C:/Users/micha/OneDrive/Pulpit/cechy/fifth-run/"+file)
    merged_data = merged_data.append(data)
    
merged_data.to_csv('feats_version_5_2233_acc.csv', index=False)   