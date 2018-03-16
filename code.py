
#!/usr/bin/python
import requests
import sys
import re
import os
import argparse
import time
import signal
import hashlib
from thread import start_new_thread
from collections import deque
import fcntl
errors		= 0
queue		= 0
count		= 1
queueLock	= False
hexValue	= hashlib.md5("".join(sys.argv)).hexdigest()
printSpool	= deque([])
currentWords	= []
errors		= []	

def signal_handler(signal, frame):
    global queueWords
    queueWords=list(queueWords)+currentWords
    queueWords.reverse()
    file=open("."+hexValue,"w")
    file.write("\n".join(queueWords))
    file.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def argRead():
	DESCRIPTION =\
	"Script used for bruteforcing web application directories and files"
	EPILOG ="""
Examples :
	Detect_Dir --fuzz -fstring "http://example.com/<FUZZ>/index.html"		
	"""
	group=argparse.ArgumentParser( description = DESCRIPTION, epilog = EPILOG,formatter_class = argparse.RawDescriptionHelpFormatter,)
	group.add_argument('-fuzz', '--fuzz', dest='FUZZ',default=False, action='store_true',
                    		help='Enable Fuzzin')
	group.add_argument('-custom', '--custom', dest='CUST',default=False, action='store_true',
                    		help='Enable custom code input')
	group.add_argument('-fstring', default = "", dest = "FUZZ_STRING", help = "Input fuzz string",)
	group.add_argument('-scodes', default = "200", dest = "SUCC_CODES", help = "Success status code comma seperated",)
	group.add_argument('-w', default = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt", dest = "WORDLIST", help = "Wordlist Location",)
	group.add_argument('-t', default = 10, dest = "MAX_QUEUE", help = "Number of parallel attemps",)
	group.add_argument('-o', default = "result.txt", dest = "OUTPUT_FILE", help = "Output file",)
	group.add_argument('-dir', '--dir', dest='DIR',default=False, action='store_true',
                    		help='Bruteforce directories')
	group.add_argument('-i', default = False, dest = "IP_ADDRESS", help = "HOST_IP",)
	group.add_argument('-p', default = '', dest = "PORT_ADDRESS", help = "Port address",)
	group.add_argument('-https', '--https', dest='HTTPS',default=False, action='store_true',
                    		help='Enable this flag if https is enabled')
	group.add_argument('-s', default = 0, dest = "SKIP_STEP", help = "Skip_first_n_entries in wordlist",)
	group.add_argument('-b', default = "", dest = "BASE_PATH", help = "Base directory to start bruteforcing",)
	group.add_argument('-r', default = ".*", dest = "REGEX", help = "Regex will be applied on each entry on wordlist to find  validity",)
	group.add_argument('-e', default = "html", dest = "EXTENSIONS", help = "COmma seperated extensions",)
	if len(sys.argv) == 1:
		group.print_help()
		sys.exit(-1)
	args=group.parse_args()
	return args

def check(wordRaw,url):
	global queue,error,args,queueLock,lock, count, currentWords,customCond
	queue+=1
	try:
		currentWords.append(wordRaw)
		k=response=requests.head(url,params={})
		scodes=(args.SUCC_CODES).split(",")
		scodes=[int(x) for x in scodes]
		checkCondition=""
		if(len(customCond)==0):
			checkCondition=int(k.status_code) in scodes
		else :
			checkCondition=eval(customCond);
		if(checkCondition):
			file=open(args.OUTPUT_FILE,"a")
			fcntl.flock(file,fcntl.LOCK_EX)
			file.write(url+" "+str(k.status_code)+"\n")
			printSpool.append("\033[1;31;40m\n"+url+" "+str(k.status_code));			
			file.close()
		else:
			printSpool.append("\033[1;32;40m\n"+"("+str(countOfWords)+"/"+str(queueWords_dummy.index(wordRaw))+")\t: "+str(url)+"  "+str(k.status_code));
		currentWords.remove(wordRaw)
		queue-=1
	except Exception as e:
		try:
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			print str(e)
			while(queueLock):
				pass
			queueLock=True
			queueWords.append(wordRaw)
			queueLock=False
			errors.append("1")
			queue-=1
		except Exception as ex:
			pass

def prints():
	try:
		global count
		while(True):
			while(len(printSpool)==0):
				pass
			sys.stdout.write(printSpool.popleft())
			count+=1
	except sys.excepthook as e:
		pass

start_new_thread(prints,())

def nonFUzzing():
	global queueLock,queueWords,args, queue, baseURL,count
	try:
		while(len(queueWords)!=0):
			while(queueLock):
				pass
			queueLock=True
			word=queueWords.pop() 
			queueLock=False
			if(len(word)==0 or word.startswith("#")):
				count+=1
				continue;
			if(args.DIR):
				start_new_thread(check,(word,baseURL+word+"/"))
				continue;
			for ext in extensions:
				while(queue>=maxQueue):
					pass
				if (re.match(args.REGEX,word)):
					start_new_thread(check,(word,baseURL+word+"."+ext))
	except Exception as e:
		#exc_type, exc_obj, exc_tb = sys.exc_info()
		#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		#print(exc_type, fname, exc_tb.tb_lineno)
		#print str(e)
		pass

def fuzzing():
	global queueLock,queueWords,args, queue, fString,count
	try:
		while(len(queueWords)!=0):
			while(queueLock):
				pass
			queueLock=True
			word=queueWords.pop() 
			queueLock=False
			if(len(word)==0 or word.startswith("#")):
				count+=1
				continue;
			while(queue>=maxQueue):
				pass
			if (re.match(args.REGEX,word)):
				start_new_thread(check,(word,fString.replace("<FUZZ>",word)))
	except Exception as e:
		#exc_type, exc_obj, exc_tb = sys.exc_info()
		#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		#print(exc_type, fname, exc_tb.tb_lineno)
		#print str(e)
		pass

workingValues=[]
args		= argRead();
maxQueue	= int(args.MAX_QUEUE)
skip		= int(args.SKIP_STEP)
wordList	= args.WORDLIST
extensions	= (args.EXTENSIONS).split(",")
port		= args.PORT_ADDRESS
https		= args.HTTPS
basePath	= args.BASE_PATH
fString		= ""
ip		= ""
wordlistFile	= ""
while("."+hexValue in os.listdir(".")):
	ch=raw_input("Previous session is not finished do you want to restore it (y/n) : ")
	if(ch[0]=='y' or ch[0] == 'Y'):
			wordlistFile	= open("."+hexValue,"r")
			break;
	elif(ch[0]=='n' or ch[0] == 'N'):
			wordlistFile	= open(wordList,"r")
			break;
	else:
			print "Oooooo Invalid choice :( "
else:
	wordlistFile	= open(wordList,"r")
			
words		= (wordlistFile.read())
queueWords	= list(words.split("\n"))
queueWords.reverse()
countOfWords	= len(queueWords)
queueWords	= queueWords[0:countOfWords-skip]
queueWords	= deque(queueWords)
queueWords_dummy= list(queueWords)
queueWords_dummy.reverse()
count		= count + skip;
baseURL		= ""

customCond	= ""
if(args.CUST):
	line=""
	print "Enter custom condition on response\nEx \nresponse.status_code==200 and \nresponse.status_code!=404 then preess <CTRL>+D\n"
	contents = []
	while True:
	    try:
		line = raw_input("")
		contents.append(line)
	    except EOFError:
		break
	customCond=" ".join(contents)
	
if(args.FUZZ):
	fString=args.FUZZ_STRING
	if(fString.count("<FUZZ>")==1):
		print "FUZZING"
		fuzzing()
	else:
		print "Ooops I am unable to find fuzz string... :( Retry"
elif(args.IP_ADDRESS):
		ip=args.IP_ADDRESS
		if(https):
			baseURL="https://"
		else:
			baseURL="http://"
		baseURL=baseURL+ip
		if(len(port)>0):
			baseURL+=":"+port	
		baseURL=baseURL+basePath+"/"
		nonFUzzing()
else:
	print "Ooops I am unable to find Target IP/Fuzzing attemp... :( Retry"
	exit(0)


while(True):
	pass
