# -*- coding:utf8 -*-
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

from itertools import chain

from konlpy.tag import Komoran

import conceptNet

"""
	ConceptNet의 후보를 가지면서,
	VA를 포함하는 문장을 걸러낸다

	이후엔, 토픽을 발견하면, 토픽뒤로 맥시멈 10개(이후엔 평균 단어 개수/1문장)
	살피면서 VA를 수집한다
"""

f = open("../step1/wise_pos.txt")
f_n_p = open("../step1/wise.txt") # no pos

# seed relations
seedRel = conceptNet.preprocess()

# make seed topic
seedTopic = []
for r in conceptNet.Relations:
	seedTopic += seedRel[r]

# seedTopic
seedTopic = list(set(seedTopic))

# seedTopic extension with topic.txt 
# 원래는 컨셉넷 기반으로 확장해야 하는데... 지금 힘들어서 집합 자체에 확장시킨다 

'''
f_t = open("topic.txt")
topicsFromCoMatrix = f_t.read().split("\n")
topicsFromCoMatrix = [t.split(",") for t in topicsFromCoMatrix]
topicsFromCoMatrix = list(set(list(chain(*topicsFromCoMatrix))))
print (",".join(topicsFromCoMatrix))
print ("==============================")

seedTopic += topicsFromCoMatrix

# 노이즈 제거해야 됌
seedTopic = [t for t in seedTopic if len(t) > 2]

conceptNet.showList(seedTopic)
'''

modified = "타이어,라이트,발동기,액세서리,엔진,가속기,가솔린,가격,장착,상태,연비,결함,옵션,배터리,성능,시승,밧데리,엔진오일,브레이크,실내,시트,서비스,운전,디자인,안전" 
seedTopic = modified.split(",")
print("modified topic set")
conceptNet.showList(seedTopic)

# 주어진 문장이, subject를 포함하고, seedTopic 및 VA(형용사)를 포함하는지 체크한다
def filter_s_t_va(line, subject, verbose=False):
	if subject not in line: return False

	if verbose: print ("\n\n\n입력 문장 :")
	if verbose: print (line)
	if verbose: print ("========================================================================================================")

	subjectOk = False
	seedOk = False
	vaOk = False

	if subject in line:
		if verbose: print ("[주제어] %s를 %d개 포함합니다" %(subject, line.count(subject)))
		subjectOk = True
	for s in seedTopic:
		if len(s.strip()) > 0 and (s in line):
			if verbose: print (s + " 를 포함 합니다")
			seedOk = True
	if "VA" in line:
		if verbose: print ("[VA] 를 %d 개 포함 합니다" %(line.count("VA")))
		vaOk = True
	if verbose: print (subjectOk, seedOk, vaOk)
	return (subjectOk and seedOk and vaOk)

# 분석 대상 뭄장을 찾는다

userInputSubject = raw_input("User's subject :") 
'''
	이름_pos.txt 는 포스 태깅 된 것으로 필터링된 결과
	이름_no_pos.txt는 오리지널 버전으로 필터링된 결과
'''
wf = open("./%s_pos.txt"%(userInputSubject), "w")
wf_n_p = open("./%s_no_pos.txt"%(userInputSubject), "w") # no pos

while True:
	line = f.readline()
	line_n_p = f_n_p.readline()
	if not line: break
	#if filter_s_t_va(line, userInputSubject, True):
	if filter_s_t_va(line, userInputSubject):
		wf.write(line)
		wf_n_p.write(line_n_p)

