import tkinter as tk
from tkinter import messagebox
from TelaInicial import TelaInicial
from TelaConectarComOponente import TelaConectarComOponente
from TelaTabuleiro import TelaTabuleiro

import sys

sys.path.append('../dog')
from dog_interface import DogPlayerInterface
from dog_actor import DogActor

sys.path.append('../game')
from Player import Player
from Sfere import Sfere
from Position import Position


class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Jogo')
        self.window.geometry('800x600')
        self.dog_server_interface_ = DogActor()
        
        # inicializa todas as telas aqui
        self.tela_inicial = None
        self.tela_jogo = None
        self.tela_vitoria = None
        self.tela_derrota = None
        self.tela_tabuleiro = TelaTabuleiro(self.window, self)

        # indica qual tela está atualmente ativa
        self.active_screen = None
        # Cria os jogadores
        self.player1 = None
        self.player2 = None

    def start(self):
        self.show_tela_inicial()
        self.window.mainloop()

    def show_tela_inicial(self):
        if self.active_screen is not None:
            self.active_screen.pack_forget()

        self.tela_inicial = TelaInicial(self.window, self)
        self.tela_inicial.pack(expand=True, fill='both')
        self.active_screen = self.tela_inicial
    
    def show_tela_conectar_oponente(self):       
        nome_jogador = self.tela_inicial.nome_jogador.get()
        self.updatePlayerLabel(nome_jogador)        
        message = self.dog_server_interface_.initialize(nome_jogador, self)
        messagebox.showinfo(message=message)
        print(message)
        if message == "Conectado a Dog Server":
            if self.active_screen is not None:
                self.active_screen.pack_forget()

                self.tela_conectar_oponente = TelaConectarComOponente(self.window, self)
                self.tela_conectar_oponente.pack(expand=True, fill='both')
                self.active_screen = self.tela_conectar_oponente       
        else:
            self.window.destroy()
    
    def show_tela_tabuleiro(self):
        start_status = self.dog_server_interface_.start_match(2)       
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        print(message)
        
        if message == 'Partida iniciada':      
            if self.active_screen is not None:
                self.active_screen.pack_forget()
            
            self.updatePlayerLabel(self.player1.name)        
            self.tela_tabuleiro = TelaTabuleiro(self.window, self)
            self.tela_tabuleiro.pack(expand=True, fill='both')
            self.active_screen = self.tela_tabuleiro


    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        if message == 'Partida iniciada':      
            if self.active_screen is not None:
                self.active_screen.pack_forget()
            
            self.tela_tabuleiro = TelaTabuleiro(self.window, self)
            self.tela_tabuleiro.pack(expand=True, fill='both')
            self.active_screen = self.tela_tabuleiro

    def updatePlayerLabel(self, nome_jogador):
        if self.player1 is None:
            self.player1 = Player(nome_jogador)
        elif self.player2 is None:
            self.player2 = Player(nome_jogador)
        else:
            self.tela_tabuleiro.nomeJogadorJ1.configure(text=self.player1.name)
            self.tela_tabuleiro.nomeJogadorJ2.configure(text=self.player2.name)

    def check_is_valid_move():
        pass

    def move_sfere():
        pass

    def check_victory():
        pass

if __name__ == "__main__":
    interface = PlayerInterface()
    interface.start()
