import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

G = nx.read_gml('netscience.gml')
#(i) y (ii)
K_dict = {}
for n in G.nodes():
    k = G.degree(n)
    p = 0
    N = G.neighbors(n)
    L = N.__length_hint__() #L = cantidad de vecinos de n
    for nn in N:
        p = p + G.degree(nn)/L
    #hasta este punto, k = grado(n) y p = promedio de sus vecinos
    if k not in K_dict.keys():
        K_dict[k] = [p]
    else:
        K_dict[k].append(p)

#K_lens = {}
#for k in K_dict.keys():
#    K_lens[k] = len(list(K_dict[k]))

K_nn = {}
for k in K_dict.keys():
    K_nn[k] = np.mean(K_dict[k])

#solo falta ordenar las abcisas para plotear
xy_plot = sorted(K_nn.items(),key=lambda x:x[0])
x_plot = [t[0] for t in xy_plot]
y_plot = [t[1] for t in xy_plot]
#vamos a quitar el degree 0, por si hay
#esto lo hacemos para que el log no tenga que dividir por cero
if x_plot[0] == 0:
    x_plot = x_plot[1:]
    y_plot = y_plot[1:]

logx = np.log(x_plot)
logy = np.log(y_plot)


#(iii)


slope, intercept, r_value, p_value, std_err = stats.linregress(logx, logy)

#X = np.linspace(min(x_plot),max(x_plot))
logX = np.linspace(min(logx),max(logx),1000)
logY = intercept + slope*logX

#plt.figure(1)
#plt.subplot(121)
plt.plot(logx,logy)
plt.plot(logX,logY)
plt.grid()
plt.show()

#plt.subplot(122)

#plt.plot(x_plot,y_plot)




#(iv)


K = []
for x in G.nodes():
    K.append(G.degree(x))

S1 = sum(K)
S2 = sum([k**2 for k in K])
S3 = sum([k**3 for k in K])
Se = 2*sum([G.degree(e[0])*G.degree(e[1]) for e in G.edges()])

r = (S1*Se-S2**2)/(S1*S3-S2**2)


