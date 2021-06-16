"""
Adrian Niedziółka-Domański
Projekt: Koło Fortuny
"""
import psycopg2 as ps
import random
import json
import os

from tkinter.ttk import Style, Combobox
from tkinter import Frame, Label, Button, Tk, BOTH, Y, TOP, LEFT, RIGHT, BOTTOM, W, E, N, S, SW, NW, NE, \
    CENTER, Canvas, messagebox, Scrollbar, Entry, END


class Record(Frame):
    color_1 = "#363636"
    color_2 = "#4E4E4E"
    color_3 = "#E2B659"
    color_4 = "#2A272A"

    def __init__(self, parent, par):
        super().__init__(parent)
        self.parent = parent
        self.config(height=30)
        self.config(bg=self.color_4)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=16)
        self.grid_columnconfigure(2, weight=4)
        self.pos_lbl = Label(self, text="Nr:", anchor=W, fg=self.color_3,
                             font="Stencil 12")
        self.pos_lbl.place(relx=0, relwidth=0.098, rely=0, relheight=1.0)
        self.name_lbl = Label(self, text="Nazwa:", anchor=W, fg=self.color_3,
                              font="Stencil 12")
        self.name_lbl.place(relx=0.102, relwidth=0.646, rely=0, relheight=1.0)
        self.score_lbl = Label(self, text="Wynik:", anchor=W, fg=self.color_3,
                               font="Stencil 12")
        self.score_lbl.place(relx=0.752, relwidth=0.248, rely=0, relheight=1.0)

        if par == 0:
            self.pos_lbl.config(bg=self.color_1)
            self.name_lbl.config(bg=self.color_1)
            self.score_lbl.config(bg=self.color_1)
        else:
            self.pos_lbl.config(bg=self.color_2)
            self.name_lbl.config(bg=self.color_2)
            self.score_lbl.config(bg=self.color_2)

    def set_pos(self, pos):
        self.pos_lbl.config(text=pos)

    def set_name(self, name):
        self.name_lbl.configure(text=name)

    def set_score(self, score):
        self.score_lbl.configure(text=score)


class PlayerEntry(Frame):
    color_1 = "#303030"
    color_2 = "#363636"
    color_3 = "#E2B659"

    def __init__(self, parent, i):
        super().__init__(parent)
        self.config(bg=self.color_2)
        self.player_lbl = Label(self, text="Gracz %02d:" % (i + 1), bg=self.color_2, fg=self.color_3,
                                anchor=W, font="Broadway 10")
        self.player_lbl.pack(side=LEFT, padx=(0, 2))
        self.player_entry = Entry(self, bg=self.color_1, fg=self.color_3)
        self.player_entry.pack(side=LEFT, expand=1, fill=BOTH)


class MainMenu(Frame):
    color_1 = "#2A272A"
    color_2 = "#303030"
    color_3 = "#E2B659"

    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)
        self.parent = parent
        self.config(bg=self.color_1)

        self.menu = Frame(self, bg=self.color_2, border=2, relief="solid", padx=20, pady=20)
        self.menu.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.title = Label(self.menu, text="WHEEL OF\n FORTUNE", justify=CENTER,
                           padx=0, pady=0, borderwidth=0, font="Ravie 48 bold", fg=self.color_3, bg=self.color_2)
        self.title.pack()

        self.start_btn = Button(self.menu, text="Start", width=20, height=2, bg=self.color_2, fg=self.color_3,
                                activebackground=self.color_1, activeforeground=self.color_3, font="Broadway 16",
                                command=lambda: self.window.change_state(Game(self.parent, self.window)))
        self.start_btn.pack(pady=(40, 20))
        self.scbrd_btn = Button(self.menu, text="Rankingi", width=20, height=2, bg=self.color_2, fg=self.color_3,
                                activebackground=self.color_1, activeforeground=self.color_3, font="Broadway 16",
                                command=lambda: self.window.change_state(Scoreboard(self.parent, self.window)))
        self.scbrd_btn.pack(pady=20)
        self.exit_btn = Button(self.menu, text="Wyjdź", width=20, height=2, bg=self.color_2, fg=self.color_3,
                               activebackground=self.color_1, activeforeground=self.color_3, font="Broadway 16",
                               command=self.parent.destroy)
        self.exit_btn.pack(pady=20)


class Game(Frame):
    color_1 = "#2A272A"
    color_2 = "#303030"
    color_3 = "#E2B659"
    color_4 = "#363636"
    color_5 = "#4E4E4E"
    color_6 = "#7B7B7B"

    category = "Tutaj powinna byc kategoria"
    slogan = "Tutaj powinno, znaleźć się hasło"
    slogan_field = []
    slogan_field_rev = []
    nplayers = 2
    players = []
    active_player = 0

    nrounds = 1
    act_round = 1
    przesuniecia = [-10 * 50, -9 * 50, -8 * 50, -7 * 50, -6 * 50, -5 * 50, -4 * 50, -3 * 50, -2 * 50, -1 * 50,
                    0,
                    1 * 50, 2 * 50, 3 * 50, 4 * 50, 5 * 50, 6 * 50, 7 * 50, 8 * 50, 9 * 50, 10 * 50]

    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)
        self.parent = parent
        self.config(bg=self.color_1)
        self.config(pady=20, padx=20)

        self.gamebox = Frame(self, bg=self.color_2, border=2, relief="solid", padx=10, pady=10)
        self.gamebox.place(relheight=1, relwidth=1)
        self.menu_btn = Button(self.gamebox, text="<<Menu Główne", fg=self.color_3, bg=self.color_1,
                               font="Broadway 11", activeforeground=self.color_3, activebackground=self.color_2,
                               command=self.draw_confirm)
        self.menu_btn.place(anchor=NW)
        self.draw_start()
        for i in range(4):
            self.slogan_field.append([])
            self.slogan_field_rev.append([])
            for j in range(15):
                self.slogan_field[i].append("")
                self.slogan_field_rev[i].append("")

        self.active_player = 0
        self.act_round = 1

    def acc_settings(self):
        """
        Sprawdza poprawność danych wprowadzonych w 1 ekranie
        """
        try:
            self.nrounds = int(self.round_cb.get())
            self.nplayers = int(self.nplayer_inp.get())
            if self.nplayers < 2 or self.nplayers > 15:
                messagebox.showerror("Nieodpowiednia liczba graczy!", "Liczba graczy powinna być z zakresu 2-15!")
            else:
                self.draw_player_names()
        except ValueError:
            messagebox.showerror("Błąd", "Wartość liczby graczy powinna być liczbą z zakresu 2-15!")

    def acc_players(self):
        """
        Sprawdza poprawność danych wprowadzonych w 2 ekranie
        """
        self.players = []
        good = True
        for i in range(self.nplayers):
            read = self.players_entry[i].player_entry.get()
            if read == '':
                messagebox.showerror("Błąd w nazwie graczy!", "Nie uzupełniono wszystkich nazwy graczy!")
                good = False
                break
            elif read in self.players:
                messagebox.showerror("Błąd w nazwie graczy!", "Przynajmniej 2 takie same nazwy gracz!")
                good = False
                break
            self.players.append(read)

        if good:
            self.draw_category()

    def los_category(self):
        """
        Losuje kategorie
        """
        categories = self.window.database.get_categories()
        self.category = categories[random.randint(0, len(categories) - 1)][0]

    def los_slogan(self):
        """
        Losuje hasło
        """
        slogans = self.window.database.get_slogans(self.category)
        self.slogan = slogans[random.randint(0, len(slogans) - 1)][0]

    def draw_confirm(self):
        """
        Messagebox dla potwierdzenia powroty do Menu Głównego
        """
        confirm = messagebox.askquestion("Powrót do Menu Głównego",
                                         "Czy napewno chcesz teraz powrócić do Menu Głównego? Stan gry nie zostanie zapisany.")
        if confirm == 'yes':
            self.window.change_state(MainMenu(self.parent, self.window))

    def print_kolej(self, ind, kol):
        """
        Wyświetla na ekranie kolejność graczy (wywolywane z opóźnieniem dla animacji)
        ind:int
            ktory gracz
        kol:int
            jaki numer startowy
        """
        self.playerpos_lbls[ind].config(text=kol)

    def make_scoreboard(self):
        """
        Tworzy tymczasowy plik z wynikami
        """
        scoreboard = dict.fromkeys(self.players)
        for key in scoreboard:
            scoreboard[key] = 0
        with open("temp_scrbrd.json", "w") as f:
            json.dump(scoreboard, f)

    def refresh_scoreboard(self):
        """
        Odświeża wyniki i aktywnych graczy w grze
        """
        with open("temp_scrbrd.json", "r") as f:
            sc = json.load(f)
        self.playernames_lbls = [Label() for i in range(self.nplayers)]
        self.playerpos_lbls = [Label() for i in range(self.nplayers)]
        for i in range(self.nplayers):
            self.playernames_lbls[i] = Label(self.players_scorebox, text=self.players[i], bg=self.color_2,
                                             fg=self.color_3, anchor=W, font="Broadway 10")
            self.playernames_lbls[i].grid(row=i, column=0, sticky=N + W + E + S, padx=(0, 2), pady=(0, 1))
            self.playerpos_lbls[i] = Label(self.players_scorebox, text=sc[self.players[i]], bg=self.color_2,
                                           fg=self.color_3, anchor=W, font="Broadway 10")
            self.playerpos_lbls[i].grid(row=i, column=1, sticky=N + W + E + S, pady=(0, 1))
            if i == self.active_player:
                self.playernames_lbls[i].config(font="Broadway 10 bold", bg=self.color_5)
                self.playerpos_lbls[i].config(font="Broadway 10 bold", bg=self.color_5)

    def delete_scoreboard(self):
        """
        Usuwa tymczasowy plik z wynikami
        """
        if os.path.exists("temp_scrbrd.json"):
            os.remove("temp_scrbrd.json")

    def set_slogan(self):
        """
        Ustawia hasło na polach
        """
        for i in range(4):
            for j in range(15):
                self.slogan_field[i][j] = ""
                self.slogan_field_rev[i][j] = ""

        tokens = self.slogan.split(" ")
        row = 0
        col = 0
        for token in tokens:
            token = token.upper()
            if 15 - col < len(token) and row < 4:
                row += 1
                col = 0
            for letter in token:
                if letter.isalpha() and col < 15:
                    self.slogan_field[row][col] = letter
                elif col < 15:
                    self.slogan_field_rev[row][col] = letter
                col += 1
            col += 1

    def spin(self):
        """
        Kręcenie kołem - losowanie wartości od -10 do 10
        """
        self.spin_btn['state'] = 'disabled'
        self.los_n = random.randint(-10, 10)
        przesuniecie = ((random.random() * 50 - 25) - self.przesuniecia[self.los_n + 10])
        self.spin_move(przesuniecie)
        if self.los_n == 0:
            self.nextpl_btn['state'] = 'normal'
            with open("temp_scrbrd.json", "r") as f:
                sc = json.load(f)
            sc[self.players[self.active_player]] = 0
            with open("temp_scrbrd.json", "w") as f:
                json.dump(sc, f)
            self.refresh_scoreboard()
        else:
            self.letter_btn['state'] = 'normal'
            self.letter_input['state'] = 'normal'

    def spin_move(self, wartosc):
        """
        Przesuwam ikony o wartosc
        wartosc:
            wartosc przesuniecia
        """
        if wartosc < 0:
            wartosc = 1050 + wartosc
        for i in range(21):
            self.przesuniecia[i] += wartosc
            if self.przesuniecia[i] > 525:
                self.przesuniecia[i] -= 1050
        self.draw_spin_elems()

    def draw_spin_elems(self):
        """
        Rysowanie elementów
        """
        self.spincanva.delete("all")
        self.box_ids = []
        self.num_ids = []
        for i in range(21):
            self.box_ids.append(
                self.spincanva.create_rectangle(self.center[0] - 25 + self.przesuniecia[i], self.center[1] - 25,
                                                self.center[0] + 25 + self.przesuniecia[i], self.center[1] + 25,
                                                fill=self.color_3))
            self.num_ids.append(
                self.spincanva.create_text(self.center[0] + self.przesuniecia[i], self.center[1], text=i - 10,
                                           font="Ravie 16"))

        # trojkąt na środku
        points = [self.center[0] - 10, 0, self.center[0] + 10, 0, self.center[0], 10]
        self.spincanva.create_polygon(points, fill=self.color_1)

    def draw_spinelems(self, e):
        """
        Wyznacza srodek canvy i rysuje elementy
        e:Event
            co wywołało tą funkcje
        """
        self.center = (e.width / 2, e.height / 2)
        self.draw_spin_elems()

    def strict_len(self, e):
        """
        Ograniczenie dlugosci wprowadzanego pola do 1 litery
        """
        # usuwa wszystko co było, przez co zostaje tylko nowo wcisnieta litera
        self.letter_input.delete(0, END)

    def check_letter(self):
        """
        Sprawdzanie litery i przyznawanie odpowiednich punktow
        """
        lett = self.letter_input.get().upper()
        if lett.isalpha():
            with open("temp_scrbrd.json", "r") as f:
                sc = json.load(f)
            self.letter_input['state'] = 'disabled'
            self.letter_btn['state'] = 'disabled'
            self.slogan_input['state'] = 'normal'
            self.slogan_btn['state'] = 'normal'
            self.nextpl_btn['state'] = 'normal'
            ile = 0
            for i in range(4):
                for j in range(15):
                    if self.slogan_field[i][j] == lett and self.slogan_field_rev[i][j] == "":
                        ile += 1
                        self.slogan_field_rev[i][j] = lett
                        self.slogan_letters[i][j].config(text=self.slogan_field_rev[i][j])
            # jezeli nie odgadnieto a byly ujemne punkty to je odejmij od wyniku
            if self.los_n < 0 and ile == 0:
                sc[self.players[self.active_player]] += self.los_n
            # jezeli odgadnieto i byly dodatnie punkty to dodaj je przemnozone przez ilosc liter odgadnietych
            elif self.los_n > 0 and ile > 0:
                sc[self.players[self.active_player]] += self.los_n * ile

            with open("temp_scrbrd.json", "w") as f:
                json.dump(sc, f)
            self.refresh_scoreboard()
        else:
            messagebox.showerror("Błąd!", "Wprowadzona wartość nie jest literą alfabetu!")

    def check_password(self):
        """
        Sprawdza poprawnosc podanego hasła i przechodzi do nastepnej rundy jezeli poprawne
        """
        self.slogan_input['state'] = 'disabled'
        self.slogan_btn['state'] = 'disabled'
        slogan_wr = self.slogan_input.get().upper()
        if slogan_wr == self.slogan.upper():
            messagebox.showinfo("Hasło!", "To było poprawne hasło!")
            mnoznik = 0
            for i in range(4):
                for j in range(15):
                    if self.slogan_field[i][j] != "" and self.slogan_field_rev[i][j] == "":
                        mnoznik += 1
            mnoznik = max(1, mnoznik)
            with open("temp_scrbrd.json", "r") as f:
                sc = json.load(f)
            # przemnozenie wyniku przez ilosc nieokrytych liter
            if sc[self.players[self.active_player]] > 0:
                sc[self.players[self.active_player]] *= mnoznik
            with open("temp_scrbrd.json", "w") as f:
                json.dump(sc, f)
            self.refresh_scoreboard()
            self.next_round()
        else:
            messagebox.showinfo("Hasło!", "To było niepoprawne hasło!")

    def next_round(self):
        if self.act_round != self.nrounds:
            self.act_round += 1
            self.playersbox.destroy()
            self.maingamebox.destroy()
            self.draw_category()
        else:
            self.draw_final()

    def next_player(self):
        """
        Przechodzi do następnego gracza
        """
        self.active_player = (self.active_player + 1) % self.nplayers
        self.spin_btn['state'] = 'normal'
        self.letter_input['state'] = 'disabled'
        self.letter_btn['state'] = 'disabled'
        self.slogan_input['state'] = 'disabled'
        self.slogan_btn['state'] = 'disabled'
        self.nextpl_btn['state'] = 'disabled'
        self.refresh_scoreboard()

    def draw_start(self):
        """
        1 ekran
        Tworzy ekran rozpoczynajacy gre, gdzie ustawia sie liczbę graczy i rund
        """
        self.options_box = Frame(self.gamebox, bg=self.color_4, border=1, relief="solid", padx=20, pady=10)
        self.nplayer_lbl = Label(self.options_box, text="Liczba graczy:", bg=self.color_4, fg=self.color_3, anchor=W,
                                 font="Broadway 12")
        self.nplayer_inp = Entry(self.options_box, bg=self.color_2, fg=self.color_3)
        self.round_lbl = Label(self.options_box, text="Liczba rund:", bg=self.color_4, fg=self.color_3, anchor=W,
                               font="Broadway 12")
        self.round_cb = Combobox(self.options_box, values=[1, 2, 3])
        self.round_cb['state'] = 'readonly'
        self.round_cb.current(0)
        self.options_acc_btn = Button(self.options_box, text="Zatwierdź", fg=self.color_3, bg=self.color_1,
                                      font="Broadway 12", activeforeground=self.color_3, activebackground=self.color_2,
                                      command=self.acc_settings)

        self.options_box.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.nplayer_lbl.pack(fill=BOTH)
        self.nplayer_inp.pack(fill=BOTH)
        self.round_lbl.pack(fill=BOTH, pady=(10, 0))
        self.round_cb.pack(fill=BOTH, pady=(0, 10))
        self.options_acc_btn.pack(pady=10)

    def draw_player_names(self):
        """
        2 ekran - wprowadzanie nazw graczy
        """
        self.options_box.destroy()
        self.playersbox = Frame(self.gamebox, bg=self.color_4, border=1, relief="solid", padx=10, pady=10)
        self.players_title_lbl = Label(self.playersbox, text="Nazwy graczy", bg=self.color_4, fg=self.color_3,
                                       font="Broadway 14")
        self.players_acc_btn = Button(self.playersbox, text="Zatwierdź", fg=self.color_3, bg=self.color_1,
                                      font="Broadway 12", activeforeground=self.color_3, activebackground=self.color_2,
                                      command=self.acc_players)

        self.playersbox.place(relwidth=0.3, relheight=1, relx=0.35)
        self.players_title_lbl.pack()

        self.players_entry = [PlayerEntry(self.playersbox, i) for i in range(self.nplayers)]
        for i in range(self.nplayers):
            self.players_entry[i].pack(fill=BOTH, pady=(0, 7))

        self.players_acc_btn.pack(side=BOTTOM)

    def draw_category(self):
        """
        3 ekran - losuje i wyświetla kategorie hasła oraz losuje hasło
        """
        self.los_category()
        self.playersbox.destroy()
        self.catbox = Frame(self.gamebox, bg=self.color_4, border=1, relief="solid", padx=10, pady=10)
        self.catbox.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.round_lbl = Label(self.catbox, text="Runda " + str(self.act_round), bg=self.color_4, fg=self.color_3,
                               font="Broadway 16")
        self.round_lbl.pack(pady=(0, 20))
        self.cat_title_lbl = Label(self.catbox, text="Kategoria", bg=self.color_4, fg=self.color_3,
                                   font="Broadway 14")
        self.cat_title_lbl.pack()
        self.categ_lbl = Label(self.catbox, text=self.category, bg=self.color_4, fg=self.color_3,
                               font="Broadway 12")
        self.categ_lbl.pack()
        self.after(2000, self.draw_kolejn)

    def draw_kolejn(self):
        """
        4 ekran - losuje kolejność i wyświetla na ekranie
        """
        self.catbox.destroy()

        self.playersbox = Frame(self.gamebox, bg=self.color_4, border=1, relief="solid", padx=10, pady=10)
        self.players_title_lbl = Label(self.playersbox, text="Kolejność", bg=self.color_4, fg=self.color_3,
                                       font="Broadway 14")
        self.playersframe = Frame(self.playersbox, bg=self.color_4)

        self.playersbox.place(relwidth=0.3, relheight=1, relx=0.35)
        self.players_title_lbl.pack()
        self.playersframe.pack(fill=BOTH)

        self.playersframe.grid_columnconfigure(0, weight=9)
        self.playersframe.grid_columnconfigure(1, weight=1)
        self.playernames_lbls = [Label() for i in range(self.nplayers)]
        self.playerpos_lbls = [Label() for i in range(self.nplayers)]
        kolejno = []
        afterms = 500
        choices = [x for x in range(self.nplayers)]
        for i in range(self.nplayers):
            self.playernames_lbls[i] = Label(self.playersframe, text=self.players[i], bg=self.color_2, fg=self.color_3,
                                             anchor=W, font="Broadway 10")
            self.playernames_lbls[i].grid(row=i, column=0, sticky=N + W + E + S, padx=(0, 4), pady=(0, 2))
            self.playerpos_lbls[i] = Label(self.playersframe, text="", bg=self.color_2, fg=self.color_3,
                                           anchor=W, font="Broadway 10")
            self.playerpos_lbls[i].grid(row=i, column=1, sticky=N + W + E + S, pady=(0, 2))
            # wybor losowej kolejnosci
            ch = random.choice(choices)
            kolejno.append(ch)
            choices.remove(ch)
            # zeby pojawiało się powoli
            self.after(afterms, self.print_kolej, i, ch + 1)
            afterms += 500

        # grupujemy graczy z kolejnoscia aby posortowac
        kolejnogr = [(kolejno[i], self.players[i]) for i in range(self.nplayers)]
        kolejnogr.sort()
        # tworzymy nowa posortowana liste graczy
        self.players = [x[1] for x in kolejnogr]
        self.after(afterms + 1500, self.draw_game)

    def draw_game(self):
        """
        5 ekran - gra
        """
        self.playersbox.destroy()
        self.active_player = 0
        # GRACZE ------------------------------------------------------------------------
        self.playersbox = Frame(self.gamebox, bg=self.color_4, border=1, relief="solid", padx=5, pady=5)
        self.playersbox.place(relx=0, rely=1, relwidth=0.2, relheight=0.90, anchor=SW)
        self.players_title_lbl = Label(self.playersbox, text="Gracze:", bg=self.color_4, fg=self.color_3,
                                       font="Broadway 12")
        self.players_title_lbl.pack(anchor=W)
        self.players_scorebox = Frame(self.playersbox, bg=self.color_4)
        self.players_scorebox.pack(fill=BOTH)
        self.players_scorebox.grid_columnconfigure(0, weight=7)
        self.players_scorebox.grid_columnconfigure(1, weight=1)

        if self.act_round == 1:
            self.make_scoreboard()
        self.refresh_scoreboard()

        self.maingamebox = Frame(self.gamebox, bg=self.color_2, padx=10)
        self.maingamebox.place(relx=1, rely=0, relwidth=0.8, relheight=1, anchor=NE)
        # KATEGORIA ----------------------------------------------------------------------
        self.round_lbl = Label(self.maingamebox, text="Runda " + str(self.act_round), bg=self.color_4, fg=self.color_3,
                               font="Broadway 18", borderwidth=1, relief="solid", anchor=E)
        self.round_lbl.pack(fill=BOTH, pady=(0, 5))
        self.categ_lbl = Label(self.maingamebox, text="Kategoria: " + self.category, bg=self.color_4, fg=self.color_3,
                               font="Broadway 16", borderwidth=1, relief="solid")
        self.categ_lbl.pack(fill=BOTH, pady=5)

        # HASLO ----------------------------------------------------------------------------------------
        self.los_slogan()
        self.set_slogan()
        self.sloganbox = Frame(self.maingamebox, bg=self.color_4, border=1, relief="solid", padx=5, pady=5)
        self.sloganbox.pack(pady=5)
        self.slogan_letters = [[Label() for i in range(15)] for j in range(4)]
        for i in range(15):
            self.sloganbox.grid_columnconfigure(i, weight=1)
            for j in range(4):
                self.slogan_letters[j][i] = Label(self.sloganbox, text=self.slogan_field_rev[j][i], bg=self.color_5,
                                                  fg=self.color_3, font="Broadway 12", width=2)
                self.slogan_letters[j][i].grid(row=j, column=i, padx=(0, 2), pady=(0, 2))
                if self.slogan_field[j][i] != "":
                    self.slogan_letters[j][i].config(bg=self.color_6)
        # SPIN -----------------------------------------------------------------------------------------
        self.spincanva = Canvas(self.maingamebox, bg="red", height=50, highlightthickness=0)
        self.spincanva.bind("<Configure>", self.draw_spinelems)
        self.spincanva.pack(fill=BOTH, pady=(5, 2))
        self.spin_btn = Button(self.maingamebox, text="Zakręć!", fg=self.color_3, bg=self.color_1,
                               font="Broadway 12 bold", activeforeground=self.color_3, activebackground=self.color_2,
                               command=self.spin)
        self.spin_btn.pack(pady=(2, 5))
        # ACTIONSBOX------------------------------------------------------------------------------------
        self.actionbox = Frame(self.maingamebox, bg=self.color_4, border=1, relief="solid", padx=20, pady=5)
        self.actionbox.pack(side=BOTTOM)
        self.actionbox.grid_columnconfigure(0, weight=1)
        self.actionbox.grid_columnconfigure(1, weight=1)
        self.actionbox.grid_columnconfigure(2, weight=1)
        self.letter_input = Entry(self.actionbox, bg=self.color_1, fg=self.color_3, width=2, justify=CENTER, disabledbackground=self.color_1)
        self.letter_input['state'] = 'disabled'
        self.letter_input.bind("<Key>", self.strict_len)
        self.letter_input.grid(row=0, column=0)
        self.letter_btn = Button(self.actionbox, text="Sprawdź literę!", fg=self.color_3, bg=self.color_1,
                                 font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                 command=self.check_letter)
        self.letter_btn['state'] = 'disabled'
        self.letter_btn.grid(row=1, column=0, padx=5, pady=2)
        self.slogan_input = Entry(self.actionbox, bg=self.color_1, fg=self.color_3, disabledbackground=self.color_1)
        self.slogan_input['state'] = 'disabled'
        self.slogan_input.grid(row=0, column=1)
        self.slogan_btn = Button(self.actionbox, text="Sprawdź hasło!", fg=self.color_3, bg=self.color_1,
                                 font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                 command=self.check_password)
        self.slogan_btn['state'] = 'disabled'
        self.slogan_btn.grid(row=1, column=1, padx=5, pady=2)
        self.nextpl_btn = Button(self.actionbox, text="Następny gracz!", fg=self.color_3, bg=self.color_1,
                                 font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                 command=self.next_player)
        self.nextpl_btn['state'] = 'disabled'
        self.nextpl_btn.grid(row=1, column=2, padx=5, pady=2)

    def draw_final(self):
        """
        Wyswietla końcowy ekran i zapisuje wyniki do bazy danych
        """
        self.menu_btn.destroy()
        self.playersbox.destroy()
        self.maingamebox.destroy()
        self.playersbox = Frame(self.gamebox, bg=self.color_4, border=1, relief="solid", padx=10, pady=10)
        self.players_title_lbl = Label(self.playersbox, text="Tabela końcowa", bg=self.color_4, fg=self.color_3,
                                       font="Broadway 14")
        self.playersframe = Frame(self.playersbox, bg=self.color_4)

        self.playersbox.place(relwidth=0.3, relheight=1, relx=0.35)
        self.players_title_lbl.pack()
        self.playersframe.pack(fill=BOTH)

        self.playersframe.grid_columnconfigure(0, weight=9)
        self.playersframe.grid_columnconfigure(1, weight=1)
        self.playernames_lbls = [Label() for i in range(self.nplayers)]
        self.playerpos_lbls = [Label() for i in range(self.nplayers)]

        with open("temp_scrbrd.json", "r") as f:
            sc = json.load(f)
        # posortowanie danych
        sc = dict(sorted(sc.items(), key=lambda item: item[1], reverse=True))
        for i in range(self.nplayers):
            row = list(sc.items())[i]
            # zapisywanie wyników do bazy danych
            self.window.database.add_score(row[0], row[1], self.nrounds)
            # wyswietlanie tabeli koncowej
            self.playernames_lbls[i] = Label(self.playersframe, text=row[0], bg=self.color_2, fg=self.color_3,
                                             anchor=W, font="Broadway 10")
            self.playernames_lbls[i].grid(row=i, column=0, sticky=N + W + E + S, padx=(0, 4), pady=(0, 2))
            self.playerpos_lbls[i] = Label(self.playersframe, text=row[1], bg=self.color_2, fg=self.color_3,
                                           anchor=W, font="Broadway 10")
            self.playerpos_lbls[i].grid(row=i, column=1, sticky=N + W + E + S, pady=(0, 2))

        # usuwanie wyników poniżej top 100
        self.window.database.remove_below_top100(self.nrounds)
        # Przyciski
        self.buttonsbox = Frame(self.playersbox, bg=self.color_5, border=1, relief="solid", padx=20, pady=5)
        self.buttonsbox.pack(side=BOTTOM, fill=BOTH)
        self.nextgame_btn = Button(self.buttonsbox, text="Następna gra!", fg=self.color_3, bg=self.color_1,
                                   font="Broadway 12 bold", activeforeground=self.color_3,
                                   activebackground=self.color_2,
                                   command=lambda: self.window.change_state(Game(self.parent, self.window)))
        self.nextgame_btn.pack(pady=5)
        self.menu_btn = Button(self.buttonsbox, text="Menu główne!", fg=self.color_3, bg=self.color_1,
                               font="Broadway 12 bold", activeforeground=self.color_3,
                               activebackground=self.color_2,
                               command=lambda: self.window.change_state(MainMenu(self.parent, self.window)))
        self.menu_btn.pack(pady=5)

    def __del__(self):
        """
        Przy niszczeniu obiektu (wyjscie z gry)
        """
        self.delete_scoreboard()


class Scoreboard(Frame):
    color_1 = "#2A272A"
    color_2 = "#303030"
    color_3 = "#E2B659"

    current_top = 0

    def __init__(self, parent, window):
        self.window = window
        super().__init__(parent)
        self.parent = parent
        self.config(bg=self.color_1)
        self.config(pady=25)

        self.middle = Frame(self, bg=self.color_2, border=2, relief="solid", padx=20, pady=20)
        self.middle.place(relheight=1, relwidth=0.8, relx=0.1, rely=0.0)

        self.middle.grid_columnconfigure(0, weight=1)
        self.middle.grid_rowconfigure(2, weight=1)
        self.menu_btn = Button(self.middle, text="<<Menu Główne", fg=self.color_3, bg=self.color_1,
                               font="Broadway 11", activeforeground=self.color_3, activebackground=self.color_2,
                               command=lambda: self.window.change_state(MainMenu(self.parent, self.window)))
        self.menu_btn.grid(row=0, sticky=N + W)
        self.title = Label(self.middle, text="Rankingi", fg=self.color_3, bg=self.color_2, anchor=SW,
                           font="Broadway 20 bold")
        self.title.grid(row=1, sticky=N + S + E + W)

        self.rnd_lbl = Label(self.middle, text="Liczba rund:", fg=self.color_3, bg=self.color_2, anchor=W,
                             font="Broadway 10")
        self.rnd_lbl.grid(row=0, column=1, sticky=N + S + E + W)

        self.cb_round = Combobox(self.middle, values=[1, 2, 3], width=1)
        self.cb_round.current(0)
        self.cb_round.grid(row=1, column=1, sticky=N + E + W)
        self.cb_round.bind("<<ComboboxSelected>>", self.change_scoreboard)
        self.cb_round['state'] = 'readonly'

        self.scrb_frame = Frame(self.middle, bg=self.color_1, padx=5, pady=5)
        self.scrb_frame.grid(row=2, columnspan=3, sticky=N + S + E + W)

        self.scrb_buttons = Frame(self.middle, bg=self.color_2)
        self.scrb_buttons.grid(row=3, columnspan=3, sticky=N + S + E + W)
        self.first10_bt = Button(self.scrb_buttons, text="|<<", fg=self.color_3, bg=self.color_2, width=4,
                                 font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                 command=lambda: self.ch_current_top(-len(self.data)))
        self.first10_bt.pack(side=LEFT)
        self.prev10_bt = Button(self.scrb_buttons, text="<<", fg=self.color_3, bg=self.color_2, width=4,
                                font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                command=lambda: self.ch_current_top(-1))
        self.prev10_bt.pack(side=LEFT)
        self.last10_bt = Button(self.scrb_buttons, text=">>|", fg=self.color_3, bg=self.color_2, width=4,
                                font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                command=lambda: self.ch_current_top(len(self.data)))
        self.last10_bt.pack(side=RIGHT)
        self.next10_bt = Button(self.scrb_buttons, text=">>", fg=self.color_3, bg=self.color_2, width=4,
                                font="Broadway 10 bold", activeforeground=self.color_3, activebackground=self.color_2,
                                command=lambda: self.ch_current_top(1))
        self.next10_bt.pack(side=RIGHT)

        self.scroll = Scrollbar(self.scrb_frame, orient="vertical")
        self.scroll.pack(side=RIGHT, fill=Y)
        self.scrb = Canvas(self.scrb_frame, bg=self.color_1, highlightthickness=0, yscrollcommand=self.scroll.set)
        self.scrb.pack(side=TOP, fill=BOTH, expand=1, padx=(0, 5))
        self.scrb.bind("<Configure>", self.rfsh_scoreboard_size)
        self.scroll.configure(command=self.scrb.yview)

        self.scrb_list = Frame(self.scrb, bg=self.color_1)
        self.scrb_list_id = self.scrb.create_window(0, 0, anchor=NW, window=self.scrb_list)
        self.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        self.down_data()
        self.rfsh_scoreboard()

    def ch_current_top(self, change):
        """
        Zmienia wyswietlaną 10
        change:int
            o ile okienek sie przesunac
        """
        self.current_top += change
        if self.current_top < 0:
            self.current_top = 0
        elif self.current_top > int(len(self.data) / 10):
            self.current_top = int(len(self.data) / 10)
        self.rfsh_scoreboard()

    def down_data(self):
        """
        Pobiera dane z bazy danych
        """
        r_id = self.cb_round.get()
        self.data = self.window.database.get_top(r_id)

    def change_scoreboard(self, e):
        """
        Zmiana tablicy wyników
        """
        self.down_data()
        self.rfsh_scoreboard()

    def rfsh_scoreboard(self):
        """
        Odświeżanie wyświetlanej tablicy
        """
        # czyszczenie wszystkich dzieci
        for widget in self.scrb_list.winfo_children():
            widget.destroy()
        # wstawienie wiersza z nazwami
        self.title_row = Record(self.scrb_list, 0)
        self.title_row.pack(fill=BOTH, pady=(0, 4))
        # wiersze z wynikami
        l = min(10, len(self.data) - self.current_top * 10)
        self.rows = [Record(self.scrb_list, i % 2) for i in range(l)]
        for i in range(l):
            ind = self.current_top * 10 + i
            self.rows[i].set_pos("%03d" % (ind + 1))
            self.rows[i].pack(fill=BOTH)
            self.rows[i].set_name(self.data[ind][1])
            self.rows[i].set_score(self.data[ind][2])

        self.scrb.update_idletasks()
        self.scrb.configure(scrollregion=self.scrb.bbox("all"))

    def rfsh_scoreboard_size(self, e):
        """
        Dla responsywnosci
        e:Event
            event jaki wywowołał tę funkcję
        """
        self.scrb.itemconfig(self.scrb_list_id, width=e.width)


class Database:
    def __init__(self):
        self.conn = ps.connect("host=212.182.24.105 port=15432 dbname=student9 user=student9 password=st2021%9")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def get_top(self, rounds):
        """
        Pobiera listę wyników o podanej liczbie rund
        rounds:int
            Liczba rund
        Return:
            zwraca pobraną listę
        """
        self.cur.execute("SELECT * FROM Scoreboard WHERE n_rounds=%s ORDER BY score DESC", (rounds,))
        data = self.cur.fetchall()
        return data

    def remove_below_top100(self, nround):
        self.cur.execute("""DELETE FROM Scoreboard sg WHERE  sg.n_rounds=%s AND 
                            sg.id NOT IN( SELECT sp.id FROM Scoreboard sp
                            WHERE sp.n_rounds=%s ORDER BY sp.score DESC LIMIT 100)""", (nround, nround,))
        self.conn.commit()

    def add_score(self, name, score, nrounds):
        """
        Dodawanie wyniku do bazy danych
        name:string
            Nazwa gracz
        score:int
            Wynik
        nrounds:int
            Liczba rund
        """
        self.cur.execute("INSERT INTO Scoreboard(name, score, n_rounds) VALUES(%s,%s, %s)", (name, score, nrounds,))
        self.conn.commit()

    def get_categories(self):
        """
        Pobiera listę kategorii
        Return:
            zwraca pobraną listę
        """
        self.cur.execute("SELECT category FROM Slogans GROUP BY category")
        data = self.cur.fetchall()
        return data

    def get_slogans(self, cat):
        """
        Pobiera listę haseł o podanej kategorii
        rounds:int
            Liczba rund
        Return:
            zwraca pobraną listę
        """
        self.cur.execute("SELECT slogan FROM Slogans WHERE category=%s", (cat,))
        data = self.cur.fetchall()
        return data


class Window:
    color_1 = "#2A272A"
    color_2 = "#E2B659"

    def __init__(self, resolution, title):
        self.database = Database()
        self.root = Tk()
        self.root.geometry(resolution)
        self.root.title(title)
        self.state = MainMenu(self.root, self)
        self.state.pack(fill=BOTH, expand=1)

        # zmiana stylu Comboboxa
        self.style = Style()
        self.style.theme_use("clam")
        self.style.map('TCombobox', fieldbackground=[('readonly', self.color_1)])
        self.style.map('TCombobox', selectbackground=[('readonly', self.color_1)])
        self.style.map('TCombobox', selectforeground=[('readonly', self.color_2)])
        self.style.map('TCombobox', foreground=[('readonly', self.color_2)])

        self.root.mainloop()

    def change_state(self, state):
        self.state.destroy()
        self.state = state
        self.state.pack(fill=BOTH, expand=1)


mainWindow = Window("1024x576", "Koło Fortuny")
