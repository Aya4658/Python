from tkinter import *
import subprocess
from PIL import ImageTk, Image
import sqlite3


def main():
    root = Tk()
    root.title("Informations Personnelles")
    
    # LOGO
    LABEL = Label(root, text="REGIE AUTONOME INTERCOMMUNALE\n DE DISTRIBUTION D'EAU ET D'ELECTRICITE DE FES\n\n\n\n", fg="blue")
    pai = Label(root, text="\n\n\n\n[Service de paiement en ligne]\n\nIDENTIFIANTS DU CLIENT:\n\n")
    logo = ImageTk.PhotoImage(Image.open('RD/RADEEF2.jpg'))
    myLabel = Label(image=logo)
    myLabel.grid(row=0, column=1)
    LABEL.config(font=("Courier", 12))
    LABEL.place(x=20, y=50)
    pai.grid(row=1, column=0)

    # NUMERO CONTRAT
    NumCont = Label(root, text="Entez votre numero de contrat:")
    NumCont.grid(row=2, column=0)

    NC = Entry(root, width=70)
    NC.grid(row=3, column=0)

    '''
    FullName = Label(root, text="Entez votre nom complet:")
    FullName.grid(row=2, column=0)

    FN = Entry(root, width=70)
    FN.grid(row=3, column=0)

    # EMAIL
    Emaill = Label(root, text="Entez votre email:")
    Emaill.grid(row=8, column=0)

    email = Entry(root, width=70)
    email.grid(row=9, column=0)

    # TEL
    telep = Label(root, text="Entez votre numero de telephone:")
    telep.grid(row=11, column=0)

    tel = Entry(root, width=70)
    tel.grid(row=12, column=0)
    '''
    # BUTTON
    def event():
        # Get the values from entries and strip whitespace
        #comFName = str(FN.get()).strip()
        comNCN = str(NC.get()).strip()  # Get the text from the Entry widget
        #comEM = str(email.get()).strip()
        #comTL = str(tel.get()).strip()

        # Read the data
        connection = sqlite3.connect('facture.db')
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("SELECT ContractNumber FROM Clients WHERE ContractNumber = ?", (comNCN,))
        # Fetch all results
        row = cursor.fetchone()  # Use fetchone() since we expect only one result
        # Check if the result is not None and has the expected structure
        if row is not None and len(row) > 0:
            NCN = str(row[0])  # Extract the integer from the tuple
        else:
            NCN = None
        '''
        # Create and Open file in write mode ('w')
        with open('RD/infos.txt', 'w') as infos:
            infos.write("Contract number: " + comNCN)
        infos.close()
        '''
        print(f"NCN: {NCN}  , comNCN: {comNCN}")
        
        # Check if entries match data
        if comNCN == NCN:
            subprocess.Popen(["python", "RD/Factureinterface.py",comNCN])
        else:
            mes = Label(root, text="Informations invalides, veuillez ressayer!", fg="red")
            mes.grid(row=14, column=0)

        connection.close()
        root.destroy

    bouton = Button(root, text="valider", command=event)
    bouton.grid(row=13, column=0)

    
    root.mainloop()


if __name__ == "__main__":
    main()
