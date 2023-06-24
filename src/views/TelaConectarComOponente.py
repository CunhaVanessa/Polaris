import tkinter as tk

class TelaConectarComOponente(tk.Frame):
    def __init__(self, master, interface):
        super().__init__(master)
        self.interface = interface
        self.config(bg='white')  # configura o fundo da tela inteira como branco

        # QGraphicsView
        graphics_view = tk.Canvas(self, bg="#44a5ff", width=100, height=50)
        graphics_view.pack(fill=tk.X, side=tk.TOP)
        
        # QLabel
        label_polaris = tk.Label(self, bg="white", fg="black", text="Polaris ✨", font=("Arial", 36, "bold"))
        label_polaris.pack(pady=30)

        # JButton
        start_game_button = tk.Button(self, bg="#44a5ff", activebackground="#44a5ff", disabledforeground="#44a5ff", text="Conectar com o oponente", font=("Arial", 20, "bold"), fg="#ffffff", command=self.start_game)
        start_game_button.pack()

    def start_game(self):
        self.interface.show_tela_tabuleiro()
