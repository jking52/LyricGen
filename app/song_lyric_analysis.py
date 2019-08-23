#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:36:06 2019

@author: jamie
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

class LyricGenerator_modeller:


    def __init__(self):
        self.genre = None
        self.complete_lyrics = None
        self.lyric_ngram = None
        self.dataset =None
        self.read_dataset()
        self.data_preprocessing()
        print(len(self.dataset))

    def read_dataset(self):
        self.dataset = pd.read_csv('/home/jamie/Development/Python/data_science/datasets/misc/380000-lyrics-from-metrolyrics/lyrics.csv',converters={'lyrics':lambda x:x.replace('\n',' ')})

    def data_preprocessing(self):
        'Remove any rows that have nan values'
        self.dataset = self.dataset[self.dataset['lyrics'].notna()]

    def get_genres(self):
        return self.dataset['genre'].value_counts().index.tolist()

    def init_model(self,genre):
        self.genre = genre.lower()
        self.complete_lyrics = self.dataset[(self.dataset.genre.str.lower() == self.genre)]
        self.lyric_ngram = Counter()


        def ngrams(input, n):
          input = input.split(' ')
          output = []
          output_dict = {}
          for i in range(len(input)-n+1):
            ngram = ' '.join(input[i:i+n])
            output.append(ngram)
            output_dict.setdefault(ngram,0)
            output_dict[ngram] +=1
          return output,output_dict


        for i in range(0,self.complete_lyrics.shape[0]):
            lyrics = self.complete_lyrics.iloc[i,5]
            lyrics = lyrics.lower()
            ngram_lyrics,ngram_lyrics_dict = ngrams(lyrics,4)

            self.lyric_ngram.update(ngram_lyrics_dict)



    def suggest_next_word(self,input_word):
        suggested_words = Counter()
        for ngram in self.lyric_ngram.elements():
            words = ngram.split(' ')
            if words[0] == input_word.lower():
                suggested_words.update([words[1]])

        return suggested_words.most_common(10)


    def suggest_next_word_bigram(self,input_bigram):
        suggested_words = Counter()
        for ngram in self.lyric_ngram.elements():
            words = ngram.split(' ')
            if (words[0] == input_bigram[0].lower() and words[1] == input_bigram[1].lower()):
                suggested_words.update([words[2]])

        return suggested_words.most_common(10)

    def suggest_next_word_trigram(self,input_bigram):
        suggested_words = Counter()
        for ngram in self.lyric_ngram.elements():
            words = ngram.split(' ')
            if (words[0] == input_bigram[0].lower() and words[1] == input_bigram[1].lower() and words[2] == input_bigram[2].lower()):
                suggested_words.update([words[3]])

        return suggested_words.most_common(10)

    def suggest_next(self,word_list):
        suggested_words = Counter()
        print(word_list)

        #if empty list provided return empty list *temp*
        if len(word_list) == 0:
            return suggested_words.most_common(0)

        #if we have a '\n' character we remove evrything to the left inclusivly from the word_list and resubmit
        if '\n' in word_list:
           sub_wordlist = word_list[word_list.index('\n')+1:]
           print(word_list)
           self.suggest_next(sub_wordlist)
        #only one word so return the unigram suggestion
        if len(word_list) == 1:
            words = self.suggest_next_word(word_list[0])
            suggested_words.update(words)
        #two words so return the bigram suggestion
        if len(word_list) == 2:
            words =self. suggest_next_word_bigram(word_list)
            suggested_words.update(words)
            #if there wasn't enough suggestions from the bigram suggestion, try the unigram suggestion
            if len(suggested_words) < 10:
                  words = self.suggest_next_word(word_list[-1])
                  suggested_words.update(words)
        if len(word_list) == 3:
            words = self.suggest_next_word_trigram(word_list)
            suggested_words.update(words)
            #if there wasn't enough suggestions from the trigram suggestion, try the bigram suggestion
            if len(suggested_words) < 10:
                  words = self.suggest_next_word_bigram([word_list[-1], word_list[-2]])
                  suggested_words.update(words)
                 #if there still wasn't enough suggestions from the bigram suggestion, try the unigram suggestion
            if len(suggested_words) < 10:
                  words = self.suggest_next_word(word_list[-1])
                  suggested_words.update(words)


        return suggested_words.most_common(10)


'''
#UI`
song = []
model = LyricGenerator_modeller()
genre = None

print('Welcome to lyric Generator 0.1')
genres = model.get_genres()
genre = input('please enter the genre of music you want to create:\n' + '\t\n'.join(genres) + '\n')
model.init_model(genre)
starting_word = input('Please type in the first word of the song: ' )
song.append(starting_word)
next_words = model.suggest_next([starting_word])
print('I suggest the following:')
for i in range(len(next_words)):
    print(next_words[i][0])

exit_loop = False

while not exit_loop:
    print('')
    print(' '.join(song))
    word = input('Enter the next word of your song or 1 to end the current line or press q to quit ')
    if word == 'q':
        exit_loop = True
        print('Your Lyrics are: ')
        print(song)
    else:
        if word == '1':
            word = '\n'
        print('...')
        song.append(word)
        if len(song) < 3:
            next_words = model.suggest_next([song[-2],song[-1]])
            print('I suggest the following:')
            for i in range(len(next_words)):
                print(next_words[i][0])
        elif len(song) >= 3:
            next_words = model.suggest_next([song[-3],song[-2],song[-1]])
            print('I suggest the following:')
            for i in range(len(next_words)):
                print(next_words[i][0])
                '''
