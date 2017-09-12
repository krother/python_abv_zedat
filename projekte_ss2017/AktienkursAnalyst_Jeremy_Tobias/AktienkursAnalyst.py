#Aktienkurse abrufen, darstellen und analysieren am Beispiel der DAX30 Unternehmen.

import os
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error


#Symbolliste der abzurufenden Aktien.
DAX30=["FME.DE","CON.DE","VNA.DE","IFX.DE","DTE.DE","HEN3.DE","LIN.DE","BEI.DE","RWE.DE","SAP.DE",
       "PSM.DE","DAI.DE","DPW.DE","BMW.DE","SIE.DE","TKA.DE","BAS.DE","BAYN.DE","VOW3.DE","DB1.DE",
       "FRE.DE","MRK.DE","HEI.DE","LHA.DE","ALV.DE","EOAN.DE","ADS.DE","MUV2.DE","DBK.DE","CBK.DE"]

#Mit den Aktienkursdaten zu füllende Liste.
DAX30_DATA_FRAMES = []

#Wiederholungsschleife bei Fehlermeldung.
print('start fetching data for DAX30')
def retryFetching(times , u):
    for i in range(times):
        try:
            result = pdr.get_data_yahoo(symbols= u , start=datetime(2012, 1, 1), end=datetime(2018, 1, 1))
        except pdr._utils.RemoteDataError:
            print("Attempt {}: couldnt fetch data for {}.".format(i , u))
            continue
        break
    return result    

#Download und Abspeichern der Daten zum Speicherort des Programms und hinterlegen der Aktienkurse in die

#leere Liste DAX30_DATA_FRAMES.
for u in DAX30:
    print('fetching data for ' + u)
    fileName = "DAX30-" + u + ".csv"
    data = retryFetching(10 , u)
    if data is None:
        raise ValueError('No data found for ' , u )  
    Endwerte=data["Adj Close"]
    Endwerte=Endwerte.fillna(method='ffill')
    Endwerte.to_csv(fileName)
    print(Endwerte)
    DAX30_DATA_FRAMES.append(Endwerte)
allFrames = pd.concat(DAX30_DATA_FRAMES, keys=DAX30 , names = ['DINDEX' , "DATE"])
grouped = allFrames.groupby('DINDEX')

#Durchschnitt des monatlichen Anstiegs der Aktienkurse.
result = grouped.nth(-1).divide(grouped.nth(0)).divide(grouped.count())

#Gibt die drei Aktienkurse mit dem höchsten Anstieg aus.
result = result.nlargest(3)

#Plottet die besten Ergebnisse.
allFrames.loc[result.keys().tolist()].unstack(level=0).plot(subplots=True , legend=True)
plt.show()

#Einlesen der drei Aktien mit dem größten Wertzugewinn durch relativen Bezug.
data_Adidas = pd.Series.from_csv(os.path.abspath("DAX30-ADS.DE.csv"))
data_Pro7 = pd.Series.from_csv(os.path.abspath("DAX30-PSM.DE.csv"))
data_Vonovia = pd.Series.from_csv(os.path.abspath("DAX30-VNA.DE.csv"))

#Plotten der Aktienkurse von 2012 bis heute.
plt.title("Historische Aktienkurse")
plt.ylabel("Aktienwert in €")
plt.xlabel("Jahr")
plt.plot(data_Adidas)
plt.plot(data_Pro7)
plt.plot(data_Vonovia)
blue_patch = mpatches.Patch(color='blue', label='Adidas')
green_patch = mpatches.Patch(color='green', label='Pro7')
orange_patch = mpatches.Patch(color='orange', label='Vonovia')
plt.legend(handles=[blue_patch,green_patch,orange_patch])
plt.show()

#Korrelogramm zur Bestimmung der Lag-Ordnung des ARIMA Prozesses am Beispiel Adidas.
#ACF geht gegen 0 und PACF bricht nach 2 lags ab.
#-> Lag-Ordnung des AR Teils entspricht voraussichtlich 2.
#Lag-Ordnung des MA Teils kann vernachlässigt werden oder anhand von Informationskriterien und 
#Mamimum Likelihood genauer bestimmt werden.
plot_acf(data_Adidas, lags=100)
plt.show()
plot_pacf(data_Adidas, lags=20)
plt.show()

#Schätzung verschiedener ARIMA Prozesse, wobei zur vereinfachung und aus 
#Übersichtsgründen auf den MA Teil und weitere Modellschätzungen verzichtet
#wird. Anhand von BIC und AIC ist ARIMA(3,1,0) zu bevorzugen.
for o in range(1,6):
    model = ARIMA(data_Adidas, order=(o,1,0))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())

#Nutzung historischer Daten als Trainingsdaten und darauf basierende Errechnung
#des Mean-Squared-Error, als Vergleichsparameter verschiedener Modelle falls vorhanden.
#https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
X = data_Adidas.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
	model = ARIMA(history, order=(3,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()

#Erwartngswert/Vorhersage des Modells für die Nächsten 5 Tage.
forecast = model_fit.forecast(steps=5)[0]
print('Die Vorhersage für die nächsten 5 Tage entspricht:')
print(forecast)
