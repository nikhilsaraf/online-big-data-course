import MapReduce
import json
import sys

# Map function
# mr - MapReduce object
# data - json object formatted as a string
def mapper(mr, data):
    # we need to treat the data as a dictionary, so we interpret it as json, this
    # converting it to a dictionary, making it more useful
    data = json.loads(data, encoding='latin-1')

    # save document_id for code readability
    # keys() gives an array as the input is a json dictionary,
    # we only want the first value as a mapper will only have one key
    document_id = data.keys()[0]
    
    # data's values contains an array of the words (tested via print statement)
    # so we only need to put the values in a set to complete the preparation of it
    # so covert the values to a set to remove duplicates
    wordSet = set(data.values()[0])
    for word in wordSet:
        # we will have uniqueue words here so we can just do an emit_intermediate
        mr.emit_intermediate(word, document_id)

# Reduce function
# mr - MapReduce object
# key - key generated from map phse, associated to list_of_values
# list_of_values - values generated from map phase, associated to key
def reducer(mr, key, list_of_values):
    # output list of values as a tuple, as specified in the question
    # this is just an identity function
    mr.emit({key: list_of_values})

def main():
    # Assumes first argument is a file of json objects formatted as strings, 
    # one per line.
    MapReduce.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
