import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDsRating(self):
        ratings = self._model.getRatings()
        for rating in ratings:
            self._view._ddrating1.options.append(
                ft.dropdown.Option(rating)
            )
            self._view._ddrating2.options.append(
                ft.dropdown.Option(rating)
            )


    def handleCreaGrafo(self, e):
        r1 = self._view._ddrating1.value
        r2 = self._view._ddrating2.value

        if not r1 or not r2:
            self._view.txt_result.controls.append(
                ft.Text("Selezionare due ratings dai menù a tendina.", color="red")
            )
            self._view.update_page()
            return

        if r2 < r1:
            self._view.txt_result.controls.append(
                ft.Text("Il rating 1 deve essere minore del rating 2.", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(r1, r2)
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato\nNumero di nodi: {len(nodes)}\nNumero di archi: {len(edges)}")
        )

        heaviest = self._model.getHeaviestEdges()
        self._view.txt_result.controls.append(
            ft.Text(f"I 5 archi più pesanti:")
        )
        for u, v, data in heaviest:
            self._view.txt_result.controls.append(
                ft.Text(f"{u} --> {v} : {data['weight']}")
            )

        compConn, maxComp = self._model.getCompConn()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {len(compConn)} componenti connesse.\nLa più lunga è di {len(maxComp)}:")
        )
        for node in maxComp:
            self._view.txt_result.controls.append(
                ft.Text(node)
            )
        self._view.update_page()

    def handleCammino(self, e):
        self._view.txt_result.controls.clear()

        bestPath = self._model.handlePath()
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino ottimo trovato di lunghezza {len(bestPath)} che attraversa: ")
        )
        for node in bestPath:
            self._view.txt_result.controls.append(
                ft.Text(node)
            )
        self._view.update_page()

