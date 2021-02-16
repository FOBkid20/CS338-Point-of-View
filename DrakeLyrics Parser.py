""" When the file drake_data.json is in the working directory, running the
main() function of this file will return a dictionary with strings as keys
list of strings as values:
{
"lyrics_title" : [...], 
"album" : [...],
"lyrics_url" : [...],
"lyrics" : [...],
"track_views" : [...] 
}

To test the GPT-2 set up, we may feed it the list of strings corresponding to
one key and checking that the output roughly follows these patterns:
d["lyrics_title"] => phrase of a few words long, words all capitalized
d["album"]        => phrase of a few words long, words all capitalized
d["lyrics_url"]   => https://genius.com/...-lyrics
d["lyrics"]       => longer string with many line breaks (\n`s)
d["track_views"]  => number followed by M or K, e.g., 1.2M or 234.8K
"""

import json

def dict_base():
    return {"lyrics_title":[],"album":[], "lyrics_url":[], "lyrics":[],
            "track_views":[]}

def convert_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def song_map(filename):
    d = dict_base()
    json_data = convert_json(filename)

    for song in json_data: # song is a dictionary
        for key in d:
            if song[key] not in d[key]: # avoids repeat entries
                d[key].append(song[key])
    return d

def main():
    return song_map('drake_data.json')
