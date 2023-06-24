import tkinter as tk
from math import sin, cos, pi

class TelaTabuleiro(tk.Frame):
    def __init__(self, master, interface):
        super().__init__(master)
        self.interface = interface
        self.config(background="white")
        self.master.geometry("1440x900")

        # Faixa superior
        self.faixa = tk.Label(self, bg="#44a5ff", fg="white", text="Polaris ✨", font=("Arial", 16, "bold"), padx=50,
                              anchor="w")
        self.faixa.pack(fill=tk.X)
        # QGraphicsView
        self.graphicsView = tk.Canvas(self, bg="white")
        self.graphicsView.pack(expand=True, fill=tk.BOTH)

        # button
        self.botaoSendMove = tk.Button(self, text="Enviar Jogada!", bg="#44a5ff", fg="white", font=("Arial", 16, "bold"), command=self.sendMove)
        self.botaoSendMove.place(x=1140, y=570, width=201, height=50)

        # Labels
        self.nomeJogadorJ1 = tk.StringVar()
        self.nomeJogadorJ1 = tk.Label(self, text="Jogadora 1", font=("Arial", 28), bg="white", fg="black")
        self.nomeJogadorJ1.place(x=40, y=90)

        self.pecasPerdidasJ1 = tk.Label(self, text="Peças perdidas", font=("Arial", 16), bg="white", fg="black")
        self.pecasPerdidasJ1.place(x=40, y=230)

        self.pecasEmpurradasJ1 = tk.Label(self, text="Peças empurradas", font=("Arial", 16), bg="white",
                                           fg="black")
        self.pecasEmpurradasJ1.place(x=40, y=430)
        
        self.nomeJogadorJ2 = tk.StringVar()
        self.nomeJogadorJ2 = tk.Label(self, text="Jogador 2", font=("Arial", 28), bg="white", fg="black")
        self.nomeJogadorJ2.place(x=1150, y=90)

        self.pecasPerdidasJ2 = tk.Label(self, text="Peças perdidas", font=("Arial", 16), bg="white", fg="black")
        self.pecasPerdidasJ2.place(x=1150, y=230)

        self.pecasEmpurradasJ2 = tk.Label(self, text="Peças empurradas", font=("Arial", 16), bg="white",
                                           fg="black")
        self.pecasEmpurradasJ2.place(x=1150, y=430)

        # graphics views
        self.qtpecasPerdidasJ1 = tk.Canvas(self, bg="white", width=81, height=51)
        self.qtpecasPerdidasJ1.place(x=1170, y=270)

        self.qtpecasEmpurradasJ1 = tk.Canvas(self, bg="white", width=81, height=51)
        self.qtpecasEmpurradasJ1.place(x=1170, y=470)

        self.qtpecasPerdidasJ2 = tk.Canvas(self, bg="white", width=81, height=51)
        self.qtpecasPerdidasJ2.place(x=70, y=270)

        self.qtpecasEmpurradasJ2 = tk.Canvas(self, bg="white", width=81, height=51)
        self.qtpecasEmpurradasJ2.place(x=70, y=470)


        # Bind event
        self.graphicsView.bind("<Configure>", self.on_resize)

    # Binding command
    def sendMove(self):
        pass

    # on_resize method
    def on_resize(self, event):
        self.graphicsView.delete("board")
        self.create_board()

    # create_board method
    def create_board(self):
        sfere_radius = 15

        # Cálculo do tamanho do hexágono
        hex_radius = sfere_radius * 20
        hex_width = hex_radius * 2
        hex_height = int(hex_width / (3 ** 0.5))

        # Cálculo do espaçamento entre as esferas
        x_spacing = sfere_radius * 1.5 + 10  # Adicionei 10 pixels de espaçamento horizontal
        y_spacing = sfere_radius * 1.5 * (3 ** 0.5)

        board_center_x = self.graphicsView.winfo_width() / 2
        board_center_y = self.graphicsView.winfo_height() / 2

        # Desenhe o hexágono de fundo
        self.create_hexagon(board_center_x, board_center_y, hex_radius, fill='#44a5ff', outline='#44a5ff', tags="board")

        c = [
            (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
            (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
            (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
            (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
            (2, 8), (3, 8), (4, 8), (5, 8), (6, 8)
        ]

        preto = [
            (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), 
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
            (3, 2), (4, 2), (5, 2)
        ]

        branco = [
            (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
            (2, 8), (3, 8), (4, 8), (5, 8), (6, 8),
            (3, 6), (4, 6), (5, 6)
        ]

        for i, j in c:
            x = board_center_x + (i - 4) * x_spacing + (j % 2) * x_spacing / 2
            y = board_center_y + (j - 4) * y_spacing

            # Verifique se a esfera está dentro do hexágono
            if abs(x - board_center_x) + abs(y - board_center_y) <= hex_radius:
                if (i, j) in preto:
                    color = 'black'
                elif (i, j) in branco:
                    color = 'white'
                else:
                    color = 'grey'

                sfere_tag = self.create_sfere(x, y, sfere_radius, fill=color, outline='black', tags="board")
                self.graphicsView.tag_bind(sfere_tag, "<Button-1>", lambda event, tag=sfere_tag: self.on_sfere_click(event, tag))

    # create_hexagon method
    def create_hexagon(self, x, y, radius, **kwargs):
        points = []
        for i in range(6):
            angle = 2 * pi * i / 6
            points.append((x + radius * cos(angle), y + radius * sin(angle)))
        return self.graphicsView.create_polygon(points, **kwargs)


    # create_sfere method
    def create_sfere(self, x, y, radius, **kwargs):  
       return self.graphicsView.create_oval(x - radius, y - radius, x + radius, y + radius, **kwargs)

    # on_sfere_click method
    def on_sfere_click(self, event, sfere_tag):
        print(f"{sfere_tag} foi clicado")
