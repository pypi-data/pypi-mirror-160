import spacy
from spacy.tokens import Doc
import spacy.attrs as ORTH
from spacy.language import Language
import logging

nlp = spacy.load('en_core_web_sm', exclude=['tagger', 'parser', 'attribute_ruler', 'lemmatizer', 'ner',])

# TODO: Fix the add_special_case, current method doesn't work
nlp.tokenizer.from_disk('src/carsomenlp/artefacts/tokenizer')

# To uncomment if need more deeper NLP use case
# @Language.component("custom_parser")
# def clean_token(doc):
#     excluded_tags = {'ADV', 'ADP', 'AUX', 'VERB', 'PUNCT'}
#     logging.info(f"Before parse -  {len(doc)} tokens.")
#     # Only get necessary token
#     # doc = [ token for token in doc if token.pos_ not in excluded_tags]
#     indexes = []
#     for index, token in enumerate(doc):
#         if (token.pos_ not in excluded_tags):
#             indexes.append(index)
#         else:
#             print(f"removing {token}")
#     mod_doc = Doc(doc.vocab, words=[
#                   t.text for i, t in enumerate(doc) if i in indexes])
#     logging.info(f"After parse -  {len(mod_doc)} tokens.")
#     return mod_doc


# nlp.add_pipe("custom_parser", name="custom_parser", last=True)
# print(nlp.pipe_names)


def tokenize(text):
    tokens = nlp(text)
    return tokens
