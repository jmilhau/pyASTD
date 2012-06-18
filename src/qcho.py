import astd

s1 = astd.Elem('s1')
s2 = astd.Elem('s2')
s3 = astd.Elem('s3')
c = astd.Automaton(s1,"c")
c.addState(s2)
c.addDFState(s3)
c.addLocalTransition(s1,s2,('e1','x'))
c.addLocalTransition(s2,s3,('e2','x'))

d = astd.qChoice(c,"x","{x4,x5,x6}")
e = astd.Kleene(d)

e.Bprint()
