# coding:utf-8

# @Created : Macielyoung
# @Time : 2019/1/11
# @Function : Generate greeting files

# 读取greeting文件
def read_greeting():
	pairs = []
	with open('qa.txt', 'r', encoding='utf-8') as qa:
		for line in qa.readlines():
			qa_pair = [each.lower().strip(' ').strip('\n') for each in line.split('-') if each != '' and each != ' ']
			pairs.append(qa_pair)
	return pairs

# 获取日常早安晚安类的对话语料
def get_maen(pairs):
	mfen = []
	for pair in pairs:
		for each in pair:
			if 'morning' in each or 'afternoon' in each or 'evening' in each or 'night' in each:
				mfen.append(pair)
				break
	with open('morning.txt', 'w', encoding='utf-8') as morn:
		for each in mfen:
			qa_line = each[0] + '|' + each[1]
			morn.write(qa_line+'\n')

# 获取见面打招呼的对话类别
def get_meet(pairs):
	how_meets = []
	what_meets = []
	nice_meets = []
	hello_meets = []
	for pair in pairs:
		for each in pair:
			# how are you | how do you do | how are you doing | how is everything
			if 'how do you do' in each or 'how are you' in each or 'how is everything' in each or 'how\'s' in each or 'how is' in each or 'how are' in each:
				if 'how\'s the weather' not in each:
					how_meets.append(pair)
					break
			# what's new | what's up | how've you been | how's it going | what's happening | anything new
			if 'what\'s up' in each or 'what\'s new' in each or 'how\'ve you been' in each or 'how\'s it' in each or 'what\'s happening' in each or 'anything new' in each:
				what_meets.append(pair)
				break
			# nice to meet you | it's a pleasure to meet you | it's great to see you again | good to see you again
			if 'nice to meet' in each or 'it\'s a pleasure to meet' in each or 'it\'s great to' in each or 'glad to meet' in each:
				nice_meets.append(pair)
			# hello | hi
			if 'hello' in each or 'hi' in each or 'hey' in each:
				hello_meets.append(pair)
	return how_meets, what_meets, nice_meets, hello_meets

# '最近还好吗'类型语料
def process_how(how_meets):
	ques, answ = [], []
	for each in how_meets:
		q, a = each[0], each[1]
		if q not in ques:
			ques.append(q)
		if a not in answ:
			answ.append(a)
	return ques, answ

# '有什么新消息，最近怎么样'类型语料
def process_what(what_meets):
	ques, answ = [], []
	for each in what_meets:
		q, a = each[0], each[1]
		if q not in ques:
			ques.append(q)
		if a not in answ:
			answ.append(a)
	return ques, answ

# '很高兴遇到你，好久不见'类型语料
def process_nice(nice_meets):
	ques, answ = [], []
	for each in nice_meets:
		q, a = each[0], each[1]
		if q not in ques:
			ques.append(q)
		if a not in answ:
			answ.append(a)
	return ques, answ

# '你好'类型语料
def process_hello(hello_meets):
	ques, answ = [], []
	for each in hello_meets:
		q, a = each[0], each[1]
		if q not in ques:
			ques.append(q)
		if a not in answ:
			answ.append(a)
	return ques, answ

if __name__ == '__main__':
	pairs = read_greeting()
	# get_maen(pairs)
	how, what, nice, hello = get_meet(pairs)
	ques_how, answ_how = process_how(how)
	ques_what, answ_what = process_what(what)
	ques_nice, answ_nice = process_nice(nice)
	ques_hello, answ_hello = process_hello(hello)

	# 生成对话对
	# with open('how.txt', 'w', encoding='utf-8') as howwriter:
	# 	qa_header = "Category : how greeting"
	# 	howwriter.write(qa_header+'\n')
	# 	for eachq in ques_how:
	# 		for eacha in answ_how:
	# 			qa_line = eachq + "|" + eacha + '\n'
	# 			howwriter.write(qa_line)
	# print(ques_how)
	# print(answ_how)

	# ques_what += ["anything new?", "what's happening?", "what's going on?", "what's wrong?"]
	# answ_what += ['The usual', 'just hanging.', 'I am fine.', 'I am good', "Good, thank you.", "You know, just life."]
	# del answ_what[4]
	# print(ques_what)
	# print(answ_what)
	# with open('what.txt', 'w', encoding='utf-8') as whatwriter:
	# 	qa_header = "Category : what greeting"
	# 	whatwriter.write(qa_header+'\n')
	# 	for eachq in ques_what:
	# 		for eacha in answ_what:
	# 			qa_line = eachq + "|" + eacha + '\n'
	# 			whatwriter.write(qa_line)
	
	# print(ques_nice)
	# print(answ_nice)
	# ques_nice = ["nice to meet you", "it's a pleasure to meet you", "it's great to see you again", "good to see you again"]
	# answ_nice = ["nice to meet you too.", "thank you, you too.", "hello", "you too", "same here.", "you too."]
	# with open('nice.txt', 'w', encoding='utf-8') as nicewriter:
	# 	qa_header = "Category : nice greeting"
	# 	nicewriter.write(qa_header+'\n')
	# 	for eachq in ques_nice:
	# 		for eacha in answ_nice:
	# 			qa_line = eachq + "|" + eacha + '\n'
	# 			nicewriter.write(qa_line)
	
	ques_hello = ["hello", "hi", "hey", "Greetings", "Good day"]
	answ_hello = ["hello", "hi", "hey", "Nice to meet you"]
	with open('hello.txt', 'w', encoding='utf-8') as hellowriter:
		qa_header = "Category : hello greeting"
		hellowriter.write(qa_header+'\n')
		for eachq in ques_hello:
			for eacha in answ_hello:
				qa_line = eachq + "|" + eacha + "\n"
				hellowriter.write(qa_line)
	# print(ques_hello)
	# print(answ_hello)