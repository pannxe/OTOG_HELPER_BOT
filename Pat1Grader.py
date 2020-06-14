from subprocess import Popen, PIPE, STDOUT
import subprocess
import signal
import os
import time

PATH = os.path.realpath(__file__)
while PATH[-1] != "\\":
	PATH = PATH[:-1]


def Grading(namae):
	Now_FILE = "VerifyCode\\" +namae + ".cpp"
	Now_EXE = "VerifyCode\\" +namae + "RUN"

	p = Popen(['g++', '-O2', PATH+Now_FILE,'-o', Now_EXE], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	(a,_) = p.communicate()
	a = a.decode()
	RET = p.returncode
	if RET!= 0:
		return "อ่อนหัด!! แค่นี้ก็ยัง ERROR\n" + a.replace(PATH,"..\\")

	Verdict = ""
	sumTime = 0
	per = True
	for i in range(1,10+1):
		startTime = time.time()
		p = Popen([PATH+Now_EXE], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		try:
			with open("Pat1TestCase\\" +str(i)+".in") as F:
				OUT = p.communicate(timeout=2,input=F.read().encode())[0]
			sumTime += time.time() - startTime
			RET = p.returncode
		except subprocess.TimeoutExpired:
			sumTime += time.time() - startTime
			p.terminate()
			Verdict += "T"
			per = False
			continue

		p.terminate()

		if RET != 0:
			Verdict += "X"
			per = False
			continue




		with open("Pat1TestCase\\" +str(i)+".sol") as F:
			SOL = F.read().strip()

		SOL = SOL.split('\n')
		OUT = OUT.decode().strip().split('\n')


		if len(OUT) != len(SOL):
			Verdict += "-"
		else:

			LL = 0
			Pass = True
			while LL < len(OUT) and Pass:
				#print(OUT[LL].rstrip(),"|vs|",SOL[LL].rstrip(),"=",OUT[LL].rstrip() == SOL[LL].rstrip())
				if OUT[LL].rstrip() != SOL[LL].rstrip():
					Pass = False
				LL+=1
			if Pass:
				Verdict +="P"
			else:
				Verdict +="-"


	return Verdict
