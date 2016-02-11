from models import *
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer


def build_search_engine():
	'''
	Returns a search function which searches the string that user enters
	within the two indexes which map from words to lists of materials.
	'''
	index_name = index("name")
	index_total = index("description")
	def search_engine(search):
		outcome_name = search_helper(search, index_name)
		if len(outcome_name) >= 30:
			return id_to_material(outcome_name)
		outcome_total = search_helper(search, index_total)
		return id_to_material(outcome_total)
	return search_engine


def search_helper(search, index):
	terms = word_list(search.term)
	for i in range(1,len(terms)+1)[::-1]:
		outcome = words2materials(terms, i, index)
		if len(outcome)>=15 or i == 1:
			return outcome


def words2materials(terms, threshold, index):
	if len(Material.objects.all())==0:
		return []
	materials = empty_list(Material.objects.all().order_by("id").reverse()[0].id)
	for term in terms:
		if term in index:
			for i in index[term]:
				materials[i-1] += 1
	outcome = []
	for i in range(len(materials)):
		if materials[i] >= threshold:
			outcome.append((materials[i], i+1))
	outcome = sorted(outcome)
	rv = [y for (x,y) in outcome]
	return rv


def index(index_type):
	dic={}
	materials=Material.objects.all()
	for material in materials:
		words=word_list(material.name)+word_list(material.tags)
		if index_type == "description":
			words=words+word_list(material.description)
		for word in words:
			if word not in dic:
				dic[word]=[]
			if material.id not in dic[word]:
				dic[word].append(material.id)
	return dic


def word_list(text):
	stemmer = SnowballStemmer("english")
	return [stemmer.stem(i) for i in word_tokenize(text.strip())]


def id_to_material(id_list):
	rv = []
	for i in id_list:
		rv.append(Material.objects.get(id=i))
	return rv


def empty_list(num):
	rv=[]
	for i in range(num):
		rv.append(0)
	return rv