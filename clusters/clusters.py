from math import sqrt

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
	
class bicluster:
	def __init__(self, vec, left=None, right=None, dist=0.0, cid=None):
	self.left = left
	self.right = right
	self.vec = vec
	self.cid = cid
	self.distance = distance

def hcluster(rows, distance=euclidean):
	distances={}
	currentclustid=-1
	
	clust = [bicluster(rows[i], cid=i) for i in range(len(rows))]
	
	while len(clust) > 1:
		lowestpair = (0, 1)
		closest = distance(clust[0].vec, clust[1].vec)
		
		for i in range(len(clust)):
			for j in range(i + 1, len(clust)):
				pair = (clust[i].cid, clust[j].cid)
				if pair not in distances:
					distances[pair] = distance(clust[i].vec, clust[j].vec)
					
				if distances[pair] < closest:
					closest = distances[pair]
					lowestpair = (i, j)
					
		mergevec = [(clust[lowestpair[0]].vec[lowestpair[1]]+clust[j].vec[k])/2.0 for k in range(len(clust[i].vec))]
		
		newcluster = bicluster(mergevec, clust[lowestpair[0]], clust[lowestpair[1]], closest, currentclustid)
		
		currentclustid -= 1
		del clust[lowestpair[1]]
		del clust[lowestpair[0]]
		clust.append(newcluster)
		
	return clust[0]
		
		
		
