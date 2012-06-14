import astd

s1 = astd.Elem('s1')
s2 = astd.Elem('s2')
s3 = astd.Elem('s3')
s4 = astd.Elem('s4')

a = astd.Automaton(s1,"a")
a.addDFState(s2)
a.addLocalTransition(s1,s2,('e1',))
a.addLocalTransition(s2,s2,('e2',))


b = astd.Automaton(s3,"b")
b.addDFState(s4)
b.addLocalTransition(s3,s4,('e3',))


c = astd.Kleene(a,"c")
d = astd.Kleene(b,"d")
e = astd.Sequence(c,d,"e")
f = astd.Kleene(e,"ff")

f.Bprint()