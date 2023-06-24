import random

class Player:
    def __init__(self, name):
        self._name = name
        self._sfere_color = None
        self._pushed_sferes = None
        self._selected_positions = None
        self._winner = False
        self._turn = False
        self._sferes = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def sfere_color(self):
        return self._sfere_color

    @sfere_color.setter
    def sfere_color(self, value):
        self._sfere_color = value

    @property
    def pushed_sferes(self):
        return self._pushed_sferes

    @pushed_sferes.setter
    def pushed_sferes(self, value):
        self._pushed_sferes = value

    @property
    def selected_positions(self):
        return self._selected_positions

    @selected_positions.setter
    def selected_positions(self, value):
        self._selected_positions = value

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, value):
        self._turn = value

    @property
    def sferes(self):
        return self._sferes

    @sferes.setter
    def sferes(self, value):
        self._sferes = value

    @staticmethod
    def decidesSfereColor(player1, player2):
        colors = [player1, player2]
        random.shuffle(colors)  # Embaralha a ordem dos jogadores
        player1.sfere_color(1)
        player2.sfere_color(2)

        return colors[0]
