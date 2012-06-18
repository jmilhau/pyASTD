from .astd import *

class Sequence(ASTD):
    """An Sequence ASTD class"""    
    _t = "seq"
        
    def __init__(self, b, c, newname="" ) :
        """ Constructor for a Sequence ASTD
        b -- astd that is the LHS operand of the sequence ASTD (mandatory)
        c -- astd that is the RHS operand of the sequence ASTD (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b
        self.c = c

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + self.getName()] = "fst"
        r = dict(list(r.items()) + list(self.b.getInit().items()))
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        pb = self.b.getBfinal()
        pc = self.C.getBfinal()
        pcinit = self.C.getBfinal()
        i = self.c.getInit()        
        for k, v in i.items():
            pcinit.replace(k, v)
        finalp = "((State_" + self.getName() + " = fst) => (("+pb+") & ("+pcinit+")))&\n" 
        finalp += "((State_" + self.getName() + " = snd) => ("+pc+"))" 
        return finalp
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        subB = self.b.toB()
        subC = self.c.toB()
                    
        machine = {}
        machine['MACHINE'] = n
        
        machine['SETS'] = subB['SETS'] + list(set(subC['SETS']) - set(subB['SETS']))
        if machine['SETS'].count("SequenceState = {fst , snd}") == 0 :
            machine['SETS'] = machine['SETS'] + ["SequenceState = {fst , snd}"]                          
        
        machine['VARIABLES'] = subB['VARIABLES'] + subC['VARIABLES']
        machine['VARIABLES'] += [ "State_" + n ]
        
        machine['INVARIANT'] = subB['INVARIANT'] + subC['INVARIANT']
        machine['INVARIANT'] += [ "State_" + n + " :  SequenceState" ]

        machine['INITIALISATION'] = subB['INITIALISATION'] + subC['INITIALISATION']
        machine['INITIALISATION'] += [ "State_" + n + " := fst" ]               
        machine['OPERATIONS'] =  {}  
        
#        operations in B              
        for subopname,subop in subB['OPERATIONS'].items():
            op = {}
            op['param'] = subop['param']   
            op['name'] = subop['name']
            op['PRE'] = []
            op['THEN'] = []  
                        
            subpreB = getPre(subop['PRE'])                        
            pre1 = "( State_" + n + " = fst & ("+ subpreB +"))"                  
            subthen1 = getThen(subop['THEN'])
           
            op['PRE'].append(pre1)           
            op['THEN'].append((pre1,subthen1))
            machine['OPERATIONS'][subopname] = op 

#        operations in C
        i = self.c.getInit()
        for subopname,subop in subC['OPERATIONS'].items():
            if subopname in machine['OPERATIONS'] :
                op = dict(machine['OPERATIONS'][subopname])
            else :
                op = {}
                op['param'] = subop['param']   
                op['name'] = subop['name']
                op['PRE'] = []
                op['THEN'] = []  

            subpre2 = list(subop['PRE'])    
            subthen2 = getThen(subop['THEN'])

            if len(subpre2)>1:
                pre2 = " or ".join(subpre2) 
            else :
                pre2 = "".join(subpre2)
            for k, v in i.items():
                map(lambda x: x.replace(k, v),subpre2)
                subthen2.replace(":= "+k, ":= "+v)

            pre2 = "( State_" + n + " = fst &\n("+ self.b.getBfinal() +") &\n("+ pre2 +"))"
            subpre3 = getPre(subop['PRE'])            
            pre3 = "( State_" + n + " = snd & ("+ subpre3 +"))"                  
            subthen3 = getThen(subop['THEN'])

            op['PRE'].append(pre2)           
            op['THEN'].append((pre2,"State_" + n + " := snd ||\n"+subthen2))

            op['PRE'].append(pre3)           
            op['THEN'].append((pre3,subthen3))

            machine['OPERATIONS'][subopname] = op 

        return machine
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "    first astd : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "   second astd : " + self.c._name + " of type " + self.c._t +"\n"
        txt += "End of " + self._name        
        return txt
        