#!/bin/python

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from time import sleep



# Set up / compile regular expressions
fullPathRegex = re.compile('http*') # Dealing with the telephone numbers in href tags
slashRegex = re.compile('^/[A-Z a-z 0-9]*')
lastSlashRegex = re.compile('/$')
domainRegex = re.compile('') #check to see what is after the :// in a url (for grabbing the base)

# Things to become arguments later down the line
initUrl = 'http://www.contextis.com'
depth = 1
singleDomain = 1
hostname = urlparse(initUrl).hostname
throttle = 10 # multiplied by 0.1 for the throttle on each request.

# Some handy lists
scannedList = [] # Will contain a list of all previously scanned pages
fullUrlDict = {} # Will contain a dictionary of items 
fullUrlList = [] # Will contain a list of every found URL


def requestFunction(url, depth, recursionLevel, singleDomain, throttle):
	if throttle > 0:
		sleep(throttle * 0.1)
	urlList = [] # Will eventually contain all URLs for this page in a list
	print ('recursionLevel = ', recursionLevel)
	print ('depth = ', depth)

	if recursionLevel <= depth:
		r = requests.get(url)
		content = r.content
		soup = BeautifulSoup(content, "html.parser")
		print("\nScanning URL:	" + url + "\n")
		scannedList.append(url)
		for link in soup.find_all('a'):
			href = link.get('href') # get the href attribute for the current link

			# Perform various regular expressions for later conditionals
			fullPathTest = fullPathRegex.match(href) # Various fringe cases (telephone numbers etc.)
			slashPathTest = slashRegex.match(href) # These regular expressions make sure only URLs come through!
			slashPathEndTest = lastSlashRegex.match(href) # This removes any slashes at the end, for formatting.

			if href.endswith("/"):
				href = href[:-1] # remove the slash at the end, if there is one.

			currentDomainParsed = urlparse(url)
			currentDomain = currentDomainParsed.scheme + "://" + currentDomainParsed.netloc

			if slashPathTest: # Matches URLS starting with a /
				# Converts it to a full URL (for consistency, of course)
				newUrl = currentDomain + href
				urlList.append(newUrl)
			if fullPathTest: # Matches full URLs
				urlList.append(href)
		urlList = list(set(urlList)) # Remove any duplicates
		urlList = sorted(urlList) # Sort the list alphabetically for readability
		fullUrlDict.update({url:urlList}) # Add the url list to the dictionary
		recursionLevel =+ 1 # Recursion is deeper now!

		for url in urlList:
			print(url)

		for nextUrl in urlList: # Go through all these scanned urls
			if not nextUrl in scannedList: # Make sure we're not re-scanning pages!
				if singleDomain == 1: # Is single domain mode turned on? 
					if urlparse(nextUrl).hostname == hostname: # Then only use urls with out hostname in.
						requestFunction(nextUrl, depth, recursionLevel, singleDomain, throttle)
				else: # if not, fuck it! Let's scan EVERYTHING
						requestFunction(nextUrl, depth, recursionLevel, singleDomain, throttle)





requestFunction(initUrl, depth, 0, singleDomain, throttle)