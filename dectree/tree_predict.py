# coding=utf-8


def filter_token(token):
	try:
		return int(token)
	except ValueError:
		return token


def read_file(file_path, data_sep=",", ignore_first_line=False):
	prototypes = []

	with open(file_path) as f:
		# Strip lines
		strip_reader = (l.strip() for l in f)  # Al fer-ho directament sobre f es fa lazy
		# Filtrar lineas vacias
		filtered_reader = (l for l in strip_reader if l)
		# eliminar primera linea si necessari
		if ignore_first_line:
			next(filtered_reader)
		# tokenitzar i afegir a prototypes
		for line in filtered_reader:  # També serveix per a consumir el generador
			print(line)
			prototypes.append([filter_token(token) for token in line.split(data_sep)])
		return prototypes


def unique_counts(part):
	results = {}
	for pr in part:
		results[pr[-1]] = results.get(pr[-1], 0) + 1
	return results


def gini_impurity(part):
	total = float(len(part))
	results = unique_counts(part)
	return 1 - sum((v / total) ** 2 for v in results.values())


def entropy(part):
	import math
	total = float(len(part))
	results = unique_counts(part)
	return - sum((v / total) * math.log(v / total, 2) for v in results.values())


def divide_set(part, column, value):
	split_function = None

	if isinstance(value, int) or isinstance(value, float):
		split_function = lambda row: row[column] >= value
	else:
		split_function = lambda row: row[column] == value

	set1 = []
	set2 = []
	for elem in part:
		if split_function(elem):
			set1.append(elem)
		else:
			set2.append(elem)

	return set1, set2


class decisionnode:
	def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
		self.col = col
		self.value = value
		self.results = results
		self.tb = tb
		self.fb = fb


readfile = read_file("decision_tree_example.txt", ignore_first_line=True)
print(unique_counts(readfile))
print(gini_impurity(readfile))
print(entropy(readfile))
print(divide_set(readfile, 0, "google"))
