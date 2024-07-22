from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
#from PIL import ImageTk, Image



root = Tk()
root.title("Payement de la facture")

# Read the data
connection = sqlite3.connect('facture.db')
cursor = connection.cursor()

# Get the command line arguments
NCN = sys.argv[1]
status = sys.argv[2]
factureT = sys.argv[3]
montantT = sys.argv[4]
dateT = sys.argv[5]

# NUMERO CONTRAT
NumCont = Label(root, text="Entrez votre numéro de contrat:")
NumCont.grid(row=5, column=0)
NC = Entry(root, width=70)
NC.grid(row=6, column=0)

# Numero de la carte
cartNum = Label(root, text="Entrez votre code de carte de paiement:")
cartNum.grid(row=2, column=0)
CN = Entry(root, width=70)
CN.grid(row=3, column=0)

def event():
    comNCN = str(NC.get()).strip()
    comCN = str(CN.get()).strip()

    # Execute a query to get the payment card number
    cursor.execute("SELECT numeroDeCarteDePayement FROM Clients WHERE ContractNumber = ?", (comNCN,))
    row = cursor.fetchone()
    
    if row: #???
        secCN = row[0]
    else:
        mes = Label(root, text="Numéro de contrat invalide, veuillez réessayer!", fg="red")
        mes.grid(row=8, column=0)
        return

    # Check if entries match data
    if comCN == secCN:
        cursor.execute("UPDATE Facture SET Status = ? WHERE genreDeFacture = ?", ('payee', factureT))
        connection.commit()
        bouton.config(state=tk.DISABLED)
        mes = Label(root, text="Paiement effectué avec succès!", fg="green")
        mes.grid(row=8, column=0)
    else:
        mes = Label(root, text="Informations invalides, veuillez réessayer!", fg="red")
        mes.grid(row=8, column=0)

    connection.close()

bouton = Button(root, text="Valider", command=event)
bouton.grid(row=7, column=0)

root.mainloop()