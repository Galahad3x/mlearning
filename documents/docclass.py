import re
import math
import pprint

def get_words(doc):
	splitter=re.compile('\\W*')
	print doc
	# words=[s.lower() for s in splitter.split(open(doc,"r").read()) if len(s) > 2 and len(s) < 20 ]
	words=[s.lower() for s in splitter.split(doc) if len(s) > 2 and len(s) < 20 ]
	
	return dict([(w,1) for w in words])
			
print get_words("doc.txt")

class Classifier:
	def __init__(self, getfeatures,filename=None):
		# Feature -> {Category -> Count}
		self.fc = {}
		self.cc = {}
		self.getfeatures = getfeatures
		
	def incf(self, f, cat): # Incrementar contador de feature/category
		self.fc.setdefault(f, {})
		self.fc[f].setdefault(cat, 0)
		
		self.fc[f][cat] += 1
	
	def incc(self, cat): # Incrementar contador de categoria
		self.cc.setdefault(cat, 0)
		self.cc[cat] += 1
	
	def fcount(self, f, cat): # Contar feature dins de categoria
		if f in self.fc and cat in self.fc[f]:
			return self.fc[f][cat]
		return 0.0
	
	def catcount(self, cat): # Numero de items d'una categoria
		if cat in self.cc:
			return self.cc[cat]
		return 0.0
	
	def totalcount(self): # Num total de items
		return sum(self.cc.values())
	
	def categories(self): # Llista de categories
		return self.cc.keys()
		
	def train(self, item, cat):
		features = self.getfeatures(item)
		
		for f in features.keys():
			self.incf(f, cat)
			
		self.incc(cat)
	
	def fprob(self, f, cat): # p(feature | categoria)
		if self.catcount(cat) == 0: return 0.0
		
		pfcat = self.fcount(f, cat) / float(self.totalcount())
		
		pcat = self.catcount(cat) / float(self.totalcount())
		
		return pfcat / float(pcat)
		
	def weightedprob(f, cat, prf=self.fprob, weight=1, ap=0.5):
		count = sum([self.fcount(f, ct) for ct in self.categories()])
		return (weight*ap + count*prf(f,cat) ) / float(weight + count)

def sampletrain(classifier):
	docs = [
		("Nobody owns the water", "good"),
		("The quick rabbit jumps fences", "good"),
		("How to make a DCU", "bad"),
		("invest in fractions of actions","bad"),
		("i am nigerian prince i have 100000 dollar", "bad"),
		("i sold my wife for internet connection", "bad"),
		("good morning beautiful im under the watur", "good"),
		("consell de l'estudiantat","bad")
	]
	for item, cat in docs:
		classifier.train(item,cat)

c1 = Classifier(get_words)
sampletrain(c1)

print c1.fcount("internet","good")
print c1.fcount("nigerian","bad")

	

