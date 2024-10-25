from pwn import *
from tqdm import tqdm
import pickle
import networkx as nx

def find_eulerian_cycle(data):
    graph = nx.parse_adjlist(data.splitlines(), nodetype=int)
    eulerian_cycle = list(nx.eulerian_circuit(graph))
    ans = [str(eulerian_cycle[0][0])]
    for el in eulerian_cycle[1:-1]:
        ans.append(str(el[0]))
    ans.append(str(eulerian_cycle[-1][0]))
    ans.append(str(eulerian_cycle[-1][1]))
    return "|".join(ans)+"\n"


def start_client():
    client_socket = remote(input("remote adress: "), int(input("port: ")))

    for i in tqdm(range(300)):
        data = client_socket.recvuntil("\nО".encode())[:-3].decode().replace(":", "")
        client_socket.send(find_eulerian_cycle(data).encode())
        client_socket.recvline().decode()
    print(client_socket.recvline().decode())
    client_socket.close()

if __name__ == "__main__":
    start_client()
