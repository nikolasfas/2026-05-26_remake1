import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._ratings = []

    def fillDDsRating(self):
        self._ratings = self._model.getAllRatings()
        for r in self._ratings:
            self._view._ddrating1.options.append(
                ft.dropdown.Option(int(r))
            )
            self._view._ddrating2.options.append(
                ft.dropdown.Option(int(r))
            )


    def handleCreaGrafo(self, e):
        pass

    def handleCammino(self, e):
        pass