from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def NER(text):
    ner_results = nlp(text)
    return ner_results


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