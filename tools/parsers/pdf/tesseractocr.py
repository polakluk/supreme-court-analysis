# -*- coding: utf-8 -*-

# general imports
from  tools.filehelper import FileHelper

import wand.api
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import ctypes
import re

MagickEvaluateImage = wand.api.library.MagickEvaluateImage
MagickEvaluateImage.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]

class TesseractOcr(object):

	# constructor
	def __init__(self, outputDir, isDebug = True):
		self.__outputDir = outputDir
#		self.__img_crop = [270, 150, 1105, 1480] #left top right bottom # 150 DPI

		self.__img_crop_modes = [[510, 310, 2260, 2980], [510, 270, 2260, 2910]]  #left top right bottom # 300DPI ]
		self.__img_crop = self.__img_crop_modes[0] # (mode 0 = page numbers top right corner) (mode = 1 page numbers bottom center)
		self.__threshold = 0.4508
		self.__dpi = 300
		self.__debug = isDebug


	def evaluate(self, img, operation, argument):
		MagickEvaluateImage(
			img.wand,
			wand.image.EVALUATE_OPS.index(operation),
			img.quantum_range * float(argument))


	# reads PDF file and returns its plain text representation
	def readFile(self, pdfFile, mode = 'top-right' ):
		mode = 0 if mode == 'top-right' else 1
		self.__img_crop = self.__img_crop_modes[mode]
		tool = pyocr.get_available_tools()[0]
		lang = tool.get_available_languages()[1]

		# this could've been done better, but for now will do
		reCaseSubmitted = re.compile(ur'The case is submitted\.\s*\(Whereupon,', re.UNICODE)
		reCaseSubmitted2 = re.compile(ur'Case is submitted\.\s*\(Whereupon,', re.UNICODE)
		reCaseSubmitted3 = re.compile(ur'\(?Whereupon, at \w\w:\w\w', re.UNICODE) # the most-relaxed

		# get file name
		helper = FileHelper()
		outfp = open(self.__outputDir + helper.GetFileName(pdfFile) + ".plain", 'w')

		with Image(filename=pdfFile, resolution=self.__dpi) as image_pdf:
			image_pngs = image_pdf.convert('png')
			idx = 0
			output_text = ''
			for img in image_pngs.sequence:
				if self.__debug:
					print "Parsing Page: " + str(idx + 1)
				cloneImg = img[self.__img_crop[0] : self.__img_crop[2], self.__img_crop[1] : self.__img_crop[3] ]
				cloneImg.alpha_channel = False
#				cloneImg.save(filename = './img_{}.png'.format(idx))
				self.evaluate( cloneImg, 'threshold', self.__threshold)

				txt = tool.image_to_string( PI.open(io.BytesIO(cloneImg.make_blob('png'))), lang=lang, builder=pyocr.builders.TextBuilder())+ "\n"
				output_text = output_text + self._clean_text(txt)
				if reCaseSubmitted.search(txt) != None or reCaseSubmitted2.search(txt) != None or reCaseSubmitted3.search(txt) != None:
					break
				idx += 1

		outfp.write(output_text)


	# clean up pdf parsed text from unwanted characters
	def _clean_text(self, txt):
		res = txt.replace(u'—','-')
		res = res.replace(u'‘','\'')
		res = res.replace(u'’','\'')
		res = res.replace(u'\xa7','')
		res = res.replace(u'\u201c', '"')
		res = res.replace(u'\u201d', '"')
		res = res.encode('ASCII')
		return res


	# testing PDF parser
	def testPdf(self, pdfFile, idx, mode = 'top-right'):
		mode = 0 if mode == 'top-right' else 1
		self.__img_crop = self.__img_crop_modes[mode]
		tool = pyocr.get_available_tools()[0]
		lang = tool.get_available_languages()[1]

		req_image = []
		final_text = []
		reCaseSubmitted = re.compile(ur'\(Whereupon, at \w\w:\w\w', re.UNICODE)
		# get file name
		helper = FileHelper()
#		outfp = open(self.__outputDir + helper.GetFileName(pdfFile) + ".plain", 'w')

#		image_pdf = Image(filename=pdfFile, resolution=self.__dpi)
#		image_pngs = image_pdf.convert('png')
#		img = image_pngs.sequence[idx]
		idx = 0
		with Image(filename = pdfFile) as img:
#			if self.__debug:
#				print "Parsing Page: " + str(idx + 1)
			cloneImg = img
			#img[self.__img_crop[0] : self.__img_crop[2], self.__img_crop[1] : self.__img_crop[3] ]
			cloneImg.alpha_channel = False
			cloneImg.save(filename = './img_{}.png'.format(idx))
			self.evaluate( cloneImg, 'threshold', self.__threshold)

			txt = tool.image_to_string( PI.open(io.BytesIO(cloneImg.make_blob('png'))), lang=lang, builder=pyocr.builders.TextBuilder())+ "\n"
			test = self._clean_text(txt)
#			print(txt[1000:1179])
			print(self._clean_text(txt))
