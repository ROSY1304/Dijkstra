from flask import Flask, request, send_from_directory
from flask_cors import CORS
import heapq

app = Flask(__name__, static_folder='static')
CORS(app)

def dijkstra(nodos, distancias, inicio, final):
    # Verificar que distancias sea un diccionario
    if not isinstance(distancias, dict):
        raise ValueError("El parámetro 'distancias' debe ser un diccionario")
    
    dist = {nodo: float('inf') for nodo in nodos}
    dist[inicio] = 0
    prev = {nodo: None for nodo in nodos}
    pq = [(0, inicio)]

    while pq:
        distancia, nodo_actual = heapq.heappop(pq)
        if distancia > dist[nodo_actual]:
            continue

        for vecino, peso in distancias.get(nodo_actual, {}).items():
            nueva_distancia = dist[nodo_actual] + peso
            if nueva_distancia < dist[vecino]:
                dist[vecino] = nueva_distancia
                prev[vecino] = nodo_actual
                heapq.heappush(pq, (nueva_distancia, vecino))

    camino = []
    nodo = final
    while nodo is not None:
        camino.append(nodo)
        nodo = prev[nodo]
    camino.reverse()

    return dist, camino

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/calcular_ruta', methods=['POST'])
def calcular_ruta():
    try:
        data = request.get_json()
        nodos = data["nodos"]
        distancias = data["distancias"]
        inicio = data["inicio"]
        final = data["final"]

        dist, camino = dijkstra(nodos, distancias, inicio, final)
        return {"camino": camino, "distancias": dist}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)