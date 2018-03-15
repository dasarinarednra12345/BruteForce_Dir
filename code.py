import requests
import sys
import re
import argparse
from thread import start_new_thread
queue=0
count=1

def argRead():
	    """
	    Returns a hash of options     
	    """
	    DESCRIPTION =\
	"Script used for bruteforcing web application directories"
	    EPILOG = \
	"""
	
	"""
	    group=argparse.ArgumentParser( description = DESCRIPTION, epilog = EPILOG,formatter_class = argparse.RawDescriptionHelpFormatter,)
	    group.add_argument('-w', default = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt", dest = "WORDLIST", help = "Wordlist Location",)
	    group.add_argument('-t', default = 10, dest = "MAX_QUEUE", help = "Number of threads",)
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

args = argRead();
maxQueue=int(args.MAX_QUEUE)
skip=int(args.SKIP_STEP)
wordList=args.WORDLIST
extensions=(args.EXTENSIONS).split(",")
port=args.PORT_ADDRESS
https=args.HTTPS
basePath=args.BASE_PATH
ip=""
if(args.IP_ADDRESS):
	ip=args.IP_ADDRESS
else:
	print "Ooops I am unable to find Target IP"
	exit(0)

urls=open(wordList,"r")
url=(urls.read())
count=count+skip;
urls_read=url.split("\n")
total=len(urls_read)
urls_read=urls_read[skip:]
if(https):
	baseURL="https://"
else:
	baseURL="http://"
baseURL=baseURL+ip

if(len(port)>0):
	baseURL+=":"+port	
baseURL=baseURL+basePath+"/"

def check(url):
	global queue
	queue+=1
	try:
		k=requests.head("%s%s"%(baseURL,url),params={})
		if(k.status_code in ['200']):
			file=open(args.OUTPUT_FILE,"a")
			file.write(url+" "+str(k.status_code)+"\n")
			file.close()
		else:
			prints(str(url)+" -> Failed");
		queue-=1
	except Exception as exp:
		print str(exp)
		queue-=1
		check(url)
lock=False
def prints(msg):
	global lock
	global count
	while(lock):
		pass
	lock=True
	sys.stdout.write("\n("+str(total)+"/"+str(count/len(extensions))+") : "+msg)
	count+=1
	lock=False
try:
	for url in urls_read:
		if(args.DIR):
			start_new_thread(check,(url+"/",))
			continue;
		for ext in extensions:
			while(queue>=maxQueue):
				pass
			if (re.match(args.REGEX,url)):
				start_new_thread(check,(url+"."+ext,))
	
except Exception as exp:
	print str(exp);

while(True):
	pass
