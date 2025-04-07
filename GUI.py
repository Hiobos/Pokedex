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
        self.window = Tk()
        self.window.title('Pokedex')
        self.window.config(bg=CLR)
        self.window.minsize(500, 500)
        self.canvas = Canvas(self.window, width=500, height=500, bg=CLR)
        self.images = []
        self.column = 0
        self.row = 0
        self.canvas.grid(row=0, column=0)
        self.inner_frame = Frame(self.canvas, bg=CLR)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.add_pokemon(1)
        self.window.mainloop()

    def add_pokemon(self, pokemon_id):
        pokemon_list, sprite_list = pokemon_data.fetch_data()
        for i in range(0, 151):#number of pokemons
            #Getting list of pokemons and their sprites in a loop
            pokemon = pb.pokemon(pokemon_list[i])
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
            #pokemon name
            pokemon_name = Label(frame, text=pokemon_list[i].capitalize(), bg=CLR)
            pokemon_name.grid(row=1, column=self.column)
            #pokemon type
            pokemon_type = Label(frame, text=pokemon.types[0].type.name, bg=CLR)
            pokemon_type.grid(row=2, column=self.column)
            frame.grid(row = self.row, column = self.column, pady=10, padx=10)
            self.column += 1

            if self.column % 3 == 0:
                self.column = 0
                self.row += 1

            self.images.append(photo)


            self.inner_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def load_pokemon_batch(self, start=1, end=20):
        if start > end:
            return
        self.add_pokemon(start)
        self.window.after(100, lambda: self.load_pokemon_batch(start + 1, end))



