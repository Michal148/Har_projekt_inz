import pyodbc
import pandas as pd 
from pathlib import Path
import os
from cechy import *

# robocza nazwa plików
# SensorNameActivityPlatform.csv

# wczytanie zmiennych środowiskowych
driver = os.environ['DBDriver']
server = os.environ['DBServer']
database = os.environ['DBDb']
username = os.environ['DBUser']
password = os.environ['DBPass']

directory = './user-features/streaming-work-dir'
dirs = sorted(Path(directory).glob('*'))

# zainicjowanie połączenia w celu utworzenia kolumn 
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        # iterowanie po plikach 
        for dir in dirs:
            files = sorted(Path(dir).glob('*'))

            for file in files:
                sensorTableName = os.path.basename(os.path.normpath(file)).replace('.csv', '')
                tableQuery = f"CREATE TABLE [dbo].[{sensorTableName}] ( \
                                    [time]            BIGINT       NULL, \
                                    [seconds_elapsed] VARCHAR (MAX) NULL, \
                                    [x]             VARCHAR (MAX) NULL, \
                                    [y]              VARCHAR (MAX) NULL, \
                                    [z]              VARCHAR (MAX) NULL, \
                                    [platform]              VARCHAR (MAX) NULL, \
                                    [activity]              VARCHAR (MAX) NULL, \
                                    [activityPackage]              VARCHAR (MAX) NULL);"

                cursor.execute(tableQuery)
                conn.commit()
                
print("tables created successfully")

# otwarcie nowego połączenia do stworzenia tabel oraz umieszczenia danych 
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        # enable fast_executemany attribute for quicker data pushing
        cursor.fast_executemany = True 
        
        for dir in dirs:
            print("currently processed directory: "+ str(dir))
            files = sorted(Path(dir).glob('*'))
            
            # umieszczanie plików do bazy danych
            for file in files:
                
                # sprawdzenie platformy oraz nazwy aktywności
                if "Apple" in str(file):
                    platform = "apple"
                else:
                    platform = "android"

                if "Upstairs" in str(file):
                    activityName = "upstairs"
                elif "Downstairs" in str(file):
                    activityName = "downstairs"
                elif "Squats" in str(file):
                    activityName = "squats"
                elif "Sitting" in str(file):
                    activityName = "sitting"
                elif "Standing" in str(file):
                    activityName = "standing"
                elif "Lying" in str(file):
                    activityName = "lying"
                elif "Walking" in str(file):
                    activityName = "walking"

            print("processed: " + str(dir))
            conn.commit()
            print("committed")







            
                    

            

    