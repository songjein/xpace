# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from konlpy.tag import Komoran

from extract import preprocess, Relations, showList

"""
	ConceptNet의 후보를 가지면서,
	VA를 포함하는 문장을 걸러낸다

	이후엔, 토픽을 발견하면, 토픽뒤로 맥시멈 10개(이후엔 평균 단어 개수/1문장)
	살피면서 VA를 수집한다
"""

f = open("../step1/wise_pos.txt")

wf = open("./result.txt", "w")

# seed relations
seedRel = preprocess()


# make seed topic
seedTopic = []
for r in Relations:
	seedTopic += seedRel[r]

seedTopic = list(set(seedTopic))

showList(seedTopic)

line = f.readline()

# 주어진 문장이, subject를 포함하고, seedTopic 및 VA(형용사)를 포함하는지 체크한다
def filter_s_t_va(line, subject):
	if subject not in line: return False

	print ("\n\n\n입력 문장 :")
	print (line)
	print ("========================================================================================================")
	subjectOk = False
	seedOk = False
	vaOk = False

	if subject in line:
		print ("[주제어] %s를 %d개 포함합니다" %(subject, line.count(subject)))
		subjectOk = True
	for s in seedTopic:
		if s in line:
			print (s + " 를 포함 합니다")
			ok = True
	if "VA" in line:
		print ("[VA] 를 %d 개 포함 합니다" %(line.count("VA")))
		vaOk = True
	return (subjectOk and seedOk and vaOk)

# 분석 대상 뭄장을 찾는다
while True:
	line = f.readline()
	if not line: break
	if filter_s_t_va(line, "그랜져"):
		wf.write(line)
