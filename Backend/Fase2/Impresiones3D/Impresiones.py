

class Impresiones:
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
        #generador.code.append("\tfmt.Printf(\"%c\", 10); //Salto ")

    def metodoPrintString(self):
        code=""
        t4=self.newTemp()
        t5=self.newTemp()
        t6=self.newTemp()
        L0=self.newLabel()
        L1=self.newLabel()
        code+="func printString(){\n "
        code+="\t"+t4+"=P+1;\n"
        code+="\t"+t5+"=stack[int("+t4+")];\n"
        code+="\t"+L1+":\n"
        code+="\t"+"\t"+t6+"=heap[int("+t5+")]; \n"
        code+="\t"+"\t"+"if "+t6+" == -1 {goto "+ L0+";}\n"
        code+="\t"+"\t"+"fmt.Printf(\"%c\", int("+t6+"));\n "
        code+="\t"+"\t"+t5+"="+t5+"+1; \n"
        code+="\t"+"\t"+"goto "+L1+";\n"
        code+="\t"+L0+":\n"
        code+="\t"+"\t"+"return;\n"
        code+="}\n"
        return code

    def imprimirCadenas(self, cadena):
        t3=self.generator.newTemp()
        self.generator.code.append(t3+"=H;\n")
        for caracter in cadena:
            self.generator.code.append("heap[int(H)]="+str(ord(caracter))+";")
            self.generator.addNextHeap()

        self.generator.code.append("heap[int(H)]=-1;")
        self.generator.addNextHeap()
        t7=self.generator.newTemp()
        self.generator.code.append(t7+"=P+0;\n")
        self.generator.code.append(t7+"="+t7+"+1;\n")
        self.generator.code.append("stack[int("+t7+")]="+t3+";\n")
        self.generator.code.append("P=P+0;\n printString();\n")
        t8=self.generator.newTemp()
        self.generator.code.append(t8+"=stack[int(P)];\n")
        self.generator.code.append("P=P-0;\n")
        
