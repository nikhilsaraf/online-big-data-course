import sys
import json
import re

scores = {}
derived_scores = {}

def read_sentiment_file(file):
    global scores
    for line in file:
        term, score = line.split("\t")
        scores[term] = int(score)

def get_derived_words_and_natural_sentiment(tweet):
    total_sentiment = 0
    derived_word_list = []
    # iterate through all words and calculate sentiment
    for word in re.compile("@*\w+-*\w*").findall(tweet):
        sentiment = scores.get(word)
        if sentiment is None and word not in derived_word_list:
            derived_word_list.append(word)
        elif sentiment is not None:
            total_sentiment += sentiment
    return derived_word_list, total_sentiment
 
def populate_derived_sentiment_dictionary(tweet):
    derived_list, total_sentiment = get_derived_words_and_natural_sentiment(tweet)
    global derived_scores
    # for each derived word, add the total sentiment value to the last known value in the map
    for word in derived_list:
        running_total_sentiment = total_sentiment
        number_of_occurrences = 1
        # if word already been seen before, add the previous value to the latest value
        if word in derived_scores:
            tuple = derived_scores[word]
            running_total_sentiment += tuple[0]
            number_of_occurrences += tuple[1]
        # finally set the dictionary value to the updated value for the word
        derived_scores[word] = (running_total_sentiment, number_of_occurrences)

def display_derived_sentiment_dictoinary():
    for key, value in derived_scores.items():
        print key + " " + str(float(value[0])/value[1])

def process_files(sent_file, tweet_file):
    read_sentiment_file(sent_file)
    for tweet in tweet_file:
        json_tweet = json.loads(tweet)
        if json_tweet is not None and json_tweet.get("text") is not None:
            tweet_text = json_tweet.get("text").encode('ascii', 'ignore')
            populate_derived_sentiment_dictionary(tweet_text)
    display_derived_sentiment_dictoinary()

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    process_files(sent_file, tweet_file)

if __name__ == '__main__':
    main()
