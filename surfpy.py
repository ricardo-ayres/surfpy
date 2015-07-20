#!/usr/bin/python2
import sys
import subprocess
import urllib

def print_help():
    print("""Usage: $ surfpy [engine tag] [your search terms]
    If the engine tag is not defined in the options the search terms along with the given tag will be passed to a fallback search engine.
    """)

# Options:
browser = "firefox" #insert the command for your preferred browser here.

# Search engines:
## Insert your custom search engines here following the syntax of the other ones. Don't forget the commas.
available_engines = {
"ddg":["https://www.duckduckgo.com/?", "q"],
"yt":["https://www.youtube.com/results?","search_query"],
"awiki":["https://wiki.archlinux.org/index.php?", "search"],
"python2":["https://docs.python.org/2/search.html?", "q"],
"imgur":["https://imgur.com/search?", "q"],
}

# End of options.
# Now this is doing stuff.

if len(sys.argv) < 3:
    print_help()
    sys.exit()

search_engine = sys.argv[1]

if search_engine in available_engines:
    engine_url = available_engines[search_engine][0]
    search_prefix = available_engines[search_engine][1]

search_string = " ".join(sys.argv[2::])
query_url = engine_url + urllib.urlencode({search_prefix:search_string})
subprocess.Popen([browser, query_url])
sys.exit(0)
