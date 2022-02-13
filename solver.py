from __future__ import annotations
from ortools.sat.python import cp_model

from typing import Iterable, List, Set

from pizza_types import Pizza, Client


def solve(clients: List[Client]) -> Pizza:
    """Solve assignment problem for given group of workers."""
    all_ingredients: Set[str] = set()
    for client in clients:
        all_ingredients = all_ingredients.union(client.likes)
        all_ingredients = all_ingredients.union(client.dislikes)

    # Data
    all_ingredients = list(all_ingredients)
    num_ingredients = len(all_ingredients)
    num_clients = len(clients)

    # Solver
    # Create the mip solver with the SCIP backend.
    model = cp_model.CpModel()

    # Variables
    # x[i] is a 0-1 variable, which will be 1
    # if ingredient i is on the pizza
    x = []
    x_inv = []
    for i in range(num_ingredients):
        x.append(model.NewBoolVar(all_ingredients[i]))
        x_inv.append(model.NewBoolVar("inv_" + all_ingredients[i]))

    satisfy_client = []
    for j in range(num_clients):
        satisfy_client.append(model.NewBoolVar(f"client_{j}"))

    # Constraints
    for i in range(num_ingredients):
        model.AddBoolXOr([x[i], x_inv[i]])

    for j, client in enumerate(clients):
        variables = []
        for i, ingredient in enumerate(all_ingredients):
            if ingredient in client.likes:
                variables.append(x[i])
            if ingredient in client.dislikes:
                variables.append(x_inv[i])
        model.AddBoolAnd(variables).OnlyEnforceIf(satisfy_client[j])

    # Objective
    model.Maximize(sum(satisfy_client))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model, solution_callback=cp_model.ObjectiveSolutionPrinter())

    # Print solution.
    pizza_ingredients: Set[str] = set()
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Solution is {'optimal' if status == cp_model.OPTIMAL else 'feasible'}")
        print("Score = ", solver.ObjectiveValue(), "\n")
        for i in range(num_ingredients):
            if solver.Value(x[i]) == 1:
                pizza_ingredients.add(all_ingredients[i])

    return Pizza(pizza_ingredients)
