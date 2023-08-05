H=str
D=bytes
import hashlib as B,platform as C,subprocess as A,time,requests as E
def F():
	B=True
	if C.system()=='Windows':D=A.check_output('echo %username%',shell=B).decode().strip();E=A.check_output('wmic csproduct get name').decode().split()[1].strip();F=A.check_output('wmic cpu get ProcessorId').decode().split()[1].strip()
	elif C.system()=='Linux':F=H(A.run(['sudo dmidecode','-s','system-uuid'])).strip();E=A.check_output('uname -r').decode().strip();D=A.check_output('whoami',shell=B).decode().strip()
	elif C.system()=='Darwin':D=A.check_output('scutil --get LocalHostName',shell=B).decode().strip();F=A.Popen('ioreg -l | grep IOPlatformSerialNumber',shell=B,stdout=A.PIPE).stdout.read().decode().split('" = "')[1].replace('"','').strip();E=A.Popen("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'",shell=B,stdout=A.PIPE).stdout.read().decode().strip()
	else:print('Windows(64 Bits) is Required.')
	I=G(E+F+D);return I
def G(msg):A='utf-8';C=B.sha256(D(msg,A));E=C.hexdigest();F=B.md5(D(E,A));G=F.hexdigest();I=B.sha256(D(G,A));J=I.hexdigest();K=B.md5(D(J,A));L=K.hexdigest();return H(L)
def I():A=E.get('https://api.ipify.org').content.decode('UTF-8');return A