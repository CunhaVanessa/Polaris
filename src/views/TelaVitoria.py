import tkinter as tk

class TelaVitoria(tk.Frame):
    def __init__(self, master, interface):
        super().__init__(master)
        self.interface = interface

        label = tk.Label(self, text="Bem-vindo ao jogo!")
        label.pack()


    def initializa(self):
        self.interface.show_tela_conectar_oponente()
