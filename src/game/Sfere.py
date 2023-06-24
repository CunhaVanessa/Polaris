class Sfere:
    def __init__(self, color, selected=False):
        self._color = color
        self._selected = selected

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
