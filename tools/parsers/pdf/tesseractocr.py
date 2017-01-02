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
import string

MagickEvaluateImage = wand.api.library.MagickEvaluateImage
MagickEvaluateImage.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]

class TesseractOcr(object):

	# constructor
	def __init__(self, outputDir, isDebug = True):
		self.__outputDir = outputDir
#		self.__img_crop = [270, 150, 1105, 1480] #left top right bottom # 150 DPI

		self.__img_crop_modes = [[510, 310, 2260, 2980], [510, 270, 2260, 2910]]  #left top right bottom # 300DPI ]
		self._middle_line = [1466, 1466]
		self.__img_crop = self.__img_crop_modes[0] # (mode 0 = page numbers top right corner) (mode = 1 page numbers bottom center)
		self.__threshold = 0.4508
		self.__dpi = 300
		self.__debug = isDebug


	def evaluate(self, img, operation, argument):
		MagickEvaluateImage(
			img.wand,
			wand.image.EVALUATE_OPS.index(operation),
			img.quantum_range * float(argument))

	def setOutpuDir(self, output):
		self.__outputDir = output

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

	# reads PDF file and returns its plain text representation
	def readFileAdvanced(self, pdfFile, mode='top-right'):
		mode = 0 if mode == 'top-right' else 1
		self.__img_crop = self.__img_crop_modes[mode]
		tool = pyocr.get_available_tools()[0]
		lang = tool.get_available_languages()[1]

		# this could've been done better, but for now will do
		reCaseSubmitted = re.compile(ur'The case is submitted\.\s*\(Whereupon,', re.UNICODE)
		reCaseSubmitted2 = re.compile(ur'Case is submitted\.\s*\(Whereupon,', re.UNICODE)
		reCaseSubmitted3 = re.compile(ur'\(?Whereupon, at \w\w:\w\w', re.UNICODE)  # the most-relaxed

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
				cloneImg = img[self.__img_crop[0]: self.__img_crop[2], self.__img_crop[1]: self.__img_crop[3]]
				cloneImg.alpha_channel = False
				cloneImg.save(filename = './img_{}.png'.format(idx))
				self.evaluate(cloneImg, 'threshold', self.__threshold)

				txt1 = tool.image_to_string(PI.open(io.BytesIO(cloneImg[:, :self._middle_line[mode]].make_blob('png'))), lang=lang,
										   builder=pyocr.builders.TextBuilder()) + "\n"
				txt2 = tool.image_to_string(PI.open(io.BytesIO(cloneImg[:, self._middle_line[mode]:].make_blob('png'))), lang=lang,
										   builder=pyocr.builders.TextBuilder()) + "\n"
				txt = txt1+txt2
				output_text = output_text + self._clean_text(txt)
				if reCaseSubmitted.search(txt) != None or reCaseSubmitted2.search(txt) != None or reCaseSubmitted3.search(txt) != None:
					print "done"
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
		res = res.replace(u'\xbb', '')
		res = res.replace(u'\ufb02', '')
		return res


	# testing PDF parser
	def testPdf(self, pdfFile, border):
		reCaseSubmitted = re.compile(ur'The case is submitted\.\s*\(Whereupon,', re.UNICODE)
		reCaseSubmitted2 = re.compile(ur'Case is submitted\.\s*\(Whereupon,', re.UNICODE)
		reCaseSubmitted3 = re.compile(ur'\(?Whereupon, at \w\w:\w\w', re.UNICODE)  # the most-relaxed
		tool = pyocr.get_available_tools()[0]
		lang = tool.get_available_languages()[1]

		req_image = []
		final_text = []
		# this could've been done better, but for now will do
		idx = 0
		with Image(filename = pdfFile, resolution=self.__dpi) as img:
#			if self.__debug:
#				print "Parsing Page: " + str(idx + 1)
			cloneImg =img

			cloneImg.alpha_channel = False
			self.evaluate( cloneImg, 'threshold', self.__threshold)

			txt1 = tool.image_to_string( PI.open(io.BytesIO(cloneImg[:, :border].make_blob('png'))), lang=lang, builder=pyocr.builders.TextBuilder())+ "\n"
			txt2 = tool.image_to_string( PI.open(io.BytesIO(cloneImg[:, border:].make_blob('png'))), lang=lang, builder=pyocr.builders.TextBuilder())+ "\n"
			txt = txt1+txt2
			test = self._clean_text(txt1)
			print(txt1)
			print(txt2)
			if reCaseSubmitted.search(txt) != None or reCaseSubmitted2.search(txt) != None or reCaseSubmitted3.search(txt) != None:
				print( 'TRUE' )
			else:
				print('FALSE')
#			print(txt[1000:1179])
#			print(self._clean_text(txt))
