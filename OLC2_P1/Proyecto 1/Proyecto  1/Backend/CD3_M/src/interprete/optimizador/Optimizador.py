from src.interprete.optimizador.instrucciones.Label import Label
from src.interprete.optimizador.Blocks import Blocks
from src.interprete.optimizador.instrucciones.Assignment import Assignment
from src.interprete.optimizador.gotos.Goto import Goto
from src.interprete.optimizador.gotos.IF import IF


class Optimizador:
    def __init__(self, packages, temps, code):
        self.packages = packages
        self.temps = temps
        self.code = code

        self.blocks = []

    def get_code(self):
        ret = f'package main;\n\nimport (\n\t"{self.get_pacakages()}"\n);\n'
        for temp in self.temps:
            ret = ret + f'var {temp}\n'
        ret = ret + '\n'

        for func in self.code:
            ret = ret + func.get_code() + '\n\n'
        return ret

    def get_pacakages(self):
        package = ''
        for pack in self.packages:
            package += pack + '\n\t'
        return pack

    def mirilla(self):
        # Por cada funcion
        for func in self.code:
            tamanio = 0

            # Mientras no nos hemos pasado del tamaño (Fin del código)
            while tamanio <= len(func.instr):
                flagOpt = False

                # Darle 5 pasadas al codigo con el tamaño actual
                for i in range(5):
                    aux = 0
                    # Dar una pasada completa
                    while (tamanio + aux) <= len(func.instr):
                        flagOpt = flagOpt or self.regla3(
                            func.instr[0 + aux : tamanio + aux]
                        )
                        flagOpt = flagOpt or self.regla6(
                            func.instr[0 + aux : tamanio + aux]
                        )
                        aux = aux + 1

                # Si no hubo optimizacion en la pasada, subir el tamaño
                if not flagOpt:
                    tamanio = tamanio + 5

    def regla3(self, array):
        # Auxiliar para verificar que la regla se implemento
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es un If
            if type(actual) is IF and not actual.deleted:
                nextIns = array[i + 1]
                # Si el siguiente es un Goto
                if type(nextIns) is Goto and not nextIns.deleted:
                    # SE DEBE ELIMINAR i+1 e i+2. Goto LBL y LBL:
                    actual.condition.get_contrary()
                    actual.label = nextIns.label
                    nextIns.deleted = True
                    array[i + 2].deleted = True
                    ret = True
        return ret

    def regla6(self, array):
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es una Asignacion
            if type(actual) is Assignment and not actual.deleted:
                # Si se esta asignando a si mismo
                if actual.self_assignment():
                    actualOpt = actual.exp.neutral_ops()
                    if actualOpt:
                        ret = True
                        actual.deleted = True
        return ret

    def bloques(self):
        self.blocks = []
        self.generarBloques()

        # APLICAR REGLAS A NIVEL LOCAL Y GLOBAL

    def generarBloques(self):
        self.generarLideres()
        self.crearBloques()
        self.connectBloques()

    def generarLideres(self):
        # Por cada funcion
        for func in self.code:
            # La primera instrucción de tres direcciones en el código intermedio es líder
            func.instr[0].isLeader = True

            # Cualquier instrucción que siga justo después de un salto
            # condicional o incondicional es líder
            flag = False
            for instr in func.instr:
                if flag:
                    instr.isLeader = True
                    flag = False
                if type(instr) is Goto or type(instr) is IF:
                    flag = True

    def crearBloques(self):
        # Por cada funcion
        for func in self.code:
            # Bloques de la funcion actual
            blocks = []
            block = None
            for instr in func.instr:
                if instr.isLeader:
                    # Si ya hay un bloque creado. Agregarlo al arreglo de bloques
                    if block != None:
                        blocks.append(block)
                    block = Blocks(instr)
                block.code.append(instr)
            # EOF
            blocks.append(block)
            # Guardo mis bloques de la funcion
            self.blocks.append(blocks)

    def connectBloques(self):
        # Por cada arreglo de bloques en una función
        for func in self.blocks:
            prevBlock = None
            # Por cada bloque en la funcion. Los uniremos en cascada
            for block in func:
                if prevBlock == None:
                    prevBlock = block
                    continue
                prevBlock.nexts.append(block)
                prevBlock = block

            # Revisar saltos entre bloques
            for block in func:
                # Obtener ultima instruccion
                lastIns = block.code[len(block.code) - 1]
                if type(lastIns) is Goto or type(lastIns) is IF:
                    label = lastIns.label
                    # Revisando todos los bloques
                    for check in func:
                        if (
                            type(check.first) is Label
                            and check.first.id == label
                        ):
                            block.nexts.append(check)
                            break