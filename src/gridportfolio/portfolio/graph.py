"""
Portfolio relationship graph.

This module provides the lightweight graph representation used by
GridPortfolio to connect assets, markets, contracts, risks, initiatives,
decisions, and actions.

The graph is intentionally implemented with plain Python objects rather
than requiring a graph database. A graph database can be introduced later
without changing the core domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GraphNode:
    """
    A node in the portfolio relationship graph.

    Nodes represent entities such as:

    - assets
    - markets
    - contracts
    - risks
    - initiatives
    - decisions
    - actions
    - organizations
    - observations
    """

    node_id: str
    node_type: str
    label: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    """
    A directed relationship between two portfolio graph nodes.

    Example:

        Asset A
            -- exposed_to -->
        Market X
    """

    source_id: str
    target_id: str
    relationship_type: str
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PortfolioGraph:
    """
    Lightweight in-memory representation of the portfolio graph.

    The graph provides the connective tissue between functional domains.

    Example:

        Asset
          ↓
        Market
          ↓
        Risk
          ↓
        Initiative
          ↓
        Decision
          ↓
        Action
    """

    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)

    def add_node(
        self,
        node: GraphNode,
    ) -> GraphNode:
        """Add or replace a node in the graph."""

        self.nodes[node.node_id] = node
        return node

    def add_edge(
        self,
        edge: GraphEdge,
    ) -> GraphEdge:
        """Add a relationship between two nodes."""

        self.edges.append(edge)
        return edge

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:
        """Return a node by ID."""

        return self.nodes.get(node_id)

    def get_edges_from(
        self,
        node_id: str,
    ) -> list[GraphEdge]:
        """Return all outgoing relationships from a node."""

        return [
            edge
            for edge in self.edges
            if edge.source_id == node_id
        ]

    def get_edges_to(
        self,
        node_id: str,
    ) -> list[GraphEdge]:
        """Return all incoming relationships to a node."""

        return [
            edge
            for edge in self.edges
            if edge.target_id == node_id
        ]

    def neighbors(
        self,
        node_id: str,
    ) -> list[GraphNode]:
        """
        Return nodes directly connected to a given node.

        Both incoming and outgoing relationships are considered.
        """

        connected_ids: set[str] = set()

        for edge in self.edges:
            if edge.source_id == node_id:
                connected_ids.add(edge.target_id)

            if edge.target_id == node_id:
                connected_ids.add(edge.source_id)

        return [
            self.nodes[node_id]
            for node_id in connected_ids
            if node_id in self.nodes
        ]

    def nodes_by_type(
        self,
        node_type: str,
    ) -> list[GraphNode]:
        """Return all nodes of a given type."""

        return [
            node
            for node in self.nodes.values()
            if node.node_type == node_type
        ]

    def edges_by_type(
        self,
        relationship_type: str,
    ) -> list[GraphEdge]:
        """Return all edges of a given relationship type."""

        return [
            edge
            for edge in self.edges
            if edge.relationship_type == relationship_type
        ]

    def degree(
        self,
        node_id: str,
    ) -> int:
        """Return the total number of relationships touching a node."""

        return sum(
            1
            for edge in self.edges
            if edge.source_id == node_id
            or edge.target_id == node_id
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the graph into a simple dictionary."""

        return {
            "nodes": [
                {
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "label": node.label,
                    "metadata": node.metadata,
                }
                for node in self.nodes.values()
            ],
            "edges": [
                {
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "relationship_type": edge.relationship_type,
                    "weight": edge.weight,
                    "metadata": edge.metadata,
                }
                for edge in self.edges
            ],
        }


def build_portfolio_graph(
    nodes: list[GraphNode] | None = None,
    edges: list[GraphEdge] | None = None,
) -> PortfolioGraph:
    """
    Build a portfolio graph from nodes and relationships.

    This helper keeps graph construction simple for downstream agents
    and pipeline components.
    """

    graph = PortfolioGraph()

    for node in nodes or []:
        graph.add_node(node)

    for edge in edges or []:
        graph.add_edge(edge)

    return graph