from typing import Iterable

from solver import solve
from pizza_types import Pizza, Client


def read_input(problem: str) -> Iterable[Client]:
    with open(f"./input/{problem}.in.txt", "r") as f:
        lines = f.readlines()

    num_clients = int(lines[0])
    id = 0
    while id < num_clients:
        yield Client(
            id,
            likes=set(lines[id * 2 + 1].split()[1:]),
            dislikes=set(lines[id * 2 + 2].split()[1:]),
        )
        id = id + 1


def write_output(problem: str, solution: Pizza):
    with open(f"./output/{problem}.out.txt", "w") as f:
        f.write(solution.to_string())


def score(clients: Iterable[Client], pizza: Pizza) -> int:
    score = 0
    for client in clients:
        if pizza.ingredients.issuperset(client.likes) and pizza.ingredients.isdisjoint(
            client.dislikes
        ):
            score = score + 1
    return score


if __name__ == "__main__":
    for problem in [
        "a_an_example",
        "b_basic",
        "c_coarse",
        "d_difficult",
        "e_elaborate",
    ]:
        clients = list(read_input(problem))
        solution_pizza = solve(clients)
        print(f"{problem}: {score(clients, solution_pizza)}")
        write_output(problem, solution_pizza)
