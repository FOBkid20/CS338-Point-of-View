"""
This code parses three .json files from the EmotionLines corpus
to create:
(1) a dictionary of key -> value pairs of emotion (string) ->
list of call-response pairs (tuple of two strings), and
(2) a dictionary of key -> value pairs of emotion (string) ->
list of utterances (string).

(1) Running the main() function with the three .json files in the
working directory returns a dictionary of the form:
{
'anger' : [(C,R), (C,R), (C,R), ...],
'disgust' : [(C,R), (C,R), (C,R), ...],
'joy' : [(C,R), (C,R), (C,R), ...],
'sadness' : [(C,R), (C,R), (C,R), ...],
'surprise' : [(C,R), (C,R), (C,R), ...],
'fear' : [(C,R), (C,R), (C,R), ...],
'neutral' : [(C,R), (C,R), (C,R), ...],
'non-neutral' : [(C,R), (C,R), (C,R), ...],
}
where `(C,R)` is a tuple of two strings, a call, C, and a response, R, that
is associated with the key emotion.

(2) Running the secondary_main() function with the three .json files in the
working directory returns a dictionary of the form:
{
'anger' : [utterance, utterance, ...],
'disgust' : [utterance, utterance, ...],
'joy' : [utterance, utterance, ...],
'sadness' : [utterance, utterance, ...],
'surprise' : [utterance, utterance, ...],
'fear' : [utterance, utterance, ...],
'neutral' : [utterance, utterance, ...],
'non-neutral' : [utterance, utterance, ...],
}
where `utterance` is an utterance associated with the key emotion.

-------------------------------------------------------------------------
Two issues I've noticed in the output values (string utterances):
 - Apostrophes appear to have been replaced with Unicode(?) that
   looks like '\x92re' or '\u0092m'. Some of these aren't even in the
   the source .json files, which is odd.
 - Some of the string utterances are singly quoted while others
   are doubly quoted, even though the source files only use double quotes.

I'm not sure the cause of either of these.  
"""

import json

class cr_pair:
    """A tuple of two strings representing a call-response pair.
    """
    call = ''
    response = ''
    
    def __init__(self, c, r):
        self.call = c
        self.response = r
        
    def get_cr(self):
        return (self.call, self.response)

def dict_base():
    """Returns a dictionary with the six emotions and the neutral and non-neutral
    emotions as keys (strings) and an empty list as values for each.
    """
    return {'anger':[], 'disgust':[], 'joy':[], 'sadness':[], 'surprise':[],
            'fear':[], 'neutral':[], 'non-neutral':[],}

def convert_json(filename):
    """Returns .json file data as a list of lists of dictionaries,
    i.e., a list of dialogues with each dialogue constituting a list of utterances
    and each utterance constituing a dictionary with keys 'speaker', 'utterance',
    'emotion', and 'annotation'. So, json_data[1][1]['utterance'] ==> quote.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def ev_utterance_map(filename):
    """Reads from a .json file and builds a dictionary that maps from
    each of six emotions and the neutral and non-neutral emotions
    to a list of corresponding utterances.

    filename: string
    returns: dictionary that maps from emotions (strings)
             to every utterance (list of strings)
    """
    d = dict_base()
    json_data = convert_json(filename)
        
    # maps each utterance to emotion 
    for dialog in json_data: # dialog is a list
        for utterance in dialog: # utterance is a dictionary
            q = utterance['utterance']
            emo = utterance['emotion']
            d[emo].append(q)
    return d

def secondary_main():
    """Returns a dictionary with emotions as keys and a corresponding list of
    all utterances (not pairs) from all the three .json files of Friends scripts
    from the EmotionLines corpus as values.
    """
    d = dict_base()
    files = ['friends_dev.json', 'friends_test.json', 'friends_train.json']
    
    for f in files:
        d_temp = ev_utterance_map(f)
        # merge dictionaries
        for key in d:
            d[key] += d_temp[key]
    return d
    

def ev_pair_map(filename):
    """Reads from a file and builds a dictionary that maps from
    each of six emotions and the neutral and non-neutral emotions
    to a list of call-response pairs.

    filename: string
    returns: map from emotion to call-response tuples
    """
    d = dict_base()
    json_data = convert_json(filename)
        
    # maps each call-response pair as a tuple to the emotion of the response
    for dialog in json_data: # dialog is a list
        pairs = len(dialog) - 1
        for i in range(pairs):
            u1 = dialog[i]['utterance']
            u2 = dialog[i+1]['utterance']
            emo = dialog[i+1]['emotion']
            cr = cr_pair(u1,u2)
            d[emo].append(cr.get_cr())     
    return d

def main():
    """Returns a dictionary with emotions as keys and a corresponding list of
    all the call-response pairs from all the three .json files of Friends scripts
    from the EmotionLines corpus as values.
    """
    d = dict_base()
    files = ['friends_dev.json', 'friends_test.json', 'friends_train.json']
    
    for f in files:
        d_temp = ev_pair_map(f)
        # merge dictionaries
        for key in d:
            d[key] += d_temp[key]
    return d
