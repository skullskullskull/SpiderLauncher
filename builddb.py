#! /usr/bin/env python3

# builds datbase for spider launcher using xml files and directory scraping.

import os, sys
import sqlite3
import xml.etree.ElementTree as ET

#Determine xml file inputs
if (len(sys.argv)<3):
	sys.exit("Please specify xml files to build database with.\nValid flags are:\n\t-console\n\t-mame\n\t-singles\n\ne.g. %s -mame exported.xml -console scraper_data.xml" % sys.argv[0])

if "-mame" in sys.argv:
	mamexml=sys.argv[sys.argv.index("-mame")+1]
else:
	mamexml=""
if "-console" in sys.argv:
	consolexml=sys.argv[sys.argv.index("-console")+1]
else:
	consolexml=""
if "-singles" in sys.argv:
	singlexml=sys.argv[sys.argv.index("-singles")+1]
else:
	singlexml=""

#Start database
db=sqlite3.connect('.Spiderdb.db')
try:
	db.execute('''DROP TABLE SL''')
except sqlite3.OperationalError:
	pass #table doesn't exist
db.execute('''CREATE TABLE SL (NAME TEXT,LAUNCHER TEXT,GAME TEXT,TAGS TEXT)''')
c=db.cursor()

#launcher = 'mednafen'
#tags='GBA'
#dir="/home/Ned/Roms/GameboyAdvanced"
#ext=".zip"

#walk the directory
def add2db(launcher,tags,dir,ext):
	a=[]
	b=[]
	for root, dirs, files in os.walk(dir):
		for f in files:
		    fullpath = os.path.join(root, f)
		    if os.path.splitext(fullpath)[1] == ext:
		        a.append(fullpath)
		        b.append(f[:-len(ext)])
	for i in range(0,len(a)):
		c.execute('''INSERT INTO SL(NAME,LAUNCHER,GAME,TAGS) VALUES (?, ?, ?, ?)''', (b[i], launcher, a[i], tags) )

#consoles
if len(consolexml)>0:
	print("* Reading %s as console data" % consolexml)
	if os.path.isfile(consolexml):
		tree = ET.parse(consolexml)
		root = tree.getroot()

		for direc in root.findall('directory'):
			launcher = direc.find('Launcher').text #'mednafen'
			tags =  direc.attrib['tag'] #'GBA'
			dir = direc.find('path').text #"/home/Ned/Roms/GameboyAdvanced"
			ext = direc.find('type').text #".zip"
			add2db(launcher,tags,dir,ext)
	else:
		print("\t>%s NOT FOUND" % consolexml)

#mame
if len(mamexml)>0:
	print("* Reading %s as mame data" % mamexml)
	if os.path.isfile(mamexml): # exported=mame
		tree = ET.parse(mamexml)
		root = tree.getroot()

		for direc in root.findall('machine'):
			Name = direc.find('description').text #'Final Fight (World, set 1)'
			Name=Name.split("/")[0].split("(")[0] #'Final Fight'
			file =  direc.attrib['name']  #'ffight'
			c.execute('''INSERT INTO SL(NAME,LAUNCHER,GAME,TAGS) VALUES (?, ?, ?, ?)''', (Name, "mame", file, "Arcade") )
	else:
		print("\t>%s NOT FOUND" % mamexml)

if len(singlexml)>0:
	print("* Reading %s as singles data" % singlexml)
	if os.path.isfile(singlexml):
		tree = ET.parse(singlexml)
		root = tree.getroot()

		for direc in root.findall('file'):
			tags =  direc.attrib['tag'] #'Notes' (name of tab)
			Name = direc.find('Name').text #'Game Notes' (name to display in Spider launcher)
			launcher = direc.find('Launcher').text #'xdg-open'
			file = direc.find('path').text # /home/Ned/temp.txt

			c.execute('''INSERT INTO SL(NAME,LAUNCHER,GAME,TAGS) VALUES (?, ?, ?, ?)''', (Name, launcher, file, tags) )
	else:
		print("\t> %s NOT FOUND" % singlexml)


db.commit()
c.close()
print("Database updated")
