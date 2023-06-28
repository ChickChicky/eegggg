import sys
import os
from eegggg import *

args = sys.argv[1:]

if len(args) == 0:
    print('\x1b[31mGIMME A FILE\x1b[39m')
    exit(1)
if not os.path.exists(args[0]):
    print('\x1b[31mGIMME AN ACTUAL FILE\x1b[39m')
    exit(1)
if not os.path.isfile(args[0]):
    print('\x1b[31mGIMME AN ACTUAL ACTUAL FILE\x1b[39m')
    exit(1)
    
def isfloatstr(s):
    try: float(s) ; return True
    except: return False
    
with open(args[0],'r') as f:
    source = f.read()
    script = parse(tokenize(source))
    
    # Init the stacks
    stacks = [[]]
    
    # Init all contexts to the beginning
    for ctx in script.contexts: 
        ctx.insert(1,0)
        ctx.insert(2,None)      
    
    ctx = script.tokens
    
    ctx[0] = ctx
    ctx[2] = ctx
    
    while True:
        
        done = False
        while len(ctx) < ctx[1]+4:
            if ctx[0] == ctx: 
                done = True
                break
            ctx[1] = 0
            ctx = ctx[2]
            #stacks.pop()
        if done: break
    
        stack = stacks[-1]
        tk = ctx[ctx[1]+3]
        
        # print('>',tk,stack)
                
        if isfloatstr(tk): stack.append(float(tk))
        if tk.isidentifier():
            if tk in script.functions:
                ctx[1] += 1
                octx = ctx
                ctx = script.functions[tk]
                ctx[2] = octx
                #stacks.append([])
                continue
            if tk in script.vars:
                stack.append(script.vars[tk])
        if tk[:1] == '"' and tk[-1:] == '"': stack.append(tk[1:-1])
        if tk == '>#': stack.append(stacks[-2].pop())
        if tk == '<#': stacks[-2].append(stack.pop())
        # if tk == '>@': stack.append(stacks[-2][-1])
        # if tk == '<@': stacks[-2].append(stack[-1])
        if tk == '>:': 
            it = int(stack.pop())
            for i in range(it): stack.append(stacks[-2][-it+i])
            for i in range(it): stacks[-2].pop()
        if tk == '<:': 
            it = int(stack.pop())
            for i in range(it): stacks[-2].append(stack[-it+i])
            for i in range(it): stack.pop()
        if tk == '>::':
            for i in range(int(stack.pop())): stack.append(stacks[-2].pop())
        if tk == '<::': 
            for i in range(int(stack.pop())): stacks[-2].append(stack.pop())
        if tk == '#':
            stack.append(stack[-1])
        if tk == ':':
            it = int(stack.pop())
            stack[len(stack):] = stack[-it:]
        if tk == '::':
            it = int(stack.pop())
            rep = int(stack.pop())
            val = stack[-it:]
            for i in range(rep): stack[len(stack):] = val
        if tk == '~#': stack[-2:] = reversed(stack[-2:])
        if tk == '~:':
            sz = stack.pop()
            stack[-sz:] = reversed(stack[-sz])
        
        if tk == '=': ctx[1] = float('inf')
        
        if tk in (
            '+','-','*','/','%', '**',
            '<','>','==','>=','<='
        ):
            b = stack.pop()
            a = stack.pop()
            if tk == '+':  stack.append(a+b)
            if tk == '-':  stack.append(a-b)
            if tk == '*':  stack.append(a*b)
            if tk == '/':  stack.append(a/b)
            if tk == '%':  stack.append(a%b)
            if tk == '**': stack.append(a**b)
            if tk == '<':  stack.append(float(a<b))
            if tk == '>':  stack.append(float(a>b))
            if tk == '<=': stack.append(float(a<=b))
            if tk == '>=': stack.append(float(a>=b))
            if tk == '==': stack.append(float(a==b))
            
        if tk == '?': 
            dest = stack.pop()
            cond = stack.pop() if len(stack) else 0
            if cond > 0 : ctx[1] = int(dest-1)
        if tk == '!': ctx[1] = int(stack.pop()-1)
        if tk == '@': print('\t'.join(map(str,stack)))
            
        if tk == '{': stacks.append([])
        if tk == '}': stacks.pop()
        if tk == ';': stack.clear()
        
        ctx[1] += 1
        
    #print(stacks)