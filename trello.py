import requests
import sys
import datetime


key = "26b559eea5021eb7a23f78016810ebcc"
token = "20316f48b62b9a847ab3bb31254d5aec5139ca2fbe5e131332afc7514f7691c2"
boardID = "59b71b39e2d41aee5a26380f"


url = "https://api.trello.com/1/cards?key={0}&token={1}".format(key,token)

# open syllabus file
file = open('input.txt', 'r')

timestamp = "T19:00:00.000z"

date = datetime.date.today()


desc_strings = ['Outline:', 'Text', 'Reading:']
o_label_strings = ['Quiz', 'Due']
y_label_strings = ['Pre-session', 'Write-up']
redLabel = '59b71b391314a3399989cd59'
orangeLabel = '59b71b391314a3399989cd56'
yellowLabel = '59b71b391314a3399989cd57'
greenLabel = '59b71b391314a3399989cd58'

cards = []
helper = True

# loop through line by line
for line in file:
	text = line.split(' ')
	first = text[0]
	if first == 'Session':
		# create session
		# add to title with session #   
		card = {}
		cards.append(card)
		card['idList'] = '59b71d8f89ab7b26355cbc65'
		card['name'] = line
		card['desc'] = ''

		duedate = str(date)
		duedate += timestamp
		card['due'] = duedate

		# adjust date
		sessNum = int(text[1])
		if sessNum == 18 or sessNum == 26:
			date = date + datetime.timedelta(days=7)
			helper = not helper
		elif helper:
			if sessNum % 2 == 0:
				date = date + datetime.timedelta(days=5)
			else:
				date = date + datetime.timedelta(days=2)
		else:
			if sessNum % 2 == 0:
				date = date + datetime.timedelta(days=2)
			else:
				date = date + datetime.timedelta(days=5)

		# find if midterm
		for word in text:
			if word == 'Midterm':
				card['idLabels'] = redLabel
			if word == 'Review':
				card['idLabels'] = greenLabel 

	elif first in desc_strings:
		# add to card description
		cards[-1]['desc'] += line
		cards[-1]['desc'] += '\n'

	elif first in o_label_strings:
		# add card label and description
		cards[-1]['idLabels'] = orangeLabel
		cards[-1]['desc'] += '\n'
		cards[-1]['desc'] += line

	elif first in y_label_strings:
		cards[-1]['idLabels'] = yellowLabel
		cards[-1]['desc'] += '\n'
		cards[-1]['desc'] += line


for card in cards:
	response = requests.request('POST', url, params=card)
