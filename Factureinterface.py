from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import sys
import subprocess

def load_factures(cursor, comNCN, table):
    '''
    # Clear the table
    for item in table.get_children():
        table.delete(item)
    '''
    # Display facture numero unique
    cursor.execute('SELECT "genreDeFacture", "Montant", "Date", "Status" FROM Facture WHERE ContractNumber = ?', (comNCN,))
    rows = cursor.fetchall()
    for row in rows:
        facture = str(row[0])
        montant = str(row[1])
        date = str(row[2])
        status = str(row[3])
        table.insert(parent="", index=0, values=(facture, montant, date, status))


def button_action(facture_id, NCN, statusT, montantT, dateT):
    subprocess.Popen(["python", "RD/Payment.py", NCN, statusT, facture_id, montantT, dateT], shell=True).wait()#???

def position_buttons(table, NCN):
    '''
    # Clear previous buttons if any
    for widget in table.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
    '''
    # Place buttons over specific cells
    for item_id in table.get_children():
        values = table.item(item_id, 'values')
        facture_id = values[0]
        status = values[3]
        bbox = table.bbox(item_id, 3)  # Get bounding box for column 'status'
        if bbox:
            x, y, width, height = bbox
            button = tk.Button(table, text="Payer", command=lambda: button_action(facture_id, NCN, status, "", ""))
            if status == "payee":
                button.config(state=DISABLED)
            button.place(x=x + width // 2, y=y + height // 2, anchor='center')



def main():
    '''
    if len(sys.argv) < 2:
        print("Error: No arguments provided")
        sys.exit()
    '''
    comNCN = sys.argv[1]

    root = Tk()
    root.title("Facture")
    root.geometry("800x500")

    # LOGO
    LABEL = Label(root, text="REGIE AUTONOME INTERCOMMUNALE\n DE DISTRIBUTION D'EAU ET D'ELECTRICITE DE FES\n\n\n\n", fg="blue")
    logo = ImageTk.PhotoImage(Image.open('RD/RADEEF2.jpg'))
    myLabel = Label(image=logo)
    myLabel.place(x=500, y=0)
    LABEL.config(font=("Courier", 12))
    LABEL.place(x=20, y=50)

    connection = sqlite3.connect('facture.db')
    cursor = connection.cursor()

    # Information
    cursor.execute("SELECT Name, ContractNumber, Email, Phone FROM Clients WHERE ContractNumber = ?", (comNCN,))
    rows = cursor.fetchall()

    for row in rows:
        FName = str(row[0])
        NCN = str(row[1])
        EM = str(row[2])
        TL = str(row[3])

    label1 = Label(root, text=f"Nom complet: {FName}")
    label1.place(x=10, y=150)
    label2 = Label(root, text=f"Numero de contrat: {NCN}")
    label2.place(x=10, y=170)
    label3 = Label(root, text=f"Email: {EM}")
    label3.place(x=10, y=190)
    label4 = Label(root, text=f"Telephone: {TL}")
    label4.place(x=10, y=210)

    table = ttk.Treeview(root, columns=('facture', 'montant', 'date', 'status'), show='headings')
    table.heading('facture', text='Facture')
    table.heading('montant', text='Montant')
    table.heading('date', text='Date')
    table.heading('status', text='Status')
    table.place(x=0, y=300)

    load_factures(cursor, comNCN, table) #???

    # Update button positions after Treeview update
    table.bind('<Configure>', lambda event: position_buttons(table, comNCN))
    table.bind('<<TreeviewSelect>>', lambda event: position_buttons(table, comNCN))#???

    # Function to refresh the data
    def refresh():
        # Clear the table
        for item in table.get_children():
            table.delete(item)

        # Reload factures into the table
        cursor.execute('SELECT "genreDeFacture", "Montant", "Date", "Status" FROM Facture WHERE ContractNumber = ?', (comNCN,))
        rows = cursor.fetchall()
        for row in rows:
            facture = str(row[0])
            montant = str(row[1])
            date = str(row[2])
            status = str(row[3])
            table.insert(parent="", index=0, values=(facture, montant, date, status))

        # Reposition the buttons
        position_buttons()

        # Schedule the next refresh
        root.after(5000, refresh)  # Refresh every 5 seconds

    # Start the automatic refresh
    root.after(5000, refresh)   #diffrence between this command and the one above?
    

    root.mainloop()
    connection.close()
    

if __name__ == "__main__":
    main()
