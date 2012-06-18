nextNumber = 0
s = "    "
ss = 2*s
t = "   "

def preIndent(text):
    rstring = []
    for l in text.splitlines() :
        rstring.append(ss+l)
    return "\n".join(rstring)
    
def printPreIndent(text):    
    print(preIndent(text))

def thenIndent(text):
    base = [ss]
    lines = text.splitlines()
    rstring = []
    for l in lines :        
        tab = base[-1]
        if ( l.find("SELECT")>=0 ):
            base.append(tab+t)
        elif ( l.find("THEN")>=0 or l.find("WHEN")>=0):
            tab = base[-2]
        elif ( l.find("END")>=0 ):
            base.pop()
            tab = base[-1]
        rstring.append(tab+l)
    return "\n".join(rstring)
    
def printThenIndent(text):
    print(thenIndent(text))

def mergeOperations(d1,d2) :
    result = dict(d1)
    for k,v in d2.items():
        if k in result.keys():
            result[k] = sameOpMerge(result[k], v)
        else:
            result[k] = v
    return result

def mergeOperationsWithStates(op1,n1,op2,n2) :
    if op1['name'] != op2['name'] :
        raise TypeError("Merging two transitions with different names")
    result = {}    
    added = " & State_" + n1 + " = " + n2 + " "
    l = map( lambda x: x+added,op2['PRE'])
    op2['PRE'] = list(l)
    for i,item in enumerate(op2['THEN']):
        op2['THEN'][i] = (op2['PRE'][i],op2['THEN'][i][1])
    result['PRE'] = op1['PRE'] + op2['PRE']
    result['THEN'] = op1['THEN'] + op2['THEN'] 
    result['param'] = op2['param']
    result['name'] = op2['name']  
    result['TYPE'] = op1['TYPE'] + op2['TYPE']
    return result    
    
def sameOpMerge(op1,op2):
    if op1['name'] != op2['name'] :
        raise TypeError("Merging two transitions with different names")
    result = {}    
    result['PRE'] = op1['PRE'] + op2['PRE']
    result['THEN'] = op1['THEN'] + op2['THEN'] 
    result['param'] = op2['param']
    result['name'] = op2['name']  
    result['TYPE'] = op1['TYPE'] + op2['TYPE']
    return result
    
def getThen(opthen,lvl=0) :
    r = ""
    r += 'SELECT\n'
    when = "\n"+"WHEN\n"            
    liste = []
    for u0,u1 in opthen :
        liste.append(str(u0)+"\n"+"THEN\n"+str(u1))                
    r += when.join(liste)
    r += "\nEND"
    return r
    
def getPre(oppre) :
    r = (' or\n').join(oppre)
    return r
   
    
class ASTDNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)+" not found"
        
class ASTD():
    """An ASTD class """    

    def __init__(self, newName = "") :
        """ Constructor for an ASTD
        newName -- name of the ASTD to be constructed (optional) """
        if newName == "" :
            global nextNumber
            newName = "_default" + str(nextNumber)
            nextNumber = nextNumber + 1
        self._name = newName
        
    def getName(self) :
        """ Getter for the name """
        return self._name  
        
    def getType(self) :
        """ Getter for the type """
        return self._t         
        
    def Bprint(self):
        m = self.toB()
        rstring = []
        rstring.append('MACHINE')
        rstring.append(s+m['MACHINE'])
        rstring.append('SETS')
        rstring.append(s+((' ;\n'+s).join(m['SETS'])))
        rstring.append('VARIABLES')
        rstring.append(s+((' ,\n'+s).join(m['VARIABLES'])))
        rstring.append('INVARIANT')
        rstring.append(s+((' &\n'+s).join(m['INVARIANT'])))
        rstring.append('INITIALISATION')
        rstring.append(s+((' ||\n'+s).join(m['INITIALISATION'])))
        rstring.append('OPERATIONS')        
        for k in sorted(m['OPERATIONS'].keys()) : 
            i = m['OPERATIONS'][k]
            if len(i['param']) != 0 :
                rstring.append(s + i['name']+"("+ ','.join(i['param']) +") = ")
            else :
                rstring.append(s + i['name']+" = ")
            rstring.append(s+t+"PRE")
            rstring.append(preIndent(getPre(i['PRE'])))
            rstring.append(s+t+"THEN")
            rstring.append(thenIndent(getThen(i['THEN'])))
            rstring.append(s+t+"END ;\n")
        rstring[-1]=rstring[-1].replace("END ;\n","END\n")
        rstring.append('END')        
        for l in rstring:
            print(l)
        
    def __str__(self):
        return "ASTD named " + self._name + " of type " + self._t
