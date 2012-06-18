from .astd import *

class Call(ASTD):
    """An Call ASTD class"""    
    _t = "cal"
        
    def __init__(self, b, newname="", p={} ) :
        """ Constructor for a call ASTD
        b -- astd that is the operand of the call ASTD (mandatory)
        newName -- name of the elem ASTD to be constructed 
        p -- dictionary mapping variables to values (empty by default)"""
        super().__init__(newname)
        self.b = b
        self.p = p

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + self.getName()] = "notcalled"
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
        for k, v in self.p.items():
            pinit.replace(k, v) 
            p.replace(k, v)               
        finalp = "(State_" + self.getName() + " = notcalled => "+ pinit +" )&\n"
        finalp += "(State_" + self.getName() + " = called => "+ p +" )"
        return finalp
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        sub = self.b.toB()
                    
        machine = {}
        machine['MACHINE'] = n
        machine['SETS'] = sub['SETS']
        if sub['SETS'].count("CallState = {called , notcalled}") == 0 :
            machine['SETS'] += ["CallState = {called , notcalled}"]                          
        machine['VARIABLES'] = sub['VARIABLES'] + [ "State_" + n ]
        machine['INVARIANT'] = sub['INVARIANT'] + [ "State_" + n + " :  CallState" ]
        machine['INITIALISATION'] =  sub['INITIALISATION'] + [ "State_" + n + " := notcalled" ]               
        machine['OPERATIONS'] =  {}        

        for subopname,subop in sub['OPERATIONS'].items():
            op = {}
            op['param'] = subop['param']   
            op['name'] = subop['name']
            op['TYPE'] = subop['TYPE']
            op['PRE'] = []
            op['THEN'] = []                   
            
            f = self.b.getBfinal()
            i = self.b.getInit()

            subpre = list(subop['PRE'])            
            subprei = list(subop['PRE'])
            subthen = getThen(subop['THEN'])
            subtheni = getThen(subop['THEN'])
            for k, v in i.items():
                map(lambda x: x.replace(k, v),subprei)
                subtheni.replace(":= "+k, ":= "+v)
            for k, v in self.p.items():
                map(lambda x: x.replace(k, v),subpre)
                map(lambda x: x.replace(k, v),subprei)
                subtheni.replace(":= "+k, ":= "+v)            
            pre = "( State_" + n + " = notcalled & "            
            if len(subprei)>1:
                pre += "(" + " or ".join(subprei) + ")"                        
            else :
                pre += "".join(subprei)
            pre +=")"    
            if len(subpre)>1:
                pre2 = "(" + " or ".join(subprei) + ")"                        
            else :
                pre2 = "".join(subprei)

            op['PRE'].append(pre)           
            op['PRE'].append(pre2)            

            op['THEN'].append((pre,"State_" + n + " := called ||\n"+subtheni))
            op['THEN'].append((pre2,subthen))
                        
            machine['OPERATIONS'][subopname] = op 
            
        return machine        
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "   Sub ASTD : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "End of " + self._name        
        return txt
        
    
      