from src.interprete.ast.TreeAST import TreeAST
from src.interprete.grafo.Grafo import Grafo


class GrafoAST:
    def __init__(self, tree_ast):
        self.tree: TreeAST = tree_ast

    def get_graph(self):
        graph_str = 'digraph G{\n\n'
        graph_str += 'nodo0[label="AST"];\n'
        grafo = Grafo(1, graph_str)
        # self.tree.
        grafo.grafo += '\n }'
        return grafo.grafo