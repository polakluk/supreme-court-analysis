from tools.parsers import basecorpus
import pandas as pd

#tools
from os import walk
import re

# this class reads MPQA corpus and turns it into a proper CSV file
class Mpqa(basecorpus.BaseCorpus):
    # constructor
    def __init__(self):
        basecorpus.BaseCorpus.__init__(self)
        self.defaultCorpusDir = '.'+self.sepDir+'corpora'+self.sepDir+'mpqa'+self.sepDir
        self.defaultFileNameProcessed = '.'+self.sepDir+'corpora'+self.sepDir+'mpqa'+self.sepDir+'mpqa.csv'
        self.defaultFileNameProcessedAnnots = '.'+self.sepDir+'corpora'+self.sepDir+'mpqa'+self.sepDir+'mpqa-annots.csv'
        self.columnsSent = ['docName', 'dirName', 'idx', 'startByte', 'endByte', 'sentLen', 'text']
        self.columnsAnnotations = ['docName', 'dirName', 'idx', 'type', 'startByte', 'endByte', 'wordLen', 'text', 'intensity', 'polarity', 'expression-intensity', 'attitude-type', 'attitude-uncertain']
        # annotations which we are interested in
        self.interestingAnnotations = ['GATE_expressive-subjectivity', 'GATE_direct-subjective', 'GATE_attitude']
        # markings for optional attributes
        self.optionalAttributes = ['intensity="', 'polarity="', 'expression-intensity="', 'attitude-type="', 'attitude-uncertain="']
        self.minLenAnnotation = 2


    # gets list of all documents in corpus
    def _getListDocumentsCorpus(self):
        searchDir = self.defaultCorpusDir+'docs'+self.sepDir
        documents = []
        docDirs = None
        for (dirpath, dirnames, filenames) in walk(searchDir):
            if dirpath == searchDir: # firstly, get only list of directories in corpus
                docDirs = dirnames
                continue

        # then, walk each directory separately and get all files in it
        for docDir in docDirs:
            searchDocDir = searchDir + docDir + self.sepDir
            for (dirpath, dirnames, filenames) in walk(searchDocDir):
                documents.extend([(docDir, fname) for fname in filenames])

        return documents


    # reads whole MPQA corpus and turns it into pandas dataframe with sentences
    def readAllFilesSentences(self):
        # first, get filenames of all documents in corpus
        documents = self._getListDocumentsCorpus()

        # now, process the documents one by one and generate sentences
        resDataFrame = pd.DataFrame([], columns = self.columnsSent)
        for doc in documents:
            processedData = self._readFileSentences(doc)
            resDataFrame = pd.concat([resDataFrame, processedData])
        return resDataFrame


    # reads the file and returns pandas DataFrame with annotated sentences
    def _readFileSentences(self, fTuple ):
        sents = []
        # format ./docs/{tuple[0]}/{tuple[1]}
        fNameDoc = self.defaultCorpusDir+'docs'+self.sepDir+fTuple[0]+self.sepDir+fTuple[1]
        # format ./man_anns/{tuple[0]}/{tuple[1]}/gatesentences.mpqa.2.0
        fNameSentencesFile = self.defaultCorpusDir+'man_anns'+self.sepDir+fTuple[0]+self.sepDir+fTuple[1]+self.sepDir+"gatesentences.mpqa.2.0"
        with open(fNameDoc, 'r') as docFile:
            with open(fNameSentencesFile, 'r') as sentFile:
                for line in sentFile: # go line by line
                    if line[0] == '#': # skip comments
                        continue
                    parts = line.split("\t")
                    if parts[3].strip() != 'GATE_sentence': # make sure, you read only sentences
                        continue

                    pos = parts[1].split(',')
                    docFile.seek(int(pos[0])) # skip to the beginning of sentence
                    sentLen = int(pos[1]) - int(pos[0]) # get length of the sentence
                    sent = docFile.read(sentLen).strip() # read the sentence
                    sentClean = re.sub('\s+', ' ', sent) # clean up multiple whitespaces in sentences
                    record = {
                                'docName' : fTuple[1], # name of document
                                'dirName' : fTuple[0], # source directory
                                'idx' : parts[0], # index of the sentece
                                'startByte' : pos[0], # start byte
                                'endByte' : pos[1], # end byte
                                'sentLen' : sentLen,
                                'text' : sentClean
                            }
                    sents.append(record)

                return pd.DataFrame(sents, columns = self.columnsSent) # return it as a DataFrame
        return None # just safety measurement


    # reads all annotations in MPQA corpus and
    def readAllFilesAnnotations(self):
        # first, get filenames of all documents in corpus
        documents = self._getListDocumentsCorpus()

        # now, process the documents one by one and generate sentences
        resDataFrame = pd.DataFrame([], columns = self.columnsAnnotations)
        for doc in documents:
            processedData = self._readFileAnnotations(doc)
            resDataFrame = pd.concat([resDataFrame, processedData])
        return resDataFrame


    # reads the file and returns pandas DataFrame with annotated sentences
    def _readFileAnnotations(self, fTuple ):
        annotations = []
        # format ./docs/{tuple[0]}/{tuple[1]}
        fNameDoc = self.defaultCorpusDir+'docs'+self.sepDir+fTuple[0]+self.sepDir+fTuple[1]
        # format ./man_anns/{tuple[0]}/{tuple[1]}/gateman.mpqa.lre.2.0
        fNameAnnotationsFile = self.defaultCorpusDir+'man_anns'+self.sepDir+fTuple[0]+self.sepDir+fTuple[1]+self.sepDir+"gateman.mpqa.lre.2.0"
        with open(fNameDoc, 'r') as docFile:
            with open(fNameAnnotationsFile, 'r') as annotsFile:
                for line in annotsFile: # go line by line
                    if line[0] == '#': # skip comments
                        continue
                    parts = line.split("\t")
                    if parts[3] in self.interestingAnnotations: # add only interesting annotations
                        pos = parts[1].split(',')
                        docFile.seek(int(pos[0])) # skip to the beginning of annotated word
                        wordLen = int(pos[1]) - int(pos[0]) # get length of the sentence
                        if wordLen < self.minLenAnnotation: # this annotation is too small
                            continue

                        word = docFile.read(wordLen).strip() # read the annotated word
                        wordClean = re.sub('\s+', ' ', word) # clean up multiple whitespaces in annotated word
                        # now, try to get out all optional attributes from part[4]
                        parts[4] = parts[4].strip()
                        parsed = {}
                        for pattern in self.optionalAttributes:
                            posPattern = parts[4].find(pattern)
                            if posPattern > -1 : #found this optional attribute there
                                endPattern = parts[4].find('"', posPattern + len(pattern)+ 1)
                                parsed[pattern[:-2]] = parts[4][posPattern + len(pattern):endPattern]


                        record = {
                                'docName' : fTuple[1], # name of document
                                'dirName' : fTuple[0], # source directory
                                'idx' : parts[0], # index of the sentece
                                'type' : parts[3], # type of annotation
                                'startByte' : pos[0], # start byte
                                'endByte' : pos[1], # end byte
                                'wordLen' : wordLen,
                                'text' : wordClean
                            }
                        # add parsed optional attributes to the record
                        for idx in parsed.keys():
                            record[idx] = parsed[idx]

                        annotations.append(record)

                return pd.DataFrame(annotations, columns = self.columnsAnnotations) # return it as a DataFrame
        return None # just safety measurement

    # saves the data with header to a file in CSV format
    def saveFileCsvAnnotations(self, data, fileName):
        if fileName == None:
            fileName = self.defaultFileNameProcessedAnnots
        with open(fileName, 'wb') as csvfile:
            data.to_csv(csvfile, index = False)
