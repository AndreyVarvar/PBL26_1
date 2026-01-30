import random

def build_graph(connections: list[tuple[str, str, int]]) -> dict[str: list]:  # bidirectional graph
    graph = {}
    for node1, node2, cost in connections:
        if node1 not in graph:
            graph[node1] = dict()
        if node2 not in graph:
            graph[node2] = dict()

        graph[node1][node2] = cost
        graph[node2][node1] = cost
    
    return graph


def find_path_BFS(graph: dict[str: dict[str: int]], start: str, end: str) -> list[str] | None:
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


def get_path_distance(graph: dict[str: dict[str: int]], path: list[str]):
    total = 0
    for i in range(len(path)-1):
        current_node = path[i]
        next_node = path[i+1]
        total += graph[current_node][next_node]
    
    return total


def generate_random_campus_paths(buildings_count=20):
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


def main():
    paths = [
        ("Camin_A", "Cantina", 150),
        ("Cantina", "Facultate_Info", 200),
        ("Camin_A", "Biblioteca", 300),
        ("Biblioteca", "Facultate_Info", 100),
        ("Facultate_Info", "Sala_Sport", 250),
        ("Cantina", "Sala_Sport", 180)
    ]
    paths = generate_random_campus_paths()
    print(paths)
    
    graph = build_graph(paths)
    start = random.choice(paths)[0]
    end = random.choice(paths)[1]
    print(f"Start: {start}, end: {end}")
    path = find_path_BFS(graph, start, end)
    print(f"Obtained path: {path}")

    if path is not None:
        print(f"Distance to destination: {get_path_distance(graph, path)}")


if __name__ == "__main__":
    main()