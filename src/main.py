from location import create_location_graph

def main():
    g = create_location_graph()

    # Plot
    print("A desenhar o mapa...")
    g.plot()

if __name__ == "__main__":
    main()