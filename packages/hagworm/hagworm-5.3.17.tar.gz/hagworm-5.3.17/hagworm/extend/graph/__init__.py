# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from typing import List, Dict

from .entity import Vertex, Edge, Tree


class Graph:

    def __init__(self):

        self._vertices = {}

    def __len__(self):

        return len(self._vertices)

    def clear(self):

        for vertex in self._vertices.values():
            vertex._in.clear()
            vertex._out.clear()

        self._vertices.clear()

    def find_vertex(self, id_: str) -> Vertex:

        return self._vertices.get(id_, None)

    def find_vertices(self, ids: List[str]) -> Dict[str, Vertex]:

        return {id_: self._vertices[id_] for id_ in ids if id_ in self._vertices}

    def add_vertex(self, id_: str) -> Vertex:

        if id_ in self._vertices:
            vertex = self._vertices[id_]
        else:
            vertex = self._vertices[id_] = Vertex(id_)

        return vertex

    def add_edge(self, source_id: str, target_id: str) -> Edge:

        source = self.find_vertex(source_id)
        target = self.find_vertex(target_id)

        if source is None or target is None:
            return None

        if source._id == target._id:
            return None

        edge = Edge(source, target)

        # 添加父类
        target._in[source._id] = edge

        # 添加子类
        source._out[target._id] = edge

        return edge

    def del_edge(self, source_id: str, target_id: str):

        # 删除子类
        source = self.find_vertex(source_id)

        if source and target_id in source._out:

            del source._out[target_id]

            if not source._in and not source._out:
                del self._vertices[source_id]

        # 删除父类
        target = self.find_vertex(target_id)

        if target and source_id in target._in:

            del target._in[source_id]

            if not source._in and not source._out:
                del self._vertices[target_id]

    def find_in_edges(self, id_: str) -> List[Edge]:

        vertex = self.find_vertex(id_)

        if vertex is None:
            return None

        return list(vertex._in.values())

    def find_out_edges(self, id_: str) -> List[Edge]:

        vertex = self.find_vertex(id_)

        if vertex is None:
            return None

        return list(vertex._out.values())

    def tree(self, id_: str) -> Tree:

        vertex = self.find_vertex(id_)

        if vertex is None:
            return None

        return Tree(vertex)
