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
                ft.dropdown.Option(float(r))
            )
            self._view._ddrating2.options.append(
                ft.dropdown.Option(float(r))
            )


    def handleCreaGrafo(self, e):
        min_value = self._view._ddrating1.value
        max_value = self._view._ddrating2.value

        if min_value >= max_value:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione selezionare un valore massimo maggiore di quello minimo!", color="red")
            )
            self._view.update_page()
            return

        top5, conn = self._model.buildGraph(min_value, max_value)
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato:\n Numero di nodi: {len(nodes)}\n Numero di archi: {len(edges)} ")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Top 5 archi:")
        )
        for c in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"Grafo correttamente creato:\n Numero di nodi: {len(nodes)}\n Numero di archi: {len(edges)} ")
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {len(conn)} componenti connesse")
        )
        self._view.update_page()

    def handleCammino(self, e):
        pass