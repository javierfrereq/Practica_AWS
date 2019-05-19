# coding=utf-8
import csv
import datetime as dt
import pandas as pd
import numpy as np
import recordatorio
import drive

hoy = dt.datetime.now().strftime("%Y-%m-%d")

def read_csv():
    eventos = {}
    with open('eventos.csv', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        i = 0
        for row in csv_reader:
            if i == 0:
                fields = row
            else:
                eventos[i - 1] = {}
                for j in range(0, len(fields)):
                    if fields[j] == "fecha":
                        eventos[i - 1][str(fields[j])] = dt.datetime.strptime(row[j], "%Y-%m-%d")
                    else:
                        eventos[i - 1][str(fields[j])] = row[j]

            i = i + 1
    df = pd.DataFrame.from_dict(eventos, orient='index')
    return df

pd.set_option('precision', 0)
#df = read_csv()
df = drive.gsheet2df()
df['fecha'] = pd.to_datetime(df['fecha'])

df.loc[df.repeticion == 'a', "año"] = int(dt.datetime.now().year)
df.loc[df.repeticion == 'a', "mes"] = pd.DatetimeIndex(df['fecha']).month
df.loc[df.repeticion == 'a', "dia"] = pd.DatetimeIndex(df['fecha']).day
df['fecha_recordatorio'] = pd.to_datetime(
    ((df.año).astype(dtype=int)).astype(dtype=str) + "-" + (df.mes).astype(dtype=str) + "-" + (df.dia).astype(
        dtype=str))

df.loc[(df.recordatorio.str.slice(-1) == 'd') & (df.repeticion == 'a'), "intervalo"] = (df.recordatorio.str.slice(0,
                                                                                                                  2).astype(
    dtype=np.int64) * 1).astype(dtype=np.str) + ' days'
df.loc[(df.recordatorio.str.slice(-1) == 's') & (df.repeticion == 'a'), "intervalo"] = (df.recordatorio.str.slice(0,
                                                                                                                  2).astype(
    dtype=np.int64) * 7).astype(dtype=np.str) + ' days'
df.loc[(df.recordatorio.str.slice(-1) == 'm') & (df.repeticion == 'a'), "intervalo"] = (df.recordatorio.str.slice(0,
                                                                                                                  2).astype(
    dtype=np.int64) * 30).astype(dtype=np.str) + ' days'
df.loc[(df.recordatorio.str.slice(-1) == 'a') & (df.repeticion == 'a'), "intervalo"] = (df.recordatorio.str.slice(0,
                                                                                                                  2).astype(
    dtype=np.int64) * 365).astype(dtype=np.str) + ' days'

df['fecha_recordatorio'] = df['fecha_recordatorio'] + pd.to_timedelta(df.intervalo)

mask = (df['fecha_recordatorio'] == hoy)
resultado = list(df.loc[mask].descripcion)
print(resultado)
mensaje = ""
mensaje += 'Este es un recordatorio de los siguientes eventos:<br><br>'
mensaje += '<br>'.join(resultado)
#print(mensaje)

######################################################################################

recordatorio.send_email("Recordatorio "+hoy,mensaje)
