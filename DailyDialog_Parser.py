"""
This code parses the DailyDialog dataset, specifically combining the emotional
utterance data in 'dialogues_emotion.txt' and the utterances from the 13,000+
dialogues in 'dialogues_text.txt'. These two files must be in the working
directory for this code to run.

Call main(filename) in the shell to produce the text file named 'filename'.
"""

def main(filename):
    """Creates a text file named `filename` in the working directory and
    fills it with dialogue and emotion informaiton nicely formatted.

    filename: a string ending in '.txt'
    """
    dlgs = text_parser('dialogues_text.txt')
    emos_list = emotion_parser('dialogues_emotion.txt')
    f = open(filename, 'w+')
    
    for (emos, dlg) in zip(emos_list, dlgs):
        f.write('\nDialogue:\n')
        for (emo, utter, i) in zip(emos, dlg, range(len(emos))):
            utter = utter.strip()
            if i % 2 == 0:
                speaker = '1'
            else:
                speaker = '2'
            ################## EDIT TRAINING FILEs HERE ##################
            # You can manipulate the presentation of the dialogue files
            # using the variables `speaker`, `utter`, and `emo`, which are 
            # strings indicating the current speaker (1 or 2), the current
            # utterance, and the associated emotion, respectively.
            # Delete the file created after each run, otherwise it'll
            # just keep adding to that text file. Change var `s`:
            s = 'S' + speaker + '_' + emo + ' : ' + utter + '\n'
            
            f.write(s)
        f.write('\n- - -\n') # Optional end of dialogue marker
    f.close()

def text_parser(filename):
    """Returns a list of lists of ints representing the emotion of each
    utterance of each dialogue. For example, lst[n][m] returns the
    numerical code representing the emotion of the mth utterance of the
    nth dialogue in the dataset."""
    with open(filename, 'r') as file:
        dlgs = file.read().split('\n')
        return [d.strip().split('__eou__') for d in dlgs]
    
def emotion_parser(filename):
    """Returns a list of lists of strings with the emotion of each
    utterance of each dialogue. So in the returned `lst`, lst[n][m] returns 
    the emotion of the mth utterance in the nth dialogue in the dataset.
    """
    # empty list for each dialogues
    dlgs = [None for i in range(13118)] 
    with open(filename, 'r') as file:
        i = 0
        f = file.readlines()
        for line in f:
            nums = line.strip().replace(' ', '')
            dlgs[i] = [emo_tag(int(n)) for n in nums] 
            i += 1
    return dlgs
                    
def emo_tag(num):
    if num == 0:
        return 'no_emotion'
    elif num == 1:
        return 'anger'
    elif num == 2:
        return 'disgust'
    elif num == 3:
        return 'fear'
    elif num == 4:
        return 'happiness'
    elif num == 5:
        return 'sadness'
    elif num == 6:
        return 'surprise'

def fix_utter(utter):
    """You can ignore me -- I don't do anything :):
    Besides stripping the utterance string, the other replacements
    don't seem to make a difference -- maybe these extra spaces are standard
    for .txt files??
    """
    u = utter.strip().replace(' , ',',').replace(' \' ','\'') \
        .replace(' . ','. ').replace(' ?','?').replace(' !','!')
