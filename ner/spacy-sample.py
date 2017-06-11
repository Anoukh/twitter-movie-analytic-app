import spacy
from spacy.gold import GoldParse
import unicodecsv as csv
import en_core_web_md
from nltk.tag.stanford import StanfordNERTagger

# str = StanfordNERTagger("/Users/anoukh/FYP/Stanford/ner-model.ser.gz", '/Users/anoukh/FYP/Stanford/stanford-ner.jar', encoding='utf-8')
str = StanfordNERTagger("/Users/anoukh/FYP/Stanford/english.all.3class.distsim.crf.ser.gz", '/Users/anoukh/FYP/Stanford/stanford-ner.jar', encoding='utf-8')
print str.tag("Anoukh is from an island called Sri Lanka located in the Indian Ocean Alia bhatt was awesome but the song of sharukh was horrible".split())

nlp = en_core_web_md.load()
# nlp = spacy.load('en_default')

text = []
entity = []
# nlp.entity.model.learn_rate = 0.001
nlp.entity.add_label('ACTOR')
nlp.entity.add_label('DIR')
nlp.entity.add_label('SONG')

with open('/Users/anoukh/FYP/Stanford/movie_ner_train_set_ner.tsv', 'r') as tsv:
    reader = csv.reader(tsv, dialect="excel-tab")
    for t, e in reader:
        text.append(t)
        entity.append(str(e))

doc = nlp.make_doc(unicode(" ".join(map(str, text)), encoding="utf-8"))

gold = GoldParse(doc, entities=entity)

nlp.entity.update(doc, gold)

doc2 = nlp(u'Desmond Miles 4 years today')

print(doc2[0].text, doc2[0].ent_iob, doc2[0].ent_type_)


# with open('/Users/anoukh/FYP/Datasets/Logan/logan.csv', 'rb') as csvfile:
#     tweet_text = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for row in tweet_text:
#         doc = nlp.make_doc(row)
#         gold = GoldParse(doc, entities=[])
#         nlp.entity.update(doc, gold)


# doc = nlp(u'London is a big city in the United Kingdom.')
# print(doc[0].text, doc[0].ent_iob, doc[0].ent_type_)
# # print(doc[1].ent_type)
# entity = []
# for temp in doc:
#     if temp.ent_type_ != "":
#         entity.append(temp.ent_type_)
#
# for temp in entity:
#     print temp
#
# nlp.save_to_directory('/Users/anoukh/FYP/en_entity_model_logan')
