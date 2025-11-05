from graph.graph import Graph 
from graph.position import Position  
import osmnx as ox

def create_location_graph(place_name="Gualtar, Braga, Portugal"): # mudar depois recebendo um json com a location
    """
    Cria um grafo da rede viária de uma dada localização, usando coordenadas projetadas (em metros).
    O grafo é convertido para a estrutura definida Graph() com nós e arestas.
    """

    print(f"A carregar mapa de: {place_name}")

    # Obtem o grafo rodoviário a partir do OpenStreetMap
    G_osm = ox.graph_from_place(place_name, network_type="drive")

    # Projeta o grafo para coordenadas métricas, i.e, converte latitude/longitude para x, y em metros
    G_proj = ox.project_graph(G_osm)

    # Converte para GeoDataFrames (para aceder facilmente aos dados dos nós e arestas)
    nodes, edges = ox.graph_to_gdfs(G_proj)

    graph = Graph()

    # Adiciona os nós
    for osm_id, data in nodes.iterrows():
        graph.add_node(data['x'], data['y'], osm_id=osm_id)

    # Adiciona as arestas
    for (u, v, key), edge in edges.iterrows():
        if u in graph.osm_to_internal and v in graph.osm_to_internal:
            id_u = graph.osm_to_internal[u]
            id_v = graph.osm_to_internal[v]
            length = edge.get("length", None)
            graph.add_edge(id_u, id_v, distance=length)
    
    print(f"Grafo criado com {len(graph.nodes)} nós e {sum(len(e) for e in graph.edges.values())} arestas.")
    return graph