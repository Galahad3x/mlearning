points = [
	[1,1],
	[2,1],
	[4,3],
	[5,4]
]

centroids = [
	[1,1],
	[2,1]
]

def euclidean_squared(p1, p2):
	return sum(
		(val1 - val2) ** 2
		for val1, val2 in zip(p1, p2)
	)
	
def get_closest_centroid(point, centroids):
	closest_idx = -1
	closest_dist = 2**64
	
	for idx, centroid in enumerate(centroids):
		distance = euclidean_squared(centroid, point)
		if < closest_dist:
			closest_id = idx
			closest_dist = distance
			
		return closest_idx, closest_dist
		
def average_points(points_in_cl):
	avgs = []
	for i in range(len(points_in_cl[0])):
		avgs.append(sum([p[i] for p in points_in_cl])/float(len(points))
	return avgs

def update_centroids(bestmatches):
	for cluster_idx in len(bestmatches):
		points = [data[i] for i in bestmatches[cluster_idx]]
		if not points:
			continue
		avrg = average_points(points)
		centroides[cluster_idx] = avgr
		

