import re

inputFile = 'Orach_Chaim'

open(inputFile)

regex = re.compile(r'<h2><span class="mw-headline" id=.*</ul>')

for line in inputFile:
    regex.findall(line)