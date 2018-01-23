# SpiderLauncher
Spider Launcher is a python script to launch other programs.

![screenshot](https://raw.githubusercontent.com/skullskullskull/SpiderLauncher/master/image.png)

Spider Launcher uses the Tkinter library for graphics. It reads from a sqlite database (.Spiderdb.db) and creates buttons in tabs to launch a *program* and a *parameter*. 

.Spiderdb.db format:
```
NAME		| LAUNCHER		| GAME				| TAGS
-------------------------------------------------------------------------------
Tekken3		mednafen		/home/Skull/PS1/tekken3.cue	PS1
Duckduckgo	firefox			wwww.duckduckgo.com		WWW
Tekken4		PCSX2 --nogui		/home/Skull/PS2/tekken4.gz	PS2
```
**NAME** is the name the button will display
**LAUNCHER** is the program used 
**GAME** is the parameter that is passed to LAUNCHER
**TAGS** is the tab the button will be displayed under in the program

Clicking on the 'Duckduckgo' button is the same as typing `firefox www.duckduckgo.com` in a terminal.
Any vaild terminal command will work as a vaild LAUNCHER/GAME pair. Additional parameters should be in the LAUNCHER field and not the GAME field.


## ADDING TO THE DATABASE
The python script `builddb.py` builds the database based on xml files. Spider Launcher does not add items to the database. There are three types of supported xml: *console*, *mame*, and *singles*. "console" is for adding a directory of files, "mame" is for adding exported xml from mame, and "singles is for single path entries. These xml files need to be passed to script as follows:
> $ python3 builddb.py -console console.xml -mame exported.xml -singles singles.xml 

1 or more xml type(s) must be used to populate the database.


### -console
builddb.py can scrape a directory (and child directories) for all files of a given extension. Directories to be scraped are defined in an xml file of the form:
```
	<?xml version="1.0"?>
	<data>
		<directory tag="Touhou">
			<Launcher>bash</Launcher>
			<type>.sh</type>
		    <path>/home/Skull/Games/TOUHOU/</path>
		</directory>
		<directory tag="PS1">
			<Launcher>mednafen</Launcher>
			<type>.cue</type>
		    <path>/home/Skull/Roms/PS1/<path>
		</directory>     
		...
	</data>
```
Based on above xml, `builddb.py` will crawl through /home/Skull/Games/TOUHOU/ and all child directories looking for any file that ends in the extension ".sh" and will add NAME (name of file) and GAME (path to file) to the database. LAUNCHER and TAGS are taken from the Launcher field and tag attribute respectively. TAGS are totally arbitrary and can be shared between launchers/directories/types. 


### -mame
builddb.py can parse exported mame (v0.189) xml files. This file, by default, is called "exported.xml". To export from mame, find the floppy disk icon with the caption that reads "Export displayed file to list" above mame's list of games. builddb.py will trim the name to exclude alternate names and parenthetical words. A name like "Pac-Man/Puck man (1980)" would get trimmed to "Pac-man".

### -singles
Single entities can be added to the database as well. xml is in the form:
```
	<?xml version="1.0"?>
	<data>
		<file tag="WWW">
			<Name>Duckduckgo</Name>
			<Launcher>firefox</Launcher>
		    <path>www.duckduckgo.com</path>
		</file> 
		...
	</data>
```
This is structurally similar to "consoles", but adds the path value to the database instead of scraping a directory. This is useful for adding paths that are not on your system, like a website, or a one off type of program, like a media player with a playlist. 
