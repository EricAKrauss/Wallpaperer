import sys
import subprocess
from antlr4 import *
from antlr4.tree.Trees import Trees
from SABLexer import SABLexer
from SABParser import SABParser
from SABListener import SABListener
from BackgroundClasses import *
from ImageBuilder import *
import random
import time

global SOURCES
SOURCES = []
global GROUPS 
GROUPS = []
global OVERLAYS 
OVERLAYS = {"TEXT":[], "IMAGES":[]}
global SLIDESHOWS 
SLIDESHOWS = []


def main(argv):
	currentImage = None	

	if len(argv) <= 1:
		print("No File Passed")
		return False
	inputFile = FileStream(argv[1])
	lexer = SABLexer(inputFile)
	stream = CommonTokenStream(lexer)
	parser = SABParser(stream)
	listener = SABListener()
	tree = parser.s()
	walker = ParseTreeWalker()

	walker.walk(listener, tree)
	buildGlobals(tree)
	
	##runSlideshow(SLIDESHOWS[0])
	
	postMain(argv)

def postMain(argv):
	overlay = True

	if len(argv) <= 2:
		variable = input("Which Slideshow or Group would you like to run?  :")
	else:
		variable = argv[2]
		if len(argv) > 3:
			if argv[3] == "False":
				overlay = False

	target = None
	for grp in GROUPS:
		if grp.name == variable:
			target = grp
			break
	if target == None:	
		for sld in SLIDESHOWS:
			if sld.name == variable:
				target = sld
				break
	
	if target != None:
		if isinstance(target, Group):
			displayGroup(target, overlay)
		if isinstance(target, Slideshow):
			runSlideshow(target, overlay)

	if len(argv) <= 2:
		return postMain(argv)
	else:
		return


def exec_overlayImage(overlay_obj, currentImage):
	if currentImage == None:
		return False
	overlayImage(currentImage, overlay_obj.image, overlay_obj.justify, overlay_obj.horizontal, overlay_obj.vertical)
	return True

def exec_overlayText(overlay_obj, currentImage):
	if currentImage == None:
		return False
	command = overlay_obj.command
	string = exec_command(command)
	overlayText(currentImage, string, overlay_obj.justify, overlay_obj.horizontal, overlay_obj.vertical)
	return True

def exec_overlays(currentImage):
	for image_overlay in OVERLAYS["IMAGES"]:
		exec_overlayImage(image_overlay, currentImage)
	for text_overlay in OVERLAYS["TEXT"]:
		exec_overlayText(text_overlay, currentImage)

def exec_command(command):
	process = subprocess.Popen([command], stdout=subprocess.PIPE, universal_newlines=True)
	process.wait()
	output = processSTDOUT(process.stdout)
	process.kill()
	return output

def buildComposite(group):
	return combineWallpaper(group.paths)

def buildCompositeFromList(images):
	return combineWallpaper(images)

def setBackground(imagePath):
	args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://"+imagePath]
	process = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)
	process.wait()
	output = processSTDOUT(process.stdout)
	if len(output) > 0:
		print(output)
	process.kill()
	
	return imagePath

def processSTDOUT(stdout): ##stdout is a stream
	outText = ""
	outLine = str(stdout.readline())
	while(outLine):
		outText+=outLine
		outText+='\n'
		outLine = str(stdout.readline())
	stdout.close()
	return outText

	
def buildGlobals(tree):
	heads = tree.head()
	for ahead in heads:
		item = ahead.source()
		if item:
			SOURCES.append(Source(item))
			continue

		item = ahead.slideshow()
		if item: 
			SLIDESHOWS.append(Slideshow(item))
			continue

		item = ahead.group()
		if item: 
			GROUPS.append(Group(item))
			continue

		item = ahead.overlay_text()
		if item: 
			OVERLAYS["TEXT"].append(Overlay_Text(item))
			continue

		item = ahead.overlay_image()
		if item:
			OVERLAYS["IMAGES"].append(Overlay_Image(item))
			continue


def displayGroup(grp, overlay):
	compositeImage = buildComposite(grp)
	if overlay:
		exec_overlays(compositeImage)
	setBackground(compositeImage)

def runSlideshow(slideshow, overlay):
	imageDict = setupSlideshow(slideshow)

	if len(imageDict.keys()) == 1:
		runSingleImageSlideshow(imageDict, slideshow.time, overlay)
	else:
		runMultiImageSlideshow(imageDict, slideshow.time, overlay)

def runSingleImageSlideshow(imageDict, delay, overlay):
	images = imageDict[list(imageDict.keys())[0]]
	while True:
		for img in images:
			tempbkg = setBackground(img)
			if overlay:
				exec_overlays(tmpbkg)
			time.sleep(delay)
		
def runMultiImageSlideshow(imageDict, delay, overlay):
	while True:
		outImages = []
		keys = list(imageDict.keys())
		keys.sort()
		for key in keys:
			images = imageDict[key]
			outImages.append(images[random.randrange(len(images))])
		compositeImage = buildCompositeFromList(outImages)
		if overlay:
			exec_overlays(compositeImage)
		setBackground(compositeImage)
		time.sleep(delay)
	

def setupSlideshow(slideshow):
	imageDict = {}
	for src in slideshow.sources:
		for s in SOURCES:
			if src[1] == s.name:
				imageDict[src[0]]=s.extractImages()
	if slideshow.order == "SHUFFLE":
		for key in list(imageDict.keys()):
			random.shuffle(imageDict[key])

	return imageDict
		
	
if __name__ == "__main__":
	main(sys.argv)
