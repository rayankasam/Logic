import string
class Invalidexpression(Exception):
    ...
operators = {
    'and':'^',
    'or':'V',
    'implies':'>',
    'not':'!'
}
breakStr = '-----------------------------------------------------------------'
permittedChars =(['(',')',operators['and'],operators['or'],'!',operators['implies']] +list(string.ascii_lowercase))
def eval(expr,propositions): # Recursive algorithm for evaluating propositional expressions given values of the propositions
    print(expr)
    if '(' not in expr: # Base case for when there are no more nested expressions
        if len(expr) != 3 or expr[1] not in ['(',')',operators['and'],operators['or'],'!',operators['implies']]:
            raise Invalidexpression
        if expr[1] == operators['and']:
                return propositions[expr[0]] and propositions[expr[-1]]
        if expr[1] == operators['or']:
            return propositions[expr[0]] or propositions[expr[-1]]
        if expr[1] == operators['implies']:
            return not(propositions[expr[0]]) or propositions[expr[-1]]
    # If there are brackers left it will split them up and evaluate them seperatly
    ranges = outerParentheses(expr)
    if len(ranges) > 2:
        raise Invalidexpression
    exprs = []
    for range in ranges:
        exprs.append(eval(getBetween(expr,(range[0],range[1])),propositions))
    
    if len(ranges) == 2:
        idxOfOperator = ranges[0][1]+1
        if expr[idxOfOperator] == operators['and']:
            return exprs[0] and exprs[1]
        if expr[idxOfOperator] == operators['or']:
            return exprs[0] or exprs[1]
        if expr[idxOfOperator] == '→ ':
            return not(exprs[0]) or exprs[1]
    elif len(ranges) == 1:
        return exprs[0]
    else:
        raise Invalidexpression
    
def outerParentheses(expr):

    istart = []  # stack of indices of opening parentheses
    pairs = []

    for i, c in enumerate(expr):
        if c == '(':
            istart.append(i)
        if c == ')':
            try:
                if len(istart) <= 1:
                    pairs.append((istart.pop(), i))
                else:
                    istart.pop()
            except IndexError:
                raise Invalidexpression
    if istart:  # check if stack is empty afterwards
        raise Invalidexpression
    return pairs
def getValues(expr): # Used to get the values for all the propositions from the user
    props = {}
    print('Enter the values of all the propositional veriables below')
    for char in set(expr): # Loops through all the unique propositional variabeles
        if char in list(string.ascii_lowercase):
            while True:
                currVal = input(f"Value of {char}: ").lower()
                if currVal in ['t','f']:
                    if currVal == 't':
                        
                        props[char] = True
                    else:
                        props[char] = False
                    break
                else:
                    print("Invalid Input")
    print(breakStr)
    return props
def getBetween(expr,range): # Used to get sub expressions
    return expr[range[0]+1:range[1]]
def takeExpression(): # Gets a propositional expression from the user
    # Takes input
    quit = False
    while True:
        try:
            userIn = input("Enter boolean expression (q to quit): ")
            userIn.replace(" ","")
            if userIn.lower() == 'q':
                print("Hope you found this useful!")
                quit = True
                break
            if False not in [(char in permittedChars) for char in userIn]:
                break
            else:
                raise ValueError
        except:
            print("Invalid expression")
    return userIn,quit
print(f"Welcome To my Propositional Solver\n{breakStr}\nTo enter a propositional expression enter all of your variables with operators in between (ex '(pVq)∧q')\nAnd: {operators['and']}\nOr: {operators['or']}\nimplies: {operators['implies']}\nNot: {operators['not']}\n{breakStr}")
while True:
    userIn, quit =  takeExpression()

    if quit: break
    props = getValues(userIn)
    print(eval(userIn,props))
