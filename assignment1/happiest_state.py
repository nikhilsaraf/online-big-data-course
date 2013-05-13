import sys
import json
import re

scores = {}
state_sentiments = {}

def read_sentiment_file(file):
    global scores
    for line in file:
        term, score = line.split("\t")
        scores[term] = int(score)

def get_natural_sentiment(text):
    total_sentiment = 0
    # iterate through all words and calculate sentiment
    for word in re.compile("@*\w+-*\w*").findall(text):
        sentiment = scores.get(word, 0)
        total_sentiment += sentiment
    return total_sentiment
 
def get_state(tweet):
    place = tweet.get("place")
    state = None
    if place is not None:
        country_code = place.get("country_code")
        if country_code is not None and country_code == "US":
            place_type = place.get("place_type")
            full_name = place.get("full_name")
            if len(full_name.split(",")) > 1:
                temp_state = full_name.split(",")[1].strip()
                if len(temp_state) == 2 and temp_state != "US":
                    state = temp_state
    return state

def populate_state_sentiments(tweet):
    tweet_text = tweet.get("text").encode('ascii', 'ignore')
    sentiment = get_natural_sentiment(tweet_text)
    state = get_state(tweet)
    if state is not None:
        global state_sentiments
        # if state already been seen before, add to previous value
        if state in state_sentiments:
            sentiment += state_sentiments[state]
        # finally set the dictionary value to the updated value for the word
        state_sentiments[state] = sentiment

def display_happiest_state():
    if not state_sentiments:
        print "XX"
    else:
        for key in list(reversed(sorted(state_sentiments.iterkeys(), key=lambda k: state_sentiments[k]))):
          print key
          break

def process_files(sent_file, tweet_file):
    read_sentiment_file(sent_file)
    for tweet in tweet_file:
        json_tweet = json.loads(tweet)
        if json_tweet is not None and json_tweet.get("text") is not None:
            populate_state_sentiments(json_tweet)
    display_happiest_state()

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    process_files(sent_file, tweet_file)

if __name__ == '__main__':
    main()
