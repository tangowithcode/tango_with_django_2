import json
import requests

# Add your Microsoft Account Key to a file called bing.key

def read_bing_key():
	"""
	reads the BING API key from a file called 'bing.key'
	returns: a string which is either None, i.e. no key found, or with a key
	remember to put bing.key in your .gitignore file to avoid committing it to the repo.
	
	
	See Python Anti-Patterns - it is an awesome resource to improve your python code
	Here we using "with" when opening documents
	http://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html
	"""
	
	
	bing_api_key = None
	try:
		with open('bing.key','r') as f:
			bing_api_key = f.readline().strip()
			
	except:
		raise IOError('bing.key file not found')
		
		
	if not bing_api_key:
		raise KeyError('Bing key not found')	
	
	return bing_api_key


def run_query(search_terms, bing_key):
	"""
	See the Microsoft's documentation on other parameters that you can set.
	https://docs.microsoft.com/en-gb/rest/api/cognitiveservices/bing-web-api-v7-reference
	"""
	
	search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
	headers = {"Ocp-Apim-Subscription-Key" : bing_key}
	params  = {"q": search_terms, "textDecorations":True, "textFormat":"HTML"}
	response = requests.get(search_url, headers=headers, params=params)
	response.raise_for_status()
	search_results = response.json()
	results = []
	for result in search_results["webPages"]["value"]:
		results.append({
			'title': result['name'],
			'link': result['url'],
			'summary': result['snippet']})
	
	return results


def main():

	bing_api_key = read_bing_key()

	print("Enter a query ")
	query = input()

	results = run_query(query, bing_api_key)	
	for result in results:
		print(result['title'])
		print('-'*len(result['title']))
		print(result['summary'])
		print(result['link'])
		print()


if __name__ == '__main__':
	main()