import tkinter as tk
from tkinter import messagebox

class TelaInicial(tk.Frame):
    def __init__(self, master, interface):
        super().__init__(master)
        self.interface = interface
        self.nome_jogador_var = tk.StringVar() 

        central_widget = tk.Frame(self, bg="white")
        central_widget.pack(expand=True, fill="both")

        graphics_view = tk.Canvas(central_widget, bg="#44a5ff", width=100, height=50)
        graphics_view.pack(side=tk.TOP, fill=tk.X)

        label_polaris = tk.Label(central_widget, text="Polaris ✨", font=("Arial", 36, "bold"), bg="white", fg="black")
        label_polaris.place(x=80, y=190)

        label_infomeseunome = tk.Label(central_widget, text='Informe seu nome para continuar', font=("Arial", 16), bg="white", fg="black")
        label_infomeseunome.place(x=80, y=230)
        
        self.initialize_button = tk.Button(central_widget, text="Iniciar", font=("Arial", 16, "bold"), activebackground="#44a5ff", bg="#44a5ff", fg="#ffffff", command=self.initialize)
        self.initialize_button.place(x=90, y=410, width=251, height=50)

        label_jogador = tk.Label(central_widget, text='Jogador(a)', font=("Arial", 16), bg="white", fg="black")
        label_jogador.place(x=90, y=340)

        self.nome_jogador = tk.Entry(central_widget, textvariable=self.nome_jogador_var, font=("Arial", 16), bg="white", fg="black")
        self.nome_jogador.place(x=90, y=370, width=251, height=31)

        self.nome_jogador_var.trace_add('write', self.check_entry)

    def check_entry(self, *args):
        # Se o Entry não estiver vazio, habilitar o botão Iniciar
        if self.nome_jogador_var.get().strip():
            self.initialize_button.config(state='normal')
        else:
            self.initialize_button.config(state='disabled')

    def initialize(self):
        if self.nome_jogador_var.get().strip():  # Checando se o nome do jogador não é vazio
            self.interface.show_tela_conectar_oponente()
        else:
            messagebox.showwarning("Erro", "Por favor, insira um nome de jogador válido")  # Exibe uma mensagem de erro se o nome do jogador for vazio

