from torchtext import datasets
from torchtext import data
from torchtext.vocab import GloVe, CharNGram
import subprocess

GIGAWORD_PATHS = ["https://s3.amazonaws.com/gigaword/gigaword_{}.txt".format(path) for path in ['train', 'val', 'test']]
GIGAWORDSMALL_PATHS = ["https://s3.amazonaws.com/gigaword/gigaword_small_{}.txt".format(path) for path in ['train', 'val', 'test']]
DATA_DIR = "data/gigaword"

class Download:
    def __init__(self,
                glove = True,
                googlenews = False,
                charngram = False,
                wiki = False,
                gigaword = False,
                gigawordsmall = False,
                imdb = False,
                mpqa_subj = False
            ):
        self.glove = glove
        self.googlenews = googlenews
        self.charngram = charngram
        self.imdb = imdb
        self.mpqa_subj = mpqa_subj
        self.wiki = wiki
        self.gigaword = gigaword
        self.gigawordsmall = gigawordsmall


        self.get_unsupervised_data()
        self.get_vectors()
        self.get_supervised_data()





    def get_vectors(self):
        if self.glove:
            print('Downloading GloVe Vectors...')
            glove = GloVe(name = '6B', cache = 'vectors')
            print('Done.')

        if self.charngram:
            print('Downloading CharNGram Vectors...')
            charVec = CharNGram(cache = 'vectors')
            print('Done.')


    def get_unsupervised_data(self):

        sentence_field = data.Field(
                            sequential = True,
                            use_vocab = True,
                            init_token = '<BOS>',
                            eos_token = '<EOS>',
                            lower = True,
                            tokenize = 'spacy',
                        )

        if self.wiki:


            print("Downloading wikitext data...")
            train_sentences, valid_sentences, test_sentences = datasets.WikiText2.splits(
                                                                            sentence_field,
                                                                            root = 'data',
                                                                            train = 'wiki.train.tokens',
                                                                            validation = 'wiki.valid.tokens',
                                                                            test = 'wiki.test.tokens'
                                                                        )
            print("Done.")

        if self.gigaword:

            for path in GIGAWORD_PATHS:
                print("Downloading Gigaword Data")
                bashCommand = "wget " + path + " -P " + DATA_DIR
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
        elif self.gigawordsmall:
            for path in GIGAWORDSMALL_PATHS:
                print("Downloading Gigaword Data")
                bashCommand = "wget " + path + " -P " + DATA_DIR
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()


    def get_supervised_data(self):
        sentence_field = data.Field(
                            sequential = True,
                            use_vocab = True,
                            init_token = '<BOS>',
                            eos_token = '<EOS>',
                            lower = True,
                            tokenize = 'spacy',
                        )
        target_field = data.Field(sequential = False, batch_first = True)

        if self.imdb:
            print('Downloading IMDB data...')
            train_data, test_data = datasets.IMDB.splits(
                                            text_field = sentence_field,
                                            label_field = target_field,
                                            root = 'data'
                                        )
            print("Done.")
        if self.mpqa_subj:
            pass



class Clean:

    def __init__(self,
                unsupervised_sizelimit = None,
                supervised_sizelimit = None,
                clf_numsplits = 2,
                lm_numsplits = 2,
                clf_trainsize = 0.9,
                lm_trainsize = 0.95
                ):

        print('INITING CLEANER')


if __name__ == '__main__':
    Downloader = Download()
    Cleaner = Clean()
