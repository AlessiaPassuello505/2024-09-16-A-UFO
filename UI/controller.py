import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._forma=None




    def fillDDForma(self):
        forme = self._model.getForme()
        formeDDI = list(map(lambda x: ft.dropdown.Option(x, on_click=self._choiceForma), forme))

        self._view.ddshape.options = formeDDI
        self._view.update_page()

    def _choiceForma(self,e):
        self._forma=e.control.data




    def handle_graph(self, e):
        lat = self._view.txt_latitude.value
        lng = self._view.txt_longitude.value
        max_lat, min_lat, max_lng, min_lng = self._model.getEstremi()
        forma=self._view.ddshape.value

        if lat == "" or lng == "" or forma is None:
            self._view.txt_result1.controls.append(ft.Text("Attenzione, inserire valore di lat e lng "))
            self._view.update_page()
            return

        try:
            lat_int = float(lat)
            lng_int = float(lng)
        except ValueError:
            self._view.txt_result1.controls.append("Inserire un valore di lat/lng intero")
            self._view.update_page()
            return
        if lat_int > max_lat or lat_int < min_lat:
            self._view.txt_result1.controls.append(
                ft.Text(f"La latitudine deve avere un valore compreso tra {min_lat} e {max_lat}"))
            self._view.update_page()
        if lng_int > max_lng or lng_int < min_lng:
            self._view.txt_result1.controls.append(
                ft.Text(f"La longitudine deve avere un valore compreso tra {min_lng} e {max_lng}"))
            self._view.update_page()

        top5Archi=self._model.creaGrafo(lat_int,lng_int,forma)
        n, m = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato! ", color="green"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {m}"))

        best5Nodi=self._model.get_top5_nodi()
        self._view.txt_result1.controls.append(ft.Text("I 5 nodi di grado maggiore sono:"))
        for n in best5Nodi:
            self._view.txt_result1.controls.append(ft.Text(f" {n[0]}--> score: {n[1]}"))

        if len(top5Archi) == 0:
            self._view.txt_result1.controls.append(ft.Text("Non ci sono archi di peso maggiore"))
        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono:"))
        for a in top5Archi:
            self._view.txt_result1.controls.append(ft.Text(f'{a[0]} <--> {a[1]} | peso:{a[2]["weight"]}'))
        self._view.update_page()

    def handle_path(self, e):
        if len(self._model._graph.nodes) == 0:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(
                ft.Text("Errore: Devi prima creare il grafo premendo il pulsante 'Crea grafo'!", color="red")
            )
            self._view.update_page()
            return

        self._view.txt_result2.controls.clear()
        path, punteggio = self._model.cammino_ottimo()
        if len(path)<=1:
            self._view.txt_result2.controls.append(ft.Text("Non ho trovato nessun percorso con questi vincoli"))
            self._view.update_page()
            return

        self._view.txt_result2.controls.append(ft.Text(f"Il punteggio del percorso ottimo è {punteggio}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ottimo è costituito da {len(path)} nodi:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p} | densità = {p.Population / p.Area}"))

        self._view.update_page()

