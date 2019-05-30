import ast

config = "{1:{'type':1,'str':'aaa'},2:{'type':2,'str':'bbb','tt':{'sun':1}},3:'test'}"
#config = ""
tab = ast.literal_eval(config)
"""
if type(tab).__name__ == "dict":
    #print "tab is dict:",tab
    for k in tab:
        if type(tab[k]).__name__ == 'dict':
            #print "tab[k] is dict:",tab[k]
            for k2 in tab[k]:
                if type(tab[k][k2]).__name__ == 'dict':
                    #print "tab[k][k2] is dict:",tab[k][k2]
                    for k3 in tab[k][k2]:
                        print "k=",k3,",v=",tab[k][k2][k3]
                else:
                    print "k=",k2,",v=",tab[k][k2]
        else:
            print "k=",k,",v=",tab[k]
else:
    print type(tab)
"""

if tab[1].has_key('type'):
    print tab[1]['type']
else:
    print "no tab[1]['type']"

if tab[1].has_key('type1'):
    print tab[1]['type1']
else:
    print "no tab[1]['type1']"