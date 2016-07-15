# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import *
import sqlite3 as lite
import sys

"""
Mini księga gości
    - nauka: python + tkinter + SQLite3
"""

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self)

        # Sprawdzenie czy istnieje / utworzenie bazy danych
        try:
          a = open('test.db')
          a.close

          print("Baza danych istnieje")

        except FileNotFoundError:
          print ("Wykryto błąd %s:" %sys.exc_info()[0])

          # Utworzenie bazy danych
          con = lite.connect('test.db')
          with con:
            cur = con.cursor()
            # Utworzenie tabeli Ksiega
            cur.execute("CREATE TABLE Ksiega(Id INTEGER PRIMARY KEY, Name TEXT)")
          con.commit()
          con.close()

          print ("dlatego została utworzona nowa baza danych")

        self.pack()
        self.createWidgets()


    def createWidgets(self):

        # Przycisk wyjścia
        self.QUIT = tk.Button(self,
                              text="QUIT",
                              fg="red",
                              command=root.destroy
                              ).grid(row=0, column = 10, sticky = E)


        # Etykietka i przycisk wprowadzania imienia
        Label(self,
              text = "Jak masz na imię?  "
              ).grid(row=2, column = 2, sticky = W)

        self.user_name = Entry(self,
                               width = 16
                               )
        self.user_name.grid(row=2, column=3, sticky=W)


        # Przycisk do zapisywania imienia
        self.get_name_bttn = Button(self,
                                    text = "Zapisz mnie!",
                                    fg="blue",
                                    command=self.zapisz_imie
                                    ).grid(row=2, column=4,sticky=W)


        # Pole Textowe - Ksiega gosci
        Label(self,
              text = "~ Księga Gości ~"
              ).grid(row=4, column=2, sticky=W)

        self.lista = self.stworz_liste()
        self.imie_txt = Text(self,
                             width=50, height=10, wrap=WORD
                             )

        self.imie_txt.delete(0.0, END)
        self.imie_txt.insert(0.0, self.lista)
        self.imie_txt.grid(row=5, column=2, columnspan = 4)


        # Licznik gosci
        Label(self,
              text = "Liczba wpisów w Księdze: "
              ).grid(row=6, column=2, sticky=W)

        self.num = self.policz_gosci()

        self.num_txt = Text(self, width=5, height=1, wrap=WORD)
        self.num_txt.delete(0.0, END)
        self.num_txt.insert(0.0, self.num)
        self.num_txt.grid(row=6, column=3, columnspan = 4)


        # Usuń z księgi ostatniego gościa
        Label(self,
              text = "Usuń z Księgi ostatnio dodanego gościa: "
              ).grid(row=8, column=2, sticky=W)
        self.del_bttn = Button(self,
                               text = "USUŃ!",
                               fg="red",
                               command=self.usun_goscia
                               ).grid(row=8, column=3,sticky=W)


    def usun_goscia(self):
      try:
        con = lite.connect('test.db')
        with con:
          cur = con.cursor()
          nr = self.policz_gosci()
          cur.execute("DELETE FROM Ksiega WHERE Id=?;", (nr,))
          con.commit()

      except lite.Error:
        if con:
          con.rollback()
        print ("Error %s:" % e.args[0])
        sys.exit(1)

      finally:
        if con:
          con.close()

      self.aktualizuj_spis_licznik()


    def policz_gosci(self):
      con = lite.connect('test.db')
      with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Ksiega")
        rows = cur.fetchall()
        l = len(rows)
      con.close()

      return l

    def stworz_liste(self):
      lista = ""
      con = lite.connect('test.db')

      with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Ksiega")
        rows = cur.fetchall()

        for row in rows:
          lista += row[1]
          lista += ", "
      con.close()

      return lista


    def zapisz_imie(self):
        imie = self.user_name.get()

        try:
          con = lite.connect('test.db')
          cur = con.cursor()
          cur.execute("INSERT INTO Ksiega(Name) VALUES (?)", (imie,))
          con.commit()

        except lite.Error:
          if con:
            con.rollback()
          print ("Error %s:" % e.args[0])
          sys.exit(1)

        finally:
          if con:
            con.close()

        self.user_name.delete(0, END)
        self.aktualizuj_spis_licznik()


    def aktualizuj_spis_licznik(self):

      self.num = self.policz_gosci()
      self.num_txt.delete(0.0,END)
      self.num_txt.insert(0.0,self.num)

      self.lista = self.stworz_liste()
      self.imie_txt.delete(0.0,END)
      self.imie_txt.insert(0.0,self.lista)


root = tk.Tk()
app = Application(master=root)
app.master.minsize(600, 400)
app.mainloop()
