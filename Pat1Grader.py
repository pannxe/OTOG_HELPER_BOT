from subprocess import Popen, PIPE, STDOUT
import subprocess
import signal
import os
import time

PATH = f"{os.getcwd()}\\"

def compare_equal(OUT):
    with open(f"Pat1TestCase\\{i}.sol") as f:
        SOL = f.read().strip().split("\n")
    OUT = OUT.decode().strip().split("\n")
    if len(OUT) != len(SOL):
        return "-"
    else:
        for j in range(len(OUT)):
            if OUT[i] != SOL[i]:
                return "-"
        return "P"

def Grading(namae):
    Now_FILE = f"VerifyCode\\{namae}.cpp"
    Now_EXE = f"VerifyCode\\{namae}RUN"

    p = Popen(
        ["g++", "-O2", PATH + Now_FILE, "-o", Now_EXE],
        stdout=PIPE,
        stdin=PIPE,
        stderr=STDOUT,
    )
    (a, _) = p.communicate()
    RET = p.returncode

    if RET != 0:
        return "อ่อนหัด!! แค่นี้ก็ยัง ERROR\n" + a.decode().replace(PATH, "..\\")

    Verdict = ""
    sumTime = 0

    for i in range(1, 11):
        startTime = time.time()
        p = Popen([PATH + Now_EXE], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        try:
            with open(f"Pat1TestCase\\{i}.in") as F:
                OUT = p.communicate(timeout=2, input=F.read().encode())[0]
            	RET = p.returncode
        except subprocess.TimeoutExpired:
            RET = 124
		
        sumTime += time.time() - startTime
        p.terminate()

        if RET != 0:
            Verdict += "T" if RET == 124 else "X"
            continue

        # Grading session
        Verdict += compare_equal(OUT)

    return Verdict
