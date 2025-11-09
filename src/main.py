from location import create_location_graph

def main():
    print("\n--- UberUM: Visualização de Grafo Urbano ---\n")
    g = create_location_graph()

    print(f"\nGrafo criado com {len(g.nodes)} nós e {sum(len(e) for e in g.edges.values())} arestas.")
    print("\nOpções de visualização:")
    print("  [S]im  - Mostrar tempo estimado de viagem em cada aresta")
    print("  [N]ão  - Mostrar apenas as distâncias das arestas")
    resposta = input("\nPretende ver o tempo estimado de viagem em cada aresta? [S/N]: ")
    resposta = resposta.strip().lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\nA desenhar o mapa com tempos de viagem (em minutos)...\n")
        g.plot(show_times=True, show_distances=False)
    else:
        print("\nA desenhar o mapa com distâncias (em metros)...\n")
        g.plot(show_times=False, show_distances=True)
    print("\n--- Fim da visualização ---\n")

if __name__ == "__main__":
    main()