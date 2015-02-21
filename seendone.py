#!/usr/bin/env python

import os
import datetime
import sys

seen_path = os.path.expanduser('~/Dropbox/todo/donetoday.txt')
done_path = os.path.expanduser('~/Dropbox/todo/done.txt')

def loadDoneTxt():
	global dones
	done_file = open(done_path, 'r')
	raw_dones = done_file.readlines()
	done_file.close()
	dones = []
	for item in raw_dones:
		item = item.strip("\n\r")
		dones.append(item)

def loadSeenTxt():
	global seens
	seen_file = open(seen_path, 'r')
	raw_seen = seen_file.readlines()
	seen_file.close()
	seens = []
	for item in raw_seen:
		item = item.strip("\n\r")
		seens.append(item)

def loadDones():
	loadSeenTxt()
	loadDoneTxt()
	
def checkDones():
	#strip out the done string
	#remove from dones
	#what remains is added to seens
	for seen in seens:
		print seen
		donestr = seen.split(",")[1]
		try:
			dones.remove(str(donestr))
		except (ValueError):
			pass
		
	seen_file = open(seen_path, 'a')
	
	# Is there a newline aready here for us? If not, add it.
	#try:
	#	if todos[-1][-1] != "\n":
	#		todo_file.write("\n")
	#except:
	#	pass
	
	for done in dones:
		#print done
		newdone = "False,"+done
		seen_file.write(str(newdone) + "\n")
	seen_file.close()
	
if __name__ == "__main__":
	loadDones()
	checkDones()
