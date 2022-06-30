class ClaseUsuario:
    __usuario = None
    __receta = None

    def __init__(self):
        self.__usuario = None
        self.__receta = None

    def __del__(self):
        self.__usuario = None
        self.__receta = None

    def addusuario(self, usuario):
        self.__usuario= usuario
    def getUsuario(self):
        return self.__usuario

    def addreceta(self, receta):
        self.__receta = receta
    def getReceta(self):
        return self.__receta