# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import operator 
import urllib2

from konlpy.tag import Kkma
from konlpy.utils import pprint
from konlpy.tag import Twitter

twitter = Twitter()

lines = [
	"튜익스서스펜션에 18인치 휠인데 고속안전성 뛰어나고 코너링이나 차체 민첩성이 수준급 이네요. Dct도 변속충격 별로 없고 연비도 나쁘지 않네요. 전에 타던게 i30 디젤 인데 소나타가 코너 한계가 더 높네요. 예전 국산차가 아닌듯합니다. 조타감각도 좋아요. ",
	"그랜져HG를 구매해서 타고다니다 보니 브레이크가 너무 밀립니다.",
	"코나 모던아트 계약해논 상태인데요.. 들은바 코나 연비가 너무 안좋다는 바람에 아이오닉으로 넘어갈까 생각중인데. 회원님들께 의견좀 듣고 싶어요 아이오닉은 직원할인받아서 1900 코나는 2200에 살수잇습니다..",
	# k7 data
	"인테리어, 옵션 인테리어 부분도 특별한 군더더기는 없는거 같습니다.",
	"실내버튼류의 적색등은 별로입니다. 실내 내장의 마감재도 스웨이드? 가볍지않고 무거우면서 고급스러운 스낌입니다",
	"익스테리어 (외관) 디자인이야 그렌져HG보다는 좀 더 감각적인 느낌입니다", 
]



print "pos---------------------------"
"""
	Hueristic Method
	=> 명사, 조사, 형용사 추출
	=> concat Nouns
	=> REGEX ; (명사+조사)+형용사
"""
for line in lines :
	print "@주어진 문장"
	print "->" + line
	for sentence in line.split("."):
		buf = []
		# PROCESS one sentence
		for word in twitter.pos(sentence, stem=True):
			if word[1] == 'Josa':
				buf.append(word)
				print word[0],word[1]
			if word[1] == 'Noun':
				buf.append(word)
				print word[0],word[1]
			if word[1] == 'Adjective':
				buf.append(word)
				print word[0],word[1]
		print "buffer : " + str(buf)

		# concat consecutive nouns
		nBuf = []
		for item in buf:
			if item[0] == "Noun":
			
		# concat consecutive nouns end

		# PROCESS one sentence end

