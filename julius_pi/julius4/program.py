#!/usr/bin/python
import os
import re

print ('Hello! Please order.')
os.system("cd /home/pi/julius4")
os.system("arecord -D plughw:0 -c 1 -r 16000 -f S16_LE -d 10  rec.wav")
os.system("julius -input rawfile -filelist recfile -quiet -C Invictus.jconf -outfile")
#os.system("cat rec.out")

input=open ('rec.out','r')
S = input.readline()
input.close()

m = re.search('<s>\s+(.+?)\s+<\/s>', S)

if m:
    found = m.group(1)

print (found)
