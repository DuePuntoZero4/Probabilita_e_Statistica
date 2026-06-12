import numpy as np
import matplotlib.pyplot as plt
import os

# Seed per poter riprodurre i risultati randomici
np.random.seed(42)

# Se non esiste già, creiamo la cartella per i grafici
os.makedirs('grafici', exist_ok=True)

def monte_carlo_pigreco(N_max):
    # Creiamo un array che contiene 1, 2, ..., N_max
    lanci = np.arange(1, N_max + 1)
    # Creiamo una lista vuota che conterrà le 3 serie di stime di pigreco
    pi_stime = []
    # Generiamo le 3 serie
    for i in range(3):
        # Generazione punti casuali distribuiti uniformemente nel quadrato
        x = np.random.uniform(-1, 1, N_max)
        y = np.random.uniform(-1, 1, N_max)
        # Somma cumulativa progressiva dei punti dentro il cerchio, che ci dice lancio dopo lancio quanti punti sono caduti dentro il cerchio 
        # fino a quel momento
        punti_dentro = np.cumsum(x**2 + y**2 <= 1)
        # Calcolo delle stime progressive di pigreco per quella serie
        stime_progressive = 4 * punti_dentro / lanci
        # Inseriamo la serie nella lista
        pi_stime.append(stime_progressive)
    return lanci, pi_stime

def monte_carlo_sfera(N_max):
    # Creiamo un array che contiene 1, 2, ..., N_max
    lanci = np.arange(1, N_max + 1)
    # Lista vuota che conterrà le 3 serie di stime del volume della sfera
    sfera_stime = []
    # Generiamo le 3 serie
    for i in range(3):
        # Generazione punti casuali uniformi nel cubo
        x = np.random.uniform(-1, 1, N_max)
        y = np.random.uniform(-1, 1, N_max)
        z = np.random.uniform(-1, 1, N_max)
        # Somma cumulativa progressiva dei punti dentro la sfera, che ci dice lancio dopo lancio quanti punti sono caduti dentro la sfera 
        # fino a quel momento
        punti_dentro = np.cumsum(x**2 + y**2 + z**2 <= 1)
        # Calcolo della stima progressiva del volume
        stime_progressive = 8 * punti_dentro / lanci
        # Inseriamo la serie nella lista
        sfera_stime.append(stime_progressive)
    return lanci, sfera_stime

def monte_carlo_solido(N_max):
    # Creiamo un array che contiene 1, 2, ..., N_max
    lanci = np.arange(1, N_max + 1)
    # Lista vuota che conterrà le 3 serie di stime del volume del solido
    solido_stime = []
    # Generiamo le 3 serie indipendenti
    for i in range(3):
        # Generazione punti casuali uniformi nel cubo
        x = np.random.uniform(-2, 2, N_max)
        y = np.random.uniform(-2, 2, N_max)
        z = np.random.uniform(-2, 2, N_max)
        # Calcoliamo la distanza radiale del punto dall'asse centrale
        distanza_radiale = np.sqrt(x**2 + y**2)
        # Calcoliamo il raggio limite del solido a quella specifica altezza z
        limite_solido = 1 + np.sin(np.pi * z)
        # Somma cumulativa progressiva dei punti che rispettano la condizione
        punti_dentro = np.cumsum(distanza_radiale <= limite_solido)
        # Calcolo della stima progressiva del volume
        stime_progressive = 64 * punti_dentro / lanci
        # Inseriamo la serie nella lista
        solido_stime.append(stime_progressive)
    return lanci, solido_stime

def disegna_grafico(lanci, lista_stime, valore_vero, titolo, nome_y, nome_file_pdf):
    plt.figure(figsize=(20, 15))
    #Disegnamo circa 5000 punti equispaziati sul grafo per non appesantire troppo l'esecuzione
    passo = max(1, len(lanci) // 5000)
    # Tracciamento le 3 serie
    for i, serie in enumerate(lista_stime):
        plt.plot(lanci[::passo], serie[::passo], label=f'Realizzazione {i+1}', alpha=0.85)
    # Disegnamo la linea del valore vero come riferimento
    plt.axhline(y=valore_vero, color='r', linestyle='--', linewidth=1.5, label=f'Valore vero ({valore_vero:.4f})')
    # Impostiamo l'aspetto del grafico
    plt.title(titolo, fontsize=24, fontweight='bold', pad=20)
    plt.xlabel('Numero di campioni ($n$)', fontsize=18, labelpad=15)
    plt.ylabel(nome_y, fontsize=18, labelpad=15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc='lower right', fontsize=16)
    plt.grid(True, linestyle=':', alpha=0.6)
    # Salvataggio in PDF nella cartella dedicata
    percorso_completo = os.path.join('grafici', nome_file_pdf)
    plt.savefig(percorso_completo, format='pdf')
    plt.close()
    print(f"Grafico salvato con successo in: {percorso_completo}")

# Errore massimo accettabiile
epsilon = 0.01
# z calcolato col teorema centrale del limite
z = 1.96

# Area del quadrato che contiene il cerchio
V_box_pi = 4 
# Valore effettivo di pigreco
valore_vero_pi = np.pi
# Probabilità ch eun punto cada nel cerchio
p_pi = valore_vero_pi / V_box_pi
# Varianza di Bernoulli
var_pi = p_pi * (1 - p_pi)
# Calcoliamo il numero di punti che ci serve per avere una stima che disti meno di epsilon dal valore vero con probabilità maggiore del 95%
N_pi = int(np.ceil(((z * V_box_pi * np.sqrt(var_pi)) / epsilon) ** 2))

# Volume del cubo che contiene la sfera
V_box_sfera = 8
# Valore effettivo del volume della sfera
valore_vero_sfera = (4/3) * np.pi
# Probabilità che un punto cada dentro la sfera
p_sfera = valore_vero_sfera / V_box_sfera
# Varianza di Bernoulli
var_sfera = p_sfera * (1 - p_sfera)
# Calcoliamo il numero di punti che ci serve per avere una stima che disti meno di epsilon dal valore vero con probabilità maggiore del 95%
N_sfera = int(np.ceil(((z * V_box_sfera * np.sqrt(var_sfera)) / epsilon) ** 2))

# Volume del cubo che contiene il solido
V_box_solido = 64
# Volume effettivo del solido
valore_vero_solido = 6 * np.pi
# Probabilità che un punto cada all'interno del solido
p_solido = valore_vero_solido / V_box_solido
# Varianza di Bernoulli
var_solido = p_solido * (1 - p_solido)
# Calcoliamo il numero di punti che ci serve per avere una stima che disti meno di epsilon dal valore vero con probabilità maggiore del 95%
N_solido = int(np.ceil(((z * V_box_solido * np.sqrt(var_solido)) / epsilon) ** 2))

print(f"Lanci necessari per Pi Greco: {N_pi}")
print(f"Lanci necessari per Sfera:    {N_sfera}")
print(f"Lanci necessari per Solido:   {N_solido}")

# Calcoliamo le stime
lanci_pi, stime_pi = monte_carlo_pigreco(N_pi)
lanci_sfera, stime_sfera = monte_carlo_sfera(N_sfera)
lanci_solido, stime_solido = monte_carlo_solido(N_solido)

# Grafico pi greco
disegna_grafico(lanci_pi, stime_pi, valore_vero_pi, 'Calcolo di pigreco', 'Stima di pigreco', 'grafico_pigreco.pdf')
# Grafico sfera
disegna_grafico(lanci_sfera, stime_sfera, valore_vero_sfera, 'Volume della Sfera', 'Stima del Volume', 'grafico_sfera.pdf')
# Grafico solido
disegna_grafico(lanci_solido, stime_solido, valore_vero_solido, 'Volume del Solido A', 'Stima del Volume','grafico_solido.pdf')