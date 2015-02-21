#!/usr/bin/env python

import os
import datetime
import sys

todo_path = os.path.expanduser('~/Dropbox/todo/todo.txt')
project_path = os.path.expanduser('~/Dropbox/projects/')
done_path = os.path.expanduser('~/Dropbox/todo/donetoday.txt')

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
		item = item.strip("\n\r")
		dones.append(item)
		
def scanLines(project, scanType, stopType):
	status = False
	returnScan = []
	for line in project:
		if stopType in line:
			status = False
		if status:
			if not line == '':
				returnScan.append(line)
			else:
				if scanType == '**Description**':
					returnScan.append(line)
		if scanType in line:
			status = True
	return returnScan
	
def loadProjects():
	global projects
	projects = []
	for root, dirs, files in os.walk(project_path):
		for file in files:
			if file.endswith(".txt"):
				project_file = open(os.path.join(root, file))
				raw_project = project_file.readlines()
				project_file.close()
				base_project = []
				for line in raw_project:
					line = line.strip("\n\r")
					base_project.append(line)
				project = {}
				project['name'] = base_project[0]
				project['status'] = base_project[3]
				project['description'] = scanLines(base_project, '**Description**', '**Todo**')
				project['todos'] = scanLines(base_project, '**Todo**', '**Done**')
				project['dones'] = scanLines(base_project, '**Done**', '**End**')
				project['filename'] = os.path.join(root, file)
				projects.append(project)

def processDones():
	loadDoneTxt()
	doneindex = []

	for i in xrange(len(dones)):
		doneitem = dones[i]
		donearray = doneitem.split(",")
		checkForNextAction = False
		if donearray[0] == 'False':
			doneindex.append(doneitem)
			try:
				projecttitle = '+' + donearray[1].split("+")[1].split(" ", 1)[0]		
				taskdate = donearray[1][2:12]
				taskdetails = donearray[1][13:].split("+")[0][:-1]
				project = [item for item in projects if item['name'] == projecttitle]
				for proj in project:
					for todo in proj['todos']:
						try:
							if taskdetails in todo.split(" ",1)[1]:
								#if todo.split(" ",1)[1] in taskdetails:
								proj['dones'].append(donearray[1])
								proj['todos'].remove(str('* '+todo.split(" ",1)[1]))
								proj['status'] = 'RVW'
								checkForNextAction = True
						except (IndexError):
							pass
						if checkForNextAction:
							onlyFirst = True
							for j in xrange(len(proj['todos'])):
								if proj['todos'][j][0] == 'n' and onlyFirst:
									proj['todos'][j] = "+" + proj['todos'][j][1:]
									proj['status'] = 'WIP'
									onlyFirst = False
							checkForNextAction = False
			except (IndexError):
				pass
			
	for ind in doneindex:
		seen = "True,"+ind.split(",")[1]
		dones.remove(ind)
		dones.append(seen)
			
def printProjects():
	print "Project Output"
	print "--------------"
	for project in projects:
		print 'Project => ' + project['name']
		print 'Status => ' + project['status']
		print 'Todos => '
		for projecttodos in project['todos']:
			print projecttodos
		print 'Dones => '
		#for line in project:
		#	if line[0] == '+':
		#		print line
		for pdones in project['dones']:
			print pdones					
	print "\nDone.txt Output"
	print "---------------"
	print dones
	
def updateTodos():
	newTodos = []
	for project in projects:
		for k in range(len(project['todos'])):
			projecttodos = project['todos'][k]
			if projecttodos[0] == '+':
				if projecttodos[2] == '(':
					newTodos.append(projecttodos[2:] + ' ' + project['name'])
				else:
					newTodos.append('(C)' + projecttodos[1:] + ' ' + project['name'])
				changetodo = list(projecttodos)
				changetodo[0] = '*'
				project['todos'][k] = "".join(changetodo)
	if newTodos != []:
		writeNewTodos(newTodos)

def writeNewTodos(arguments = ""):
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

def saveProjects():
	for project in projects:
		project_file = open(project['filename'],'w')
		project_file.write(project['name'] + "\n\n**Status**\n")
		project_file.write(project['status'] + "\n\n**Description**\n")
		for projtodos in project['description']:
			project_file.write(projtodos + "\n")
		project_file.write("**Todo**\n")
		for projtodos in project['todos']:
			project_file.write(projtodos + "\n")
		project_file.write("\n**Done**\n")
		for projdones in project['dones']:
			project_file.write(projdones + "\n")
		project_file.write("\n**End**")
		project_file.close()
	
	done_file = open(done_path, 'w')
		
	# If we've been given something, add each of them followed by a new line.
	for item in dones:
		done_file.write(str(item) + "\n")
	done_file.close()
		
	
## MAIN ##

if __name__ == "__main__":
	loadProjects()
	processDones()
	updateTodos()
	#printProjects()
	saveProjects()
	sys.exit()