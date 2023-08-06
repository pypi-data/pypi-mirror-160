#Main class
class Unicodex():
    """"Unicodex class
    
    Unicodex objects are responsible of encoding, decoding & converting unicodes.
    
    Available options:
        - chr:       Codex to unicode character converter.
        - ord:       Unicode character to codex converter.
        - encode:    Encoding any text to unicodes.
        - decode:    Decoding any unicodes to text.
    """
          
    #CODE TO CHARACTER
    @classmethod
    def chr(cls, codex: int):
        "Codex to character"
        return str(chr(codex))
    
    #CHARACTER TO CODE
    @classmethod
    def ord(cls, character: str):
        "Codex to character"
        return int(ord(character))
    
    #ENCODER
    @classmethod
    def encode(cls, text: str, codex: int, CR=33, RCR=130):
        "Encode text to unicode"
        if codex < RCR: codex+=RCR
        
        char = [str(chr(i)) for i in range(CR, RCR)]
        emo = [str(chr(i)) for i in range(codex, codex+int(len(char)))]
        
        odict = {char[i]:emo[i] for i in range(0, int(len(char)))}
        tr = text.translate(text.maketrans(odict))
        return str(tr)
    
    #DECODER
    @classmethod
    def decode(cls, text: str, codex: int, CR=33, RCR=130):
        "Decode unicode to text"
        if codex < RCR: codex+=RCR
        
        char = [str(chr(i)) for i in range(CR, RCR)]
        emo = [str(chr(i)) for i in range(codex, codex+int(len(char)))]
        
        odict = {char[i]:emo[i] for i in range(0, int(len(char)))}
        rdict = {v: k for k, v in odict.items()}
        tr = text.translate(text.maketrans(odict))
        rv = tr.translate(tr.maketrans(rdict))
        return str(rv)