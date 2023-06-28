def tokenize( source:str ) -> list[str]:
    tokens:list[str] = []
    token:str = ''
    skip:int = 0
    instr:bool = False
    for c in source:
        if skip > 0: skip -= 1
        token += c
        if not instr:
            if c in ' +-*/$&^|}{;?<>!,%~@#=:,\n':
                l:str = (tokens[-1] if len(tokens)>0 else '')+c
                if (
                    l in [
                        '>#','<#','>@','<@',
                        '>:', '<:', '>::', '<::', '::',
                        '~#', '~:',
                        '**',
                        '==', '>=', '<='
                    ]
                ):
                    if len(tokens): tokens.pop()
                    tokens.append(l)
                    token = ''
                elif token[:-1].isidentifier() and c == ':':
                    tokens.append(token)
                    token = ''
                else:
                    token = token[:-1]
                    tokens.append(token)
                    tokens.append(c)
                    token = ''
            if c == '"' and len(token) == 1:
                instr = True
        else:
            if skip == 0:
                if c == '"':
                    instr = False
                if c == '\\':
                    skip = 2
    if token: tokens.append(token)
    return list(filter(lambda tk:len(tk.strip()),tokens))

class EggScript:
    
    tokens:list[str]
    functions:dict[str,list[str]]
    vars:dict[str,list[str]]
    
    contexts:list[list[str]]
        
    def __init__(self,tokens:list[str],functions:dict[str,list[str]],vars:dict[str,list[str]]):
        self.tokens = tokens
        self.functions = functions
        self.vars = vars
    
        self.contexts = [tokens,*functions.values()]
        
    def __str__(self) -> str:
        return f'{{ tokens : {self.tokens}, functions: {self.functions} }}'

def parse( source:list[str] ) -> EggScript:
    
    tokens:list[str] = []
    functions:dict[str,list[str]] = {}
    vars:dict[str,list[str]] = {}

    ctx:list[str] = tokens
    fnname:bool = False
    
    ctx.append(ctx)
    
    for tk in source:
        
        if tk == 'f': 
            fnname = True
            continue
            
        elif tk == 'end':
            ctx = ctx[0]
        
        elif fnname:
            functions[tk] = ctx = []
            ctx.append(tokens)
            fnname = False
            
        elif tk[:-1].isidentifier() and tk[-1] == ':':
            vars[tk[:-1]] = len(ctx)-1
        
        else:
            ctx.append(tk)
            
    return EggScript(tokens,functions,vars)