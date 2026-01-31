import flet as ft
from UI.view import View
from model.model import Model
from UI.alert import AlertManager

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.soglia=None
        self.album_selezionato=None
        self._alert_manager = AlertManager(self._view.page)


    def take_data(self):


        self._model.take_nodi()
        self._model.take_archi()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO

        self.take_data()

        valore_input = self._view.txt_durata.value

        try:
            self.soglia = int(valore_input)
        except (ValueError, TypeError):
            # Se l'utente ha lasciato vuoto o scritto lettere, appare l'alert
            self._view.show_alert("Errore: Inserire un numero intero valido per la durata.")
            return

        self._model.crea_grafo(self.soglia)


        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(
                                                         f'Numero di nodi:{self._model.G.number_of_nodes()}\n'
                                                         f'Numero di archi:{self._model.G.number_of_edges()}\n'))


        self._view.dd_album.options = [ft.dropdown.Option(key=s.album_id, text=s.title) for s in self._model.dizionario_nodi_creati.values()]
        self._view.dd_album.update()

        self._view.page.update()





    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO

        self.album_selezionato=int(self._view.dd_album.value)




    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO



        if self._model.G.number_of_nodes() == 0:
            self._alert_manager.show_alert("Il grafo è vuoto! Crea prima il grafo.")
            return

        if self.album_selezionato is None:
            self._alert_manager.show_alert("Seleziona un album dal menu a tendina.")
            return


        try:
            dimensione, durata = self._model.trova_dimensione_componente(self.album_selezionato)

            self._view.lista_visualizzazione_2.controls.clear()
            self._view.lista_visualizzazione_2.controls.append(ft.Text(
                f'Dimensioni componente: {dimensione}\n'
                f'Durata totale: {durata}\n'))
            self._view.page.update()

        except KeyError:
            self._alert_manager.show_alert("Errore: l'album selezionato non è presente nel grafo.")

        self._view.page.update()



    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO


        try:
            durata=int(self._view.txt_durata_totale.value)
        except (ValueError, TypeError):
            self._view.show_alert('Inserire un valore numerico')


        a1=self._model.dizionario_nodi_creati[self.album_selezionato]

        best_path,best_durata=self._model.get_best_path(durata,a1)

        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Set trovato ({len(best_path)} album, durata {best_durata})\n"))
        for p in best_path:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"-{p} ({p.time_album})"))

        self._view.update()