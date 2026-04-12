import math
import matplotlib.pyplot as plt
import os

#Funzione che calcola la probabilità di vittoria del candidato A
def probabilita_vittoria(N, M):
    
    #Calcoliamo il punto di partenza approssimando con il logaritmo per evitare errori di underflow
    log_p_corrente = N * math.log(0.5)
    
    #Calcoliamo la soglia di voti sopra cui il candidato A ha vinto
    soglia = math.floor((N - M) / 2) + 1

    #Inizializziamo la variabile della probabilità totale a zero
    prob_totale = 0
    
    #Ciclo che percorre tutte le possibili quantità di voti possibili da ottenere dagli elettori indecisi
    for k in range(N + 1):

        #Se k supera la soglia, allora convertiamo la probabilità p(k) dal logaritmo al valore reale e la sommiamo alla probabilità totale
        if k >= soglia:
            prob_totale += math.exp(log_p_corrente)
            
            #Se la probabilità diventa trascurabile concludiamo prima il ciclo
            if k > (N / 2) + 500 and math.exp(log_p_corrente) < 1e-18:
                break
        
        #Se k non supera la soglia, allora aggiorniamo il valore 
        if k < N:
            log_p_corrente += math.log(N - k) - math.log(k + 1)

    #Restituiamo la probabilità totale ottenuta 
    return prob_totale

#Funzione che crea il grafico
def creazione_grafico(titolo, nome_x, nome_y, m, r):
    #Impostiamo la grandezza della figura
    plt.figure(figsize=(10, 6))
    #Impostiamo il nome dell'asse x
    plt.xlabel(nome_x)
    #Impostiamo il nome dell'asse y
    plt.ylabel(nome_y)
    #Impostiamo il titolo del grafico
    plt.title(titolo)
    #Mettiamo una griglia di sfondo al grafico
    plt.grid(True, linestyle='--', alpha=0.7)
    #Creiamo la retta
    plt.plot(m, r)
    #Salviamo il grafico
    salvataggio_grafico(titolo)

#Funzione che salva il grafico
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
    plt.savefig(percorso_salvataggio)
    print(f"Grafico salvato in: {percorso_salvataggio}")
    #Chiudiamo la figura per liberare memoria
    plt.close()

#Numero di votanti totali
votanti = 10**6
#Possibili quantità di elettori che sicuramente votano per il candidato A
m_values = list(range(0, 5010, 10))
#Lista vuota per conservare i risultati e poi usarli per tracciare il grafico
risultati = []

#Ciclo che viene eseguito per ogni possibile valore di elettori che sicuramente votano per A
for M in m_values:
    #Calcoliamo il numero di votanti indecisi
    N = votanti - M
    #Calcoliamo la probabilità che A vinca in questo scenario e la mettiamo nella lista dei risultati
    risultati.append(probabilita_vittoria(N, M))

creazione_grafico("Grafico Vittoria", "Numero di elettori certi (M)", "Probabilita' di vittoria di A", m_values, risultati)
