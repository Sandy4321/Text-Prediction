from gather_data import read_twitter_data
from models import vocabulary
from math import fabs
import sys
import plot_helper



def voc_trie(data):

	voc = vocabulary()
	for d in data:
		voc.add_string( d['text'].lower() )

	print "Finished reading!"
	return voc

def prediction_main(voc):
	while True:
		line = sys.stdin.readline().strip().lower()
		print voc.predict_next_word(line)

