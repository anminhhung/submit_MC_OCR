# !pip3 install python-levenshtein

from Levenshtein import *
import codecs

sellers = codecs.open('seller_dictionary.txt','r',encoding='utf-8').read().split('\n')
Sellers = [_.upper() for _ in sellers]

def sellerMatch(raw_input):
	raw_input = raw_input.upper()
	index_min = max(range(len(Sellers)), \
		key=lambda x: ratio(raw_input, Sellers[x]))
	return sellers[index_min]

print(sellerMatch('hello demo ai'))