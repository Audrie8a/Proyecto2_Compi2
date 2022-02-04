from datetime import datetime


class ExceptionError:
    """
    ExceptionError
    Args:
        descripcion (str): descripcion del error
        linea (int): numero de la linea
        columna (int): numero de la columna
    """

    def __init__(self, descripcion: str, linea: int, columna: int):
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna
        self.date_time = datetime.now()

    def to_string(self):
        return f'{self.descripcion} - ' + (
            f'[Ln {self.linea}, Col {self.columna}]\n'
        )

    def to_json(self):
        return {
            'descripcion': str(self.descripcion),
            'line': str(self.linea),
            'column': str(self.columna),
            'time': str(self.date_time),
        }