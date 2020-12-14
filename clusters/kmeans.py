import random

def euclidean_squared(p1, p2):
	return sum(
		(val1 - val2) ** 2
		for val1, val2 in zip(p1, p2)
	)
		
class Kmeans:
	def __init__(self, k, distance, max_iters, use_range=True):
		self.k = k # Número de clusters
		self.distance = distance # Funció de distància que farem servir
		self.use_range = use_range
		self.max_iters = max_iters
		self.centroids = []
		
	# Crear un centroide random
	def _get_range_random_value(self, points, feature_idx):
		feat_values = [point[feature_idx] for point in points] # Valors de la feature
		feat_max = max(feat_values)
		feat_min = min(feat_values)
		return random.random() * (feat_max - feat_min) + feat_min
	
	# Crear centroides random
	def _create_random_centroids(self, rows):
		n_feats = len(points[0])
		for cluster_idx in range(self.k): # Per el número de clusters que volem
			point = [0.0] * n_feats
			for feature_idx in range(n_feats): # Crear un centroid passant per tots els features
				point[feature_idx] = self._get_range_random_value(points, feature_idx)
			self.centroids.append(point)
		
	def _create_points_centroids(self, points):
		raise NotImplementedError
		
	# Row es una llista que representa un punt
	# Busquem els centroide més proper al punt i retorna el id
	def _find_closest_centroid(self, row):
		min_dist = 2**64
		closest_centroid_idx = None
		
		for centroid_idx, centroid in enumerate(self.centroids): # self.centroids es una llista amb els centroides
			dist = self.distance(row, centroid) # Distància del punt al centroide segons la funció que hem passat
			if dist < min_dist:
				closest_centroid_idx = centroid_idx
				min_dist = dist
				
		return closest_centroid_idx

	# Retornar el punt mitjana de points_in_cl, que es els punts que hi ha a un cluster
	def _average_points(self, points_in_cl):
		avgs = []
		for i in range(len(points_in_cl[0])):
			avgs.append(sum([p[i] for p in points_in_cl])/float(len(points)))
		return avgs

	# matches es una llista on per cada cluster hi ha els ids dels punts que li toquen
	# rows es la llista amb tots els punts
	# Actualitzar els centroides dels clusters
	def _update_centroids(self, matches, rows):
		for cluster_idx in range(len(matches)): # Per cada cluster
			points_2 = [rows[i] for i in matches[cluster_idx]] # Agafo els punts enlloc dels ids
			if not points_2: # Si no hi ha punts no hi ha centre
				continue
			avrg = self._average_points(points_2)
			self.centroids[cluster_idx] = avrg # El nou centroide del cluster es la mitjana de tots els punts
		
	def fit(self,rows):
		if self.use_range:
			self._create_random_centroids(rows) # Crear centroides random el primer cop
		else:
			self._create_points_centroids(rows)
			
		lastmatches = None # Assignacions anteriors
			
		for iteration in range(self.max_iters): # Limit d'iteracions per evitar bucle infinit
			bestmatches = [[] for _ in range(self.k)] # Matches buits al principi
			
			for row_idx, row in enumerate(rows): # Per tots els punts
				centroid = self._find_closest_centroid(row) # Trobem el centroide mes proper i l'afegim
				bestmatches[centroid].append(row_idx)
		
			# Si anteriors i actuals son iguals hem acabat
			if bestmatches == lastmatches:
				break
				
			lastmatches = bestmatches
			
			# Actualitzar els centroides dels clusters segons les noves assignacions
			self._update_centroids(bestmatches, rows)
		return bestmatches
	
	# Passat una llista de punts retornar de quin cluster serien
	def predict(self, rows):
		predictions = list(map(self._find_closest_centroid, rows))
		return predictions
			
			
points = [
	[1,1],
	[2,1],
	[4,3],
	[5,4]
]

points2 = [
	[2,4],
	[3,5],
	[3,2],
	[5,2],
	[5,4],
	[7,3],
	[7,8],
	[8,4],
]

centroids = [
	[1,1],
	[2,1]
]
			
kmeans = Kmeans(k=2, distance=euclidean_squared, max_iters=5)
bestmatches = kmeans.fit(points2)
print(bestmatches)






