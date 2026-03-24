#Questa libreria serve per poter fare le operazioni sui vettori senza dover scrivere cicli estesi ogni volta e per rendere l'esecuzione più veloce
import numpy
#Questa libreria è necessaria per poter disegnare i grafici
import matplotlib.pyplot as plot
#Questa libreria serve per interagire con le cartelle
import os
#-------------------------------------------------------------------------------------------------------------------------------------------------
#FUNZIONE CHE CALCOLA IL PUNTO DI MINIMO USANDO IL METODO DELLA DISCESA DEL GRADIENTE
def discesa_gradiente(x, y, gamma=0.0001, iterazioni=2000000, tol=0.0000001):
    #gamma: serve a determinare la grandezza di ogni passaggio
    #iterazioni: serve a determinare il numero massimo di volte che verrà eseguito il ciclo
    #tol: indica la soglia di precisione
    
    #Determinazione della numerosità del campione 
    n = len(x)

    #Inizializzazione dei parametri 
    a = 0.0
    b = 0.0
    
    for i in range(iterazioni):
        #Calcolo del vettore di previsioni del valore y
        y_prev = a*x + b
        
        #Calcolo delle derivate parziali rispetto ad a e b
        da = (-2/n)*numpy.sum(x*(y - y_prev))
        db = (-2/n)*numpy.sum(y - y_prev)

        #Calcolo degli incrementi dei parametri
        incr_a = gamma*da
        incr_b = gamma*db
        
        #Controlliamo se la distanza dei vecchi a e b rispetto ai nuovi a e b è minore della tolleranza accettabile
        if abs(incr_a) < tol and abs(incr_b) < tol:
            #La distanza è minore della soglia, quindi abbiamo finito
            break

        #Aggiornamento dei parametri
        a = a - incr_a
        b = b - incr_b

    #Gli a e b ottenuti alla fine del ciclo sono le coordinate approssimate del punto di minimo   
    return a, b
#-------------------------------------------------------------------------------------------------------------------------------------------------
#FUNZIONE CHE CALCOLA LA MATRICE DI COVARIANZA
def matrice_covarianza(dati):
    mat_covarianza = numpy.cov(dati, rowvar=False)
    print("\nMatrice di Covarianza:\n", mat_covarianza)

    return mat_covarianza
#-------------------------------------------------------------------------------------------------------------------------------------------------
#FUNZIONE CHE CALCOLA L'AUTODECOMPOSIZIONE
def autodecomposizione(dati, matrice):
    #Calcoliamo autovettori (direzioni lungo cui i dati variano di più) e autovalori (importanza di ogni direzione)
    autovalori, autovettori = numpy.linalg.eigh(matrice)

    #Riordiniamo autovalori in ordine decrescente, in modo da avere le due direzioni più importanti per prime
    indici = autovalori.argsort()[::-1]
    autovalori = autovalori[indici]
    autovettori = autovettori[:, indici]

    print("\nAutovalori:", autovalori)
    print("Le due direzioni più importanti sono i primi due autovettori.")

    #Estraiamo le due direzioni principali per poter disegnare il grafico, che si trovano come prime due tra gli autovettori
    direzioni = autovettori[:, :2]

    #Prepariamo i dati per inserirli nel grafico spostando il centro dei dati nell'origine (mean) e calcolando la loro posizione nel nuovo sistema 
    #a 2 assi (dot)
    dati_trasformati = numpy.dot(dati - numpy.mean(dati, axis=0), direzioni)
    
    #Creiamo lo scatterplot
    splot("Scatterplot", "Prima Componente Principale", dati_trasformati[:, 0], "Seconda Componente Principale (PC2)", dati_trasformati[:, 1])
#-------------------------------------------------------------------------------------------------------------------------------------------------
#FUNZIONE CHE DISEGNA LO SCATTERPLOT
def splot(titolo, nome_x, asse_x, nome_y, asse_y):
    #Scegliamo la dimensione della figura
    plot.figure(figsize=(10, 6))
    #Disegnamo i vari punti del campione
    plot.scatter(asse_x, asse_y, alpha=0.7, color='blue', edgecolor='black')
    #Impostiamo il titolo del grafico
    plot.title(titolo)
    #Impostiamo il nome dell'asse x
    plot.xlabel(nome_x)
    #Impostiamo il nome dell'asse y
    plot.ylabel(nome_y)
    #Mettiamo una griglia di sfondo del grafico
    plot.grid(True, linestyle='--', alpha=0.7)
    #Salviamo il grafico
    salvataggio_grafico(titolo)
#-------------------------------------------------------------------------------------------------------------------------------------------------
#FUNZIONE CHE DISEGNA LO SCATTERPLOT CON RETTA DI REGRESSIONE
def splot_retta(titolo, nome_x, asse_x, nome_y, asse_y, a, b):
    #Scegliamo la dimensione della figura
    plot.figure(figsize=(10, 6))
    #Disegnamo i vari punti del campione
    plot.scatter(asse_x, asse_y, alpha=0.7, color='blue', edgecolor='black', label='Dati reali')
    
    #Disegniamo la retta di regressione
    x_range = numpy.array([min(asse_x), max(asse_x)])
    y_range = a * x_range + b
    plot.plot(x_range, y_range, color='red', linewidth=2, label=f'Retta: y={a:.2f}x + {b:.2f}')
    
    #Impostiamo il titolo del grafico
    plot.title(titolo)
    #Impostiamo il nome dell'asse x
    plot.xlabel(nome_x)
    #Impostiamo il nome dell'asse y
    plot.ylabel(nome_y)
    #Mettiamo la legenda visibile all'interno del grafico
    plot.legend()
    #Mettiamo una griglia di sfondo del grafico
    plot.grid(True, linestyle='--', alpha=0.7)

    #Salviamo il grafico
    salvataggio_grafico(titolo)
#-------------------------------------------------------------------------------------------------------------------------------------------------
#FUNZIONE CHE SALVA UN GRAFICO NELLA CARTELLA GRAFICI
def salvataggio_grafico(titolo):
    #Prendiamo il percorso in cui creare la cartella dove salvare il grafico
    cartella_progetto = os.path.dirname(os.path.abspath(__file__))
    percorso_cartella_grafici = os.path.join(cartella_progetto, 'Grafici')

    #Creiamo una cartella 'grafici' se non esiste già
    if not os.path.exists(percorso_cartella_grafici):
        os.makedirs(percorso_cartella_grafici)
    
    #Puliamo il titolo da spazi e caratteri speciali per usarlo come nome file
    nome_file = titolo.replace(" ", "_").replace(":", "") + ".pdf"
    percorso_salvataggio = os.path.join(percorso_cartella_grafici, nome_file)
    
    #Salviamo il file
    plot.savefig(percorso_salvataggio)
    print(f"Grafico salvato in: {percorso_salvataggio}")
    
    #Chiudiamo la figura per liberare memoria
    plot.close()
#-------------------------------------------------------------------------------------------------------------------------------------------------
#MAIN

#Array contenenti i dati
tmin = numpy.array([21.9, 25.2, 25.4, 25.8, 26.0, 23.4, 24.1, 24.7, 24.5, 24.9, 23.8, 20.7, 20.3, 22.5, 21.9, 23.6, 19.0, 20.3, 20.4, 22.5, 23.5, 
                    22.8, 24.3, 24.6, 25.0, 22.6, 22.1, 22.9, 23.9, 21.1, 22.8, 21.6, 20.6, 21.5, 22.5, 23.0, 23.4, 22.9, 21.3, 19.4, 19.0, 21.1, 
                    21.4, 21.3, 22.3, 19.8, 13.4, 12.0, 13.6, 17.3, 15.8, 14.3, 13.7, 15.9, 15.4, 14.6, 16.1, 15.7, 15.7, 15.7])

tmed = numpy.array([27.0, 28.2, 29.0, 29.6, 29.4, 26.7, 27.4, 27.0, 27.2, 27.2, 25.8, 24.2, 25.3, 26.8, 25.1, 26.2, 24.5, 23.3, 25.5, 26.4, 26.4, 25.5, 
                    26.4, 27.2, 27.3, 26.1, 25.4, 26.2, 26.0, 23.9, 23.6, 23.4, 23.4, 24.1, 24.7, 25.4, 25.3, 24.7, 23.9, 23.3, 22.7, 23.4, 24.0, 25.3, 
                    25.1, 22.9, 16.7, 17.7, 19.1, 19.4, 18.1, 17.2, 17.7, 18.8, 17.5, 18.5, 18.3, 17.7, 18.9, 17.4])

tmax = numpy.array([31.6, 31.8, 32.2, 32.7, 34.1, 29.2, 31.1, 29.3, 30.0, 30.4, 29.0, 26.4, 29.9, 29.6, 27.8, 28.3, 26.2, 26.4, 31.3, 29.5, 29.3, 27.7, 
                    29.6, 30.7, 30.3, 30.4, 27.8, 29.2, 28.8, 26.2, 25.3, 25.8, 25.9, 26.6, 27.4, 27.7, 26.9, 27.0, 27.2, 27.5, 25.4, 26.1, 26.9, 29.5, 
                    30.1, 27.2, 20.7, 23.3, 24.7, 22.0, 19.9, 19.9, 21.2, 21.7, 19.6, 23.5, 20.3, 20.2, 22.5, 19.7])

ptot = numpy.array([1.2, 0.0, 0.0, 0.0, 1.8, 6.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.6, 0.0, 1.8, 26.4, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                    0.0, 0.0, 0.0, 5.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.2, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 22.8, 49.4, 0.0, 0.0, 1.4, 1.0, 
                    0.0, 0.0, 9.8, 8.4, 0.0, 0.8, 0.0, 0.0, 16.0])

#Cerchiamo il punto di minimo del campione bivariato (Tmin, Tmed)
print("Ricerca punto di minimo del campione (Tmin, Tmed)")
a1, b1 = discesa_gradiente(tmin, tmed)
print(f"Il punto di minimo e': ({a1}, {b1})")
#Creiamo il grafico per il campione (Tmin, Tmed)
splot_retta("Regressione Lineare: Tmin e Tmed", "Tmin (°C)", tmin, "Tmed (°C)", tmed, a1, b1)

#Cerchiamo il punto di minimo del campione bivariato (Tmin, Ptot)
print("\nRicerca punto di minimo del campione (Tmin, Ptot)")
a2, b2 = discesa_gradiente(tmin, ptot)
print(f"Il punto di minimo e': ({a2}, {b2})")
#Creiamo il grafico per il campione (Tmin, Ptot)
splot_retta("Regressione Lineare: Tmin e Ptot", "Tmin (°C)", tmin, "Ptot (mm)", ptot, a2, b2)

#Prepariamo i dati accorpandoli in una sola matrice e trasponendola
dati = numpy.array([tmin, tmed, tmax, ptot]).T
#Calcoliamo la matrice di covarianza
mat_covarianza = matrice_covarianza(dati)
#Calcoliamo l'autodecomposizione della matrice di covarianza
autodecomposizione(dati, mat_covarianza)