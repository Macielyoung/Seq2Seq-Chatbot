# coding:utf-8

# @Created : Macielyoung
# @Time : 2019/1/11
# @Function : Use some given seeds and random noises to test the Seq2Seq Model

from urllib import request
import urllib
import random
import logging
import json

base_url = "http://192.168.88.50:8080/polls/?query="

# 获取词库
def get_vocabuary():
	vocab = []
	with open('vocab', 'r', encoding='utf-8') as reader:
		for line in reader.readlines():
			word = line.split()
			vocab.append(word[0])
	return vocab

# 获取测试样例
def get_seeds():
	given_seeds = []
	with open('testfile.txt', 'r', encoding='utf-8') as seed:
		for line in seed.readlines():
			line = line.lower().strip('\n')
			given_seeds.append(line)
	return given_seeds

# 获取query对应的answer
def get_answer():
	print('>> Read given seeds\n')
	given_seeds = get_seeds()
	print('>> Read vocabulary\n')
	vocab = get_vocabuary()
	print('>> Read Logger\n')
	logger = get_logger()
	print('>> Generate URL and visit the webpage\n')
	for seed in given_seeds:
		for i in range(2):
			random_seed = random.random()
			if random_seed > 0.2:
				query = seed
			else:
				seed_list = seed.split(' ')
				seed_len = len(seed_list)
				random_loc = random.randint(0, seed_len)
				random_voc = random.choice(vocab)
				logger.debug("Random loc and voc : {} {}".format(str(random_loc), random_voc))
				# print(random_loc, random_voc)
				seed_list.insert(random_loc, random_voc)
				query = ' '.join(seed_list)
			url = base_url + urllib.parse.quote(query)
			# print(url)
			try:
				with request.urlopen(url) as response:
					content = response.read().decode("utf-8")
					content = json.loads(content)
					print(content)
					answer = content['answer']
					print(answer)
					logger.info('Query  : {}'.format(query))
					logger.info('Answer : {}\n'.format(answer))
			except Exception as e:
				print(e)
				logger.error(url+'\n')

# 设定日志
def get_logger():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("test.log")
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

if __name__ == '__main__':
	get_answer()
