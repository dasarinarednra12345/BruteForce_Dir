# BruteForce_Dir is a python script designed for bruteforcing web application directories and files. It can also fuzz the web application
New features:
  1. Custom code can be given by user
  2. Restore option on bruteforce attack
  3. Much control for user 
  
  ```
usage: Detect_Dir [-h] [-fuzz] [-custom] [-fstring FUZZ_STRING]
                  [-scodes SUCC_CODES] [-w WORDLIST] [-t MAX_QUEUE]
                  [-o OUTPUT_FILE] [-dir] [-i IP_ADDRESS] [-p PORT_ADDRESS]
                  [-https] [-s SKIP_STEP] [-b BASE_PATH] [-r REGEX]
                  [-e EXTENSIONS]

Script used for bruteforcing web application directories and files

optional arguments:
  -h, --help            show this help message and exit
  -fuzz, --fuzz         Enable Fuzzin
  -custom, --custom     Enable custom code input
  -fstring FUZZ_STRING  Input fuzz string
  -scodes SUCC_CODES    Success status code comma seperated
  -w WORDLIST           Wordlist Location
  -t MAX_QUEUE          Number of parallel attemps
  -o OUTPUT_FILE        Output file
  -dir, --dir           Bruteforce directories
  -i IP_ADDRESS         HOST_IP
  -p PORT_ADDRESS       Port address
  -https, --https       Enable this flag if https is enabled
  -s SKIP_STEP          Skip_first_n_entries in wordlist
  -b BASE_PATH          Base directory to start bruteforcing
  -r REGEX              Regex will be applied on each entry on wordlist to
                        find validity
  -e EXTENSIONS         COmma seperated extensions

Examples :
	Detect_Dir --fuzz -fstring "http://example.com/<FUZZ>/index.html"	
  ```
