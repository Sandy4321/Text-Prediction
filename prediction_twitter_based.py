from gather_data import read_twitter_data
from models import vocabulary
import sys

data = read_twitter_data("../tweets.csv")
voc = vocabulary()

for d in data:
	voc.add_string( d['text'].lower() )

print "Finished reading!"
while True:
	line = sys.stdin.readline().strip().lower()
	print voc.predict_next_word(line)