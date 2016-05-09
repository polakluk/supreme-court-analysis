# general imports
from  tools.filehelper import FileHelper
# PDF related imports
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import pdfminer.pdfdocument
import pdfminer.pdfpage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


# this class reads pdf with oral argument and is supposed to simply turn it into a plain text
class Pdf(object):

	# constructor
	def __init__(self, outputDir):
		self.__outputDir = outputDir


	# reads PDF file and returns its plain text representation
	def readFile(self, pdfFile ):
		rsrcmgr = PDFResourceManager(caching=True)

		pagenos = set()
		# get file name
		helper = FileHelper()
		outfp = file(self.__outputDir + helper.GetFileName(pdfFile) + ".plain", 'w')

		# read PDF
		laparams = LAParams()
		laparams.all_texts = False
		device = TextConverter(rsrcmgr, outfp, codec='ascii', laparams=laparams )
		fp = file(pdfFile, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		for page in pdfminer.pdfpage.PDFPage.get_pages(fp, pagenos,  caching= True, check_extractable=True):
			interpreter.process_page(page)
		fp.close()
		device.close()
		outfp.close()
