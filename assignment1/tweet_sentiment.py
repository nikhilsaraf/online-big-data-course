import sys
import json

scores = {}

def readSentimentFile(file):
    global scores
    for line in file:
        term, score = line.split("\t")
        scores[term] = int(score)

def calculateSentiment(tweet):
    total_sentiment = 0
    # iterate through all words and calculate sentiment
    for word in tweet.split():
        #print word
        # default value of 0 if word is not in dictionary
        sentiment = scores.get(word, 0)
        total_sentiment += sentiment
    return total_sentiment

def process_files(sent_file, tweet_file):
    readSentimentFile(sent_file)
    for tweet in tweet_file:
        json_tweet = json.loads(tweet)
        if json_tweet is not None and json_tweet.get("text") is not None:
            tweet_text = json_tweet.get("text").encode('ascii', 'ignore')
            sentiment = calculateSentiment(tweet_text)
            print sentiment

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    process_files(sent_file, tweet_file)

if __name__ == '__main__':
    main()
