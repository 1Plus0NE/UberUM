from database import load_dataset

def assign_request(request, vehicles, current_time, search_algorithm, db):
    # search_algorithm: função que recebe (graph, origem, destino) e retorna o caminho/custo

    available_vehicles = [v for v in vehicles if v.is_available(current_time)]
    if not available_vehicles:
        return None

    # Encontra o veículo com menor custo usando o algoritmo de procura
    best_vehicle = None
    best_cost = float('inf')
    for v in available_vehicles:
        cost = search_algorithm(v.position, request['origin'], db.graph)
        if cost < best_cost:
            best_cost = cost
            best_vehicle = v

    if best_vehicle:
        best_vehicle.assign(request, current_time)
    return best_vehicle


def run_simulation():
    current_time = 8 * 60  # 8h00 em minutos
    end_time = 20 * 60     # 20h00 em minutos

    requests = load_requests()
    taxis = initialize_taxis()

    while current_time < end_time:
        new_requests = [r for r in requests if r.time == current_time]
        for req in new_requests:
            assign_request(req, taxis)
        update_taxis(taxis, current_time)
        #log_metrics(taxis, current_time)
        current_time += 1

if __name__ == "__main__":
    run_simulation()


def main():
    print("\n--- UberUM: Visualização de Grafo Urbano ---\n")
    db = load_dataset("../data/dataset.json")

    print(f"\nGrafo criado com {len(db.graph.nodes)} nós e {sum(len(e) for e in db.graph.edges.values())} arestas.")
    print("\nOpções de visualização:")
    print("  [S]im  - Mostrar tempo estimado de viagem em cada aresta")
    print("  [N]ão  - Mostrar apenas as distâncias das arestas")
    resposta = input("\nPretende ver o tempo estimado de viagem em cada aresta? [S/N]: ")
    resposta = resposta.strip().lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\nA desenhar o mapa com tempos de viagem (em minutos)...\n")
        db.graph.plot(show_times=True, show_distances=False)
    else:
        print("\nA desenhar o mapa com distâncias (em metros)...\n")
        db.graph.plot(show_times=False, show_distances=True)
    print("\n--- Fim da visualização ---\n")

    db.list_vehicles()

if __name__ == "__main__":
    main()