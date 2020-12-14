from math import sqrt
import dendrogram

#Llegir el fitxer i retornar els noms dels blogs, els noms de les features i els numeros que apareixen
def readfile(filename):
	lines = [line for line in open(filename,"r")]
	colnames = lines[0].strip().split('\t')[1:]
	rownames = []
	data = []
	for line in lines[1:]:
		p=line.strip().split('\t')
		rownames.append(p[0])
		data.append([float(x) for x in p [1:]])
	return rownames, colnames, data
	
def euclidean(v1, v2):
	distance = sqrt(sum([(v1[i] - v2[i])**2 for i in range(len(v1))]))
	return 1/1+distance
	
def pearson(v1, v2):
	sum1 = sum(v1)
	sum2 = sum(v2)
	
	sum1Sq = sum([pow(v, 2) for v in v1])
	sum2Sq = sum([pow(v, 2) for v in v2])
	
	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])
	
	num = pSum-(sum1*sum2/len(v1))
	den = sqrt((sum1Sq-pow(sum1, 2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
	if den == 0: return 0
	return 1.0-num/den
	
class bicluster:
	def __init__(self, vec, left=None, right=None, dist=0.0, cid=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = cid
		self.distance = dist

def hcluster(rows, distance=euclidean):
	distances={}
	currentclustid=-1
	
	# Crear un cluster per cada blog
	clust = [bicluster(rows[i], cid=i) for i in range(len(rows))]
	
	# Mentre hi hagi més d'un cluster
	while len(clust) > 1:
		lowestpair = (0, 1)
		closest = distance(clust[0].vec, clust[1].vec)
		
		# Buscar els 2 clusters més propers
		for i in range(len(clust)):
			for j in range(i + 1, len(clust)):
				pair = (clust[i].id, clust[j].id)
				if pair not in distances:
					distances[pair] = distance(clust[i].vec, clust[j].vec)
					
				if distances[pair] < closest:
					closest = distances[pair]
					lowestpair = (i, j)
					
		# Unir els 2 clusters més propers en un de sol
		mergevec = [(clust[lowestpair[0]].vec[lowestpair[1]]+clust[j].vec[k])/2.0 for k in range(len(clust[i].vec))]
		
		newcluster = bicluster(mergevec, clust[lowestpair[0]], clust[lowestpair[1]], closest, currentclustid)
		
		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)
		
	return clust[0]
	
blognames, words, data = readfile("blogdata_full.txt")
clst = hcluster(data)
dendrogram.drawdendrogram(clst, "hola.jpg")

