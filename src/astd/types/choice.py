from .astd import *

class Choice(ASTD):
    """An Choice ASTD class"""    
    _t = "cho"
        
    def __init__(self, b, c, newname="" ) :
        """ Constructor for a Choice ASTD
        b -- astd that is the LHS operand of the choice ASTD (mandatory)
        c -- astd that is the RHS operand of the choice ASTD (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b
        self.c = c

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + self.getName()] = "none"
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        fb = self.b.getBfinal()
        fc = self.c.getBfinal()
        ifb = self.b.getBfinal()
        ifc = self.c.getBfinal()
        ib = self.b.getInit()
        ic = self.c.getInit()
        
        for k, v in ib.items():
            ifb.replace(k, v)
        for k, v in ic.items():
            ifc.replace(k, v)

        f1 = "((State_" + self.getName() + " = none) => ( "+ifb+" & "+ifc+" ))&\n" 
        f1 += "((State_" + self.getName() + " = leftS) => "+fb+" )&\n"        
        f1 += "((State_" + self.getName() + " = rightS) => "+fc+" )&\n"        
        return f1
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        subB = self.b.toB()
        subC = self.c.toB()
                    
        machine = {}
        machine['MACHINE'] = n
        
        machine['SETS'] = subB['SETS'] + list(set(subC['SETS']) - set(subB['SETS']))
        if machine['SETS'].count("ChoiceState = {none , leftS , rightS}") == 0 :
            machine['SETS'] = machine['SETS'] + ["ChoiceState = {none , leftS , rightS}"]                          
        
        machine['VARIABLES'] = subB['VARIABLES'] + subC['VARIABLES']
        machine['VARIABLES'] += [ "State_" + n ]
        
        machine['INVARIANT'] = subB['INVARIANT'] + subC['INVARIANT']
        machine['INVARIANT'] += [ "State_" + n + " :  ChoiceState" ]

        machine['INITIALISATION'] = subB['INITIALISATION'] + subC['INITIALISATION']
        machine['INITIALISATION'] += [ "State_" + n + " := none" ]               
        machine['OPERATIONS'] =  {}  
        
#        operations in B              
        ib = self.b.getInit()
        for subopname,subop in subB['OPERATIONS'].items():
            op = {}
            op['param'] = subop['param']   
            op['name'] = subop['name']
            op['TYPE'] = subop['TYPE']
            op['PRE'] = []
            op['THEN'] = []  
                        
            preB1 = list(subop['PRE'])                        
            preB3 = getPre(subop['PRE'])                                    
            thenB1 = getThen(subop['THEN'])
            thenB3 = getThen(subop['THEN'])
            
            for k, v in ib.items():
                map(lambda x: x.replace(k, v),preB1)
                thenB1.replace(":= "+k, ":= "+v)
            if len(preB1)>1:
                pre1 = " or ".join(preB1) 
            else :
                pre1 = "".join(preB1)
                
            pre1 = "( State_" + n + " = none & ("+ pre1 +") )"                  
            pre3 = "( State_" + n + " = leftS & ("+ preB3 +") )"                  
            
            then1 = "State_" + n + " := leftS ||\n"+ thenB1 
            then3 = thenB3
                       
            op['PRE'].append(pre1)           
            op['THEN'].append((pre1,then1))
            op['PRE'].append(pre3)           
            op['THEN'].append((pre3,then3))

            machine['OPERATIONS'][subopname] = op 

#        operations in C
        ic = self.c.getInit()
        for subopname,subop in subC['OPERATIONS'].items():
            if subopname in machine['OPERATIONS'] :
                op = dict(machine['OPERATIONS'][subopname])
                op['TYPE'] += subop['TYPE']
            else :
                op = {}
                op['param'] = subop['param']   
                op['name'] = subop['name']
                op['PRE'] = []
                op['THEN'] = []  
                op['TYPE'] = subop['TYPE']

            preC2 = list(subop['PRE'])                        
            preC4 = getPre(subop['PRE'])                                    
            thenC2 = getThen(subop['THEN'])
            thenC4 = getThen(subop['THEN'])
            
            for k, v in ib.items():
                map(lambda x: x.replace(k, v),preC2)
                thenC4.replace(":= "+k, ":= "+v)
            if len(preC2)>1:
                pre2 = " or ".join(preC2) 
            else :
                pre2 = "".join(preC2)
                
            pre2 = "( State_" + n + " = none & ("+ pre2 +") )"                  
            pre4 = "( State_" + n + " = rightS & ("+ preC4 +") )"                  
            
            then2 = "State_" + n + " := rightS ||\n"+ thenC2 
            then4 = thenC4
                       
            op['PRE'].append(pre2)           
            op['THEN'].append((pre2,then2))
            op['PRE'].append(pre4)           
            op['THEN'].append((pre4,then4))

            machine['OPERATIONS'][subopname] = op 

        return machine
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "    first astd : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "   second astd : " + self.c._name + " of type " + self.c._t +"\n"
        txt += "End of " + self._name        
        return txt
        