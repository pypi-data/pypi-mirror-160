class codex():
    """A simple class to encode given string using uncodeA simple class to encode given string using unicode
    Avaliable functions are:
        encoder - encoder(text, codex)
                  encoder(text=string, codex=unicode, r1=range1, r2=range2)
                  
        decoder - decode(text, codex)
                  decode(text=string, codex=unicode, r1=range1, r2=range2)"""
    @classmethod
    def encoder(cls, text: str, codex: int, r1=33, r2=130):
        char = [str(chr(i)) for i in range(r1, r2)]
        rahc = [str(chr(i)) for i in range(codex, codex+int(len(char)))]
        dict = {char[i]:rahc[i] for i in range(0, int(len(char)))}
        tred = text.translate(text.maketrans(dict))
        return tred
    @classmethod
    def decoder(cls, text: str, codex: int, r1=33, r2=130):
        char = [str(chr(i)) for i in range(r1, r2)]
        rahc = [str(chr(i)) for i in range(codex, codex+int(len(char)))]
        dict = {rahc[i]:char[i] for i in range(0, int(len(char)))}
        tred = text.translate(text.maketrans(dict))
        return tred
    