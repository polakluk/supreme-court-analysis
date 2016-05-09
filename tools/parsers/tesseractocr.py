# general imports
from  tools.filehelper import FileHelper

import wand.api
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import ctypes

MagickEvaluateImage = wand.api.library.MagickEvaluateImage
MagickEvaluateImage.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]

class TesseractOcr(object):

	# constructor
	def __init__(self, outputDir, isDebug = True):
		self.__outputDir = outputDir
#		self.__img_crop = [270, 150, 1105, 1480] #left top right bottom # 150 DPI
		self.__img_crop = [510, 310, 2260, 2980] #left top right bottom # 300DPI
		self.__threshold = 0.4508
		self.__dpi = 300
		self.__debug = isDebug

	def evaluate(self, img, operation, argument):
		MagickEvaluateImage(
			img.wand,
			wand.image.EVALUATE_OPS.index(operation),
			img.quantum_range * float(argument))


	# reads PDF file and returns its plain text representation
	def readFile(self, pdfFile ):
		tool = pyocr.get_available_tools()[0]
		lang = tool.get_available_languages()[1]

		req_image = []
		final_text = []

		# get file name
		helper = FileHelper()
		outfp = open(self.__outputDir + helper.GetFileName(pdfFile) + ".plain", 'w')

		image_pdf = Image(filename=pdfFile, resolution=self.__dpi)
		image_pngs = image_pdf.convert('png')
		idx = 0
		for img in image_pngs.sequence:
			if self.__debug:
				print "Parsing Page: " + str(idx + 1)
			cloneImg = img[self.__img_crop[0] : self.__img_crop[2], self.__img_crop[1] : self.__img_crop[3] ]
			self.evaluate( cloneImg, 'threshold', self.__threshold)

			txt = tool.image_to_string( PI.open(io.BytesIO(cloneImg.make_blob('png'))), lang=lang, builder=pyocr.builders.TextBuilder())+ "\n"
			outfp.write(txt.encode("utf8"))
			idx += 1
		return 0
