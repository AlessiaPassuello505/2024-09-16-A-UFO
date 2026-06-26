import copy

from database.DAO import DAO
import networkx as nx

from model.state import State


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapS={}

    def creaGrafo(self,lat,lng,forma):
        self._graph.clear()
        nodi = DAO.getNodi(lat,lng,forma)
        for n in nodi:
            self._idMapS[n.id] = n
            self._graph.add_node(n)

        for i in range(0, len(nodi) - 1):
            for j in range(i + 1, len(nodi)):
                if nodi[i].id in nodi[j].Neighbors or nodi[j].id in nodi[i].Neighbors:
                    self._graph.add_edge(nodi[i], nodi[j], weight=nodi[i].duration + nodi[j].duration)

        allArchi = self._graph.edges(data=True)
        best5 = sorted(allArchi, key=lambda x: x[2]["weight"], reverse=True)
        return best5[:5]

    def get_top5_nodi(self):
        nodes_deg = [(n, self._graph.degree(n)) for n in self._graph.nodes()]
        nodes_deg.sort(key=lambda x: x[1], reverse=True)
        return nodes_deg[0:5]

    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._punteggio_ottimo = 0.0

        for nodo in self._graph.nodes():
            self._ricorsione([nodo], self._calcola_successivi(nodo))
        return self._cammino_ottimo, self._punteggio_ottimo

    def _ricorsione(self, parziale: list[State], successivi: list[State]):
        if len(successivi) == 0:
            score = self._calcola_score(parziale)
            if score > self._punteggio_ottimo:
                self._punteggio_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                parziale.append(nodo)
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._ricorsione(parziale, nuovi_successivi)
                parziale.pop()

    def _calcola_successivi(self, nodo: State) -> list[State]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo
        """
        successivi = self._graph.neighbors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if (s.Population / s.Area) > (nodo.Population / nodo.Area):
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    def _calcola_score(self, cammino: list[State]) -> float:
        """
        Funzione che calcola il punteggio di un cammino.
        """
        score = 0
        for i in range(0, len(cammino) - 1):
            peso = self._graph.get_edge_data(cammino[i], cammino[i + 1])["weight"]
            distanza = cammino[i].distance_HV(cammino[i + 1])
            score += peso / distanza
        return score

    def getEstremi(self):
        return DAO.getEstremi()

    def getForme(self):
        return DAO.getForma()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
