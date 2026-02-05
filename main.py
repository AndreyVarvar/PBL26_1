import random
import graphviz
from colorama import init, Fore

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

def find_central_building(graph: dict[str, dict[str, int]]) -> str:
    current_min_longest_path = float("inf")

    for start_building in graph:
        max_path = 0
        for end_building in graph: # find the longest path
            path = find_path_BFS(graph, start_building, end_building)
            if path is None: # no path - skip
                continue
            distance = len(path) - 1
            max_path = max(max_path, distance)

        # the building is central if its longest path is the smallest
        if max_path < current_min_longest_path: 
            central_building = start_building
            current_min_longest_path = max_path

    return central_building 
        

def get_path_distance(graph: dict[str, dict[str, int]], path: list[str]):
    total = 0
    for i in range(len(path)-1):
        current_node = path[i]
        next_node = path[i+1]
        total += graph[current_node][next_node]

    return total


def generate_random_campus_paths(buildings_count: int = 20) -> list[tuple[str, str, int]]:
    types_of_buildings = ["Camin", "Facultate", "Biblioteca", "Cantina", "Sala_Sport", "Parc", "Laborator", "Amfiteatru"]
    buildings = ["Camin_A"]

    for i in range(buildings_count):
        building_type = random.choice(types_of_buildings)
        buildings.append(f"{building_type}_{chr(67+i)}")  # GET OUT OF MY HEAD GET OUT OF MY HEAD GET OUT OF MY HEAD GET OUT OF MY HEAD

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

    return paths, buildings

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

def get_longest_path(graph: dict[str, dict[str, int]], start: str):
    if start not in graph:
        return []

    trails = [(start, 0, [start])]
    longest_path = [start]
    longest_length = 0 # Boy am I good at this

    while trails:
        current_node, length, path = trails.pop(0)

        for neighbor, distance in graph[current_node].items():
            if neighbor not in path:
                new_path = path + [neighbor]
                trails.append((neighbor, length + distance, new_path))

                if len(new_path) > len(longest_path):
                    longest_path = new_path
                    longest_length = length + distance

    return longest_path, longest_length

def get_reachable_from_camin_a(graph: dict[str: dict[str: int]], start_node: str):
    reachable = set()
    step_1_neighbors = graph.get(start_node)
    for neighbor in step_1_neighbors:
        if neighbor != start_node:
            reachable.add(neighbor)
            step_2_neighbors = graph.get(neighbor)
            for next_neighbor in step_2_neighbors:
                if next_neighbor != start_node:
                    reachable.add(next_neighbor)

    return list(reachable)

def format_path(path: list[str]) -> str:
    formatted = ""
    for building in path:
        formatted += building

        if building != path[-1]:
            formatted += " → "
    
    return formatted


def main():
    paths, buildings = generate_random_campus_paths()
    graph = build_graph(paths)

    start = random.choice(paths)[0]
    end = random.choice(paths)[1]  # chance of getting start = end is VERY low (but not 0)


    options = [
        "help -- print this menu",
        "path -- display path between `start` and `end`",
        "graph -- visualize the graph (in a PDF file)",
        "longest_path -- display the longest path from `start`",
        "average_distance -- display average distance between adjacent buildings",
        "all_paths -- display all possible paths from `start` to `end`",
        "dist_2 -- display all buildings reachable in 2 steps from `start`",
        "central_building -- display the central building",
        "change_points -- change the initial position and destination buildings",
        "quit -- quit the program"
    ]

    user_option = ""
    while user_option != "quit":
        user_option = input("Enter command (enter `help` to list all possible commands): ")

        if user_option == "quit":
            break

        elif user_option == "help":
            print("Here are all the options:")
            for i, option in enumerate(options):
                option = option.replace("start", f"{Fore.RED}{start}{Fore.WHITE}")
                option = option.replace("end", f"{Fore.RED}{end}{Fore.WHITE}")
                print(f"  {i+1}) {option}")

        elif user_option == "path":
            path = find_path_BFS(graph, start, end)
            print(f"{Fore.LIGHTBLUE_EX}Path from {Fore.RED}{start} {Fore.LIGHTBLUE_EX}to {Fore.RED}{end} {Fore.LIGHTBLUE_EX}is: {Fore.WHITE}{format_path(path)}")
            if path is not None:
                distance = get_path_distance(graph, path)
                print(f"{Fore.LIGHTCYAN_EX}Distance to destination is {Fore.GREEN}{distance} meters")

        elif user_option == "graph":
            sketch_graph("campus", graph)

        elif user_option == "longest_path":
            longest_path, length = get_longest_path(graph, start)
            print(f"{Fore.LIGHTCYAN_EX}The longest path starting at {Fore.RED}{start} {Fore.LIGHTCYAN_EX}is: {Fore.WHITE}{format_path(longest_path)}")
            print(f"{Fore.BLUE}Its length is {Fore.GREEN}{length} meters{Fore.WHITE}.")

        elif user_option == "average_distance":
            average_distance = find_average_distance_between_vertices(graph)
            print(f"The average distance between adjacent buildings is {Fore.GREEN}{average_distance:0.3f} meters")

        elif user_option == "all_paths":
            paths = get_all_paths_BFS(graph, start, end)
            if len(paths):
                print(f"{Fore.BLUE}All possible paths ({Fore.GREEN}{len(paths)} {Fore.BLUE}total):")
                for i, path in enumerate(paths):
                    print(f"{Fore.GREEN}{i+1}) {Fore.WHITE}{format_path(path)}", end="\n")
            else:
                print(f"{Fore.RED}No paths found D:")
        
        elif user_option == "dist_2":
            print(f"{Fore.LIGHTCYAN_EX}Destinations reachable from {Fore.YELLOW}Camin_A {Fore.LIGHTCYAN_EX}in {Fore.GREEN}2 {Fore.LIGHTCYAN_EX}steps are:")
            reachable_by_2_steps = get_reachable_from_camin_a(graph, "Camin_A")
            print(", ".join(reachable_by_2_steps))

        elif user_option == "central_building":
            central_building = find_central_building(graph)
            print(f"{Fore.BLUE}The central building in the campus is: {Fore.MAGENTA}{central_building}")
        
        elif user_option == "change_points":
            print("Available buildings: " + ", ".join(buildings))
            new_start = ""
            while new_start not in buildings:
                new_start = input("Choose one of the starting buildings (type its name): ")
                if new_start not in buildings:
                    print("Invalid choice.")

            new_end = ""
            while new_end not in buildings:
                new_end = input("Choose one of the destination buildings (type its name): ")
                if new_end not in buildings:
                    print("Invalid choice.")
                
            start = new_start
            end = new_end

        else:
            print(f"{Fore.RED}Invalid option.")
        
        print()            


if __name__ == "__main__":
    init(autoreset=True)
    main()
