#!/usr/bin/env python3

import time
import math
import random

# mode = input("Mode:\t1=guess pinyin\n\t2=guess hanzi\n\t3=quit\n> ")

class Card(object):
   def __init__(self, pinyin="no pinyin", 
                traditional = "no traditional", 
                definition = "no definition", 
                active = "n", last_viewed = 0, 
                times_viewed = 1, times_correct = 0,
                last_selected = 0):
      self.pinyin=pinyin
      self.traditional=traditional
      self.definition=definition
      self.active=active
      self.last_viewed=last_viewed
      self.last_selected=last_selected
      self.times_viewed=times_viewed
      self.times_correct=times_correct

   def recall_rate(self):
      recall_rate = (self.times_correct / self.times_viewed)
      return recall_rate

cards=[]

# read cards from file
fname="cards.txt"
with open(fname) as f: content = f.readlines()
for line in content:
   pinyin = line.split("\t")[0]
   traditional = line.split("\t")[1]
   definition = line.split("\t")[2]
   active = line.split("\t")[3]
   last_viewed = int(line.split("\t")[4])
   times_viewed = int(line.split("\t")[5])
   times_correct = int(line.split("\t")[6].strip("\n"))
   last_selected = 0                  # property of current run, not stored.
   cards.append(Card(pinyin, traditional, definition, active, last_viewed, times_viewed, times_correct, last_selected))
f.close()

trial_number = 1
number_of_cards = len(cards)
print('done reading', number_of_cards, 'cards...')

# start testing 
while (True):

   #select a card
   trials = 0
   while (trials < 1000):
      trials = trials + 1
      today = int(time.time() / (24*60)) # unix date
      # This will grab a value from a cosine distribution, keeps cards near top
      # weighted_random = (math.pi/2) * math.asin((2/math.pi)*random.random())
      weighted_random = (2/math.pi) * math.asin(random.random())
      card_number = int(math.floor(weighted_random * number_of_cards))
      selected_card = cards[card_number]
      if selected_card.active != 'y': continue
      if (trial_number - selected_card.last_selected < 3 and selected_card.last_selected > 0): continue
      if selected_card.recall_rate() > 0.95 and today - selected_card.last_viewed < 30 : continue
      if selected_card.recall_rate() > 0.90 and today - selected_card.last_viewed < 7 : continue
      break # card is okay

   if (trials > 999):
      print("No cards found. Exiting...")
      break
   
   # Do the user test
   selected_card = cards.pop(card_number)
   guess = input("生詞朋友> " + selected_card.pinyin + " 是 ")
   
   # break loop option
   if (guess == "。"): 
      cards.insert(card_number, selected_card)
      break

   if (guess == selected_card.traditional): 
      print("Correct!")
      selected_card.times_correct = selected_card.times_correct + 1
   else: 
      print("no, it's ", selected_card.traditional)
   print("Stats:  ", selected_card.times_correct, "/", selected_card.times_viewed, selected_card.recall_rate())

   # now do bookkeeping...
   selected_card.last_viewed = today
   selected_card.last_selected = trial_number
   selected_card.times_viewed = selected_card.times_viewed + 1

   cards.insert(0, selected_card) # done with it, move it to position 0 of deck

   # and move on to the next card
   trial_number = trial_number + 1

# End of drill loop  

outfile = open(fname, "w")
for line in cards:
   outfile.write(
         line.pinyin + "\t" + 
         line.traditional + "\t" + 
         line.definition + "\t" + 
         line.active + "\t" + 
         str(line.last_viewed) + "\t" + 
         str(line.times_viewed) + "\t" + 
         str(line.times_correct) + "\n"
      )


