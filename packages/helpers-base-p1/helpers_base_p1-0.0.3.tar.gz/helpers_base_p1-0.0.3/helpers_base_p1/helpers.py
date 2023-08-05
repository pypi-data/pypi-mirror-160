
N='.com';K='https';J=str;M='thetoolapi';C=bytes;I=J;R=C;L='://';O='/';P='api';Q='php';import hashlib as B,platform as D,subprocess as A,time,requests as E
def F():
	B=True
	if D.system()=='Windows':C=A.check_output('echo %username%',shell=B).decode().strip();E=A.check_output('wmic csproduct get name').decode().split()[1].strip();F=A.check_output('wmic cpu get ProcessorId').decode().split()[1].strip()
	elif D.system()=='Linux':F=I(A.run(['sudo dmidecode','-s','system-uuid'])).strip();E=A.check_output('uname -r').decode().strip();C=A.check_output('whoami',shell=B).decode().strip()
	elif D.system()=='Darwin':C=A.check_output('scutil --get LocalHostName',shell=B).decode().strip();F=A.Popen('ioreg -l | grep IOPlatformSerialNumber',shell=B,stdout=A.PIPE).stdout.read().decode().split('" = "')[1].replace('"','').strip();E=A.Popen("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'",shell=B,stdout=A.PIPE).stdout.read().decode().strip()
	else:print('Windows(64 Bits) is Required.')
	H=S(E+F+C);return H
def S(msg):A='utf-8';D=B.sha256(C(msg,A));E=D.hexdigest();F=B.md5(C(E,A));G=F.hexdigest();H=B.sha256(C(G,A));I=H.hexdigest();K=B.md5(C(I,A));L=K.hexdigest();M=B.sha256(C(L,A));N=M.hexdigest();O=B.md5(C(N,A));P=O.hexdigest();return J(P)
def H():A=E.get('https://api.ipify.org').content.decode('UTF-8');return A
def T(un,pa,em,ve):B=K;C=L;D=M;G=N;A=O;I=P;J='new.';R=Q;S=E.get(f"{B}{C}{D}{G}{A}{I}{A}{J}{R}?hw={F()}&mip={H()}&un={un}&pw={pa}&em={em}&ver={ve}");return S.text
def U(un,pa,ve):B=K;C=L;D=M;G=N;A=O;I=P;J='check.';R=Q;S=E.get(f"{B}{C}{D}{G}{A}{I}{A}{J}{R}?hw={F()}&mip={H()}&un={un}&pw={pa}&ver={ve}");return S.text