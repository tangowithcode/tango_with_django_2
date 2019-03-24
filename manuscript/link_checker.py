# Checks for broken links in the book chapters, printing the status of each link found to stdout.
# The Python package 'requests' must be installed and available for this simple module to work.
# Author: David Maxwell
# Date: 2017-02-14
import re
import requests

def main(chapters_list_filename, hide_success=True):
	"""
	hide_success = a boolean switch that determines whether to show URLs that return a HTTP 200.
	If set to true, only URLs that fail will be printed.
	"""
	chapters_f = open(chapters_list_filename, 'r')
	pattern = re.compile(r'\[([^]]+)]\(\s*(http[s]?://[^)]+)\s*\)')  # http://stackoverflow.com/a/23395483
	
	print('filename\tline_no\ttitle\turl\tstatus_code')
	
	for filename in chapters_f:
		filename = filename.strip()
		
		if not filename or filename.startswith('{'):  # Skip non-filename lines
			continue
		
		chapter_f = open(filename, 'r')
		line_no = 1
		
		for line in chapter_f:
			line = line.strip()
			
			for match in re.findall(pattern, line):
				title = match[0]
				url = match[1]
				
				if '127.0.0.1' in url or 'localhost' in url:  # Don't check localhost URLs
					continue
				
				request = None
				status_code = -1
				
				try:
					request = requests.get(url)
					status_code = request.status_code
				except requests.exceptions.ConnectionError:
					request = None
					status_code = 'FAILED_TO_CONNECT'
				
				if hide_success and status_code == 200:
					continue
				
				title = title.replace('\t', ' ')
				
				print('{filename}\t{line_no}\t{title}\t{url}\t{status_code}'.format(filename=filename,
																					line_no=line_no,
																					title=title,
																					url=url,
																					status_code=status_code))
			
			line_no = line_no + 1
		
		chapter_f.close()
	
	chapters_f.close()

if __name__ == '__main__':
	main('Book.txt', hide_success=False)