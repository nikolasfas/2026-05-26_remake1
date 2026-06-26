import copy
from datetime import datetime

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapA = {}
        self._bestPath = []

    def handlePath(self):

        self._bestPath = []
        parziale = []

        for node in self._graph.nodes:

            currentDate = node.date_of_birth
            parziale.append(node)
            self._ricorsione(parziale, currentDate)
            parziale.pop()

        return self._bestPath

    def _ricorsione(self, parziale, currentDate):

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for node in self._graph.neighbors(parziale[-1]):
            if node not in parziale:

                newDate = node.date_of_birth
                if newDate < currentDate:

                    parziale.append(node)
                    self._ricorsione(parziale, newDate)
                    parziale.pop()



    def getCompConn(self):

        compConn = list(nx.connected_components(self._graph))
        maxComp = max(compConn, key=len)

        return compConn, maxComp

    def getHeaviestEdges(self):

        edges = list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'], reverse=True)
        heaviest = edges[:5]
        return heaviest


    def getRatings(self):
        ratings = DAO.getAllRatings()
        return ratings

    def buildGraph(self, startR, endR):

        actors = DAO.getAllActors(startR, endR)
        for actor in actors:
            self._idMapA[actor.id] = actor
        self._graph.add_nodes_from(actors)

        connections = DAO.getAllConnections(startR, endR)
        for connection in connections:
            a1 = self._idMapA[connection[0]]
            a2 = self._idMapA[connection[1]]
            wgi = int(connection[2][2:])

            if a1 in self._graph.nodes and a2 in self._graph.nodes:

                if self._graph.has_edge(a1, a2):
                    self._graph[a1][a2]['weight'] += wgi
                else:
                    self._graph.add_edge(a1, a2,weight=wgi)

    def getGraphDetails(self):
        nodes = self._graph.nodes
        edges = self._graph.edges
        return nodes, edges



