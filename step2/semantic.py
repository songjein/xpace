# -*- coding:utf8 -*- 
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

#http://pythonstudy.xyz/python/article/205-JSON-%EB%8D%B0%EC%9D%B4%ED%83%80
import json

import conceptNet
from itertools import chain

from konlpy.tag import Komoran
komoran = Komoran()

# jinja template engine example : http://matthiaseisen.com/pp/patterns/p0198/
import jinja2
import os
# for rendering result template (template.html)
def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

# seed relations
seedRel = conceptNet.preprocess(verbose=False)

# make seed topic
seedTopic = []
for r in conceptNet.Relations:
	seedTopic += seedRel[r]

# seedTopic
seedTopic = list(set(seedTopic))

# seedTopic extension with topic.txt 
# 원래는 컨셉넷 기반으로 확장해야 하는데... 지금 힘들어서 집합 자체에 확장시킨다 

f_t = open("topic.txt")
topicsFromCoMatrix = f_t.read().split("\n")
topicsFromCoMatrix = [t.split(",") for t in topicsFromCoMatrix]
topicsFromCoMatrix = list(set(list(chain(*topicsFromCoMatrix))))

seedTopic += topicsFromCoMatrix

# 노이즈 제거해야 됌
seedTopic = [t for t in seedTopic if len(t) > 2]
conceptNet.showList(seedTopic)

# + 사람의 수정
# 제외하거나 추가하고 싶은 것 입력
# 일단 위의 결과 복붙했음 파일에 write하고 사람이 수정할수 있게끔 할것임
modified = "타이어,라이트,발동기,액세서리,엔진,가속기,가솔린,가격,장착,상태,연비,결함,옵션,배터리,성능,시승,밧데리,엔진오일,브레이크,실내,시트,서비스,운전,디자인,안전" 
seedTopic = modified.split(",")
print("modified topic set")
conceptNet.showList(seedTopic)

# ex) 아반떼, 쏘나타, 그렌져 (filter.py 로 걸러 놓은 것중 선택)
userInputSubject = raw_input("User's subject (candidate file name without .txt):") 

f_p = open("%s_pos.txt" %(userInputSubject)) # pos tagged file
f_n_p = open("%s_no_pos.txt" %(userInputSubject)) # no pos tagged file

# 의미없는 오피니언들
STOPWORD_VA= ["같/VA", "이렇/VA", "그렇/VA", "어떻/VA", "없/VA", "높/VA", "시/VA"]

# 휴리스틱 메서드에서 최대 5칸만 스캔
WINDOW_LIMIT = 5

"""
{
	topic1 : [("VA1", count) , ("VA2", count)],
	topic2 : [("VA1", count) , ("VA2", count)],
	topic3 : [("VA1", count) , ("VA2", count)],
}
"""
graph = {} 
examples = {} 

# line 안에서 topic으로 시작해서 limit 안에서 va로 끝나는 문장을 리턴 (최초 발견 리턴)
# topic ~ va segment 를 검출 
def extractSegment(line, topic, va, limit):
	topic = topic.split("/")[0]
	wList = line.split()	# non pos tagged words
	cursor = 0 
	while cursor < len(wList):
		if topic in wList[cursor]: 
			ret = []
			for i in range(WINDOW_LIMIT + 1):
				if cursor + i < len(wList):
					ret.append(wList[cursor + i])
			ret.append("...")
			if va in [ t[0] + "/" + t[1] for t in komoran.pos(" ".join(ret))]:
				return " ".join(ret)
		cursor += 1
	return "" 

while True:	
	p_line = f_p.readline() # pos tagged line
	n_p_line = f_n_p.readline() # non pos line 
	if not p_line: break

	# 휴리스틱 메서드 (지배소후위 원칙에 따라, topic -> VA 의 관계를 찾음)
	wList = p_line.split()
	# 주어진 문장을 단어단위로 스캔하면서...
	#print ("[LINE START][LINE START][LINE START][LINE START][LINE START][LINE START][LINE START][LINE START][LINE START]")
	#print (p_line)
	for i, w in enumerate(wList):
		topic_candidate = w.split("/")[0]
		# [START IF] 현재 단어가 명사이면서 seed topic에 있다면
		if ("NN" in w) and (topic_candidate in seedTopic):
			cursor = i + 1;
			# [TODO] 통계적 수치로 수정
			limit = WINDOW_LIMIT 
			# [START LOOP] 뒤로 살펴보면서 VA를 찾는다 
			while cursor < len(wList) and limit > 0:
				# [START IF] VA(형용사)를 찾으면
				if ("/VA" in wList[cursor]) and (wList[cursor] not in STOPWORD_VA):
					#print ("[TOPIC/VA]")
					#print ("%s \n--> "%(topic_candidate))
					#print (wList[cursor])
					# 그래프를 구성하는 부분
					# (이미 토픽이 존재한다면)
					if topic_candidate in graph:
						find = False
						# topic에 속해있는 
						# 오피니언(VA); wList[cursor] 가 이미 있는지 확인 -> 카운트만 늘려줌
						for idx, item in enumerate(graph[topic_candidate]):
							if (item[0] == wList[cursor]):
								graph[topic_candidate][idx][1] += 1
								find = True
								break
						# 없다면 새로운 표현으로서 추가
						if not find:
							graph[topic_candidate].append([wList[cursor], 1])
					# (토픽이 없다면 추가)
					else:
						graph[topic_candidate] = [[wList[cursor],1]]

					# Topic ~ VA substr 추출 및 examples에 추가
					seg = extractSegment(n_p_line, topic_candidate, wList[cursor], limit)
					if topic_candidate in examples:
						if seg not in examples[topic_candidate]:
							examples[topic_candidate].append(seg)
					else:
						examples[topic_candidate] = [seg]
					break
				# [END IF] if "VA" in wList[cursor]
				cursor += 1
				limit -= 1
			# [END LOOP] while cursor < len(wList) and limit > 0 

		# [END IF] if ("NN" in w) and (topic_candidate in seedTopic):

f_r = open("%s-result.txt" %(userInputSubject), "w")
f_r.write(json.dumps(graph))

f_e = open("%s-examples.txt" %(userInputSubject), "w")
f_e.write(json.dumps(examples))

# show graph
"""
for key in graph:
	print ("======================================================\n-->%s" %(key))
	graph[key] = sorted(graph[key], key=lambda tup:tup[1], reverse=True)
	for item in graph[key]:
		print (item[0] + "," + str(item[1]))
"""


"""
	build graph for visualization
	{
		"nodes": [{name:"abc"}],
		"edges": [{source:0, target:1}]
	}
"""
# build viz graph
viz_graph = {
		"nodes": [],
		"edges": []
	}
voca = []
topics = []
sup = 5 
for key in graph:
	voca.append(key)
	topics.append(key)
	graph[key] = sorted(graph[key], key=lambda tup:tup[1], reverse=True)
	for item in graph[key]:
		if item[1] > sup: 
			voca.append(item[0])

voca = (list(set(voca)))
viz_graph["nodes"] = [{"name": v} for v in voca]
rev_idx = {v: idx for idx, v in enumerate(voca)}

for key in graph:
	graph[key] = sorted(graph[key], key=lambda tup:tup[1], reverse=True)
	#for item in graph[key]:
	viz_graph["edges"].extend([{"source": rev_idx[key], "target": rev_idx[item[0]]} for item in graph[key] if item[1] > sup])

print ("topics : ")
print (",".join(topics))
print (json.dumps(viz_graph))




# output html file
context = {
	"subject": userInputSubject,
	"topics": ",".join(topics),
	'graph': json.dumps(graph),
	'viz_graph': json.dumps(viz_graph),
	'examples': json.dumps(examples)
}
result = render('./template.html', context)
f_html = open("%s.html" %(userInputSubject), "w")
f_html.write(result)


