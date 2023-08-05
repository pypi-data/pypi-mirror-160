from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.columns import Columns
from rich.markdown import Markdown
from rich.table import Table
from rich import print
from rich.text import Text
from rich.json import JSON
from rich.prompt import Prompt, Confirm
from rich.padding import Padding
import argparse
import requests
import time
import json


console = Console()
parser = argparse.ArgumentParser(prog='ShortPaw CLI')
parser.add_argument('-v','--version', action='version', version='%(prog)s 0.1.1')
parser.add_argument("-c", help="Custom URL")
parser.add_argument("-u", help="URL to Shorten")
parser.add_argument("-i", help="Interactive Mode", action="store_true")
args = parser.parse_args()

def interactive():
	url = Prompt.ask("Enter The URL You want to Shorten")
	custom_ask = Confirm.ask("Do You Want to Use a Custom URL?")
	if custom_ask:
		custom_url = Prompt.ask("Enter Your Custom URL and ShortPaw will use it if there are no copies")
		return {"url": url, "custom_url": custom_url, "custom": True}
	else:
		return {"url": url, "custom": False}

def shorten(data_dict):
	if data_dict["custom"]:
		console.log(":green_circle: Detected to Use CUSTOM URLS")
		data = {"url": data_dict["url"], "custom_url": data_dict["custom_url"]}
		url_info_json = requests.post(f'https://shortpaw.herokuapp.com/custom_api', params=data).content
		console.log(":cookie:Successfully Retrived DATA from DATABASE")
		return url_info_json
	else:
		data = {"url": data_dict["url"]}
		console.log(":green_circle: Detected to NOT Use CUSTOM URLS")
		url_info_json = requests.post(f'https://shortpaw.herokuapp.com/api', params=data).content
		console.log(":cookie:Successfully Retrived DATA from DATABASE")
		return url_info_json

console.rule("[bold violet]:dog: ShortPaw: Woof Woof")

if args.i:
	data_dict = interactive()
else:
	if args.u is None:
		console.print("[!] No Specification of URL Found...Opening User Prompt", style="bold red")
		data_dict = interactive()
	else:
		url = args.u
		if args.c is None:
			data_dict = {"url": url, "custom": False}
		else:
			data_dict = {"url": url, "custom_url": args.c, "custom": True}

with console.status("Working On That", spinner="clock"):
	url_info = shorten(data_dict)
console.rule("[bold red]JSON Results")
console.print(JSON(url_info))
console.rule("[bold green]Readable Results")
url_info_json = json.loads(url_info)
console.print(f'Visit your shortened url here [link=https://shortpaw.herokuapp.com/{url_info_json["hash"]}]/{url_info_json["hash"]}[/link]')
panel_1 = Panel(Text("By NoobScience", justify="center", style="bold green"))
print(panel_1)