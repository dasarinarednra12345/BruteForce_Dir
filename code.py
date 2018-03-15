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

errors=0
queue=0
count=1
queueLock=False

def signal_handler(signal, frame):
    word=queueWords.pop() 
    file=open(".dir_restore","a")
    file.write(hashlib.md5("".join(sys.argv)).hexdigest()+" "+str(word))
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
	global queue,error,args,queueLock,lock, count
	queue+=1
	try:
		k=requests.head(url,params={})
		scodes=(args.SUCC_CODES).split(",")
		scodes=[int(x) for x in scodes]
		if(int(k.status_code) in scodes):
			file=open(args.OUTPUT_FILE,"a")
			file.write(url+" "+str(k.status_code)+"\n")
			while(lock):
				pass
			lock=True
			sys.stdout.write ("\033[1;31;40m\n"+url+" "+str(k.status_code));
			lock=False
			file.close()
			count+=1
		else:
			prints(str(url)+"  "+str(k.status_code));
		queue-=1
	except Exception as e:
		#exc_type, exc_obj, exc_tb = sys.exc_info()
		#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		#print(exc_type, fname, exc_tb.tb_lineno)
		print str(e)
		while(queueLock):
			pass
		queueLock=True
		queueWords.append(wordRaw)
		queueLock=False
		queue-=1
		

lock=False
def prints(msg):
	global lock
	global count
	while(lock):
		pass
	lock=True
	sys.stdout.write ("\033[1;32;40m\n"+"("+str(countOfWords)+"/"+str(count/len(extensions))+") : "+msg+ " (F) ")
	count+=1
	lock=False

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
wordlistFile	= open(wordList,"r")
words		= (wordlistFile.read())
queueWords	= list(words.split("\n"))
queueWords.reverse()
countOfWords	= len(queueWords)
queueWords	= queueWords[0:countOfWords-skip]
queueWords	= deque(queueWords)
count		= count + skip;
baseURL		= ""

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
