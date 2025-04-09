from tkinter import *
import pokebase as pb
from PIL import Image, ImageTk
from data import GetData
import requests
import os

CLR = 'lightyellow'

pokemon_data = GetData()

class GraphicInterface:
    def __init__(self):
        #main window
        self.window = Tk()
        self.window.title('Pokedex')
        self.window.config(bg=CLR)
        self.window.minsize(500, 500)
        self.popup_generation()
        #Setting range of Pokemon from API and fetching data
        self.pokemon_list = pokemon_data.fetch_data()

        #defining empty variables
        self.images, self.column, self.row = [], 0, 0
        #canvas, frame, scrollbar
        self.canvas = Canvas(self.window, width=500, height=500, bg=CLR)
        self.canvas.grid(row=0, column=0)
        self.inner_frame = Frame(self.canvas, bg=CLR)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.window.mainloop()

    def popup_generation(self):
        win = Toplevel(bg=CLR)
        win.wm_title("Choose generation")
        win.minsize(300, 60)
        GENERATIONS = {
            'Kanto': (1, 151),  # Gen 1
            'Johto': (152, 251),  # Gen 2
            'Hoenn': (252, 386),  # Gen 3
            'Sinnoh': (387, 493),  # Gen 4
            'Unova': (494, 649),  # Gen 5
            'Kalos': (650, 721),  # Gen 6
            'Alola': (722, 809),  # Gen 7
            'Galar': (810, 905),  # Gen 8
            'Paldea': (906, 1025),  # Gen 9 (Scarlet/Violet)
        }

        offset = Label(win, text="Generation: ", bg=CLR)
        offset.grid(row=0, column=0, pady=5, padx=5)

        variable = StringVar(win)
        variable.set(["Select Generation"])  # default value

        menu = OptionMenu(win, variable, *GENERATIONS)
        menu.grid(row=0, column=1, pady=5, padx=5, sticky=NSEW)

        def submit_action():
            gen_name = variable.get()
            start, end = GENERATIONS[gen_name]
            self.add_pokemon(start - 1, end)
            win.destroy()

        submit = Button(win, text="proceed", command=lambda: submit_action(), width=40, bg=CLR)
        submit.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky=NSEW)
    def add_pokemon(self, index_start, index_end):

        if index_start >= index_end:
            return 0
        print(f"i: {index_start}, len(poke_list): {len(self.pokemon_list)}")

        #Getting list of Pokemon and their sprites in a loop
        pokemon = pb.pokemon(self.pokemon_list[index_start])
        sprite = pb.SpriteResource('pokemon', pokemon.id)
        sprite_url = sprite.url
        #getting photo to PhotoImage
        if not os.path.exists('sprites'):
            os.mkdir('sprites')

        if not os.path.exists(f'sprites/{pokemon.id}.png'):
            response = requests.get(sprite_url)
            with open(f"sprites/{pokemon.id}.png", 'wb') as file:
                file.write(response.content)

        image = Image.open(f'sprites/{pokemon.id}.png')
        photo = ImageTk.PhotoImage(image)
        #frame with photo
        frame = Frame(self.inner_frame, bg=CLR)
        pokemon_img = Label(frame, image=photo, bg=CLR)
        pokemon_img.grid(row=0, column=self.column)
        #Pokedex index
        pokemon_name = Label(frame, text=f"#{index_start + 1}", bg=CLR)
        pokemon_name.grid(row=1, column=self.column)
        #pokemon name
        pokemon_name = Label(frame, text=self.pokemon_list[index_start].capitalize(), bg=CLR)
        pokemon_name.grid(row=2, column=self.column)
        #Pokemon type
        pokemon_type = Label(frame, text=pokemon.types[0].type.name, bg=CLR)
        pokemon_type.grid(row=3, column=self.column)
        frame.grid(row = self.row, column = self.column, pady=10, padx=10)
        self.column += 1

        if self.column % 3 == 0:
            self.column = 0
            self.row += 1

        self.images.append(photo)


        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.window.after(40, lambda: self.add_pokemon(index_start + 1, index_end))