from tkinter import *
from tkinter import filedialog
from backend import enc, dec
import random, string, sqlite3


root = Tk()
root.title("CRYPTBOI")
root.geometry("1300x800")

'''Didn't work with function generatePassword and db functions being in backend.py'''

#make sure that crypter can connect to DB
try:
    sqlite3.connect('keys.db')
except:
    print("Can't connect to the db")


#function to list all tables in the database
def listTables():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()


    c.execute('SELECT name from sqlite_master where type= "table"')
    listoftables = c.fetchall()

    for tables in listoftables:
        tablelist.insert('end', tables)


#function for creating new table in the database
def createTable():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()

    tableName = createtableEntry.get()

    try:
        c.execute(""" create table if not exists """ + tableName + """ (
                          file text,
                          key text 
                          )""")
        conn.commit()
        conn.close()

        createtableEntry.delete(0, END)

    except:
        print("Something went wrong")

        conn.close()


#function for deleting a table in the database
def deleteTable():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()

    showTable = "".join(tablelist.get(tablelist.curselection()))
    c.execute("DROP TABLE "+showTable)

    conn.commit()
    conn.close()


#add info to the database
def addtoTable():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()

    showTable = "".join(tablelist.get(tablelist.curselection()))

    c.execute("INSERT INTO "+showTable+" VALUES (:file, :key)",
              {
                  'file': filenameEntry.get(),
                  'key': passEntry.get(),

              })

    filenameEntry.delete(0, END)
    passEntry.delete(0, END)

    conn.commit()
    conn.close()


#gui window for deleting info from chosen table in the database
def removefromtableWin():
    #function for deleting info from chosen table in the database
    def removefromTable():
        conn = sqlite3.connect('keys.db')
        c = conn.cursor()

        showTable = "".join(tablelist.get(tablelist.curselection()))

        c.execute("DELETE from "+showTable+" WHERE oid = " + oidremoveEntry.get())

        conn.commit()
        conn.close()
        removeWin.destroy()


    removeWin = Tk()
    removeWin.geometry('300x300')

    removeLabel = Label(removeWin,
                        text="Give the number of the record\n"
                             "you want to to delete")
    removeLabel.grid()

    oidremoveLabel = Label(removeWin, text="OID")
    oidremoveLabel.grid(row=1)
    oidremoveEntry = Entry(removeWin,widt=2)
    oidremoveEntry.grid(row=1, column=1)
    removesubmitButton = Button(removeWin,
                                text="Submit",
                                command=removefromTable)
    removesubmitButton.grid(row=1, column=2)


#function to display content for the chosen table in the database
def queryTable():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()

    showTable = "".join(tablelist.get(tablelist.curselection()))
    c.execute("SELECT *,oid FROM "+showTable)
    records = c.fetchall()

    print_records = ''
    for record in records:
        print_records += str(record[0]) + "  " + "\t" + \
                         str(record[1]) + "  " + "\t" + \
                         str(record[2]) + "  " + "\t\n"

    db_query.config(state=NORMAL)
    db_query.delete(1.0,END)
    db_query.update()
    db_query.insert(INSERT, print_records)
    db_query.config(state=DISABLED)

    conn.commit()
    conn.close()


#gui window for updatedb function
def updateTable():
    # changing existing content in the chosen table in the database
    def updatedb():

        conn = sqlite3.connect('keys.db')
        c = conn.cursor()
        record_id = oidEntry.get()


        newpass = ("".join(updatepassEntry.get()),)
        c.execute("SELECT * FROM " + showTable)
        c.execute("UPDATE "+showTable+" SET key=? WHERE oid = "+oidEntry.get(), newpass)


        conn.commit()
        conn.close()
        updatewin.destroy()
        return

    showTable = "".join(tablelist.get(tablelist.curselection()))

    updatewin = Tk()
    updatewin.geometry("500x500")
    oidLabel = Label(updatewin, text="OID")
    oidEntry = Entry(updatewin, width=2)
    oidLabel.grid()
    oidEntry.grid(row=1)

    updatepassLabel = Label(updatewin, text="Passphrase")
    updatepassEntry = Entry(updatewin, width=30)
    updatepassLabel.grid(row=4)
    updatepassEntry.grid(row=5)

    updatetableinfoButton = Button(updatewin,
                                   text="Submit",
                                   command=updatedb)
    updatetableinfoButton.grid(row=6)

    updatewin.mainloop()



#Generating passphrase for encryption
def generatePassword():
    pass_min_char = 20
    pass_allchar = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(pass_allchar) for x in range(pass_min_char))
    password_result = str(password)

    generatedEntry.delete(0, END)
    generatedEntry.insert(string=password_result, index=0)



'''GUI '''

#gui for showing all the tables in the db
tablelist = Listbox(root,selectmode=SINGLE)
tablelist.grid(row=0)

#Show tables in db
showtableinfoButton = Button(root,
                            text="Show",
                            command=queryTable,
                            bg="green")
showtableinfoButton.grid(row=1,column=3)

#button for updating info in table
updatetableButton = Button(root,
                           text="Update",
                           command=updateTable,
                           bg="green")
updatetableButton.grid(row=1,column=4)

#Remove table info
RemovetabelButton = Button(root,
                           text="Remove",
                           command=removefromtableWin,
                           bg="green")
RemovetabelButton.grid(row=1, column=5)

db_query = Text(root,
                width=80,
                height=10,
                state=DISABLED)
db_query.grid(row=0,column=3)


#filename to store in db
filenameLabel = Label(root,text="Filename")
filenameEntry = Entry(root,width=30)
filenameLabel.grid(row=3, column=0)
filenameEntry.grid(row=4, column=0)
#passphrase to encrypted file in db
passLabel = Label(root,text="Passphrase")
passEntry = Entry(root, width=30)
passLabel.grid(row=5, column=0)
passEntry.grid(row=6, column=0)
#submit
submitButton = Button(root,
                      text="submit",
                      padx=10,
                      bg="green",
                      command=addtoTable)
submitButton.grid(row=5, column=1)


tableLabel = Label(root,text="Table")
tableLabel.grid(row=9)

#Creating new table
createtableEntry = Entry(root,width=20)
createtableEntry.grid(row=10)
#button to create new table in db
createtableButton = Button(root,
                           text="Create table",
                           padx=10,
                           bg="green",
                           command=createTable)
createtableButton.grid(row=10, column=1)

#Button for deleting selected table
deletetableButton = Button(root,
                           text="Delete table",
                           padx=10,
                           bg="green",
                           command=deleteTable)
deletetableButton.grid(row=11, column=1)


encButton = Button(root,
                   text="Encrypt",
                   padx=10,
                   command=enc,
                   bg="green")
encButton.grid(row=11)

decButton = Button(root,
                   text="Decrypt",
                   padx=10,
                   command=dec,
                   bg="green")
decButton.grid(row=12)


generatedLabel = Label(root,
                       text="Generated password")
generatedLabel.grid(row=3, column=3)

generatedEntry = Entry(root,
                           text=generatePassword,
                           width=30)
generatedEntry.grid(row=4, column=3)

generateButton = Button(root,
                        text="Generate",
                        padx=10,
                        command=generatePassword,
                         bg="green")
generateButton.grid(row=4,column=4)


listTables()
root.mainloop()