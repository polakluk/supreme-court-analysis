# my tools
from tools.parsers import mpqa as mpqaParser


# class that prepares data for training and testing phase
class Preparation(object):

    # constructor
    def __init__(self):
        # constants for calculation of sentiment based on provided annotations
        self.sentimentConstants = {
            'intensity' : {
                            'low' : 0.2,
                            'medium' : 0.5,
                            'high' : 1,
                            'extreme' : 2
                        },
            'expression-intensity' : {
                            'neutral' : 1.01,
                            'low' : 1.25,
                            'medium' : 1.5,
                            'high' : 2,
                            'extreme' : 2.5
                        },
            'polarity' : {
                        'positive' : 1,
                        'negative' : 2,
                        'both' : 3,
                        'neutral' : 4,
                        'uncertain-positive' : 5,
                        'uncertain-negative' : 6,
                        'uncertain-both' : 7,
                        'uncertain-neutral' : 8,
                        'unknown' : 9
            },
            'attitude-type' : {
                            'other' : 0,
                            'other-attitude' : 1,
                            'arguing-neg' : 2,
                            'arguing-pos' : 2,
                            'sentiment-neg' : 3,
                            'sentiment-pos' : 3,
                            'agree-neg' : 5,
                            'agree-pos' : 6,
                            'intention-neg' : 5,
                            'intention-pos' : 6,
                            'specilation' : 7,
                            'speculation' : 8,
            }
            'attitude-uncertain' : {
                            'somewhat-uncertain' : 0.9,
                            'very-uncertain' : 0.5
            }
        }


    # assigns sentiment to each sentence from MPQA corpus based on provided annotations
    # the final sentiment is returned as pandas DataFrame
    def AssignSentimentSentences(self):
        # load up both MQPA corpus and MPQA annotations
        parser = mpqaParser.Mpqa()
        sentences = parser.readFileCsv(parser.defaultFileNameProcessed)
        annotations = parser.readFileCsv(parser.defaultFileNameProcessedAnnots)

        counter = 0
        for index, sentence in sentences.iterrows():
            currentAnnots = annotations[(annotations['docName'] == sentence['docName']) & (annotations['dirName'] == sentence['dirName']) & (annotations['startByte'] >= sentence['startByte'] ) & (annotations['endByte'] <= sentence['endByte']) ]
            if len(currentAnnots.index) > 0:
                print(sentence['text'])
                for idx, annot in currentAnnots.iterrows():
                    print(annot)
            else:
                continue
            print(len(currentAnnots.index))
            print("############################")
            if counter > 2:
                return
            else:
                counter += 1
        pass

    # calculates sentiment from provided annotations
    def _calculateSentimentSentenceAnnotations(self):
        pass
