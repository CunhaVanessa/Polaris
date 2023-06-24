class Position:
    def __init__(self, row, column, sfere=None):
        self._row = row
        self._column = column
        self._sfere = sfere

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    @property
    def sfere(self):
        return self._sfere

    @sfere.setter
    def sfere(self, value):
        self._sfere = value
