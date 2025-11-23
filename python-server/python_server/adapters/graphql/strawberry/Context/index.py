from dataclasses import dataclass

from punq import Container


@dataclass
class GraphQLContext:
    container: Container
