from typing import List
from Environment.Listas import Listas


class Impresiones:

    PrintAux=""
    PotenciaAux=""
    PotenciaStrAux=""
    ModAux=""
    MenorAux=""
    MayorAux=""
    MenorQueAux=""
    MayorQueAux=""
    IgualIgualAux=""
    NoIgualAux=""
    printBooleansAux=""

    MenorStrAux=""
    MayorStrAux=""
    MenorQueStrAux=""
    MayorQueStrAux=""
    IgualIgualStrAux=""
    NoIgualStrAux=""

    AndAux=""
    OrAux=""
    NotAux=""





    
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

# FUNCION PRINT STRING
    def metodoPrintString(self):
        if Listas.checkExistencia("printString","void","father","global","2","function"):
            index=self.PointerFree(0)
            code=""
            t4=self.newTemp()
            t5=self.newTemp()
            t6=self.newTemp()
            L0=self.newLabel()
            L01=self.newLabel()
            L1=self.newLabel()
            code+="func printString(){\n "
            code+="\t"+t4+"=P;\n"
            code+="\t"+t5+"=stack[int("+t4+")];\n"
            code+="\t"+L1+":\n"
            code+="\t"+"\t"+t6+"=heap[int("+t5+")]; \n"
            code+="\t"+"\t"+"if "+t6+" == -1 {goto "+ L0+";}\n"
            code+="\t"+"\t"+"goto "+L01+";\n"
            code+="\t"+L01+":\n"
            code+="\t"+"\t"+"fmt.Printf(\"%c\", int("+t6+"));\n "
            code+="\t"+"\t"+t5+"="+t5+"+1; \n"
            code+="\t"+"\t"+"goto "+L1+";\n"
            code+="\t"+L0+":\n"
            code+="\t"+"\t"+"return;\n"
            code+="}\n"
            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("printString","void","father","global","2","~","function")
            Listas.saveTabla("entrada","object","printString","local","1",str(index),"parameter")
            Impresiones.PrintAux=code
            return code
        return

    def imprimirCadenas(self, cadena):
        metodoPrint=Impresiones.metodoPrintString(self)
        t3=self.newTemp()
        self.code.append(t3+"=H;\n")
        for caracter in cadena:
            self.code.append("heap[int(H)]="+str(ord(caracter))+";")
            self.addNextHeap()

        self.code.append("heap[int(H)]=-1;")
        self.addNextHeap()
        t7=self.newTemp()
        entradaParameter= Listas.searchTabla("entrada","printString")
        self.code.append(t7+"="+entradaParameter[5]+";\n")
        self.code.append("stack[int("+t7+")]="+t3+";\n")
        self.addNextStack(int(entradaParameter[5]))
        self.code.append("printString();\n")
        self.addBackStack(int(entradaParameter[5]))

    def imprimirCadenasPosicion(self, temp):
        metodoPrint=Impresiones.metodoPrintString(self)
        t7=self.newTemp()
        entradaParameter= Listas.searchTabla("entrada","printString")
        self.code.append(t7+"="+entradaParameter[5]+";\n")
        self.code.append("stack[int("+t7+")]="+temp+";\n")
        self.addNextStack(int(entradaParameter[5]))
        self.code.append("printString();\n")
        self.addBackStack(int(entradaParameter[5]))
               
# FUNCION POTENCIA STRING
    def PowString(self):
        if Listas.checkExistencia("potenciaString","string","father","global","3","function"):

            codigo=""
            codigo+=("func potenciaString(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"
            codigo+="\t"+L0+":\n"
            
            entradaString=Listas.searchTabla("entrada","printString")            
            codigo+="\t\t"+"stack[int("+entradaString[5]+")]="+t2+";\n"
            codigo+="\t"+"\t"+"P =" + entradaString[5] + ";\n"        
            codigo+="\t"+"\t"+("printString();\n")
            t8=self.newTemp()
            codigo+="\t"+"\t"+(t8+"=stack[int("+str(index+1)+")];\n")
            codigo+="\t"+"\t"+"P ="+str(index)+";\n"
            self.P=self.P-index
            codigo+="\t"+"\t"+(t0 + " = " + t0 + " " + "+" + " " + "1" + ";\n")
            codigo+="\t"+"\t"+("if " + t0 + " " + "<" + " " + t8 + " {goto " + L0+ ";}\n")
            codigo+="\t\t goto "+L1+";\n"
            codigo+="\t"+L1+":\n"
            
            codigo+=("\t\t"+"return;\n}\n")
            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("potenciaString","string","father","global","4","~","function")
            Listas.saveTabla("entrada1PowStr","string","potenciaString","local","1",str(index),"parameter")
            Listas.saveTabla("entrada2PowStr","string","potenciaString","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","string","potenciaString","local","entrada2PowStr",str(index+2),"S.Transferencia")
            Impresiones.PotenciaStrAux=codigo
            return codigo
        return

    def imprimirCadenasPotencia(self, cadena,temp):
        codigo=Impresiones.metodoPrintString(self)
        codigo=Impresiones.PowString(self)
     
        t3=self.newTemp()
        self.code.append(t3+"=H;\n")
        for caracter in cadena:
            self.code.append("heap[int(H)]="+str(ord(caracter))+";")
            self.addNextHeap()

        self.code.append("heap[int(H)]=-1;")
        self.addNextHeap()
        
    

        t4 = self.newTemp()
        entrada1Parameter=Listas.searchTabla("entrada1PowStr","potenciaString")
        self.addExpression(t4,str(entrada1Parameter[5]),"","")
        self.addSetStack(t4,t3)

        entrada2Parameter=Listas.searchTabla("entrada2PowStr","potenciaString")
        self.addExpression(t4,str(entrada2Parameter[5]),"","")
        self.addSetStack(t4,temp)


        self.addNextStack(int(entrada1Parameter[5]))
        self.addCallFunc("potenciaString")
        
    
        self.addBackStack(int(entrada1Parameter[5]))

    def imprimirCadenasPotenciaPosicion(self, cadena,temp):
        codigo=Impresiones.metodoPrintString(self)
        codigo=Impresiones.PowString(self)       
    

        t4 = self.newTemp()
        entrada1Parameter=Listas.searchTabla("entrada1PowStr","potenciaString")
        self.addExpression(t4,str(entrada1Parameter[5]),"","")
        self.addSetStack(t4,cadena)

        entrada2Parameter=Listas.searchTabla("entrada2PowStr","potenciaString")
        self.addExpression(t4,str(entrada2Parameter[5]),"","")
        self.addSetStack(t4,temp)


        self.addNextStack(int(entrada1Parameter[5]))
        self.addCallFunc("potenciaString")
        
    
        self.addBackStack(int(entrada1Parameter[5]))

# FUNCION POTENCIA
    def potencia(self):
        if Listas.checkExistencia("potencia","object","father","global","3","function"):
            index=self.PointerFree(0)
            L0=self.newLabel()
            L01=self.newLabel()
            L1=self.newLabel()
            L11=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()
            L41=self.newLabel()
            L5=self.newLabel()
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            t4=self.newTemp()
            codigo=""
            codigo+="func potencia(){\n"
            codigo+="\t"+t0+" = P;\n"
            codigo+="\t"+t1+" = stack[int("+t0+")];\n"          #Izquierda
            codigo+="\t"+t0+" = "+t0+" + 1;\n"
            codigo+="\t"+t2+" = stack[int("+t0+")];\n"          #Derecha
            codigo+="\t"+t0+" = "+t1+";\n"
            codigo+="\t"+L0+":\n"
            codigo+="\t\tif "+t2+" <= 1 {goto "+L1+";}\n"
            codigo+="\t\t goto "+L01+";\n"
            codigo+="\t"+L01+":\n"
            codigo+="\t\t"+t1+" = "+t1+" * "+t0+";\n"
            codigo+="\t\t"+t2+" = "+t2+" - 1;\n"
            codigo+="\t\tgoto "+L0+";\n"
            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+"if "+t2+"==0 {goto "+L2+";}\n"
            codigo+="\t\t"+"if "+t2+"<0 {goto "+L3+";}\n"
            codigo+="\t\t"+"goto "+L11+";\n"
            codigo+="\t"+L11+":\n"
            codigo+="\t\tstack[int("+str(index+2)+")] = "+t1+";\n"
            codigo+="\t\treturn;\n"
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t4+"="+t4+"/"+t4+";\n"
            codigo+="\t\tstack[int(P)] = "+t4+";\n"
            codigo+="\t"+L3+":\n"
            codigo+="\t\t"+t2+"="+t2+"*-1;\n"
            codigo+="\t"+L4+":\n"
            codigo+="\t\tif "+t2+" <= 1 {goto "+L5+";}\n"
            codigo+="\t\t goto "+L41+";\n"
            codigo+="\t"+L41+":\n"
            codigo+="\t\t"+t1+" = "+t1+" * "+t0+";\n"
            codigo+="\t\t"+t2+" = "+t2+" - 1;\n"
            codigo+="\t\t goto "+L4+";\n"
            codigo+="\t"+L5+":\n"
            codigo+="\t\t"+t3+"=1/"+t1+";\n"
            codigo+="\t\tstack[int("+str(index+2)+")] = "+t3+";\n"       #Return
            codigo+="\t\treturn;\n"
            codigo+="}\n"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("potencia","object","father","global","4","~","function")
            Listas.saveTabla("izq","object","potencia","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","potencia","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","object","potencia","local","1",str(index+2),"S.Transferencia")
            Impresiones.PotenciaAux=codigo
            return codigo
        return
        
    def powAritmetica(self,left,right):
        metodoPow=Impresiones.potencia(self)
        t0=self.newTemp()
        t1=self.newTemp()

        entrada1Pow=Listas.searchTabla("izq","potencia")
        self.addExpression(t0,str(entrada1Pow[5]),"","")

        self.addSetStack(t0,str(left))
        entrada2Pow=Listas.searchTabla("der","potencia")
        self.addExpression(t0,str(entrada2Pow[5]),"","")
        self.addSetStack(t0,str(right))
        self.addNextStack(int(entrada1Pow[5]))
        self.addCallFunc("potencia")
        returnPow=Listas.searchTabla("return","potencia")
        self.addGetStack(t1,returnPow[5])
        self.addBackStack(int(entrada1Pow[5]))
        return t1

# FUNCION MOD
    def mod(self):
        if Listas.checkExistencia("mod","object","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t01=self.newTemp()
            t02=self.newTemp()
            t03=self.newTemp()
            t04=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L1=self.newLabel()
            L11=self.newLabel()
            L12=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()
            L5=self.newLabel()
            L51=self.newLabel()
            L6=self.newLabel()

            codigo=""
            codigo+="func mod(){\n"
            codigo+="\t"+t0+"=P;\n"
            codigo+="\t"+t01+"=stack[int("+t0+")];\n"
            codigo+="\t"+t0+"="+t0+"+1;\n"
            codigo+="\t"+t1+"=stack[int("+t0+")];\n"
            codigo+="\t"+t0+"="+t01+";\n"
            codigo+="\t"+t02+"=0;\n"
            codigo+="\t"+t03+"=0;\n"
            codigo+="\t"+t04+"=0-1;\n"

            codigo+="\t"+"if( "+t1+"!=0){ goto "+L1+";}\n"
            codigo+="\t goto "+ L11+";\n"
            codigo+="\t"+L11+":\n"
            codigo+="\t"+"fmt.Printf(\"%c\",77);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",97);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",116);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",104);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",69);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",114);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",114);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",111);\n"
            codigo+="\t"+"fmt.Printf(\"%c\",114);\n"

            codigo+="\t"+t2+"="+"0;\n"
            codigo+="\t"+"goto "+L2+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t if("+t0+"< 0){ goto "+L3+";}\n"
            codigo+="\t\t if("+t1+"< 0){ goto "+L4+";}\n"
            codigo+="\t\t if("+t0+"<"+t1+"){ goto "+L2+";}\n"
            codigo+="\t\t goto "+L12+";\n"
            codigo+="\t"+L12+":\n"
            codigo+="\t\t "+t0+"="+t0+"-"+t1+";\n"
            codigo+="\t\t goto "+L1+";\n"

            codigo+="\t"+L3+":\n"
            codigo+="\t\t"+t02+"="+"0-1;\n"
            codigo+="\t\t"+t0+"="+t0+"*"+t02+";\n"
            codigo+="\t\t goto "+L1+";\n"

            codigo+="\t"+L4+":\n"
            codigo+="\t\t"+t03+"="+"0-1;\n"
            codigo+="\t\t"+t1+"="+t1+"*"+t03+";\n"
            codigo+="\t\t goto "+L1+";\n"

            codigo+="\t"+L2+":\n"
            codigo+="\t\t if("+t02+"==-1){ goto "+L5+";}\n"
            codigo+="\t\t goto "+ L51+";\n"
            codigo+="\t"+L51+":\n"
            codigo+="\t\t"+t3+"="+t0+";\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            codigo+="\t\t goto "+L6+";\n"

            codigo+="\t"+L5+":\n"            
            codigo+="\t\t"+t0+"="+t0+"*"+t02+";\n"
            codigo+="\t\t"+t3+"="+t0+";\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            codigo+="\t\t goto "+L6+";\n"


            codigo+="\t"+L6+":\n" 
            codigo+="\t\t return;\n"
            codigo+="}\n"


            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("mod","object","father","global","4","~","function")
            Listas.saveTabla("izq","object","mod","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","mod","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","object","mod","local","1",str(index+2),"S.Transferencia")
            Impresiones.ModAux=codigo
            return codigo
        return

    def modAritmetica(self,left,right):
        metodoPod=Impresiones.mod(self)
        t0=self.newTemp()
        t1=self.newTemp()

        entrada1Mod=Listas.searchTabla("izq","mod")
        self.addExpression(t0,entrada1Mod[5],"","")   #izq
        self.addSetStack(t0,left)
        entrada2Mod=Listas.searchTabla("der","mod")
        self.addExpression(t0,entrada2Mod[5],"","")
        self.addSetStack(t0,right)          #der

        

        self.addNextStack(int(entrada1Mod[5]))
        self.addCallFunc("mod")
        returnMod=Listas.searchTabla("return","mod")
        self.addGetStack(t1,returnMod[5])  # return
        self.addBackStack(int(entrada1Mod[5]))

        return t1
    
# FUNCION RELACIONAL    
    def boolMenor(self):
        if Listas.checkExistencia("Menor","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc Menor(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"
            
            code+="\t if "+t0+"<"+t2+"{goto "+L0+";}\n"
            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("Menor","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","object","Menor","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","Menor","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","Menor","local","1",str(index+2),"S.Transferencia")
            Impresiones.MenorAux=code
            return code
        return

    def boolMayor(self):
        if Listas.checkExistencia("Mayor","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc Mayor(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"
            
            code+="\t if "+t0+">"+t2+"{goto "+L0+";}\n"
            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("Mayor","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","object","Mayor","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","Mayor","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","Mayor","local","1",str(index+2),"S.Transferencia")
            Impresiones.MayorAux=code
            return code
        return

    def boolMenorQue(self):
        if Listas.checkExistencia("MenorQue","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc MenorQue(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"
            
            code+="\t if "+t0+"<="+t2+"{goto "+L0+";}\n"
            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("MenorQue","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","object","MenorQue","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","MenorQue","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","MenorQue","local","1",str(index+2),"S.Transferencia")
            Impresiones.MenorQueAux=code
            return code
        return

    def boolMayorQue(self):
        if Listas.checkExistencia("MayorQue","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc MayorQue(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"
            
            code+="\t if "+t0+">="+t2+"{goto "+L0+";}\n"
            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("MayorQue","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","object","MayorQue","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","MayorQue","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","MayorQue","local","1",str(index+2),"S.Transferencia")
            Impresiones.MayorQueAux=code
            return code
        return

    def boolIgualIgual(self):
        if Listas.checkExistencia("IgualIgual","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc IgualIgual(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"
            
            code+="\t if "+t0+"=="+t2+"{goto "+L0+";}\n"
            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("IgualIgual","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","object","IgualIgual","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","IgualIgual","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","IgualIgual","local","1",str(index+2),"S.Transferencia")
            Impresiones.IgualIgualAux=code
            return code
        return

    def boolNoIgual(self):
        if Listas.checkExistencia("NoIgual","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc NoIgual(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"
            
            code+="\t if "+t0+"!="+t2+"{goto "+L0+";}\n"
            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("NoIgual","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","object","NoIgual","local","1",str(index),"parameter")
            Listas.saveTabla("der","object","NoIgual","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","NoIgual","local","1",str(index+2),"S.Transferencia")
            Impresiones.NoIgualAux=code
            return code
        return

    def imprimirRelatonals(self,left,right,operador):
        if operador=="Menor":
            Impresiones.boolMenor(self)
        elif operador=="Mayor":
            Impresiones.boolMayor(self)
        elif operador=="MenorQue":
            Impresiones.boolMenorQue(self)
        elif operador=="MayorQue":
            Impresiones.boolMayorQue(self)
        elif operador=="IgualIgual":
            Impresiones.boolIgualIgual(self)
        elif operador=="NoIgual":
            Impresiones.boolNoIgual(self)
        elif operador=="AndF":
            Impresiones.boolAnd(self)
        elif operador=="OrF":
            Impresiones.boolOr(self)
        elif operador=="NotF":
            Impresiones.boolNot(self)


        t0=self.newTemp()
        t1=self.newTemp()



        entrada1=Listas.searchTabla("izq",operador)
        self.addExpression(t0,entrada1[5],"0","+")   #izq
        self.addSetStack(t0,left)

        if operador!="NotF":
            entrada2=Listas.searchTabla("der",operador)
            self.addExpression(t0,entrada2[5],"0","+")
            self.addSetStack(t0,right)          #der

        

        self.addNextStack(int(entrada1[5]))
        self.addCallFunc(operador)
        returnRela=Listas.searchTabla("return",operador)
        self.addGetStack(t1,returnRela[5])  # return
        self.addBackStack(int(entrada1[5]))

        return t1



    def boolMenorStr(self):
        if Listas.checkExistencia("MenorStr","boolean","father","global","4","function"):

            codigo=""
            codigo+=("\nfunc MenorStr(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"            #Param 1 - Cadena
            codigo+="\t"+t7+"="+t7+"+1;\n"
            t8=self.newTemp()
            codigo+="\t"+(t8+"=stack[int("+t7+")];\n")       #Param 2
            codigo+="\t"+t7+"="+t2+";"                      #t7=Param 1
            t9=self.newTemp()
            t10=self.newTemp()
            codigo+="\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char

            codigo+="\t"+L0+":\n"
            
            codigo+="\t"+"\t"+("if " + t9 + " " + "==" + " " + t10 + " {goto " + L1+ ";}\n")
            codigo+="\t"+"\t"+("if " + t9 + " " + "<" + " " + t10 + " {goto " + L2+ ";}\n")
            codigo+="\t\t goto "+L3+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+t7+"="+t7+"+1;\n"
            codigo+="\t\t"+t8+"="+t8+"+1;\n"
            codigo+="\t\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char
            codigo+="\t"+"\t"+("if " + t9 + " " + "==-1 {goto " + L3+ ";}\n")
            

            codigo+="\t\tgoto "+L0+";\n"
            
            t11=self.newTemp()
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t11+"=1+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L3+":\n"
            codigo+="\t\t"+t11+"=0+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L4+":\n"
            codigo+="\t\t return;\n}"



            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("MenorStr","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","string","MenorStr","local","1",str(index),"parameter")
            Listas.saveTabla("der","string","MenorStr","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","MenorStr","local","1",str(index+2),"S.Transferencia")
            Impresiones.MenorStrAux=codigo
            return codigo
        return
    
    def boolMayorStr(self):
        if Listas.checkExistencia("MayorStr","boolean","father","global","4","function"):

            codigo=""
            codigo+=("\nfunc MayorStr(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"            #Param 1 - Cadena
            codigo+="\t"+t7+"="+t7+"+1;\n"
            t8=self.newTemp()
            codigo+="\t"+(t8+"=stack[int("+t7+")];\n")       #Param 2
            codigo+="\t"+t7+"="+t2+";"                      #t7=Param 1
            t9=self.newTemp()
            t10=self.newTemp()
            codigo+="\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char

            codigo+="\t"+L0+":\n"
            
            codigo+="\t"+"\t"+("if " + t9 + " " + "==" + " " + t10 + " {goto " + L1+ ";}\n")
            codigo+="\t"+"\t"+("if " + t9 + " " + ">" + " " + t10 + " {goto " + L2+ ";}\n")
            codigo+="\t\t goto "+L3+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+t7+"="+t7+"+1;\n"
            codigo+="\t\t"+t8+"="+t8+"+1;\n"
            codigo+="\t\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char
            codigo+="\t"+"\t"+("if " + t9 + " " + "==-1 {goto " + L3+ ";}\n")
            

            codigo+="\t\tgoto "+L0+";\n"
            
            t11=self.newTemp()
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t11+"=1+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L3+":\n"
            codigo+="\t\t"+t11+"=0+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L4+":\n"
            codigo+="\t\t return;\n}"



            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("MayorStr","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","string","MayorStr","local","1",str(index),"parameter")
            Listas.saveTabla("der","string","MayorStr","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","MayorStr","local","1",str(index+2),"S.Transferencia")
            Impresiones.MayorStrAux=codigo
            return codigo
        return
     
    def boolMayorQueStr(self):
        if Listas.checkExistencia("MayorQueStr","boolean","father","global","4","function"):

            codigo=""
            codigo+=("\nfunc MayorQueStr(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"            #Param 1 - Cadena
            codigo+="\t"+t7+"="+t7+"+1;\n"
            t8=self.newTemp()
            codigo+="\t"+(t8+"=stack[int("+t7+")];\n")       #Param 2
            codigo+="\t"+t7+"="+t2+";"                      #t7=Param 1
            t9=self.newTemp()
            t10=self.newTemp()
            codigo+="\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char

            codigo+="\t"+L0+":\n"
            
            codigo+="\t"+"\t"+("if " + t9 + " " + "==" + " " + t10 + " {goto " + L1+ ";}\n")
            codigo+="\t"+"\t"+("if " + t9 + " " + ">=" + " " + t10 + " {goto " + L2+ ";}\n")
            codigo+="\t\t goto "+L3+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+t7+"="+t7+"+1;\n"
            codigo+="\t\t"+t8+"="+t8+"+1;\n"
            codigo+="\t\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char
            codigo+="\t"+"\t"+("if " + t9 + " " + "==-1 {goto " + L3+ ";}\n")
            

            codigo+="\t\tgoto "+L0+";\n"
            
            t11=self.newTemp()
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t11+"=1+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L3+":\n"
            codigo+="\t\t"+t11+"=0+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L4+":\n"
            codigo+="\t\t return;\n}"



            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("MayorQueStr","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","string","MayorQueStr","local","1",str(index),"parameter")
            Listas.saveTabla("der","string","MayorQueStr","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","MayorQueStr","local","1",str(index+2),"S.Transferencia")
            Impresiones.MayorQueStrAux=codigo
            return codigo
        return
    
    def boolMenorQueStr(self):
        if Listas.checkExistencia("MenorQueStr","boolean","father","global","4","function"):

            codigo=""
            codigo+=("\nfunc MenorQueStr(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"            #Param 1 - Cadena
            codigo+="\t"+t7+"="+t7+"+1;\n"
            t8=self.newTemp()
            codigo+="\t"+(t8+"=stack[int("+t7+")];\n")       #Param 2
            codigo+="\t"+t7+"="+t2+";"                      #t7=Param 1
            t9=self.newTemp()
            t10=self.newTemp()
            codigo+="\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char

            codigo+="\t"+L0+":\n"
            
            codigo+="\t"+"\t"+("if " + t9 + " " + "==" + " " + t10 + " {goto " + L1+ ";}\n")
            codigo+="\t"+"\t"+("if " + t9 + " " + "<=" + " " + t10 + " {goto " + L2+ ";}\n")
            codigo+="\t\t goto "+L3+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+t7+"="+t7+"+1;\n"
            codigo+="\t\t"+t8+"="+t8+"+1;\n"
            codigo+="\t\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char
            codigo+="\t"+"\t"+("if " + t9 + " " + "==-1 {goto " + L3+ ";}\n")
            

            codigo+="\t\tgoto "+L0+";\n"
            
            t11=self.newTemp()
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t11+"=1+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L3+":\n"
            codigo+="\t\t"+t11+"=0+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L4+":\n"
            codigo+="\t\t return;\n}"



            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("MenorQueStr","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","string","MenorQueStr","local","1",str(index),"parameter")
            Listas.saveTabla("der","string","MenorQueStr","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","MenorQueStr","local","1",str(index+2),"S.Transferencia")
            Impresiones.MenorQueStrAux=codigo
            return codigo
        return
    
    def boolNoIgualStr(self):
        if Listas.checkExistencia("NoIgualStr","boolean","father","global","4","function"):

            codigo=""
            codigo+=("\nfunc NoIgualStr(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()
            L5=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"            #Param 1 - Cadena
            codigo+="\t"+t7+"="+t7+"+1;\n"
            t8=self.newTemp()
            codigo+="\t"+(t8+"=stack[int("+t7+")];\n")       #Param 2
            codigo+="\t"+t7+"="+t2+";"                      #t7=Param 1
            t9=self.newTemp()
            t10=self.newTemp()
            codigo+="\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char

            codigo+="\t"+L0+":\n"
            
            codigo+="\t"+"\t"+("if " + t9 + " " + "!=" + " " + t10 + " {goto " + L1+ ";}\n")
            codigo+="\t\t goto "+L3+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+t7+"="+t7+"+1;\n"
            codigo+="\t\t"+t8+"="+t8+"+1;\n"
            codigo+="\t\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char
            codigo+="\t"+"\t"+("if " + t9 + " " + "==-1 {goto " + L5+ ";}\n")
            

            codigo+="\t\tgoto "+L0+";\n"
            
            t11=self.newTemp()
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t11+"=1+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L3+":\n"            
            codigo+="\t\t"+t11+"=0+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            
            codigo+="\t"+L5+":\n"
            codigo+="\t"+"\t"+("if " + t10 + " " + "==-1 {goto " + L2+ ";}\n") #Verdadero
            codigo+="\t\t goto "+L3+";\n"   #Falso

            codigo+="\t"+L4+":\n"
            codigo+="\t\t return;\n}"



            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("NoIgualStr","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","string","NoIgualStr","local","1",str(index),"parameter")
            Listas.saveTabla("der","string","NoIgualStr","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","NoIgualStr","local","1",str(index+2),"S.Transferencia")
            Impresiones.NoIgualStrAux=codigo
            return codigo
        return
     
    def boolIgualIgualStr(self):
        if Listas.checkExistencia("IgualIgualStr","boolean","father","global","4","function"):

            codigo=""
            codigo+=("\nfunc IgualIgualStr(){\n")
            t7=self.newTemp()
            index=self.PointerFree(0)
            
            t0=self.newTemp()
            L0=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()
            L3=self.newLabel()
            L4=self.newLabel()
            L5=self.newLabel()

            codigo+="\t"+t0+"=0;\n"
            codigo+="\t"+(t7+"=P;\n")
            t2=self.newTemp()
            codigo+="\t"+t2+"=stack[int("+t7+")];\n"            #Param 1 - Cadena
            codigo+="\t"+t7+"="+t7+"+1;\n"
            t8=self.newTemp()
            codigo+="\t"+(t8+"=stack[int("+t7+")];\n")       #Param 2
            codigo+="\t"+t7+"="+t2+";"                      #t7=Param 1
            t9=self.newTemp()
            t10=self.newTemp()
            codigo+="\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char

            codigo+="\t"+L0+":\n"
            
            codigo+="\t"+"\t"+("if " + t9 + " " + "==" + " " + t10 + " {goto " + L1+ ";}\n")
            codigo+="\t\t goto "+L3+";\n"

            codigo+="\t"+L1+":\n"
            codigo+="\t\t"+t7+"="+t7+"+1;\n"
            codigo+="\t\t"+t8+"="+t8+"+1;\n"
            codigo+="\t\t"+t9+"=heap[int("+t7+")];\n"     #Parama 1   -   Char
            codigo+="\t\t"+t10+"=heap[int("+t8+")];\n"     #Parama 2   -   Char
            codigo+="\t"+"\t"+("if " + t9 + " " + "==-1 {goto " + L5+ ";}\n")
            

            codigo+="\t\tgoto "+L0+";\n"
            
            t11=self.newTemp()
            codigo+="\t"+L2+":\n"
            codigo+="\t\t"+t11+"=1+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            codigo+="\t"+L3+":\n"            
            codigo+="\t\t"+t11+"=0+0;\n"
            codigo+="\t\t stack[int("+str(index+2)+")]="+t11+";\n"
            codigo+="\t\t goto "+L4+";\n"

            
            codigo+="\t"+L5+":\n"
            codigo+="\t"+"\t"+("if " + t10 + " " + "==-1 {goto " + L2+ ";}\n") #Verdadero
            codigo+="\t\t goto "+L3+";\n"   #Falso

            codigo+="\t"+L4+":\n"
            codigo+="\t\t return;\n}"



            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("IgualIgualStr","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","string","IgualIgualStr","local","1",str(index),"parameter")
            Listas.saveTabla("der","string","IgualIgualStr","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","IgualIgualStr","local","1",str(index+2),"S.Transferencia")
            Impresiones.IgualIgualStrAux=codigo
            return codigo
        return

    def imprimirRelationalsStr(self, cadena1,cadena2, operador):
        
        if operador=="MenorStr":
            Impresiones.boolMenorStr(self)
        elif operador=="MayorStr":
            Impresiones.boolMayorStr(self)
        elif operador=="MenorQueStr":
            Impresiones.boolMenorQueStr(self)
        elif operador=="MayorQueStr":
            Impresiones.boolMayorQueStr(self)
        elif operador=="IgualIgualStr":
            Impresiones.boolIgualIgualStr(self)
        elif operador=="NoIgualStr":
            Impresiones.boolNoIgualStr(self)

        #Cadena 1
        t3=self.newTemp()
        self.code.append(t3+"=H;\n")
        for caracter in cadena1:
            self.code.append("heap[int(H)]="+str(ord(caracter))+";")
            self.addNextHeap()

        self.code.append("heap[int(H)]=-1;")
        self.addNextHeap()

        #Cadena 2
        t31=self.newTemp()
        self.code.append(t31+"=H;\n")
        for caracter in cadena2:
            self.code.append("heap[int(H)]="+str(ord(caracter))+";")
            self.addNextHeap()

        self.code.append("heap[int(H)]=-1;")
        self.addNextHeap()
        
    

        t4 = self.newTemp()
        entrada1Parameter=Listas.searchTabla("izq",operador)
        self.addExpression(t4,str(entrada1Parameter[5]),"0","+")
        self.addSetStack(t4,t3)

        t5=self.newTemp()
        entrada2Parameter=Listas.searchTabla("der",operador)
        self.addExpression(t5,str(entrada2Parameter[5]),"0","+")
        self.addSetStack(t5,t31)


        self.addNextStack(int(entrada1Parameter[5]))
        self.addCallFunc(operador)
        returnRela=Listas.searchTabla("return",operador)
        t1= self.newTemp()
        self.addGetStack(t1,returnRela[5])  # return
    
        self.addBackStack(int(entrada1Parameter[5]))

        return t1

# FUNCION LÓGICA
    def boolAnd(self):
        if Listas.checkExistencia("AndF","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L01=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc AndF(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"      #der
            code+="\t"+t0+"="+t1+";\n"                  #izq
            
            code+="\t if "+t0+"==1 {goto "+L0+";}\n"            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t if "+t2+"==1 {goto "+L01+";}\n"            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L01+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("AndF","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","boolean","AndF","local","1",str(index),"parameter")
            Listas.saveTabla("der","boolean","AndF","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","AndF","local","1",str(index+2),"S.Transferencia")
            Impresiones.AndAux=code
            return code
        return

    def boolOr(self):
        if Listas.checkExistencia("OrF","boolean","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L01=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc OrF(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t0+"+1;\n"
            code+="\t"+t2+"=stack[int("+t0+")];\n"      #der
            code+="\t"+t0+"="+t1+";\n"                  #izq
            
            code+="\t if "+t0+"==0 {goto "+L0+";}\n"            
            code+="\tgoto "+L01+";\n"

            code+="\t"+L0+":\n"
            code+="\t if "+t2+"==0 {goto "+L1+";}\n"            
            code+="\tgoto "+L01+";\n"

            code+="\t"+L01+":\n"
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("OrF","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","boolean","OrF","local","1",str(index),"parameter")
            Listas.saveTabla("der","boolean","OrF","local","1",str(index+1),"parameter")
            Listas.saveTabla("return","boolean","OrF","local","1",str(index+2),"S.Transferencia")
            Impresiones.OrAux=code
            return code
        return

    def boolNot(self):
        if Listas.checkExistencia("NotF","boolean","father","global","3","~","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            t2=self.newTemp()
            t3=self.newTemp()
            L0=self.newLabel()
            L01=self.newLabel()
            L1=self.newLabel()
            L2=self.newLabel()

            code=""
            code+="\nfunc NotF(){\n"
            code+="\t"+t0+"=P+0;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+";\n"                  #izq
            
            code+="\t if "+t0+"==0 {goto "+L0+";}\n"            
            code+="\tgoto "+L1+";\n"

            code+="\t"+L0+":\n"            
            code+="\t\t"+t3+"=1+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"


            code+="\t"+L1+":\n"
            code+="\t\t"+t3+"=0+0;\n"
            code+="\t\t stack[int("+str(index+2)+")]="+t3+";\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t\t return;\n}"

            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("NotF","boolean","father","global","4","~","function")
            Listas.saveTabla("izq","boolean","NotF","local","1",str(index),"parameter")
            Listas.saveTabla("return","boolean","NotF","local","1",str(index+2),"S.Transferencia")
            Impresiones.NotAux=code
            return code
        return

# FUNCTION PRINT BOOLEANOS
    def printBooleans(self):
        if Listas.checkExistencia("printBooleans","void","father","global","4","function"):
            index=self.PointerFree(0)
            t0=self.newTemp()
            t1=self.newTemp()
            L0=self.newTemp()
            L1=self.newTemp()
            L2=self.newTemp()

            code=""
            code+="func printBooleans(){\n "
            code+="\t"+t0+"=P;\n"
            code+="\t"+t1+"=stack[int("+t0+")];\n"
            code+="\t"+t0+"="+t1+"+0;\n"
            code+="\t"+"\t"+"if "+t0+" == 1 {goto "+ L0+";}\n"
            code+="\t"+"\t"+"goto "+L1+";\n"

            code+="\t"+L0+":\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('t'))+"); //t\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('r'))+"); //r\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('u'))+"); //u\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('e'))+"); //e\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L1+":\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('f'))+"); //f\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('a'))+"); //a\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('l'))+"); //l\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('s'))+"); //s\n"
            code+="\t\tfmt.Printf(\"%c\", "+str(ord('e'))+"); //e\n"
            code+="\t\t goto "+L2+";\n"

            code+="\t"+L2+":\n"
            code+="\t"+"\t"+"return;\n"
            code+="}\n"

            
            
            # Nombre/Tipo/Ambito/Visibilidad/Tamaño/Posicion/Rol
            Listas.saveTabla("printBooleans","void","father","global","2","~","function")
            Listas.saveTabla("entrada","object","printBooleans","local","1",str(index),"parameter")
            Impresiones.printBooleansAux=code
            return code
        return

    def imprimirBooleans(self,temp):
        Impresiones.printBooleans(self)
        t7=self.newTemp()
        entrada=Listas.searchTabla("entrada","printBooleans")
        self.code.append(t7+"="+entrada[5]+";\n")
        self.code.append("stack[int("+t7+")]="+temp+";\n")
        self.addNextStack(int(entrada[5]))
        self.code.append("printBooleans();\n")
        self.addBackStack(int(entrada[5]))


# Variables
    def saveVariable3D(self,enviroment,visibilidad, id, valor, tipo, index, tipoSave):    
        if tipoSave=="numeros":        
            t0=self.newTemp()

            self.addExpression(t0,str(index),"","")
            self.addSetStack(t0,valor)
            self.addGetStack(id,t0)
        else:
            t3=self.newTemp()
            self.code.append(t3+"=H;\n")
            for caracter in valor:
                self.code.append("heap[int(H)]="+str(ord(caracter))+";")
                self.addNextHeap()
            self.code.append("heap[int(H)]=-1;")
            self.addNextHeap()

            t7=self.newTemp()
            self.addExpression(t7,str(index),"","")
            self.addSetStack(t7,t3)
            self.addGetStack(id,t7)

