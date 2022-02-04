from os import error
from Environment.Listas import Listas

class Node:

    def __init__(self, value: str) -> None:
        self.value = value
        self.child = []
        self.contador = 0
        self.grafo = ""

    def insertChild(self,temp):
        self.child.append(temp)


    def getGraphAST(self) -> str:

        self.grafo = "digraph Tree{ \n"
        Listas.saveAst("digraph Tree{ \n")
        print("digraph Tree{ \n")
        self.grafo += "nodo0[label=\"" + str(self.value) + "\"];\n"
        print("nodo0[label=\"" + str(self.value) + "\"];\n")
        Listas.saveAst( "nodo0[label=\"" + str(self.value) + "\"];\n")
        print("nodo0[label=\"" + str(self.value) + "\"];\n")
        self.contador = 1
        self.graphAST("nodo0", self)
        self.grafo += "}"
        Listas.saveAst("}")
        print("}")
        return self.grafo
    

    def graphAST(self, padre: str, temp):
        try:
            for hijo in temp.child:
                nameChild: str = "nodo" + str(self.contador)
                self.grafo += nameChild + "[label=\"" + str(hijo.value) + "\"];\n"
                Listas.saveAst( nameChild + "[label=\"" + str(hijo.value) + "\"];\n")
                print(nameChild + "[label=\"" + str(hijo.value) + "\"];\n")
                self.grafo += padre + "->" + nameChild + ";\n"
                Listas.saveAst( padre + "->" + nameChild + ";\n")
                print( padre + "->" + nameChild + ";\n")
                self.contador = self.contador + 1
                self.graphAST(nameChild, hijo)
            
            return
        except(error):
            print(error)
            return "error"