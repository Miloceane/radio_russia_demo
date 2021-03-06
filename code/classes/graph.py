import csv

from .node import Node


class Graph():
    def __init__(self, source_file, geo_json=None):
        self.nodes = self.load_nodes(source_file)
        self.load_neighbours(source_file)

    def load_nodes(self, source_file):
        """
        Load all the nodes into the graph.
        """
        nodes = {}
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                nodes[row['id']] = Node(row['id'], row['id'])

        return nodes

    def load_neighbours(self, source_file):
        """
        Load all the neighbours into the loaded nodes.
        """
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                neighbours = []

                for neighbour in row['neighbours'].split(','):
                    # Only add if the result is not an empty string
                    if neighbour.strip('[] ') != '':
                        neighbours.append(neighbour.strip('[] '))

                node_id = row['id']

                # Add the neighbours to the correct node
                for neighbour in neighbours:
                    neighbour = self.nodes[neighbour]
                    self.nodes[node_id].add_neighbour(neighbour)

    def get_violations(self):
        """
        Returns the ids of all nodes that have a neighbour with the same value.
        """
        violations = []

        for node in self.nodes.values():
            if not node.is_valid():
                violations.append(node)

        return violations

    def is_solution(self):
        """
        Returns True if each node in the graph is assigned a value.
        False otherwise.
        """
        for node in self.nodes.values():
            if not node.has_value():
                return False

        return True

    def calculate_value(self):
        """
        Returns the sum of the values of all nodes.
        """
        value = 0
        for node in self.nodes.values():
            value += node.get_value().value

        return value

    def get_empty_node(self):
        """
        Returns the first empty node.
        """
        for node in self.nodes.values():
            if not node.has_value():
                return node

        return None
