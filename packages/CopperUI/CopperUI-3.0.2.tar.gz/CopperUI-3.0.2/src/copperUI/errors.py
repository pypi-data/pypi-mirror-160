class NameSpace(Exception):
    class BackgroundColorError(Exception):
        """this is called when a user calls a foreground color in the case of a background usage"""
        pass

    class ForegroundColorError(Exception):
        """this is called when a user calls a background color in the case of a foreground usage"""
        pass

class ArgumentError(Exception):
    print("incorrect argument")
