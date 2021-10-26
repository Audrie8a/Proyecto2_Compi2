from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

def DivisionCero(self, generador,temp,izq, der):
    resultado=generador.newLabel()
    generador.code.append("\nif("+str(der)+"!=0){goto "+resultado+";}")    
    generador.code.append("fmt.Printf(\"%c\", 77); //M ")
    generador.code.append("fmt.Printf(\"%c\", 97); //a ")
    generador.code.append("fmt.Printf(\"%c\", 116); //t ")
    generador.code.append("fmt.Printf(\"%c\", 104); //h ")
    generador.code.append("fmt.Printf(\"%c\", 69); //E ")
    generador.code.append("fmt.Printf(\"%c\", 114); //r ")
    generador.code.append("fmt.Printf(\"%c\", 114); //r ")
    generador.code.append("fmt.Printf(\"%c\", 111); //o ")
    generador.code.append("fmt.Printf(\"%c\", 114); //r ")
    generador.code.append(temp+"=0; ")
    salida=generador.newLabel()
    generador.code.append("goto "+salida+"; ")
    generador.code.append(resultado+": ")
    if(der==str(0) and izq[0]!="t"):
        generador.code.append("//"+temp+"="+str(izq)+"/"+str(der)+";")
    else:
        generador.addExpression(temp,izq,der,"/")
    generador.code.append(salida+": ")
    generador.code.append("\tfmt.Printf(\"%c\", 10); //Salto ")

    
    
