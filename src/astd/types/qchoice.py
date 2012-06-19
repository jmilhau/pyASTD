from .astd import *

class qChoice(ASTD):
    """An qchoice ASTD class"""    
    _t = "kle"
        
    def __init__(self, b, x, t, newname="" ) :
        """ Constructor for a qchoice ASTD
        b -- astd that is the operand of the qchoice ASTD (mandatory)
        x -- variable name of the qchoice (mandatory)
        t -- set of the quantified variable values (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b
        self.x = x
        self.t = t

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + self.getName()] = "notchosen"
        r = dict(list(r.items()) + list(self.b.getInit().items()))
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        pb = self.b.getBfinal()
        pbi = self.b.getBfinal()
        i = self.b.getInit()        
        i[self.x] = "vv"
        pb.replace(self.x,"Value_" + self.getName())
        for k, v in i.items():
            pbi.replace(k, v)
        finalp = "((State_" + self.getName() + " = notchosen) => ( #vv. ( vv : T_" + self.getName() +" & ("+pbi+"))))&\n" 
        finalp += "((State_" + self.getName() + " = chosen) => ( "+pb+" ))&\n" 
        return finalp
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        sub = self.b.toB()
                    
        machine = {}
        machine['MACHINE'] = n       
        
        machine['SETS'] = sub['SETS'] + ["T_" + self.getName()+" = "+self.t]        
        if sub['SETS'].count("qChoiceState = {chosen , notchosen}") == 0 :
            machine['SETS'] += ["qChoiceState = {chosen , notchosen}"]                          
        machine['VARIABLES'] = sub['VARIABLES'] + [ "State_" + n ]
        machine['VARIABLES'] += [ "Value_" + n ]
        machine['INVARIANT'] = sub['INVARIANT'] + [ "State_" + n + " :  qChoiceState" ]
        machine['INVARIANT'] += [ "Value_" + n + " :  T_" + n ]
        machine['INITIALISATION'] =  sub['INITIALISATION'] + [ "State_" + n + " := notchosen" ] 
        machine['INITIALISATION'] += [ "Value_" + n + " :: T_" + n ]               
        machine['OPERATIONS'] =  {}        
            
        for subopname,subop in sub['OPERATIONS'].items():
            op = {}
            op['param'] = subop['param']   
            op['name'] = subop['name']
            op['PRE'] = []
            op['THEN'] = []       
            op['TYPE'] = subop['TYPE'] + [ self.x + " :  T_" + self.getName()]
                                
            f = self.b.getBfinal()
            i = self.b.getInit()
            
            subpre = getPre(subop['PRE'])
            subthen = getThen(subop['THEN'])

            subprei = list(subop['PRE'])
            subtheni = getThen(subop['THEN'])


            for k, v in i.items():
                map(lambda x: x.replace(k, v),subprei)
                subtheni.replace(":= "+k, ":= "+v)

            pre1 = "State_" + n + " = notchosen"
            
            if len(subprei)>0:
                pre1 += " &\n( " + " or ".join(subprei) + " )"                        
                
            pre2 = "State_" + n + " = chosen & Value_" + n + " = "+self.x
            if len(subpre)>0 :
                pre2 += " &\n"+subpre
                
            op['PRE'].append("("+pre1+")")           
            op['PRE'].append("("+pre2+")")            

            op['THEN'].append((pre1,"State_" + n + " := chosen ||\n Value_" + n + " := "+self.x+" ||\n"+subtheni))
            op['THEN'].append((pre2,subthen))
                        
            machine['OPERATIONS'][subopname] = op        
            
        return machine        
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "   Sub ASTD : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "End of " + self._name        
        return txt
        
    
      