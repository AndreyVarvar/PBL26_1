import random
import graphviz

def build_graph(connections: list[tuple[str, str, int]]) -> dict[str, dict[str, int]]:  # bidirectional graph
    graph = {}
    for node1, node2, cost in connections:
        if node1 not in graph:
            graph[node1] = dict()
        if node2 not in graph:
            graph[node2] = dict()

        graph[node1][node2] = cost
        graph[node2][node1] = cost

    return graph


def find_path_BFS(graph: dict[str, dict[str, int]], start: str, end: str) -> list[str] | None:
    if start not in graph or end not in graph:
        return None

    trails = [(start, [start])]  # (node: str, path_to_node: list[str])
    visited = set([start])

    while trails:
        current_node, path = trails.pop(0)

        if current_node == end:
            return path

        for neighbor, _ in graph[current_node].items():
            if neighbor not in visited:  
                visited.update({neighbor})
                new_path = path + [neighbor]
                trails.append((neighbor, new_path))

    return None  # no path was found


def get_path_distance(graph: dict[str, dict[str, int]], path: list[str]):
    total = 0
    for i in range(len(path)-1):
        current_node = path[i]
        next_node = path[i+1]
        total += graph[current_node][next_node]

    return total


def generate_random_campus_paths(buildings_count: int = 20) -> list[tuple[str, str, int]]:
    types_of_buildings = ["Camin", "Facultate", "Biblioteca", "Cantina", "Sala_Sport", "Parc", "Laborator", "Amfiteatru"]
    buildings = []

    for i in range(buildings_count):
        building_type = random.choice(types_of_buildings)
        buildings.append(f"{building_type}_{chr(65+i)}")

    paths = []

    for i in range(len(buildings) - 1):
        distance = random.randint(50, 300)
        paths.append((buildings[i], buildings[i+1], distance))

    for i in range(buildings_count // 3):
        building1 = random.choice(buildings)
        building2 = random.choice(buildings)

        if building1 != building2:
            distance = random.randint(80, 400)
            paths.append((building1, building2, distance))

    return paths

def sketch_graph(name: str, graph: dict[str, dict[str, int]]) -> None:
    plot = graphviz.Graph(name)
    for node in graph.keys():
        plot.node(node, node)
    for node in graph.keys():
        for connection in graph[node].keys():
            if f"\t{connection} -- {node} [label={str(graph[node][connection])}]\n" in plot.body:
                continue
            plot.edge(node, connection, str(graph[node][connection]))
    plot.render(filename=None, view=True)

def get_all_paths_BFS(graph: dict[str, dict[str, int]], start: str, end: str) -> list[list[str]]:
    if start not in graph or end not in graph:
        return []

    trails = [(start, [start])]  # (node: str, path_to_node: list[str])
    paths = []

    while trails:
        current_node, path = trails.pop(0)

        if current_node == end:
            paths.append(path)
            continue

        for neighbor, _ in graph[current_node].items():
            if neighbor not in path:  
                new_path = path + [neighbor]
                trails.append((neighbor, new_path))

    return paths

def find_average_distance_between_vertices(graph: dict[str, dict[str, int]]) -> float:
    number_of_vertices = len(graph.keys())

    return sum([sum(edges.values()) for edges in graph.values()])/(2*number_of_vertices) # we multiply by 2 because we count every edge twice

def main():
    paths = generate_random_campus_paths()
    # Debug info
    # print(paths)
    graph = build_graph(paths)
    sketch_graph("campus", graph)

    average_distance = find_average_distance_between_vertices(graph)
    print(f"The average distance between adjacent buildings is: {average_distance}")


    start = random.choice(paths)[0]
    end = random.choice(paths)[1]
    print(f"Start: {start}, end: {end}")

    path = find_path_BFS(graph, start, end)
    print(f"Obtained path: {path}")

    if path is not None:
        print(f"Distance to destination: {get_path_distance(graph, path)}")

    paths = get_all_paths_BFS(graph, start, end)

    if len(paths):
        print("All possible paths:")
        for path in paths:
            print(path, end="\n")
    else:
        print("No paths found D:")

if __name__ == "__main__":
    main()
