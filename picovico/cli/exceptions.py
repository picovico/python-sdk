class PicovicoProfileError(Exception):
    """ Handle Picovico CLI errors with some code. """
    def __init__(self, message, code=-1):
        self.message = message
        self.code = code

    def __str__(self):
		return  repr('{}'.format(self.message))

class PicovicoCLIError(Exception):
    pass
        
