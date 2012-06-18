from .astd import *

class Guard(ASTD):
    """An Guard ASTD class"""    
    _t = "gua"
        
    def __init__(self, b, g, newname="" ) :
        """ Constructor for a Guard ASTD
        b -- astd that is the operand of the guard ASTD (mandatory)
        g -- a predicate that is the Guard of the ASTD with logical operators : &, or, not (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b
        self.g = g

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + self.getName()] = "notchecked"
        r = dict(list(r.items()) + list(self.b.getInit().items()))
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        p = self.b.getBfinal()       
        pinit = self.b.getBfinal()
        i = self.b.getInit()            
        for k, v in i.items():
            pinit.replace(k, v)               
        finalp = "(State_" + self.getName() + " = notchecked => "+ pinit +" )&\n"
        finalp += "(State_" + self.getName() + " = checked => "+ p +" )"
        return finalp
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        sub = self.b.toB()
                    
        machine = {}
        machine['MACHINE'] = n
        machine['SETS'] = sub['SETS']
        if sub['SETS'].count("GuardState = {checked , notchecked}") == 0 :
            machine['SETS'] += ["GuardState = {checked , notchecked}"]                          
        machine['VARIABLES'] = sub['VARIABLES'] + [ "State_" + n ]
        machine['INVARIANT'] = sub['INVARIANT'] + [ "State_" + n + " :  GuardState" ]
        machine['INITIALISATION'] =  sub['INITIALISATION'] + [ "State_" + n + " := notchecked" ]               
        machine['OPERATIONS'] =  {}        

        for subopname,subop in sub['OPERATIONS'].items():
            op = {}
            op['param'] = subop['param']   
            op['name'] = subop['name']
            op['PRE'] = []
            op['THEN'] = []  
            op['TYPE'] = subop['TYPE']                 
            
            f = self.b.getBfinal()
            i = self.b.getInit()
            
            subprei = list(subop['PRE'])
            subthen = getThen(subop['THEN'])
            subtheni = getThen(subop['THEN'])
            for k, v in i.items():
                map(lambda x: x.replace(k, v),subprei)
                subtheni.replace(":= "+k, ":= "+v)
            pre = "("+ self.g +") & State_" + n + " = notchecked & "            
            if len(subprei)>1:
                pre += "(" + " or ".join(subprei) + ")"                        
            else :
                pre += "".join(subprei)
            op['PRE'].append("("+pre+")")           
            op['PRE'].append(getPre(subop['PRE']))            

            op['THEN'].append((pre,"State_" + n + " := checked ||\n"+subtheni))
            op['THEN'].append((getPre(subop['PRE']),subthen))
                        
            machine['OPERATIONS'][subopname] = op 
            
        return machine        
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "   Sub ASTD : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "End of " + self._name        
        return txt
        
    
      