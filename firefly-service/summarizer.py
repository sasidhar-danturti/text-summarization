import os
import vocab

def summarize(input):
    # create the vocabulary file first and then  submit the job
    v = vocab.Vocab("gs://sasidhar-project1-mlengine","data/vocab")
    v.create_vocab_file()
    os.system("sudo sh train_textsum_dist.sh " + input)
    return "done"

