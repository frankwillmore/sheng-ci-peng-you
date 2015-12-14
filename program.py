#!/usr/bin/env python3

fname="cards.txt"

mode = input("Mode:\t1=guess pinyin\n\t2=guess hanzi\n\t3=quit\n> ")
pinyin=[]
traditional=[]

# read cards from file
with open(fname) as f: content = f.readlines()
i=0
for line in content:
  pinyin.append(line.split("\t")[0])
  traditional.append(line.split("\t")[1].strip("\n"))
  guess = input("生詞朋友> " + pinyin[i] + " 是 ")
  if (guess == traditional[i]): print("Correct!")
  else: print("no, it's ", traditional[i])
  i = i + 1

print('done reading cards...')

for x in pinyin[0:]:
  print (x)



