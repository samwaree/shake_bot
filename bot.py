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
import pronouncing
from twython import Twython
from OpenSSL.SSL import SysCallError, Error

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
        if len(play[index].split()) <= 3:
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
        if not properEnding:
            if len(tweet) > 80 and play[index - 1].endswith('.'):
                return tweet

        #Adds the line to the tweet if it is less than 140 characters
        if len(tweet) + len(play[index]) < 140 and not(play[index] == '' or play[index] == '\n'):
            tweet += play[index]
            tweet += '\n'
        else:
            break
        
        #Moves to the next line
        if index < len(play) - 1:
            index += 1
            
    #Checks to see if the tweet ended in a proper punctuation       
    if (tweet.endswith('.') or tweet.endswith('!') or tweet.endswith('?')):
        return tweet
    #Otherwise, checks to see if the last word rhymes with any other last word on the lines
    else:
        words = []
        for line in tweet.splitlines():
            line = line.rstrip('?:!.,;')
            words.append(line.split(" ")[-1])
        for a in range(0, len(words)-1):
            if (a in pronouncing.rhymes(words[len(words) - 1])):
                return tweet.rstrip('?:!.,;')
    
    #If it doesn't end in a period and it doesn't rhyme, start over                
    return quote(play)
        
        
    
    
apiKey = 'Enter'
apiSecret = 'Your'
accessToken = 'Own'
accessTokenSecret = 'Values'

client_args = {
    'verify': False
}

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret,client_args=client_args)

#Tweets once an hour between 7AM and 12AM
while True:
    hour = datetime.datetime.now().hour

    print (hour)
    if hour > 6:
        try:
            api.update_status(status=tweet())
        except (SysCallError, Error):
            time.sleep(30)
            continue
        print ('Tweeted')
    
    time.sleep(60 * 60)



    
