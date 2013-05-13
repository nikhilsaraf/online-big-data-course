import sys
import json
import re
from operator import itemgetter

frequency_table = {}

def count_term_frequency(hashtag):
    global frequency_table
    # for each word, increment the count in the freq table
    number_of_occurrences = 1
    # if word already been seen before, add the previous value to the latest value
    if hashtag in frequency_table:
        number_of_occurrences += frequency_table[hashtag]
    # finally set the dictionary value to the updated value for the word
    frequency_table[hashtag] = number_of_occurrences

def display_output():
    for key, value in frequency_table.items():
        print key + " " + str(float(value))

def display_top_ten():
    i = 0
    for key, value in list(reversed(sorted(frequency_table.items(), key=itemgetter(1)))):
        print key + " " + str(float(value))
        i += 1
        if i == 10:
            break

def process_entities(entities):
    if entities is not None and entities.get("hashtags") is not None:
        for hashtag in entities.get("hashtags"):
            tag_text = hashtag.get("text")
            if tag_text is not None and len(tag_text.encode('ascii', 'ignore').strip()) > 0:
                count_term_frequency(tag_text.encode('ascii', 'ignore'))

def process_file(tweet_file):
    for tweet in tweet_file:
        json_tweet = json.loads(tweet)
        if json_tweet is not None:
            process_entities(json_tweet.get("entities"))
            # to count hashtags from retweets
            #if json_tweet.get("retweeted_status") is not None:
                #process_entities(json_tweet.get("retweeted_status").get("entities"))
    #display_output()
    display_top_ten()

def main():
    tweet_file = open(sys.argv[1])
    process_file(tweet_file)

if __name__ == '__main__':
    main()
