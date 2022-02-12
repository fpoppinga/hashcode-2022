from __future__ import annotations
from ctypes import Union
import random
from typing import List, Set
from xmlrpc.client import boolean

from pizza_types import Pizza, Client


class Group:
    clients: List[Client]
    likes: Set[str]
    dislikes: Set[str]

    def __init__(self) -> None:
        self.clients = []
        self.likes = set()
        self.dislikes = set()

    def add(self, other):
        self.clients.append(other)
        self.likes = self.likes.union(other.likes)
        self.dislikes = self.dislikes.union(other.dislikes)

    def is_compatible(self, other) -> bool:
        return other.dislikes.isdisjoint(self.likes) and other.likes.isdisjoint(
            self.dislikes
        )

    def split_compatible(self, client: Client) -> Group:
        new_group = Group()
        new_group.add(client)
        for existing_client in self.clients:
            if new_group.is_compatible(existing_client):
                new_group.add(existing_client)

        return new_group


NUM_SEEDS = 100
DRAW_MULTIPLIER = 100
SUPER_GROUP_ROUNDS = 10


def solve(clients: List[Client]) -> Pizza:
    seeds: List[Client] = random.sample(clients, k=min(NUM_SEEDS, len(clients)))

    num_draws = int(DRAW_MULTIPLIER * len(clients) / NUM_SEEDS)
    groups = create_groups(
        random.choices(clients, k=min(num_draws, len(clients))), seeds
    )

    super_groups = groups
    for i in range(SUPER_GROUP_ROUNDS):
        super_groups = create_groups(super_groups, super_groups)

    best_group = max(super_groups, key=lambda g: len(g.clients))
    return Pizza(best_group.likes)


def create_groups(clients, seeds):
    groups: List[Group] = []
    for seed in seeds:
        group = Group()
        group.add(seed)
        for client in clients:
            if group.is_compatible(client):
                group.add(client)

        groups.append(group)
    return groups
