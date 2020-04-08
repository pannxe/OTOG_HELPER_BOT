from subprocess import Popen, PIPE, STDOUT
import subprocess
import os

PATH = os.path.realpath(__file__)
while PATH[-1] != "\\":
	PATH = PATH[:-1]


def Grading(namae):

	Now_FILE = namae+".cpp"
	Now_EXE = namae+"RUN"

	p = Popen(['g++',PATH+Now_FILE,'-o',Now_EXE], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	(a,b) = p.communicate()
	a = a.decode()
	RET = p.wait()
	if RET!= 0:
		return "อ่อนหัด!! แค่นี้ก็ยัง ERROR\n"+a.replace(PATH,"..\\")
	Verdict = ""

	for i in range(1,11):
		p = Popen([PATH+Now_EXE], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		F = open("Pat1TestCase\\"+str(i)+".in","r")
		try:
			OUT = p.communicate(timeout=10,input=F.read().encode())[0]
		except subprocess.TimeoutExpired:
			Verdict += "T"
			per= False
			continue

		F.close()
		RET = p.wait()
		if RET != 0:
			Verdict += "X"
			per= False
			continue

		OUT = OUT.decode()
		OUT  = OUT.replace("\r","")
		while OUT[-1] == " " or OUT[-1] == "\n":
			OUT = OUT[:-1]
		F = open("Pat1TestCase\\"+str(i)+".sol","r")
		SOL = F.read()
		F.close()
		while SOL[-1] == " " or SOL[-1] == "\n":
			SOL = SOL[:-1]

		if OUT != SOL:
			Verdict += "-"
		else:
			Verdict += "P"
	return Verdict
