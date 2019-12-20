import networkx as nx
import matplotlib.pylab as plt
import numpy as np

def ldata(archive):
        f=open(archive)
        data=[]
        for line in f:
            line=line.strip()
            col=line.split()
            data.append(col)	
        return data
    
LIT=ldata("yeast_LIT.txt")
APMS=ldata("yeast_AP-MS.txt")
Y2H=ldata("yeast_Y2H.txt")

##ej 1
print("1)")
print("a)")
G1=nx.Graph()
for i in range (len(LIT)):
    G1.add_edges_from([(LIT[i][0], LIT[i][1])])
    
print("red LIT")
nx.draw(G1, with_labels=False, font_weight='bold', size_nodes=1)
plt.show()

G2=nx.Graph()
for i in range (len(APMS)):
    G2.add_edges_from([(APMS[i][0], APMS[i][1])])
    
print("red APMS")
nx.draw(G2, with_labels=False, font_weight='bold', size_nodes=1)
plt.show()

G3=nx.Graph()
for i in range (len(Y2H)):
    G3.add_edges_from([(Y2H[i][0], Y2H[i][1])])
    
print("red Y2H")
nx.draw(G3, with_labels=False, font_weight='bold', size_nodes=1)
plt.show()


print("b)")
##nùmero de nodos
N1=G1.number_of_nodes()
print("i) el número de nodos de la red LIT es",N1)
N2=G2.number_of_nodes()
print("i) el número de nodos de la red APMS es",N2)
N3=G3.number_of_nodes()
print("i) el número de nodos de la red Y2h es",N3)

##nùmero de enlaces
E1=G1.number_of_edges()
print("ii) el número de enlaces de la red LIT es",E1)
E2=G2.number_of_edges()
print("ii) el número de enlaces de la red APMS es",E2)
E3=G3.number_of_edges()
print("ii) el número de enlaces de la red Y2H es",E3)

##Red dirigida ?

LIT_temp=LIT
for enlace in LIT:
    if enlace[1] != enlace[0] and [enlace[1], enlace[0]] in LIT_temp:
        print("iii) la red LIT es dirigida")
    else:
        print("iii) la red LIT es no-dirigida")
        break
    
APMS_temp=APMS
for enlace in APMS:
    if enlace[1] != enlace[0] and [enlace[1], enlace[0]] in APMS_temp:
        print("iii) la red APMS es dirigida")
    else:
        print("iii) la red APMS es no-dirigida")
        break
    
Y2H_temp=Y2H
for enlace in Y2H:
    if enlace[1] != enlace[0] and [enlace[1], enlace[0]] in Y2H_temp:
        print("iii) la red Y2H es dirigida")
    else:
        print("iii) la red Y2H es no-dirigida")
        break
            
##Grado medio
G1.degree
deg1= dict(G1.degree())
prom1=0
suma1=0
for grado in deg1.values():
    suma1=suma1+grado
prom=suma1/N1
print("iv.1) el grado medio de la red LIT es", prom)

    
G2.degree
deg2= dict(G2.degree())
prom2=0
suma2=0
for grado in deg2.values():
    suma2=suma2+grado
prom=suma2/N2
print("iv.1) el grado medio de la red APMS es", prom)
    
G3.degree
deg3= dict(G3.degree())
prom3=0
suma3=0
for grado in deg3.values():
    suma3=suma3+grado
prom=suma3/N3
print("iv.1) el grado medio de la red Y2H es", prom)

##Grado màximo y mìnimo
deg1= dict(G1.degree())

valores_grado1=[]
for grado in deg1.values():
    valores_grado1.append(grado)
print("iv.2) el grado máximo de la red LIT es",max(valores_grado1))
print("iv.3) el grado mínimo de la red LIT es",min(valores_grado1))
    
    
deg2= dict(G2.degree())

valores_grado2=[]
for grado in deg2.values():
    valores_grado2.append(grado)
print("iv.2) el grado máximo de la red APMS es",max(valores_grado2))
print("iv.3) el grado mínimo de la red APMS es",min(valores_grado2))
    
deg3= dict(G3.degree())

valores_grado3=[]
for grado in deg3.values():
    valores_grado3.append(grado)
print("iv.2) el grado máximo de la red Y2H es",max(valores_grado3))
print("iv.3) el grado mínimo de la red Y2H es",min(valores_grado3))

##Densidad

print("v) la densidad de la red LIT es",nx.density(G1))
print("v) la densidad de la red APMS es",nx.density(G2))
print("v) la densidad de la red Y2H es",nx.density(G3))

#Coef de Clústering promedio
    
CC1=nx.average_clustering(G1)
print("el coef de Clústering <C> de la red LIT es", CC1)
CC2=nx.average_clustering(G2)
print("el coef de Clústering <C> de la red APMS es", CC2)
CC3=nx.average_clustering(G3)
print("el coef de Clústering <C> de la red Y2H es", CC3)
    
    
    
#Coef  de Clustering Global


CCG1=nx.transitivity(G1)
print("el coef de Clústering global de la red LIT es", CCG1)

CCG2=nx.transitivity(G2)
print("el coef de Clústering global de la red APMS es", CCG2)

CCG3=nx.transitivity(G3)
print("el coef de Clústering global de la red Y2H es", CCG3)

CG1=max(nx.connected_component_subgraphs(G1), key=len)
D1=nx.diameter(CG1)
print("el diámetro de la red LIT es",  D1)

CG2=max(nx.connected_component_subgraphs(G2), key=len)
D2=nx.diameter(CG2)
print("el diámetro de la red APMS es",  D2)

CG3=max(nx.connected_component_subgraphs(G3), key=len)
D3=nx.diameter(CG3)
print("el diámetro de la red Y2H es",  D3)

    
    
