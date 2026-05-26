import copy
from datetime import datetime

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._ratings = []
        self._min_rate = None
        self._max_rate = None
        self._actors = []
        self._bestPath = []
        self._idMapActors = {}

    def getAllRatings(self):
        self._ratings = DAO.getAllRatings()
        return self._ratings

    def buildGraph(self, min_rate, max_rate):
        self._min_rate = min_rate
        self._max_rate = max_rate
        self._actors = DAO.getAllActors(self._min_rate, self._max_rate)

        for a in self._actors:
            self._idMapActors[a.id] = a

        self._graph.add_nodes_from(self._actors)
        self._addEdges()
        edges = list(self._graph.edges(data=True))
        edges.sort(key= lambda x: x[2]["weight"], reverse = True)
        top5 = edges[:5]
        cnn = list(nx.connected_components(self._graph))
        biggest = max(nx.connected_components(self._graph), key = len)
        return top5, cnn, biggest

    def _addEdges(self):

        edges = DAO.getAllEdges(self._min_rate, self._max_rate)

        """
        dict arch -> key = (a1. a2). val = income
        for m in movies
            for a1 in attori
              fro a2 in attori
                a1 < a2
                    if a1 in m and a2 in m
                        
        """
        for e in edges:

            a1 = self._idMapActors[e["a1"]]
            a2 = self._idMapActors[e["a2"]]
            income = self._cleanIncome(e["income"])

            if self._graph.has_edge(a1, a2):
                self._graph[a1][a2]["weight"] += income

            else:
                self._graph.add_edge(a1, a2, weight = income)

    def getGraphDetails(self):
        return self._graph.nodes, self._graph.edges

    def _cleanIncome(self, income):
        if income[0] == "$":
            realI = int(income[2:])
            return realI
        else:
            return 0

    def trovaCammino(self):

        self._bestPath = []

        parziale = []

        for n in self._graph.nodes:
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath


    def _ricorsione(self, parziale):
        attivo = parziale[-1]

        # Condizione terminale: se la mia soluzione parziale ha trovato più soluzione della migliore
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph.neighbors(attivo):
            # Cammino semplice -> non passo dallo stesso nodo più di una volta sola
            if n not in parziale:

                if n.date_of_birth > attivo.date_of_birth:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()


