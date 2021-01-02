# !pip3 install python-levenshtein

from Levenshtein import *
import codecs
from create_prices_proprocess_json import SELLER_PREPROCESS


Sellers = [_.upper() for _ in SELLER_PREPROCESS]

def sellerMatch(raw_input):
	raw_input = raw_input.upper()
	index_min = max(range(len(Sellers)), \
		key=lambda x: ratio(raw_input, Sellers[x]))
	return SELLER_PREPROCESS[index_min]

print(sellerMatch('Vncommerced'))