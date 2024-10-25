import socket
import threading
import random
import logging
import sys
import os

import networkx as nx


def create_random_eulerian_graph():
    n = random.randint(4, 20)
    G = nx.Graph()
    G.add_nodes_from(range(n))

    nodes = list(G.nodes)
    random.shuffle(nodes)
    for i in range(n):
        G.add_edge(nodes[i], nodes[(i + 1) % n])

    possible_edges = [(u, v) for u in range(n) for v in range(u + 1, n) if not G.has_edge(u, v)]
    random.shuffle(possible_edges)

    for u, v in possible_edges:
        if random.random() > 0.7:
            G.add_edge(u, v)
        if all(G.degree(node) % 2 == 0 for node in G.nodes):
            break 

    return G

def graph_to_string(G):
    result = []
    for node in G.nodes:
        connections = list(G.neighbors(node))
        result.append(f"{node}: {' '.join(map(str, connections))}")
    return "\n".join(result)


def is_eulerian_cycle(G, cycle):
    return nx.is_eulerian(G) and list(cycle) == list(nx.eulerian_circuit(G))


def handle_client(conn, addr):
    logging.info(f"Клиент {addr} подключился")
    return_flag = True

    try:
        for i in range(300):
            graph = create_random_eulerian_graph()
            while not nx.is_eulerian(graph):
                graph = create_random_eulerian_graph()
            
            graph_str = graph_to_string(graph) + "\n"
            
            conn.send(graph_str.encode())
            conn.send("Ответ: ".encode())

            data = conn.recv(4096).decode()[:-1].split("|")

            data = list(map(int, data))
            if data[0] != data[-1]:
                conn.send("Пакет так и не вернулся в первый компьютер.\nПока!\n".encode())
                conn.close()
                return

            for i in range(1, len(data)):
                now = data[i-1]
                next_edge = data[i]
                if (now, next_edge) in graph.edges(now):
                    graph.remove_edge(next_edge, now)
                else:
                    return_flag = False
                    logging.info(f"Клиент {addr} отправил несуществующее ребро {now}-{next_edge}")
                    conn.send("Ты ввел несуществующее ребро. Пока\n".encode())
                    conn.close()
                    return

            if graph.number_of_edges() != 0:
                logging.info(f"Клиент {addr} не обошел все кабеля в графе")
                conn.send("Пакет не прошел по всем кабелям. ПОКА!\n".encode())
                conn.close()
                return_flag = False
                return
            else:
                conn.send("Молодец, так держать, держи еще задачку!\n".encode())
            
        if return_flag:
            logging.info(f"Клиенту {addr} отправлен флаг")
            conn.send((os.getenv("FLAG")+"\n").encode())
            conn.close()
            logging.info(f"Клиент {addr} отключился")
    except Exception as e:
        logging.warning(f"Сработало исключение {e}: {str(e)}")
        conn.send("Это была хорошая попытка, но она не удалась\nПока!\n".encode())
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9090))
    server_socket.listen(30)
    logging.info("Таск запущен")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
    
    # conn, addr = server_socket.accept()
    # client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    # client_thread.start()
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="ppc.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    start_server()
