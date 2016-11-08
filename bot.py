# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 18:32:07 2016

@author: Sam Ware
"""

import os
import time
import datetime
import random
import fnmatch
from twython import Twython

def tweet():
    
    #Picks a random play
    play = 'plays/' + random.choice(fnmatch.filter(os.listdir('plays'), '*.txt'))
    
    #Puts the play into a list where each line is its own element
    playText = [line.strip() for line in open(play)]
    
    return quote(play = playText)
    
def quote(play):
    
    #Picks a random line to start
    index = random.randint(2, len(play) - 1)
    tweet = ''
    
    while len(tweet) <= 140:

        #Checks to see if any of the lines contains the flag words
        for line in set(open('flag_words.txt')):
            if play[index].startswith(line.strip()):
                if len(tweet) > 100:
                    return tweet
                else:
                    return quote(play)
                
        #Looks for character cues and starts over if tweet is less than 100
        #characters, else starts over
        if play[index].startswith(play[index].upper()):
            if (len(tweet) > 100):
                return tweet
            else:
                return quote(play)
        
        #Checks if the line has more than two words and starts over if the tweet is less than
        #80 characters, else just returns tweet
        if len(play[index].split()) <= 2:
            if len(tweet) < 80:
                return quote(play)
            else:
                return tweet
                
        #Makes sure that line is not prose        
        if not len(play[index]) == 0:
            if play[index][0].lower() == play[index][0]:
                return quote(play)
                
        properEnding = play[index].endswith('.') or play[index].endswith('?') or play[index].endswith('!')
        
        #If the line doesn't end with a "." or "?" check to see if the
	   #line before it did, and if it did and the tweet is greater than length 80
	   #just return the tweet as it is
	   #Also removes commas, semi-colons, and colons on last lines
        if not properEnding:
            if len(play[index]) > 80 and play[index - 1].endswith('.'):
                return tweet;
            if index < len(play) - 1 and len(tweet) + len(play[index]) + len(play[index + 1]) > 140:
                if play[index].endswith(',') or play[index].endswith(';') or play[index].endswith(':'):
                    play[index] = play[index][:-1]

        # Prints out tweet
        if len(tweet) + len(play[index]) < 140 and not(play[index] == '' or play[index] == '\n'):
            tweet += play[index]
            tweet += '\n'
        else:
            break
        if index < len(play) - 1:
            index += 1
    
    return tweet
    
    
apiKey = 'Enter'
apiSecret = 'Your'
accessToken = 'Own'
accessTokenSecret = 'Values'

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

#Tweets 4 times a day at hours 6AM 12PM 6PM and 12PM
while True:
    hour = datetime.datetime.now().hour

    if hour == 0 or hour == 6 or hour == 12 or hour == 18:
        api.update_status(status=tweet())
        print('Hour: ' + str(hour))
        print('Tweeted...')
    else:
        print('Hour: ' + str(hour))
    
    time.sleep(60 * 60)
        
    