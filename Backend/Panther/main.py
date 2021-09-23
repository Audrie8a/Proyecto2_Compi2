from Analyzer.Panther import parser
from Environment.Listas import Listas
#from AnalyzerTree.PantherTree import Ast


f = open("./entrada.txt", "r")
input = f.read()
#input="while true   println(true);   return; end;"
parser.parse(input)
#Ast(input)
#Listas.printSimbolos()
Listas.printErrores()
Listas.printSaida()
#Listas.printAst()
#Reportes.Tabla_Errores()