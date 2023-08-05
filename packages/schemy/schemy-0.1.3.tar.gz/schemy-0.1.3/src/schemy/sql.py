from schemy import Schema

class SQL(object):
    """
    Classe para criar comandos SQL
    baseando-se num objeto Schema.
    """

    def __init__(self, schema:Schema):
        self._schema = schema