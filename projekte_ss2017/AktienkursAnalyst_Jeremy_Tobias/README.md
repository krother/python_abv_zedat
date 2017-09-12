
# AktienkursAnalyst 

**von Jeremy Zeisler (jeremy.zeisler@googlemail.com) und Tobias Fl�rchinger (to-flor@web.de)**

*Version vom 06/09/2017*

![Aktienkurse](aktienkurse.png)

## Programmidee

Der Grundgedanke des Programms ist es Aktienkurse abzurufen, graphisch darzustellen und zu analysieren bzw. zu prognostizieren. Hierf�r werden bespielhaft die DAX30 Unternehmen und f�r die Analysen bzw. Prognosen die Adidas Aktie herangezogen.


## Aufbau des Programms

Der erste Teil des Programms liest die Daten der Aktienkurse aus der Yahoo Datenbank aus und l�dt sie herunter, wobei f�r jede Aktie eine CSV Datei entsteht. Daraufhin werden die Dateien analysiert und die Kurse der drei Unternehmen, welche sich im monatlichen Schnitt des Aktienwertes am besten entwickelt haben, graphisch ausgeben. Anschlie�end folgen einige statistische Analysen am Beispiel der Adidas Aktie. Ziel ist es Vorhersagen �ber den Aktienkurs treffen zu k�nnen. Dazu wird mit Hilfe von Informationskriterien, wie dem Autokorrelogramm, dem partiellen Autokorrelogramm, BIC, AIC und MSE, ein durch differenzieren station�rer und m�glichst zweckm��iger ARIMA(p,1,q) Prozess gesucht, welcher Prognosen f�r den Wert der Akite in kommenden Perioden ausgeben kann.


## Nutzen und Nutzung

In dem aktuellen Zustand l�st das Programm noch kein klar benanntes gr��eres Problem, bildet allerdings eine Code Basis f�r finanzwissenschaftliche Fragestellungen. Durch jeweilige Erweiterungen l�sst es sich f�r Portfolioanalysen, die Anwendung Sigma-mue-Theorie, Trading und weitere Aktienkursanalysen einsetzen.

Der Programmcode ist unter den Bedingungen der MIT-Lizenz nutzbar.


## Hinweise und Quellen

* bei Ausf�hrung des Programms entstehen 30 CSV Dateien im Speicherort des Programms.
* das Downloaden der Aktienkurse kann zum Teil lange dauern, da unter umst�nden mehrfach
  zugegriffen werden muss bis die Aktienkurse erfasst werden.
* Sch�tzungen des ARIMA Prozesses ben�tigen mitunter hohe Rechenleistung
* die Sch�tzung es MSE basiert auf folgener Quelle: https://machinelearningmastery.com/arima-for-time-seriesforecasting-with-python/
