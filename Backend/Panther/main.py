from Analyzer.Panther import parser



f = open("./entrada.txt", "r")
input = f.read()
parser.parse(input)