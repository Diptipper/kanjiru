from os import system
import random

def reset_screen():
	system("clear")
	print()

available_levels = [5,4]

JN = {}
KN = {}
for level in available_levels :
	with open(f"data/J{level}.js","r") as file :
		JN[level] = []
		for line in file :
			line = line.replace("\n","")
			if "`" not in [line[0],line[-1]] :
				line = line.split(" ")
				word = line[0]
				reading = line[1]
				meaning = " ".join(line[2:])
				JN[level].append({"word":word,"reading":reading,"meaning":meaning})

	with open(f"data/K{level}.js","r") as file :
		KN[level] = []
		for line in file :
			line = line.replace("\n","").split(" ")
			if "`" not in [line[0],line[-1]] :
				KN[level] += line

def join_list(LIST,nl=False):
	strLIST = [ str(elem) for elem in LIST ]
	if len(strLIST)<=1 :
		return "".join(strLIST)
	else:
		if nl :
			spaces = " "*19
			return (f",\n{spaces}".join(strLIST[:-1])
						+f",\n{spaces}or "+strLIST[-1])
		else :
			if len(strLIST) == 2:
				return strLIST[0]+" or "+strLIST[1]
			else :
				return ", ".join(strLIST[:-1])+", or "+strLIST[-1]

#### Setting
LEVEL = 5        # JLPT level
MODE  = "meaning"
QUESTIONS = 10   # Questions per session
comment = ""

available_modes = ["meaning",
					"reading",
					"kanji"]

while True :

	reset_screen()
	txt_comment = f"\n\n{comment}\n\033[A\033[A\033[A"
	inp = input(txt_comment+" > ").strip().lower()
	comment = ""
	
	if inp == "exit" :
		break

	if inp.count("=") == 1 :
		var,val = inp.split("=")
		var = var.strip()
		val = val.strip()
		if var == "level" :
			try:
				ival = int(val)
			except:
				ival = -1
			if ival not in available_levels :
				comment = "Invalid level. Try "+join_list(available_levels)
			else :
				LEVEL = ival
		elif var == "questions" :
			try:
				ival = int(val)
			except:
				ival = -1
			if ival < 1 :
				comment = "Invalid number of questions. Try value > 0."
			else :
				QUESTIONS = ival
		elif var == "mode" :
			if val not in available_modes :
				comment = "Invalid mode. Try "+join_list(available_modes,True)
			else :
				MODE = val

	if inp == "start" :

		# Generate the questions
		questions = []
		while True :
			pool = [ elem for elem in JN[LEVEL]
						if elem not in questions ]
			if len(pool) == 0 :
				break
			this_question = random.choice(pool)
			questions.append(this_question)
			if len(questions)==QUESTIONS :
				break

		for iq,question in enumerate(questions) :
			word = question["word"]
			reading = question["reading"]
			meaning = question["meaning"]
			if MODE == "meaning" :
				# Generate choices
				choices = [meaning]
				while True :
					pool = [ q["meaning"] for q in questions
								if q["meaning"] not in choices ]
					if len(pool) == 0 :
						break
					choice = random.choice(pool)
					choices.append(choice)
					if len(choices)==4 :
						break
				question_text = f"What's the meaning of {word} ({reading}) ?"
				answer = meaning
			elif MODE == "reading" :
				# Generate choices
				choices = [reading]
				while True :
					pool = [ q["reading"] for q in questions
								if q["reading"] not in choices ]
					if len(pool) == 0 :
						break
					choice = random.choice(pool)
					choices.append(choice)
					if len(choices)==4 :
						break
				question_text = f"What's the reading of {word} ({meaning}) ?"
				answer = reading
			elif MODE == "kanji" :
				# Generate choices
				choices = [word]
				while True :
					pool = [ q["word"] for q in questions
								if q["word"] not in choices ]
					if len(pool) == 0 :
						break
					choice = random.choice(pool)
					choices.append(choice)
					if len(choices)==4 :
						break
				question_text = f"What's the kanji for {meaning} ({reading}) ?"
				answer = word

			random.shuffle(choices)

			# Loop until getting a correct answer
			while True :
				reset_screen()
				print(f" {iq+1}) {question_text}")
				for i in range(4) :
					print(f"    {i+1}: {choices[i]}")

				# Answer processing
				txt_comment = f"\n\n{comment}\n\033[A\033[A\033[A"
				my_answer = input(txt_comment+" answer: ")
				try :
					ians = int(my_answer)
				except :
					ians = 0
				ians -= 1
				is_correct = False
				if ians not in [0,1,2,3] :
					comment = "Invalid choice"
					continue
				elif choices[ians] != answer :
					comment = "Incorrect!"
					continue
				else :
					comment = ""
				break

print()