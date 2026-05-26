import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._ratings = []
        self._min_rate = None
        self._max_rate = None
        self._bestPath = []

    def getAllRatings(self):
        self._ratings = DAO.getAllRatings()
        return self._ratings

    def buildGraph(self, min_rate, max_rate):
        self._min_rate = min_rate
        self._max_rate = max_rate
        self._actors = DAO.getAllActors(self._min_rate, self._max_rate)
        self._graph.add_nodes_from(self._actors)
        self._addEdges()
        edges = list(self._graph.edges)
        top5 = edges.sort(key= lambda x: x["weight"])
        cnn = nx.connected_components(self._graph)
        return top5[:4], cnn

    def _addEdges(self):

        movies = DAO.getAllEdges(self._min_rate, self._max_rate)

        """
        dict arch -> key = (a1. a2). val = income
        for m in movies
            for a1 in attori
              fro a2 in attori
                a1 < a2
                    if a1 in m and a2 in m
                        
        """
        for m in movies:

            for a1 in self._graph.nodes:
                    for a2 in self._graph.nodes:

                        if a1.id < a2.id:

                            if a1.movieId == m.id and a2.movieId == m.id:

                                movieI = self.cleanIncome(m.income)

                                if self._graph.has_edge(a1, a2):
                                    self._graph[a1][a2]["weight"] += movieI

                                else:
                                    self._graph.add_edge(a1, a2, weight = movieI)

    def getGraphDetails(self):
        return self._graph.nodes, self._graph.edges

    def cleanIncome(self, income):
        if income[0] == "$":
            realI = int(income[2:])
            return realI
        else:
            return 0

    def trovaCammino(self):

        self._bestPath = []
        self._age = 100

        parziale = []
