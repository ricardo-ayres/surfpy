#!/bin/env python3
import sys
import subprocess
import validators
from urllib.parse import quote_plus


def print_help():
	global fallback_engine
	help_message = "\n".join([
		"Usage:\n$ surfpy [engine tag] [your search terms]",
		"$ surfpy -l (or --list) lists your tags and descriptions and exits.",
		"$ surfpy -h (or --help) prints this help and exits.",
		"$ surfpy --print-only will print the string to stdout without passing it to the browser.",
		"$ surfpy -b [browser] uses [browser] instead of the browser defined in the options.",
		"$ surfpy --dmenu launches dmenu for interactive tag selection.",
		"If the engine tag is not defined in the options all the arguments will be passed to a fallback search engine defined in the options."
	])

	print(
		"Current fallback engine:\n",
		f"{sengine.fallback}"
	)


class sengine:
	tags = {}
	fallback = None
	browser = ""

	def __init__(self, tag, url=None, fallback=False, **kwds):
		self.tag = tag
		self.url = url

		# register itself as one of the available engines
		sengine.tags[self.tag] = self

		# set itself as the fallback engine if explicitly specified
		if fallback:
			sengine.fallback = self

		if 'browser' in kwds:
			self.browser = kwds['browser']
		if 'description' in kwds:
			self.description =  kwds['description']

	def get_query(self, search_string):
		return self.url + quote_plus(search_string)

	def __repr__(self):
		return f"{self.tag}\t\t{self.description}"

	def instances():
		return list(sengine.tags.values())

	def print_engines(self):
		for engine in sengine.instances():
			print(engine)


class plain_url(sengine):
	def get_query(self, url):
		return url


##### Options: #####
# set additional arguments for dmenu, like font selection or color options.
dmenu_arguments = ""

# set default browser
sengine.browser = "surf"

# create a plain_url instance and tag to handle direct urls correctly
plain_url(tag="url")

# Search engines:
# Insert your custom search engines here.

sengine(fallback=True,
		tag="ddg",
		url="https://www.duckduckgo.com/?q=",
		description="DuckDuckGo")

sengine(tag="yt",
		url="https://www.youtube.com/results?search_query=",
		description="YouTube")

sengine(tag="img",
		url="https://duckduckgo.com/?ia=images&iax=1&q=",
		description="DuckDuckGo image search")

##### End of options. #####

print_only = False
input_list = sys.argv[1::]
browser = None

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
	for engine in sengine.instances():
		dmenu_tags += engine.tag + '\n'
	dmenu_command = f"echo \"{dmenu_tags}\" | dmenu -p 'Surfpy:' {dmenu_arguments}"

	try:
		input_list = subprocess.check_output(
			dmenu_command,
			stderr=subprocess.STDOUT,
			shell=True,
			text=True).strip().split()

	except subprocess.CalledProcessError:
		print("could not run dmenu!")
		sys.exit(0)

try:
	chosen = sengine.tags[input_list[0]]
	input_list.pop(0)

except:
	arg = input_list[0]
	url = lambda x: validators.url(x)
	if url(arg) or url("http://"+arg) or url("https://"+arg):
		chosen = sengine.tags['url']
	else:
		chosen = sengine.fallback

search_string = " ".join(input_list)
query_url = chosen.get_query(search_string)

if not browser:
	browser = chosen.browser

if print_only:
	print(query_url)

else:
	subprocess.Popen([browser, query_url])

sys.exit(0)
