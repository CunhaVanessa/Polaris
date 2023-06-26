from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from board import Board
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from math import sin, cos, pi


class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.main_window = Tk()  # instanciar Tk
        self.fill_main_window()  # organização e preenchimento da janela
        self.board = Board()  # tratamento do domínio do problema
        game_state = self.board.get_status()
        self.update_gui(game_state)
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        self.main_window.mainloop()  # abrir a janela

    def fill_main_window(self):
        # Título, ícone, dimensionamento e fundo da janela
        self.main_window.title("Polaris ✨")
        self.main_window.geometry("1280x720")
        self.main_window.resizable(True, True)
        self.main_window["bg"] = "white"

        # Criação de 2 frames e organização da janela em um grid de 2 linhas e 1 coluna,
        # sendo que table_frame ocupa a linha superior e message_frame, a inferior
        self.table_frame = Canvas(self.main_window, bg="white")
        self.table_frame.grid(row=0, column=0, sticky='nsew')

        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        self.message_frame = Label(self.main_window, bg="white", fg="black")
        self.message_frame.grid(row=1, column=0, sticky='nsew')
        
        self.table_frame.bind("<Configure>", self.on_resize)

        # Preenchimento de table_frame com 21 imagens iguais, organizadas em 3 linhas e 7 colunas

        # Preenchimento de message_frame com 1 imagem com logo (label) e 1 label com texto,
        # organizadas em 1 linha e 2 colunas

        self.message_label = Label(self.message_frame, bg="white", text=" Gobblet Gobblers", font="arial 30", fg="black")
        self.message_label.grid(row=0, column=1)

        # Criação de um menu para o programa
        # Criar a barra de menu (menubar) e adicionar à janela:
        self.menubar = Menu(self.main_window)
        self.menubar.option_add("*tearOff", FALSE)
        self.main_window["menu"] = self.menubar
        # Adicionar menu(s) à barra de menu:
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")
        # Adicionar itens de menu a cada menu adicionado à barra de menu:
        self.menu_file.add_command(label="Iniciar jogo", command=self.start_match)
        self.menu_file.add_command(label="Restaurar estado inicial", command=self.start_game)
    
        # on_resize method
    def on_resize(self, event):
        self.table_frame.delete("board")
        self.create_board()

    def select_board_place(self, event, line, column):
        match_status = self.board.get_match_status()
        if match_status == 3 or match_status == 4:
            move_to_send = self.board.select_board_place(line, column)
            game_state = self.board.get_status()
            self.update_gui(game_state)
            if bool(move_to_send):
                self.dog_server_interface.send_move(move_to_send)

    def receive_move(self, a_move):
        self.board.receive_move(a_move)
        game_state = self.board.get_status()
        self.update_gui(game_state)

    def start_match(self):
        match_status = self.board.get_match_status()
        if match_status == 1:
            answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
            if answer:
                start_status = self.dog_server_interface.start_match(2)
                code = start_status.get_code()
                message = start_status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                else:  #    (code=='2')
                    players = start_status.get_players()
                    local_player_id = start_status.get_local_id()
                    self.board.start_match(players, local_player_id)
                    game_state = self.board.get_status()
                    self.update_gui(game_state)
                    messagebox.showinfo(message=start_status.get_message())

    def receive_start(self, start_status):
        self.start_game()  #    use case reset game
        players = start_status.get_players()
        local_player_id = start_status.get_local_id()
        self.board.start_match(players, local_player_id)
        game_state = self.board.get_status()
        self.update_gui(game_state)

    def start_game(self):
        match_status = self.board.get_match_status()
        if match_status == 2 or match_status == 6:
            self.board.reset_game()
            game_state = self.board.get_status()
            self.update_gui(game_state)

    def receive_withdrawal_notification(self):
        self.board.receive_withdrawal_notification()
        game_state = self.board.get_status()
        self.update_gui(game_state)

    def update_gui(self, game_state):
        self.update_menu_status()
        self.message_label["text"] = game_state.get_message()
        self.image_to_draw = []


    def update_menu_status(self):
        match_status = self.board.get_match_status()
        if match_status == 2 or match_status == 6:
            self.menu_file.entryconfigure("Restaurar estado inicial", state="normal")
        else:
            self.menu_file.entryconfigure("Restaurar estado inicial", state="disabled")
        if match_status == 1:
            self.menu_file.entryconfigure("Iniciar jogo", state="normal")
        else:
            self.menu_file.entryconfigure("Iniciar jogo", state="disabled")

    def get_image_id(self, match_status, line, column):
        if column == 0 or column == 1:  #   red pieces space
            player1_pieces = match_status.get_player1_pieces()
            if line == 0:
                if player1_pieces[2] == 2 or (player1_pieces[2] == 1 and column == 0):
                    if player1_pieces[3] == 3 and column == 0:
                        return "src/images/pecaVGs.png"
                    else:
                        return "src/images/pecaVG.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 1:
                if player1_pieces[1] == 2 or (player1_pieces[1] == 1 and column == 0):
                    if player1_pieces[3] == 2 and column == 0:
                        return "src/images/pecaVMs.png"
                    else:
                        return "src/images/pecaVM.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 2:
                if player1_pieces[0] == 2 or (player1_pieces[0] == 1 and column == 0):
                    if player1_pieces[3] == 1 and column == 0:
                        return "src/images/pecaVPs.png"
                    else:
                        return "src/images/pecaVP.png"
                else:
                    return "src/images/pecaSem.png"

        elif column == 5 or column == 6:  #   blue pieces space
            player2_pieces = match_status.get_player2_pieces()
            if line == 0:
                if player2_pieces[2] == 2 or (player2_pieces[2] == 1 and column == 6):
                    if player2_pieces[3] == 3 and column == 6:
                        return "src/images/pecaAGs.png"
                    else:
                        return "src/images/pecaAG.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 1:
                if player2_pieces[1] == 2 or (player2_pieces[1] == 1 and column == 6):
                    if player2_pieces[3] == 2 and column == 6:
                        return "src/images/pecaAMs.png"
                    else:
                        return "src/images/pecaAM.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 2:
                if player2_pieces[0] == 2 or (player2_pieces[0] == 1 and column == 6):
                    if player2_pieces[3] == 1 and column == 6:
                        return "src/images/pecaAPs.png"
                    else:
                        return "src/images/pecaAP.png"
                else:
                    return "src/images/pecaSem.png"
        else:  #   board space
            selected_position = match_status.get_selected_position()
            selected_line = selected_position[0]
            selected_column = selected_position[1]
            if match_status.getValue(line, column - 2) == 6:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posAGs.png"
                else:
                    return "src/images/posAG.png"
            if match_status.getValue(line, column - 2) == 5:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posAMs.png"
                else:
                    return "src/images/posAM.png"
            if match_status.getValue(line, column - 2) == 4:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posAPs.png"
                else:
                    return "src/images/posAP.png"
            if match_status.getValue(line, column - 2) == 3:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posVGs.png"
                else:
                    return "src/images/posVG.png"
            if match_status.getValue(line, column - 2) == 2:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posVMs.png"
                else:
                    return "src/images/posVM.png"
            if match_status.getValue(line, column - 2) == 1:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posVPs.png"
                else:
                    return "src/images/posVP.png"
            else:
                return "src/images/posSem.png"

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

        board_center_x = self.table_frame.winfo_width() / 2
        board_center_y = self.table_frame.winfo_height() / 2

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
                self.table_frame.tag_bind(sfere_tag, "<Button-1>", lambda event, tag=sfere_tag: self.on_sfere_click(event, tag))

    # create_hexagon method
    def create_hexagon(self, x, y, radius, **kwargs):
        points = []
        for i in range(6):
            angle = 2 * pi * i / 6
            points.append((x + radius * cos(angle), y + radius * sin(angle)))
        return self.table_frame.create_polygon(points, **kwargs)


    # create_sfere method
    def create_sfere(self, x, y, radius, **kwargs):  
       return self.table_frame.create_oval(x - radius, y - radius, x + radius, y + radius, **kwargs)

    # on_sfere_click method
    def on_sfere_click(self, event, sfere_tag):
        print(f"{sfere_tag} foi clicado")
