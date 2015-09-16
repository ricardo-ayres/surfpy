#!/usr/bin/python2
import sys
import subprocess
from urllib import urlencode

def print_help():
    global fallback_engine
    print("Usage:\n$ surfpy [engine tag] [your search terms]")
    print("$ surfpy -l (or --list) lists your tags and descriptions and exits.")
    print("$ surfpy -h (or --help) prints this help and exits.")
    print("$ surfpy --dmenu launches dmenu for interactive tag selection.")
    print("""If the engine tag is not defined in the options all
the arguments will be passed to a fallback search engine
defined in the options.""")
    print("Current fallback engine:\n%s\t\t%s" % (fallback_engine, available_engines[fallback_engine][2]))

def list_engines():
    for i in available_engines:
        if len(i) > 7:
            print("%s\t%s" % (i, available_engines[i][2]))
        else:
            print("%s\t\t%s" % (i, available_engines[i][2]))

##### Options: #####

browser = "firefox" #insert the command for your preferred browser here.
fallback_engine = "ddg" #set the fallback engine tag you want to use.

# Search engines:
## Insert your custom search engines here following the syntax of the other ones. Don't forget the commas.
# "engine-tag":["engine url with trailing '?' ", " search prefix ", "name or short description"],

available_engines = {
"ddg":["https://www.duckduckgo.com/?", "q", "DuckDuckGo"],
"yt":["https://www.youtube.com/results?","search_query", "YouTube"],
"awiki":["https://wiki.archlinux.org/index.php?", "search", "Arch Wiki"],
"python2":["https://docs.python.org/2/search.html?", "q", "Python 2.7 documentation"],
"imgur":["https://imgur.com/search?", "q", "imgur"],
"wallhaven":["http://alpha.wallhaven.cc/search?", "q", "Wallhaven"],
"dA":["http://www.deviantart.com/browse/all/?", "section=&global=1&q", "deviantART"],
"img":["https://duckduckgo.com/?ia=images&iax=1&", "q", "DuckDuckGo image search"],
}

##### End of options. #####

print_only = False
input_list = sys.argv[1::]

if "--list" in sys.argv[:2:] or "-l" in sys.argv[:2:]:
    list_engines()
    sys.exit(0)
    
if "--help" in sys.argv[:2:] or "-h" in sys.argv or len(sys.argv[:2:]) < 2:
    print_help()
    sys.exit(0)
    
if "-b" in sys.argv:
    browser_index = sys.argv.index("-b")+1
    browser = sys.argv[browser_index]
    input_list.remove("-b")
    input_list.remove(browser)

if "--print-only" in sys.argv:
    input_list.remove("--print-only")
    print_only = True
    
if "--dmenu" in sys.argv:
    input_list.remove("--dmenu")
    dmenu_tags = ''
    for tag in available_engines:
        dmenu_tags += tag + '\n'
    dmenu_command = "echo \"%s\" | dmenu -p 'Surfpy:'" % dmenu_tags
    
    try:
        input_list = subprocess.check_output(
            dmenu_command,
            stderr=subprocess.STDOUT,
            shell=True).strip().split()
      
    except subprocess.CalledProcessError:
        sys.exit(0)

if input_list[0] in available_engines:
    search_engine = input_list[0]
    search_string = " ".join(input_list[1::])
    
else:
    search_engine = fallback_engine
    search_string = " ".join(input_list)

engine_url = available_engines[search_engine][0]
search_prefix = available_engines[search_engine][1]
query_url = engine_url + urlencode({search_prefix:search_string})

if print_only:
    print(query_url)
else:
    subprocess.Popen([browser, query_url])

sys.exit(0)
