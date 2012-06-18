from .astd import *

class Kleene(ASTD):
    """An Kleene Closure ASTD class"""    
    _t = "kle"
        
    def __init__(self, b, newname="" ) :
        """ Constructor for a Kleene ASTD
        b -- astd that is the operand of the Closure Kleene ASTD (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + self.getName()] = "notstarted"
        r = dict(list(r.items()) + list(self.b.getInit().items()))
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        finalp = "State_" + self.getName() + " = notstarted" 
        p = self.b.getBfinal()
        if p != "true":
            finalp += " or ("+ p +")"        
        return finalp
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        sub = self.b.toB()
                    
        machine = {}
        machine['MACHINE'] = n
        machine['SETS'] = sub['SETS']
        if sub['SETS'].count("KleeneState = {started , notstarted}") == 0 :
            machine['SETS'] += ["KleeneState = {started , notstarted}"]                          
        machine['VARIABLES'] = sub['VARIABLES'] + [ "State_" + n ]
        machine['INVARIANT'] = sub['INVARIANT'] + [ "State_" + n + " :  KleeneState" ]
        machine['INITIALISATION'] =  sub['INITIALISATION'] + [ "State_" + n + " := notstarted" ]               
        machine['OPERATIONS'] =  {}        

        for subopname,subop in sub['OPERATIONS'].items():
            op = {}
            op['param'] = subop['param']   
            op['name'] = subop['name']
            op['PRE'] = []
            op['THEN'] = []                   
            
            f = self.b.getBfinal()
            i = self.b.getInit()
            
            subpre = list(subop['PRE'])
            subthen = getThen(subop['THEN'])
            for k, v in i.items():
                map(lambda x: x.replace(k, v),subpre)
                subthen.replace(":= "+k, ":= "+v)
            pre = "(("+ f +") or State_" + n + " = notstarted) &\n"
            
            if len(subpre)>1:
                pre += "( " + " or ".join(subpre) + " )"                        
            else :
                pre += "".join(subpre)
                
            op['PRE'].append("("+pre+")")           
            op['PRE'].append(getPre(subop['PRE']))            

            op['THEN'].append((pre,"State_" + n + " := started ||\n"+subthen))
            op['THEN'].append((getPre(subop['PRE']),"State_" + n + " := started ||\n"+getThen(subop['THEN'])))
                        
            machine['OPERATIONS'][subopname] = op    
            
        return machine        
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "   Sub ASTD : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "End of " + self._name        
        return txt