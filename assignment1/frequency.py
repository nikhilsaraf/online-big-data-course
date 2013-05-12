import sys
import json
import re

frequency_table = {}

def count_term_frequency(tweet):
    global frequency_table
    # for each word, increment the count in the freq table
    for word in re.compile("#*@*\w+-*\w*").findall(tweet):
        number_of_occurrences = 1
        # if word already been seen before, add the previous value to the latest value
        if word in frequency_table:
            number_of_occurrences += frequency_table[word]
        # finally set the dictionary value to the updated value for the word
        frequency_table[word] = number_of_occurrences

def calculate_total_occurrences():
    total = 0
    for key, value in frequency_table.items():
        total += value
    return total

def display_output(total_occurrences):
    for key, value in frequency_table.items():
        print key + " " + str(float(value)/float(total_occurrences))

def process_files(tweet_file):
    for tweet in tweet_file:
        json_tweet = json.loads(tweet)
        if json_tweet is not None and json_tweet.get("text") is not None:
            tweet_text = json_tweet.get("text").encode('ascii', 'ignore')
            count_term_frequency(tweet_text)
    total_occurrences = calculate_total_occurrences()
    display_output(total_occurrences)

def main():
    tweet_file = open(sys.argv[1])
    process_files(tweet_file)

if __name__ == '__main__':
    main()
