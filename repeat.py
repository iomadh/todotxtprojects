#!/usr/bin/env python

import os
import datetime
import sys

todo_path = os.path.expanduser('~/Dropbox/todo/todo.txt')
repeat_path = os.path.expanduser('~/Dropbox/todo/repeat.txt')
done_path = os.path.expanduser('~/Dropbox/todo/done.txt')


def checkTodayAgainstRepeatTaskDate(repeatDateString):
	today = datetime.date.today()
	repeatDate = datetime.datetime.strptime(repeatDateString, "%Y-%m-%d").date()
	if repeatDate == today:
		return True
	else:
		return False
		
def addDaysToRepeatTask(repeatDateString, noOfDays):
	return dateString + datetime.timedelta(days=noOfDays)
	
def loadTodoTxt():
	global todos
	todo_file = open(todo_path, 'r')
	raw_todos = todo_file.readlines()
	todo_file.close()
	todos = []
	for item in raw_todos:
		item = item.strip("\n")
		todos.append(item)
	
def loadDoneTxt():
	global dones
	done_file = open(done_path, 'r')
	raw_dones = done_file.readlines()
	done_file.close()
	dones = []
	for item in raw_dones:
		item = item.strip("\n")
		dones.append(item)
	
def loadRepeatTxt():
	global repeats
	repeat_file = open(repeat_path, 'r')
	raw_repeats = repeat_file.readlines()
	repeat_file.close()
	repeats = []
	for item in raw_repeats:
		item = item.strip("\n")
		repeats.append(item)

def isRepeatToday(individualRepeat):
	repeatList = individualRepeat.split(",")
	if checkTodayAgainstRepeatTaskDate(repeatList[1]):
		return True
		
def ShowResults(results, numbers = 1):
	print('')
	if len(results) == 0:
		print("No results.")
	else:
		i = 1
		for item in results:
			if numbers == 1:
				print("{0}. {1}".format(i, item))
			else:
				print(item)
			i += 1
	print('')

def writeNewRepeats(arguments = ""):
	loadTodoTxt()
	todo_file = open(todo_path, 'a')
	
	# Is there a newline aready here for us? If not, add it.
	try:
		if todos[-1][-1] != "\n":
			todo_file.write("\n")
	except:
		pass
	
	# If we've been given something, add each of them followed by a new line.
	if arguments != "":
		for item in arguments:
			todo_file.write(str(item) + "\n")
	todo_file.close()
	
def writeNewRepeatFile(arguments = ""):
	repeat_file = open(repeat_path, 'w')
		
	# If we've been given something, add each of them followed by a new line.
	if arguments != "":
		for item in arguments:
			repeat_file.write(str(item) + "\n")
	repeat_file.close()
	
def wasItemDoneYesterday(item):
	try :
		# yesterday = today = datetime.date.today()-datetime.timedelta(days=1)
		yesterday = datetime.date.today()
		doneDate = datetime.datetime.strptime(item[2:12], "%Y-%m-%d").date()
		if doneDate == yesterday:
			return True
		else:
			return False
	except:
		return False
	
def updateRepeatDates():
	loadDoneTxt()
	loadRepeatTxt()
	# if done is yesterday add to a list
	doneyesterday = []
	repeatRenewals = []
	newRepeats = []
	for doneitem in dones:
		if wasItemDoneYesterday(doneitem):
			doneyesterday.append(doneitem)
	# check doneyesterday against repeat
	for repeat in repeats:
		isanupdate = False
		repeat2 = removePriority(repeat)
		repeat2 = repeat2.strip("\n")
		repeat2 = repeat2.strip("\r")
		for item in doneyesterday:
			item = item.strip("\n")
			item = item.strip("\r")
			if item[13:] == repeat2.split(",")[0]:
				newRepeatItem = updateDateInRepeat(repeat)
				isanupdate = True
		if isanupdate:
			newRepeats.append(newRepeatItem)
		else:
			newRepeats.append(repeat)
	
	writeNewRepeatFile(newRepeats)			

def updateDateInRepeat(item):
	repeatText = item.split(",")[0]
	repeatDays = datetime.timedelta(days=(int(item.split(",")[2]))-1)
	newRepeatDate = datetime.date.today() + repeatDays
	# possible bug here as it may be doing one extra day
	newRepeatItem = repeatText+",%s,%s" % (newRepeatDate, item.split(",")[2])
	return newRepeatItem
	
def removePriority(item):
	try:
		if item[0] == "(":
			return item[4:]
		else:
			return item
	except:
		return item
	
def addNewRepeats():
	loadRepeatTxt()
	includeNewRepeats =  []
	# TODO if it already exists - dont add it
	for repeat in repeats:
		if isRepeatToday(repeat):
			if newRepeatDoesNotExist(repeat):
				includeNewRepeats.append(repeat.split(",")[0])
	writeNewRepeats(includeNewRepeats)

def newRepeatDoesNotExist(item):
	repeatItem = removePriority(item.split(",")[0])
	loadTodoTxt()
	notARepeat = True
	for item in todos:
		#print "Testing %s against %s" % (repeatItem, item)
		if removePriority(item) == repeatItem:
			notARepeat = False	
			#print "Already exists"
	return notARepeat
	
## MAIN ##

if len(sys.argv) == 1:
	updateRepeatDates()
	addNewRepeats()
	sys.exit()

		
	
