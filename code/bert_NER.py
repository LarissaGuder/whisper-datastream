# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline

# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")

# nlp = pipeline("ner", model=model, tokenizer=tokenizer)
# text = "I DOUBT OUR BEING ABLE TO DO SO MUCH SAID MORLAND YOU CROAKING FELLOW CRIED THORPE WE SHALL BE ABLE TO DO TEN TIMES MORE KINGSWESTON AYE AND BLAIZE CASTLE TOO AND ANYTHING ELSE WE CAN HEAR OF"
# def NER(text):
#     ner_results = nlp(text)
#     return ner_results
# print(NER(text))

import spacy
nlp = spacy.load("en_core_web_sm")
def NER(text):
    doc = nlp(text)
    # print(doc.text)
    return doc
    # for token in doc:
    #     return token.text, token.pos_,
    #     print(token.text, token.pos_, token.dep_)

# @article{DBLP:journals/corr/abs-1810-04805,
#   author    = {Jacob Devlin and
#                Ming{-}Wei Chang and
#                Kenton Lee and
#                Kristina Toutanova},
#   title     = {{BERT:} Pre-training of Deep Bidirectional Transformers for Language
#                Understanding},
#   journal   = {CoRR},
#   volume    = {abs/1810.04805},
#   year      = {2018},
#   url       = {http://arxiv.org/abs/1810.04805},
#   archivePrefix = {arXiv},
#   eprint    = {1810.04805},
#   timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},
#   biburl    = {https://dblp.org/rec/journals/corr/abs-1810-04805.bib},
#   bibsource = {dblp computer science bibliography, https://dblp.org}
# }