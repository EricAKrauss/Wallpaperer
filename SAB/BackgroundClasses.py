from antlr4 import *
from antlr4.tree.Trees import Trees
import os


class Source:
	def __init__(self, SourceContext):
		line = SourceContext.getText()
		
		self.name = SourceContext.variable().getText()
		self.path = SourceContext.path().getText()
		if self.path[-1] != '/':
			self.path+= '/'
		##print(self.name, self.path)

	def __str__(self):
		return self.name

	def extractImages(self):
		if not os.path.isdir(self.path):
			print(self.path + " is not a valid path")
			return []
		
		files = os.listdir(self.path)
		for i in range(len(files)):
			files[i] = self.path+files[i]
		return files		

class Group:
	def __init__(self, GroupContext):
		self.name = GroupContext.variable().getText()
		##	sources is a list of tuples of numbers with paths
		##	[(1, path), (2, path), (4, path), etc]
		self.paths = []		


		images = GroupContext.image()
		paths = GroupContext.path()
		digits = GroupContext.DIGIT()
		for i in range(len(images)):
			##newPath = [digits[i].getText()]
			##newPath.append(paths[i].getText()+images[i].getText())
			newPath = paths[i].getText()+images[i].getText()
			self.paths.append(newPath)

	def __str__(self):
		return self.name

class Overlay_Text:
	def __init__(self, OverlayContext):
		self.name = OverlayContext.variable().getText()
		self.command = OverlayContext.command().path().getText()+OverlayContext.command().script().getText()
		self.horizontal = self.parseHorizontal(OverlayContext.position())
		self.vertical = self.parseVertical(OverlayContext.position())
		self.justify = self.parseJustify(OverlayContext.position())
		

	def __str__(self):
		return self.name

	def parseHorizontal(self, Position):
		offset = 0
		val = Position.RIGHT()
		if not hasattr(val, "__len__"): ##Really Hacky way of checking whether or not it is a Terminal Node 
			offset = int(Position.PERCENT()[0].getText()[:-1])
		else:
			val = Position.LEFT()
			offset = 100-int(Position.PERCENT()[0].getText()[:-1])

		return offset

	def parseVertical(self, Position):
		offset = 0
		val = Position.TOP()
		if not hasattr(val, "__len__"):
			offset = int(Position.PERCENT()[1].getText()[:-1])
		else:
			val = Position.BOTTOM()
			offset = 100-int(Position.PERCENT()[1].getText()[:-1])

		return offset

	def parseJustify(self, Position):
		return Position.JUSTIFY().getText()

class Overlay_Image:
	def __init__(self, OverlayContext):
		self.name = OverlayContext.variable().getText()
		self.image = OverlayContext.path().getText()+OverlayContext.image().getText()
		self.horizontal = self.parseHorizontal(OverlayContext.position())
		self.vertical = self.parseVertical(OverlayContext.position())
		self.justify = self.parseJustify(OverlayContext.position())

	def __str__(self):
		return self.name

	def parseHorizontal(self, Position):
		offset = 0
		val = Position.RIGHT()
		if not hasattr(val, "__len__"): ##Really Hacky way of checking whether or not it is a Terminal Node 
			offset = int(Position.PERCENT()[0].getText()[:-1])
		else:
			val = Position.LEFT()
			offset = 100-int(Position.PERCENT()[0].getText()[:-1])

		return offset

	def parseVertical(self, Position):
		offset = 0
		val = Position.TOP()
		if not hasattr(val, "__len__"):
			offset = int(Position.PERCENT()[1].getText()[:-1])
		else:
			val = Position.BOTTOM()
			offset = 100-int(Position.PERCENT()[1].getText()[:-1])

		return offset

	def parseJustify(self, Position):
		return Position.justified_pos().getText()

class Slideshow:
	def __init__(self, SlideshowContext):
		self.name = SlideshowContext.variable().getText()
		##	sources is a list of tuples of numbers with paths or Sources
		##	[(1, path), (2, path), (4, path), etc]
		self.sources = self.parseSources(SlideshowContext.slidesource())
		self.time = self.parseTime(SlideshowContext.slidetime()) ##In seconds
		self.order = SlideshowContext.slideorder().getText().split(' ')[-1]

	def __str__(self):
		return self.name
	
	def parseSources(self, ContextList):
		outList = []
		for i in range(len(ContextList.DIGIT())):
			outList.append([int(ContextList.DIGIT()[i].getText()), ContextList.variable()[i].getText()])
		return outList

	def parseTime(self, SlideTime):
		digitStream = ""
		for i in range(len(SlideTime.DIGIT())):
			digitStream += SlideTime.DIGIT()[i].getText()
		time = int(digitStream)
		timetype = SlideTime.timetype().getText()
		if timetype[0] in "Mm": #If it's in minutes
			time = time * 60
		if timetype[0] in "Hh": #If it's in hours
			time = time * 60 * 60
		return time

	
