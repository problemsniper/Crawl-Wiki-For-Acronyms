# coding=utf-8
__author__ = 'krishnateja'
import urllib
from bs4 import BeautifulSoup
import string
import re
# This Python file uses the following encoding: utf-8

checker = True
multipleAcronyms = False
multipleAcroLines = False
listOfAbbr = []
alphabets = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# websiteFile = open("WikiWebsite.txt", "w")
wedSiteClean = open("WikiWebsiteClean.txt", "w")
acronymsFile = open("AcronymsFile.csv", "w")

for alphabet in alphabets:
    if checker:
        url = "https://en.wikipedia.org/wiki/List_of_acronyms"
        checker = False
        print url
    else:
        url = "https://en.wikipedia.org/wiki/List_of_acronyms:_" + alphabet
        print url

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    websiteFile.write(text.encode('utf-8'))

delete_list = ["(a)", "(i)", "(p)", "(s)", "Article", "Talk", "Variants", "Views", "Read", "Edit-View history", "More", "Jargon", "Edit"]

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

with open('WikiWebsite.txt') as fin:
    for line in fin:
        for word in delete_list:
            line = line.replace(word, "")

        if not is_ascii(line):
            line = line.replace('–', '-')

        wedSiteClean.write(line)

with open('WikiWebsiteClean.txt') as f:
    content = f.readlines()
    for line in content:
        if re.match("^[A-Za-z0-9]+\s-\s.*", line):
            # print line
            if multipleAcronyms:
                multipleAcronyms = False
                multipleAcroLines = False
                severalAcronyms = ",".join(listOfAbbr)
                acronymsFile.write(severalAcronyms+"\n")
                listOfAbbr = []
            acronymsFile.write(line)

        elif re.match("[A-Za-z0-9,]{2,8}$", line):
            # print line
            if multipleAcronyms:
                multipleAcronyms = False
                multipleAcroLines = False
                severalAcronyms = ",".join(listOfAbbr)
                acronymsFile.write(severalAcronyms+"\n")
                listOfAbbr = []
            acronymsFile.write(line.strip("\n"))
            acronymsFile.write('-')
            multipleAcroLines = True
            multipleAcronyms = True

        elif multipleAcroLines:
            listOfAbbr.append(line.strip("\n"))
            multipleAcronyms = True

