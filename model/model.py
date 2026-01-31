
from database.dao import DAO
import networkx as nx




class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.lista_archi=[]
        self.dizionario_nodi_creati={}
        self.nodi_map = {}

    def take_nodi(self):

        self.nodi_map = DAO.query_album()

    def take_archi(self):

        self.lista_archi = DAO.query_archi()



    def crea_grafo(self,soglia):

        self.G.clear()
        id_album_adatti=[]

        for n in self.nodi_map.values():
            if n.time_album>=int(soglia):
                self.G.add_node(n)
                self.dizionario_nodi_creati[n.album_id]=n
                id_album_adatti.append(n.album_id)

        archi_adatti=[]

        for a in self.lista_archi:
            if a.album_id in id_album_adatti:
                archi_adatti.append(a)



        for a1 in archi_adatti:
            for a2 in archi_adatti:

                print(a1,a2)

                if a1.album_id!=a2.album_id and a1.playlist_id==a2.playlist_id :
                    nodo1=self.nodi_map[a1.album_id]
                    nodo2=self.nodi_map[a2.album_id]
                    self.G.add_edge(nodo1,nodo2)



    def trova_dimensione_componente(self,ID):


        nodo_partenza=self.dizionario_nodi_creati[ID]

        componente_nodi = nx.node_connected_component(self.G, nodo_partenza)

        durata_totale=0

        for n in componente_nodi:
            durata=n.time_album
            durata_totale+=durata

        return len(componente_nodi),durata_totale



    def get_best_path(self,durata_tot,a1):
        self.best_path = []
        self.durata_finale=0

        parziale = [a1]
        durata_corrente=a1.time_album
        self._ricorsione(parziale,durata_corrente,durata_tot)
        return self.best_path,self.durata_finale

    def _ricorsione(self, parziale,durata_corrente,durata_tot):
        if durata_corrente<=durata_tot:
            if len(parziale)>len(self.best_path):
                self.best_path=parziale.copy()
                self.durata_finale=durata_corrente


        for n in self.G.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                durata_corrente += n.time_album
                self._ricorsione(parziale,durata_corrente,durata_tot)
                parziale.pop()


