from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.error.Exception import ExceptionError
from src.interprete.compilador.tipos.Tipo import TipoPrint, get_type_print


class Generador:
    __instance = None

    @staticmethod
    def get_instance():
        """
        STATIC ACCESS METHOD
        Forma de correcta de utilizar:
            generator = Generador.get_instance()
        """
        if Generador.__instance is None:
            Generador.__instance = Generador()
        return Generador.__instance

    def __init__(self):
        # contadores
        self.index_temp = 0
        self.index_label = 0
        # codigo
        self.code = ''
        self.func = ''
        self.natives = ''
        self.in_func = False
        self.in_native = False
        # lista temporales y nativas
        self.temp_list: list = []
        self.temp_recors: dict = {}
        # print
        self.is_print = False
        # Error List
        self.error_list: list = []
        # joinString
        self.is_join_str = False
        # potencia string
        self.is_pot_str = False
        # Upper Case
        self.is_to_upper = False
        # Lower Case
        self.is_to_lower = False
        # validate division
        self.is_validate_div = False
        # Index Validated
        self.is_index_validate = False
        # Comparar String
        self.is_equals_str = False
        # Lenght String
        self.is_len_str = False
        # Truncate
        self.is_truncate = False

    def clean(self):
        # contadores
        self.index_temp = 0
        self.index_label = 0
        # codigo
        self.code = ''
        self.func = ''
        self.natives = ''
        self.in_func = False
        self.in_native = False
        # lista temporales y nativas
        self.temp_list: list = []
        self.temp_recors: dict = {}
        # print
        self.is_print = False
        # Error List
        self.error_list: list = []
        # joinString
        self.is_join_str = False
        # potencia string
        self.is_pot_str = False
        # Upper Case
        self.is_to_upper = False
        # Lower Case
        self.is_to_lower = False
        # validate division
        self.is_validate_div = False
        # Index validated
        self.is_index_validate = False
        # Comparar String
        self.is_equals_str = False
        # Lenght String
        self.is_len_str = False
        # Truncate
        self.is_truncate = False

    # --------------------------------------------------------------------------
    # NUEVO TEMPORAL, LABEL, GOTO && IF
    # --------------------------------------------------------------------------
    # -------------- -> TEMPORAL <- --------------
    def new_temp(self):
        """Crea nueva variable temporal
        Returns:
            str: Nuevo temporal de tipo str
        """
        temp = f't{self.index_temp}'
        self.index_temp += 1
        self.temp_list.append(temp)
        self.temp_recors[temp] = temp
        return temp

    def free_temp(self, tmp: str):
        if tmp in self.temp_recors:
            self.temp_recors.pop(tmp, None)

    # def add_temp(self, tmp: str):
    #     if tmp not in self.temp_recors.keys():
    #         self.temp_recors[tmp] = tmp

    # def set_temp_record(self, tmp_record: dict):
    #     self.temp_recors = tmp_record

    # def get_temp_record(self):
    #     return self.temp_recors

    def free_all_temps(self):
        self.temp_recors = {}

    # -------------- -> SAVE TEMPS  <- --------------
    def save_temps(self, entorno: Entorno):
        size = 0
        if len(self.temp_recors) > 0:
            tmp = self.new_temp()
            self.free_temp(tmp)

            self.new_commnet('Guardar temporales')
            self.line_break()
            self.new_exp(tmp, 'P', entorno.get_size(), '+')

            for value in self.temp_recors:
                size += 1
                self.set_stack(tmp, value, '', False)
                if size != len(self.temp_recors):  # Revisar si -1
                    self.new_exp(tmp, tmp, '1', '+')

            self.line_break()
            self.new_commnet('fin de guardar temporales')

        lenght = entorno.get_size()
        entorno.set_size(lenght + size)
        return lenght

    def recover_tmp(self, entorno: Entorno, pos: int):
        if len(self.temp_recors) > 0:
            tmp = self.new_temp()
            self.free_temp(tmp)
            size = 0

            self.new_commnet('Recuperar temporales')
            self.line_break()

            self.new_exp(tmp, 'P', pos, '+')

            for value in self.temp_recors:
                size += 1
                self.get_stack(value, tmp)
                if size != len(self.temp_recors):
                    self.new_exp(tmp, tmp, '1', '+')

            self.line_break()
            self.new_commnet('fin de recuperacion')

            entorno.set_size(pos)

    # -------------- -> LABEL O ETIQUTA <- --------------
    def new_label(self):
        """Crea un nuevo label o etiqueta
        Returns:
            str: Debuevelve el label o etiqueta de tipo str
        """
        label = f'L{self.index_label}'
        self.index_label += 1
        return label

    def set_label(self, label: str):
        """Agregae el label o etiqueta al codigo
        Args:
            label (str): etiqueta
        """
        self.set_code(f'{label}:\n')

    # -------------- -> GOTO <- --------------
    def new_goto(self, label: str):
        """Agrega el label o etiqueta a un goto y setea al codigo
        Args:
            label (str): etiqueta
        """
        self.set_code(f'goto {label};\n')

    # -------------- -> IF <- --------------
    def new_if(self, left: str, right: str, op: str, label: str):
        """Agrega un nuevo if con un goto y setea al codigo
        Args:
            left (str): operador izquierdo
            right (str): operador derecho
            op (str): operacion a realizar
            label (str): etiqueta a saltar
        """
        self.free_temp(left)
        self.free_temp(right)
        if_str = f'if {left} {op} {right} '
        if_str += '{ goto ' + str(label) + '; }\n'
        self.set_code(if_str)

    # --------------------------------------------------------------------------
    # CODE MAIN GOLANG
    # --------------------------------------------------------------------------
    def set_code(self, code: str):
        if self.in_native:
            if self.natives == '':
                self.natives += (
                    '// -----------------------------------------------------------\n// FUNCIONES NATIVAS \n'
                    + code
                )
            else:
                self.natives += '\t' + code
        elif self.in_func:
            if self.func == '':
                self.func += (
                    '// -----------------------------------------------------------\n// FUNCIONES \n'
                    + code
                )
            else:
                self.func += '\t' + code
        else:
            self.code += '\t' + code

    def get_code(self):
        text = self.get_header()
        text += self.natives + '\n'
        text += self.func + '\n'
        text += '\n'
        text += '// ===========================================================\n// MAIN \n'
        text += (
            '// ===========================================================\n'
        )
        text += 'func main() {\n'
        text += '\t P = 0; // Puntero Stack \n'
        text += '\t H = 0; //Puntero Heap \n'
        text += self.code + '\n'
        text += '}\n'
        return str(text)

    # -------------- -> HEADER <- --------------
    def get_header(self):
        text = 'package main\n'
        text += 'import (\n\t"fmt"\n\t"math"\n)\n\n'
        # Declaracion de variables
        text += 'var P, H float64;\n'
        text += 'var stack [50000000]float64;\n'
        text += 'var heap [50000000]float64;\n'
        # if len(self.temp_list) > 0:
        #     text += 'var '
        #     for i in range(len(self.temp_list)):
        #         text += self.temp_list[i]
        #         if i != len(self.temp_list) - 1:
        #             text += ', '
        #     text += ' float64;\n\n'
        # return text
        if self.index_temp > 0:
            var = 'var '
            float_str = ' float64;\n'
            text += var
            aux_i = 10
            temp_i = 0
            for i in range(self.index_temp):
                text += f't{i}'
                if i != self.index_temp - 1 and i != aux_i:
                    text += ', '
                if i == aux_i:
                    text += float_str
                    if i != self.index_temp - 1:
                        aux_i += 10
                        text += var

                temp_i = i

            text += ' float64;\n\n' if temp_i != aux_i else ' \n'
        return text

    # -------------- -> FUNCTION <- --------------

    def new_commnet(self, text: str):
        comment = f'// {text.upper()}\n'
        self.set_code(comment)

    def new_comment_line(self):
        comment = (
            '// -----------------------------------------------------------\n'
        )
        self.set_code(comment)

    def line_break(self):
        """Salto de linea"""
        self.set_code('\n')

    def begin_comment(self, text: str):
        self.new_comment_line()
        self.new_commnet(text)

    def end_comment(self, text: str):
        self.new_commnet(text)
        self.new_comment_line()
        self.line_break()

    # --------------------------------------------------------------------------
    # EXPRESIONES
    # --------------------------------------------------------------------------
    def new_exp(
        self, result: str, left: str, right: str, op: str, comment: str = ''
    ):
        self.free_temp(left)
        self.free_temp(right)
        text = ''
        if right == '' and op == '':
            text = (
                f'{result} = {left};\n'
                if comment == ''
                else f'{result} = {left}; // {comment}\n'
            )
        else:
            text = (
                f'{result} = {left} {op} {right}; \n'
                if comment == ''
                else f'{result} = {left} {op} {right}; //{comment}\n'
            )
        self.set_code(text)

    def mod_operation(self, result: str, left: str, right):
        text = f'{result} = math.Mod({left}, {right}); \n'
        self.set_code(text)

    # --------------------------------------------------------------------------
    # INSTRUCCIONES: PRINT
    # --------------------------------------------------------------------------
    # fmt.Printf("%c", 116)     // Imprimir un caracter
    # fmt.Printf("%d", 116)     // Imprimir un numero
    # fmt.Printf("%g", 2.05)    // Imprimir un float
    # fmt.Printf("%c", int(10)) // Imprimir un salto de linea

    def print_new(self, type: TipoPrint, value):
        """Agregar un Print
        Args:
            type (TipoPrint): tipo del print
            value (any): valor a imprimir
        """
        self.free_temp(value)
        tipo, casteo = get_type_print(type)
        data = ''
        if casteo is None:
            data = f'fmt.Printf("%{tipo}", {value});\n'
        else:
            data = f'fmt.Printf("%{tipo}", {casteo}({value}));\n'
        self.set_code(data)

    def print_line_break(self):
        """Print Salto de Linea"""
        self.print_new(TipoPrint.CARACTER, 10)

    def print_space(self):
        self.print_new(TipoPrint.CARACTER, 32)

    def print_true(self):
        self.print_new(TipoPrint.CARACTER, 116)  # T
        self.print_new(TipoPrint.CARACTER, 114)  # R
        self.print_new(TipoPrint.CARACTER, 117)  # U
        self.print_new(TipoPrint.CARACTER, 101)  # E

    def print_false(self):
        self.print_new(TipoPrint.CARACTER, 102)  # F
        self.print_new(TipoPrint.CARACTER, 97)  # A
        self.print_new(TipoPrint.CARACTER, 108)  # L
        self.print_new(TipoPrint.CARACTER, 115)  # S
        self.print_new(TipoPrint.CARACTER, 101)  # E

    def print_math_err(self):
        self.print_new(TipoPrint.CARACTER, 77)
        self.print_new(TipoPrint.CARACTER, 97)
        self.print_new(TipoPrint.CARACTER, 116)
        self.print_new(TipoPrint.CARACTER, 104)
        self.print_new(TipoPrint.CARACTER, 69)
        self.print_new(TipoPrint.CARACTER, 114)
        self.print_new(TipoPrint.CARACTER, 114)
        self.print_new(TipoPrint.CARACTER, 111)
        self.print_new(TipoPrint.CARACTER, 114)
        self.print_line_break()

    def print_index_error(self):
        self.print_new(TipoPrint.CARACTER, 66)
        self.print_new(TipoPrint.CARACTER, 111)
        self.print_new(TipoPrint.CARACTER, 117)
        self.print_new(TipoPrint.CARACTER, 110)
        self.print_new(TipoPrint.CARACTER, 100)
        self.print_new(TipoPrint.CARACTER, 115)
        self.print_new(TipoPrint.CARACTER, 69)
        self.print_new(TipoPrint.CARACTER, 114)
        self.print_new(TipoPrint.CARACTER, 114)
        self.print_new(TipoPrint.CARACTER, 111)
        self.print_new(TipoPrint.CARACTER, 114)

    # --------------------------------------------------------------------------
    # ERROR_LIST
    # --------------------------------------------------------------------------
    def new_error(self, descripcion: str, line: int, column: int):
        """NUEVO ERROR
        Args:
            descripcion (str): descripcion del error
            line (int): linea del error
            column (int): columna del error
        """
        new_error = ExceptionError(descripcion, line, column)
        self.error_list.append(new_error)

    def get_erro_str(self):
        text: str = ''
        for error in self.error_list:
            text += error.to_string()
        return text

    def get_erro_json(self):
        new_list: list = []
        for error in self.error_list:
            new_list.append(error.to_json())
        return new_list

    def get_error_list(self):
        return self.error_list

    # --------------------------------------------------------------------------
    # ENTORNOS
    # --------------------------------------------------------------------------
    def new_entorno(self, size):
        self.set_code(f'P = P + {size};\n')

    def call_function(self, name):
        self.set_code(f'{name}();\n')

    def ret_entorno(self, size):
        self.set_code(f'P = P - {size};\n')

    # --------------------------------------------------------------------------
    # HEAP && STACK
    # --------------------------------------------------------------------------
    # -------------- -> HEAP <- --------------
    def set_heap(self, index: str, value: str, comment: str = ''):
        """
        Guardar en el heap
        heap[(int)INDEX] = VALUE
        Args:
            index (str): posicion del heap
            value (str): valor a guardar
            comment (str, optional): comentario. Defaults to ''.
        """
        self.free_temp(index)
        self.free_temp(value)
        text = (
            f'heap[int({index})] = {value};\n'
            if comment == ''
            else f'heap[int({index})] = {value}; // {comment}\n'
        )
        self.set_code(text)

    def get_heap(self, place: str, index: str, comment: str = ''):
        """
        Obtener valor del heap
        PLACE = heap[(int)INDEX];
        Args:
            place (str): donde se guardara
            index (str): posicion en el heap
            comment (str, optional): comentario. Defaults to ''.
        """
        self.free_temp(index)
        text = (
            f'{place} = heap[int({index})];\n'
            if comment == ''
            else f'{place} = heap[int({index})]; // {comment}\n'
        )
        self.set_code(text)

    def nex_heap(self):
        """
        Incrementar el heap
        H = H + 1;
        """
        self.set_code('H = H + 1;\n')

    # -------------- -> STACK <- --------------
    def set_stack(
        self, index: str, value: str, comment: str = '', free_val=True
    ):
        """
        Guardar en el stack
        stack[(int)INDEX] = VALUE;
        Args:
            index (str): posicion en el stack
            value (str): valor a guardar
            comment (str, optional): comentario. Defaults to ''.
        """
        self.free_temp(index)
        if free_val:
            self.free_temp(value)
        text = (
            f'stack[int({index})] = {value};\n'
            if comment == ''
            else f'stack[int({index})] = {value}; // {comment}\n'
        )
        self.set_code(text)

    def get_stack(self, place: str, index: str):
        """Obtener el valor del stack
        PLACE = stack[int(INDEX)];
        Args:
            place (str): variable donde se guardara
            index (str): posicion en el stack
        """
        self.free_temp(index)
        self.set_code(f'{place} = stack[int({index})];\n')

    # --------------------------------------------------------------------------
    # NATIVES FUNCTIONS
    # --------------------------------------------------------------------------
    def new_begin_func(self, name_func: str):
        if not self.in_native:
            self.in_func = True
        self.set_code(f'func {name_func}(){{\n')

    def new_end_funct(self):
        self.set_code('return; \n}\n')
        if not self.in_native:
            self.in_func = False

    def fPrintln(self):
        if self.is_print:
            return

        self.is_print = True
        self.in_native = True

        self.new_begin_func('printStr')

        # Label de salida
        end_lb = self.new_label()  # L0
        # Label del ciclo para imprimir
        while_lb = self.new_label()

        # Temporal puntero stack
        tmp_P = self.new_temp()

        # Temporal puntero heap
        tmp_H = self.new_temp()

        self.new_exp(tmp_P, 'P', '1', '+', ' Puntero del parametro')

        # t4 = stack[int(tem_p)] -> Donde Inicia la cadena en el heap
        self.get_stack(tmp_H, tmp_P)

        # Temporal para comparar
        tmp_compare = self.new_temp()

        self.set_label(while_lb)

        # t5 = heap[int(tmp_p)] -> 1: 'h', 2: 'o', 3: 'l', 4: 'a'
        self.get_heap(tmp_compare, tmp_H)

        # condicion
        self.new_if(tmp_compare, '-1', '==', end_lb)

        self.print_new(TipoPrint.CARACTER, tmp_compare)
        # incrementar contador
        self.new_exp(tmp_H, tmp_H, '1', '+', 'aumentar el contador del heap')
        # regresar al while
        self.new_goto(while_lb)

        # Label de salir
        self.set_label(end_lb)  # L0

        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_P)
        self.free_temp(tmp_H)
        self.free_temp(tmp_compare)

    def concat_string(self):
        if self.is_join_str:
            return

        self.is_join_str = True
        self.in_native = True
        self.new_begin_func('joinStr')

        # -------------- -> L0...Ln <- --------------
        # Label de salida
        end_lb = self.new_label()

        # Label del While1 para la cadena 1
        wh1_lb = self.new_label()
        # Label para asignar el puntero donde inicia la cadena 2
        set_lb = self.new_label()
        # Label del While1 para la cadena 1
        wh2_lb = self.new_label()

        # -------------- -> T0...Tn <- --------------
        # Temporal donde inicia la cadena unida
        tmp_ret = self.new_temp()
        # Temporal para el primer parametro, puntero P
        tmp_p = self.new_temp()
        # Temporal para el segudo parametro, puntero P
        tmp_p2 = self.new_temp()
        # Temporal para valor del heap, puntero del Heap
        tmp_h = self.new_temp()
        # Temporal para comapara
        tmp_compare = self.new_temp()

        # tmp_ret = H
        self.new_exp(tmp_ret, 'H', '', '', 'Puntero, iniciara la nueva cadena')
        # posicionamineto puntero para obtener el primer parametro
        self.new_exp(tmp_p, 'P', '1', '+', 'Puntero, para el 1re parametro')
        # obtener el puntero donde inica el primer parametro
        # tmp_h = stack[int(tem_p)] -> Donde Inicia la cadena en el heap
        self.get_stack(tmp_h, tmp_p)
        # posicionamineto puntero para obtener el segudo parametro
        self.new_exp(tmp_p2, 'P', '2', '+', 'Puntero, para el 2do parametro')

        self.set_label(wh1_lb)  # L1: -> While 1

        # tmp_compare = heap[int(tmp_h)] -> 1: 'h', 2: 'o', 3: 'l', 4: 'a'
        self.get_heap(tmp_compare, tmp_h, 'Valor de la cadena No.1')

        # condicion
        self.new_if(tmp_compare, '-1', '==', set_lb)
        # guardar el primer parametro en el heap
        self.set_heap('H', tmp_compare)
        # Incrementar el heap
        self.nex_heap()
        # Incrementar contador del heap
        self.new_exp(tmp_h, tmp_h, '1', '+', 'Aumentar el contador heap')
        # regresar al while
        self.new_goto(wh1_lb)

        # Obtener puntero donde inicia el 2do parametro
        self.set_label(set_lb)
        self.get_stack(tmp_h, tmp_p2)

        # While 2
        self.set_label(wh2_lb)
        self.get_heap(tmp_compare, tmp_h, 'Valor de la cadena No.2')
        # condicion
        self.new_if(tmp_compare, '-1', '==', end_lb)
        self.set_heap('H', tmp_compare)
        self.nex_heap()
        self.new_exp(tmp_h, tmp_h, '1', '+', 'Aumentar el contador heap')
        self.new_goto(wh2_lb)

        # L0: Salida
        self.set_label(end_lb)
        # Fin de cadena
        self.set_heap('H', '-1', 'FIN CADENA')
        self.nex_heap()
        self.set_stack('P', tmp_ret, 'Guardar el inicio de la cadena unida')
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_p)
        self.free_temp(tmp_p2)
        self.free_temp(tmp_h)
        self.free_temp(tmp_compare)
        self.free_temp(tmp_ret)

    def pot_string(self):
        if self.is_pot_str:
            return

        self.is_pot_str = True
        self.in_native = True
        self.new_begin_func('potenciaStr')

        # -------------- -> L0..Ln <- --------------
        # Label de salida
        end_lb = self.new_label()
        # Label del while
        whl_lb = self.new_label()
        # Label del continue
        cont_lb = self.new_label()
        # -------------- -> T0...Tn <- --------------
        # Temporal dnde inicia la cadena unida
        tmp_ret = self.new_temp()
        # Temporal para el primer parametro, puntero P
        tmp_p = self.new_temp()
        # Temporal para puntero del heap, inicia el primer parametro
        tmp_h = self.new_temp()
        # Temporal para guardar el exponente
        tmp_exp = self.new_temp()
        # Temporal para comparar la cadena ->> h,o,l,a
        tmp_compare = self.new_temp()
        # Temporal para comparar el expomenete
        tmp_com_exp = self.new_temp()
        # Copia del inicio del cadena
        tmp_h_copy = self.new_temp()

        # -------------- -> EXPRESIONES <- --------------
        # tmp_ret = H
        self.new_exp(tmp_ret, 'H', '', '', 'Puntero, iniciara la nueva cadena')
        # tmp_p = P + 1 ->> posicionamineto puntero para obtener el 1er param
        self.new_exp(tmp_p, 'P', '1', '+', 'Puntero, 1er parametro')
        # tmp_h = stack[int(tmp_p)] ->> Inicia el 1er parametro del heap
        self.get_stack(tmp_h, tmp_p)
        # tmp_p = tmp_p + 1 ->> posicionamint. puntero para obtener el 2do param
        # Esta caso es un exponente (numero)
        self.new_exp(tmp_p, tmp_p, '1', '+', 'Puntero, 2do parametro')
        # tmp_exp = stack[int(tmp_p)] ->> 2do parametro del heap
        self.get_stack(tmp_exp, tmp_p)
        # tmp_com_exp = 1 ->> Aumenta, comparar con el exponente
        self.new_exp(tmp_com_exp, '1', '', '', 'Contador, compara con el expo')
        # tmp_h_copy = tmp_h -> copia del inicio de la cadena
        self.new_exp(tmp_h_copy, tmp_h, '', '', 'Copia del incio del 1er param')

        # -------------- -> WHILE <- --------------
        # L1 -> while:
        self.set_label(whl_lb)
        # tmp_comare = heap[int(tmp_h)] -> 1: 'h', 2: 'o', 3: 'l', 4: 'a'
        self.get_heap(tmp_compare, tmp_h)
        # condicion
        self.new_if(tmp_compare, '-1', '==', cont_lb)
        # Guardar parametro en el heap
        self.set_heap('H', tmp_compare)
        # Incrementar el heap
        self.nex_heap()
        # aumentar el contador del heap
        self.new_exp(tmp_h, tmp_h, '1', '+', 'Aumentar puntero del heap')
        self.new_goto(whl_lb)

        # -------------- -> CONTINUE <- --------------
        # L2 -> continue:
        self.set_label(cont_lb)
        # condicion
        self.new_if(tmp_com_exp, tmp_exp, '==', end_lb)
        # tmp_com_exp = tmp_com_exp + 1 -> Incrementar contador del exp
        self.new_exp(
            tmp_com_exp,
            tmp_com_exp,
            '1',
            '+',
            'Aumentar contador de comparacion con el exp.',
        )
        # Reiniciar el contador del contador del heap
        self.new_exp(tmp_h, tmp_h_copy, '', '', 'Reiniciar puntero del heap')
        # Regresar al while
        self.new_goto(whl_lb)

        # -------------- -> EXIT <- --------------
        # L0: Salida
        self.set_label(end_lb)
        # Fin de cadena
        self.set_heap('H', '-1', 'FIN CADENA')
        self.nex_heap()
        self.set_stack('P', tmp_ret, 'Guardar donde inica la cadena unida')
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_ret)
        self.free_temp(tmp_p)
        self.free_temp(tmp_h)
        self.free_temp(tmp_exp)
        self.free_temp(tmp_compare)
        self.free_temp(tmp_com_exp)
        self.free_temp(tmp_h_copy)

    def to_upper(self):
        if self.is_to_upper:
            return

        self.is_to_upper = True
        self.in_native = True
        self.new_begin_func('toUpperCase')

        # -------------- -> L0...Ln <- --------------
        # Label de salida
        end_lb = self.new_label()
        # Label del while
        whl_lb = self.new_label()
        # Label del continue
        cont_lb = self.new_label()
        # -------------- -> T0...Tn <- --------------
        tmp_ret = self.new_temp()
        tmp_p = self.new_temp()
        tmp_h = self.new_temp()
        tmp_comp = self.new_temp()
        # -------------- -> EXPRESIONES <- --------------
        self.new_exp(tmp_ret, 'H', '', '')
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_h, tmp_p)
        # -------------- -> WHILE <- --------------
        self.set_label(whl_lb)
        self.get_heap(tmp_comp, tmp_h)
        self.new_if(tmp_comp, '-1', '==', end_lb)
        self.new_if(tmp_comp, '97', '<', cont_lb)
        self.new_if(tmp_comp, '122', '>', cont_lb)
        self.new_exp(tmp_comp, tmp_comp, '32', '-', 'Convertir en mayuscula')
        # -------------- -> CONTINUE <- --------------
        # L2: continue
        self.set_label(cont_lb)
        self.set_heap('H', tmp_comp)
        self.nex_heap()
        self.new_exp(tmp_h, tmp_h, '1', '+')
        self.new_goto(whl_lb)
        # -------------- -> SALIDA <- --------------
        # L0: Salida
        self.set_label(end_lb)
        # Fin de cadena
        self.set_heap('H', '-1', 'FIN CADENA')
        self.nex_heap()
        self.set_stack('P', tmp_ret, 'Guardar donde inica la nueva cadena')
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_ret)
        self.free_temp(tmp_p)
        self.free_temp(tmp_h)
        self.free_temp(tmp_comp)

    def to_lower(self):
        if self.is_to_lower:
            return

        self.is_to_lower = True
        self.in_native = True
        self.new_begin_func('toLowerCase')

        # -------------- -> L0...Ln <- --------------
        # Label de salida
        end_lb = self.new_label()
        # Label del while
        whl_lb = self.new_label()
        # Label del continue
        cont_lb = self.new_label()
        # -------------- -> T0...Tn <- --------------
        tmp_ret = self.new_temp()
        tmp_p = self.new_temp()
        tmp_h = self.new_temp()
        tmp_comp = self.new_temp()
        # -------------- -> EXPRESIONES <- --------------
        self.new_exp(tmp_ret, 'H', '', '')
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_h, tmp_p)
        # -------------- -> WHILE <- --------------
        self.set_label(whl_lb)
        self.get_heap(tmp_comp, tmp_h)
        self.new_if(tmp_comp, '-1', '==', end_lb)
        self.new_if(tmp_comp, '65', '<', cont_lb)
        self.new_if(tmp_comp, '90', '>', cont_lb)
        self.new_exp(tmp_comp, tmp_comp, '32', '+', 'Convertir en mayuscula')
        # -------------- -> CONTINUE <- --------------
        # L2: continue
        self.set_label(cont_lb)
        self.set_heap('H', tmp_comp)
        self.nex_heap()
        self.new_exp(tmp_h, tmp_h, '1', '+')
        self.new_goto(whl_lb)
        # -------------- -> SALIDA <- --------------
        # L0: Salida
        self.set_label(end_lb)
        # Fin de cadena
        self.set_heap('H', '-1', 'FIN CADENA')
        self.nex_heap()
        self.set_stack('P', tmp_ret, 'Guardar donde inica la nueva cadena')
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_ret)
        self.free_temp(tmp_p)
        self.free_temp(tmp_h)
        self.free_temp(tmp_comp)

    def division_validate(self):
        if self.is_validate_div:
            return

        self.is_validate_div = True
        self.in_native = True
        self.new_begin_func('divValidate')

        # -------------- -> L0..Ln <- --------------
        end_lb = self.new_label()  # L0: Salida
        succ_lb = self.new_label()  # L1: Correcto
        # -------------- -> T0...Tn <- --------------
        tmp_p = self.new_temp()  # T0 = P + 1
        tmp_lf = self.new_temp()  # T1 = 5 + 5
        tmp_rg = self.new_temp()  # T2 = 3 - 3
        tmp_ret = self.new_temp()  # T3 = result
        # -------------- -> EXPRESIONES <- --------------
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_lf, tmp_p)
        self.new_exp(tmp_p, tmp_p, '1', '+')
        self.get_stack(tmp_rg, tmp_p)

        # if T2 != 0 { goto L1 }
        self.new_if(tmp_rg, '0', '!=', succ_lb)
        # PRINT ERROR
        self.print_math_err()
        self.new_exp(tmp_ret, '0', '', '', 'resultado incorrecto')
        self.new_goto(end_lb)
        # SUCCESS
        self.set_label(succ_lb)
        self.new_exp(tmp_ret, tmp_lf, tmp_rg, '/')
        # EXIT
        self.set_label(end_lb)
        self.set_stack('P', tmp_ret, 'gurdar resultado')
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_p)
        self.free_temp(tmp_lf)
        self.free_temp(tmp_rg)
        self.free_temp(tmp_ret)

    def validate_index_array(self):
        if self.is_index_validate:
            return

        self.is_index_validate = True
        self.in_native = True
        self.new_begin_func('indexValidate')

        # -------------- -> L0...Ln <- --------------
        end_lb = self.new_label()
        true_lb = self.new_label()
        false_lb = self.new_label()
        # -------------- -> T0...Tn <- --------------
        tmp_p = self.new_temp()  # T0 = P + 1
        tmp_len = self.new_temp()  # T1 = 3 -> longiud
        tmp_i = self.new_temp()  # T2 = 5 -> index
        tmp_result = self.new_temp()
        # -------------- -> EXPRESIONE <- --------------
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_len, tmp_p)
        self.new_exp(tmp_p, tmp_p, '1', '+')
        self.get_stack(tmp_i, tmp_p)

        # if tmp_i < 1 { goto L2 }
        self.new_if(tmp_i, '1', '<', true_lb)
        # if tmp_i > tmp_len { goto L2 }
        self.new_if(tmp_i, tmp_len, '>', true_lb)
        # goto false_lb
        self.new_goto(false_lb)
        # L2: true_lb
        self.set_label(true_lb)
        self.print_index_error()
        self.new_exp(tmp_result, '1', '', '')  # Esta malo el index
        self.new_goto(end_lb)
        # L3: false labe
        self.set_label(false_lb)
        self.new_exp(tmp_result, '0', '', '')  # Esta correcto el index
        # EXIT
        self.set_label(end_lb)
        self.set_stack('P', tmp_result)
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_p)
        self.free_temp(tmp_len)
        self.free_temp(tmp_i)
        self.free_temp(tmp_result)

    def verify_equals_str(self):
        if self.is_equals_str:
            return

        self.is_equals_str = True
        self.in_native = True
        self.new_begin_func('isEqualsStr')
        # -------------- -> L0..L1 <- --------------
        end_lb = self.new_label()
        whl_lb = self.new_label()
        err_lb = self.new_label()
        succ_lb = self.new_label()
        # -------------- -> T0..Tn <- --------------
        tmp_p = self.new_temp()
        tmp_h_1 = self.new_temp()  # Inicia el primera parametro
        tmp_h_2 = self.new_temp()  # Inicia el segundo parametro
        tmp_comp_1 = self.new_temp()  # El valor de la cadena 'h', 'o'
        tmp_comp_2 = self.new_temp()  # El valor de 2da cadena
        # -------------- -> EXPRESIONES <- --------------
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_h_1, tmp_p)
        self.new_exp(tmp_p, tmp_p, '1', '+')
        self.get_stack(tmp_h_2, tmp_p)

        # L1: -> While
        self.set_label(whl_lb)
        # obtener valores del heap
        self.get_heap(tmp_comp_1, tmp_h_1)
        self.get_heap(tmp_comp_2, tmp_h_2)
        # verficaciones
        self.new_if(tmp_comp_1, tmp_comp_2, '!=', err_lb)
        self.new_if(tmp_comp_1, '- 1', '==', succ_lb)
        # aumentar contadores
        self.new_exp(tmp_h_1, tmp_h_1, '1', '+')
        self.new_exp(tmp_h_2, tmp_h_2, '1', '+')
        # regresar al while
        self.new_goto(whl_lb)

        # L2: -> Succes
        self.set_label(succ_lb)
        self.set_stack('P', '1')
        self.new_goto(end_lb)

        # L3: -> Error
        self.set_label(err_lb)
        self.set_stack('P', '0')

        # L0: -> Salir
        self.set_label(end_lb)
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_p)
        self.free_temp(tmp_h_1)
        self.free_temp(tmp_h_2)
        self.free_temp(tmp_comp_1)
        self.free_temp(tmp_comp_2)

    def get_len_str(self):
        if self.is_len_str:
            return

        self.is_len_str = True
        self.in_native = True
        self.new_begin_func('getLenStr')
        # -------------- -> L0...Ln <- --------------
        end_lb = self.new_label()
        whl_lb = self.new_label()
        # -------------- -> T0...Tn <- --------------
        tmp_p = self.new_temp()
        tmp_h = self.new_temp()
        tmp_result = self.new_temp()
        tmp_compare = self.new_temp()
        # -------------- -> EXPRESIONES <- --------------
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_h, tmp_p)
        self.get_heap(tmp_compare, tmp_h)
        self.new_exp(tmp_result, '0', '', '')

        # L1: -> While
        self.set_label(whl_lb)
        # verificar si es la ultima posicion
        self.new_if(tmp_compare, '- 1', '==', end_lb)
        # aumenar contador
        self.new_exp(tmp_h, tmp_h, '1', '+')
        self.get_heap(tmp_compare, tmp_h)
        self.new_exp(tmp_result, tmp_result, '1', '+')
        self.new_goto(whl_lb)

        # L0: -> Exit
        self.set_label(end_lb)
        self.set_stack('P', tmp_result)
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_p)
        self.free_temp(tmp_h)
        self.free_temp(tmp_result)
        self.free_temp(tmp_compare)

    def trucate_num(self):
        if self.is_truncate:
            return

        self.is_truncate = True
        self.in_native = True
        self.new_begin_func('truncNum')

        # -------------- -> L0..Ln <- --------------
        end_lb = self.new_label()  # L0: Salida
        wh_lb = self.new_label()  # L1: While
        # -------------- -> T0...Tn <- --------------
        tmp_p = self.new_temp()  # T0 = P + 1
        tmp_num = self.new_temp()  # T1 = 5
        tmp_count = self.new_temp()  # Contador
        # -------------- -> EXPRESIONES <- --------------
        self.new_exp(tmp_p, 'P', '1', '+')
        self.get_stack(tmp_num, tmp_p)
        self.new_exp(tmp_count, '0', '', '')

        # While:
        self.set_label(wh_lb)
        # verificar si es la ultima posicion
        self.new_if(tmp_count, tmp_num, '>', end_lb)
        # aumentar contador
        self.new_exp(tmp_count, tmp_count, '1', '+')
        self.new_goto(wh_lb)

        # Exit:
        self.set_label(end_lb)
        self.new_exp(tmp_count, tmp_count, '1', '-')
        self.set_stack('P', tmp_count, 'gurdar resultado')
        self.new_end_funct()
        self.in_native = False
        self.free_temp(tmp_p)
        self.free_temp(tmp_num)
        self.free_temp(tmp_count)