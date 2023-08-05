# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from typing import List, Dict


class Vertex:

    __slots__ = [r'_id', r'_in', r'_out']

    def __init__(self, id_: str):

        self._id = id_

        self._in = {}
        self._out = {}

    def __repr__(self):
        return f'<Vertex: {self._id}>'

    @property
    def id(self):
        return self._id


class Edge:

    __slots__ = [r'_in', r'_out']

    def __init__(self, source: Vertex, target: Vertex):

        if source._id == target._id:
            raise Exception(f'vertices like same: {source._id} => {target._id}')

        # 父类
        self._in = source

        # 子类
        self._out = target


class Tree:

    def __init__(self, vertex: Vertex):

        self._steps = [[vertex]]
        self._nodes = {}

    @property
    def steps(self) -> List[List[str]]:

        return self._steps

    @property
    def nodes(self) -> Dict[str, List[str]]:

        return self._nodes

    def find_in(self) -> Dict[str, List[str]]:

        nodes = {}
        vertices = []

        for vertex in self._steps[-1]:

            _vertices = [v._in for v in vertex._in.values() if v._in._id not in self._nodes]

            if _vertices:
                vertices.extend(_vertices)
                nodes[vertex._id] = [v._id for v in _vertices]

        if nodes and vertices:
            self._nodes.update(nodes)
            self._steps.append(vertices)

        return nodes

    def find_out(self) -> Dict[str, List[str]]:

        nodes = {}
        vertices = []

        for vertex in self._steps[-1]:

            _vertices = [v._out for v in vertex._out.values() if v._out._id not in self._nodes]

            if _vertices:
                vertices.extend(_vertices)
                nodes[vertex._id] = [v._id for v in _vertices]

        if nodes and vertices:
            self._nodes.update(nodes)
            self._steps.append(vertices)

        return nodes


