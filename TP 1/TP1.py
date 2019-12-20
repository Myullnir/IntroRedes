import networkx as nx
import matplotlib.pylab as plt

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



G1=nx.Graph()
for i in range (len(LIT)):
    G1.add_edges_from([(LIT[i][0], LIT[i][1])])
    
# nx.draw(G1, with_labels=False, font_weight='bold', size_nodes=1)
plt.show()

G2=nx.Graph()
for i in range (len(APMS)):
    G2.add_edges_from([(APMS[i][0], APMS[i][1])])

# nx.draw(G2, with_labels=False, font_weight='bold', size_nodes=1)
# plt.show()

G3=nx.Graph()
for i in range (len(Y2H)):
    G3.add_edges_from([(Y2H[i][0], Y2H[i][1])])

# nx.draw(G3, with_labels=False, font_weight='bold', size_nodes=1)
# plt.show()

##nùmero de nodos
N1=G1.number_of_nodes()
print("i) el número de nodos es",N1)
G2.number_of_nodes()
G3.number_of_nodes()

##nùmero de enlaces
E1=G1.number_of_edges()
print("ii) el número de enlaces es",E1)
G2.number_of_edges()
G3.number_of_edges()

##Red dirigida ?

LIT_temp=LIT
for enlace in LIT:
    if enlace[1] != enlace[0] and [enlace[1], enlace[0]] in LIT_temp:
        print("iii) la red es dirigida")
    else:
        print("iii) la red es no-dirigida")
        break
            
##Grado medio
G1.degree
deg = dict(G1.degree())
prom=0
suma=0
for grado in deg.values():
    suma=suma+grado
prom=suma/N1
print("iv.1) el grado medio es", prom)

##Grado màximo y mìnimo
deg = dict(G1.degree())

a=[]
for grado in deg.values():
    a.append(grado)
print("iv.2) el grado màximo es",max(a))
print("iv.3) el grado mìnimo es",min(a))

##Densidad

print("v) la densidad de la red es",nx.density(G1))

##Coef  de Clustering

for grado in deg.values():
    T_enlaces=E1*(E1-1)/2
    C=grado/T_enlaces
    C_prom=C/N1
print(C_prom)
