La deformazione è d(x, y, z) vettore con (d1, d2, d3) INCOGNITA 
Ho un piano f(i) = alpha*x + beta*y + gamma con coefficienti incogniti per ogni sensore
Conosciamo le LOS (versori di direzioni di vista) (l1, l2, l3)(i)
Conosciamo le misure (rilevazioni) lungo le linee di vista mi, mj, mk


quante equazioni possiamo scrivere? tante quante le misure (i, j, k)
tante sia per lo stesso punto che per punti diversi (cambio punto e sensore)

d1(x1, y, z) * l1(i= 1) + d2*l2 + d3*l3 + alpha(i=1)*x1 + beta*y + gamma - m(x1, y, z, i=1) = 0
d1(x1, y, z) * l1(i= 2) + d2*l2 + d3*l3 + alpha(i=2)*x1 + beta*y + gamma - m(x1, y, z, i=2) = 0
d1(x1, y, z) * l1(i= 3) + d2*l2 + d3*l3 + alpha(i=3)*x1 + beta*y + gamma - m(x1, y, z, i=3) = 0
d1(x1, y, z) * l1(i= 4) + d2*l2 + d3*l3 + alpha(i=4)*x1 + beta*y + gamma - m(x1, y, z, i=4) = 0

d1 = d2=d3 =0

min somma delta + somma d 
(le x sono note)

csv
funzione che crea dati dimensione che scelgo 
leggo come dask dataframe
applico clusterizzazione
uscita: oggetto in formato sparso 
