from utils import *
import time

# Checking triangle inequality
# Note that violations are only in the equality cases due to the precision error

Glst = nx.readwrite.graph6.read_graph6('graph5c.g6')
violated = []

for i in range(len(Glst)):
    G = Glst[i]
    for j in range(i+1, len(Glst)):
        H = Glst[j]
        GH = round(distance(G, H, max_iter=3), 6)
        
        for l in range(j+1, len(Glst)):
            F = Glst[l]
        
            GF = round(distance(G, F, max_iter=3), 6)
            FH = round(distance(F, H, max_iter=3), 6)

            a = GH + GF >= FH
            b = GH + FH >= GF
            c = FH + GF >= GH
            if int(a)+int(b)+int(c) != 3:
                print('Graphs no. {}, no. {} and no. {} violate triangle inequality'.format(i, j, l))
                print('Distances are {}, {}, {}'.format(GH, GF, FH))

         
