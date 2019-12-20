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



G=nx.Graph()
for i in range (len(LIT)):
    G.add_edges_from([(LIT[i][0], LIT[i][1])])

nx.draw(G, with_labels=False, font_weight='bold', size_nodes=1)
plt.title("LIT")
plt.show()

print("Numero de nodos=")
print(G.number_of_nodes())
print("Numero de enlaces=")
print(G.number_of_edges())


#G1=nx.Graph()
#for i in range (len(APMS)):
#    G1.add_edges_from([(APMS[i][0], APMS[i][1])])

#nx.draw(G1, with_labels=False, font_weight='bold', size_nodes=1)
#plt.title("Y2H")
#plt.show()


#G2=nx.Graph()
#for i in range (len(Y2H)):
#    G2.add_edges_from([(Y2H[i][0], Y2H[i][1])])

#nx.draw(G2, with_labels=False, font_weight='bold', size_nodes=1)
#plt.title("AP-MS")
#plt.show()