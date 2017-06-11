import json
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import unicodecsv as csv
import emojiDictionary
import emoticonDictionary
import re
import string
import en_core_web_md

actor = ['hugh', 'jackman', 'patrick', 'stewart', 'wolverine', 'dafne', 'keen']
director = ['james', 'mangold']


def main():
    # Load Scipy Model for Entity Recognition
    # nlp = en_core_web_md.load()

    # Output file
    output_file = open('/Users/anoukh/FYP/Datasets/Yashoda/LoganPreProcessed.csv', "wb")
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',',
                        encoding="utf-8")
    lemmatizer = WordNetLemmatizer()
    count = 0
    output_twitter_array = []

    # Append Headings
    output_twitter_array.append("date")
    output_twitter_array.append("text")
    output_twitter_array.append("lat")
    output_twitter_array.append("long")
    output_twitter_array.append("ner")
    output_twitter_array.append("total")
    writer.writerow(output_twitter_array)
    # End Append Headings

    twitter_array = []
    counter = 0

    # Load JSON Object to Python Array
    for line in open('/Users/anoukh/FYP/Datasets/Logan/logan.json', 'r'):
        line = json.loads(line)
        twitter_array.append([line["text"], line["created_at"], line["coordinates"], line['favorite_count',
                                                                                          line['retweet_count']]])
    print len(twitter_array)

    # Remove duplicate tweets
    unique_tweet_set = dict((x[0], x[1:]) for x in twitter_array)
    print len(unique_tweet_set)
    count1 = 0
    for key in unique_tweet_set:
        output_twitter_array = []
        date_coordinate_object = unique_tweet_set[key]

        # Only process tweets with coordinates
        if date_coordinate_object[1] != None:
            print "Cordinates"
            count1 += 1
            print count1

            # Tokenize
            tokenized_tweets = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(key)

            # Part of Speech Tagging
            pos_tagged = pos_tag(tokenized_tweets)

            # Lemmatization
            lemmatized_sentence = []
            for tag in pos_tagged:
                if tag[1].startswith('J'):
                    lemmatized_sentence.append(lemmatizer.lemmatize(tag[0], pos='a'))
                elif tag[1].startswith('V'):
                    lemmatized_sentence.append(lemmatizer.lemmatize(tag[0], pos='v'))
                elif tag[1].startswith('N'):
                    lemmatized_sentence.append(lemmatizer.lemmatize(tag[0], pos='n'))
                elif tag[1].startswith('R'):
                    lemmatized_sentence.append(lemmatizer.lemmatize(tag[0], pos='r'))
                else:
                    lemmatized_sentence.append(tag[0])

            # Remove Stop Words and Punctuations
            stopwords_punctuations = stopwords.words('english') + list(string.punctuation)
            new_tokenized_tweets = [word for word in lemmatized_sentence if word.lower() not in stopwords_punctuations]

            # Print Date, Retweet Count, Favorite Count
            output_twitter_array.append(date_coordinate_object[0])
            output_twitter_array.append(date_coordinate_object[2])
            output_twitter_array.append(date_coordinate_object[3])
            try:
                find_entity = " ".join(map(str, replace_unnecessary_tokens(new_tokenized_tweets)))
                output_twitter_array.append(find_entity)
            except UnicodeEncodeError:
                continue

            try:
                output_twitter_array.append(date_coordinate_object[1]['coordinates'][0])
                output_twitter_array.append(date_coordinate_object[1]['coordinates'][1])
            except TypeError:
                output_twitter_array.append(0.0)
                output_twitter_array.append(0.0)
            except KeyError:
                output_twitter_array.append(0.0)
                output_twitter_array.append(0.0)

            # Finding Entities

            # entity = []
            # doc = nlp(unicode(find_entity))
            # for temp in doc:
            #     if temp.ent_type_ != "":
            #         entity.append(temp.ent_type_)

            entity = get_entity(find_entity)
            output_twitter_array.append(entity)
            output_twitter_array.append(key)
            writer.writerow(output_twitter_array)
            # print output_twitter_array

            # Break the loop at 10 for testing
            count += 1
            # print count
            # if (count == 10):
            #     break
    print count


# TODO: Remove RT that have no location
# TODO: Detect Outliers
def replace_unnecessary_tokens(tokens):
    i = 0
    new_tokens = []
    flag = 'false'
    hyphen_pattern = re.compile(r'\w+(?:-\w+)+')
    url_pattern = rtext = re.compile(r'^https?:\/\/.*[\r\n]*')
    for index in range(len(tokens)):
        if flag == 'false':
            try:
                if tokens[index] == u'\u2026':
                    continue
                elif tokens[index] == u'\u2764':
                    new_tokens.append("love")
                    flag = 'true'
                elif tokens[index] == u'\ud83d':
                    emojiWord = emojiDictionary.select_emoji(tokens[index+1])
                    if emojiWord != 'unknown':
                        new_tokens.append(emojiWord)
                    flag = 'true'
                # Remove Hashtags and Mentions
                elif tokens[index][:1] == '#' or tokens[index][:1] == '@':
                    continue
                # Break Hyphenated Words
                elif hyphen_pattern.match(tokens[index]):
                    word = tokens[index].split('-')
                    for w in word:
                        new_tokens.append(w)
                # URL removal
                elif url_pattern.match(tokens[index]):
                    continue
                # # Emoticon
                # elif tokens[index] == ':)' or tokens[index] == ':-)':
                #     newTokens.append('happy')
                # elif tokens[index] == ':(' or tokens[index] == ':-(':
                #     newTokens.append('sad')
                elif tokens[index].lower().strip() == "rt":
                    continue
                # Replace Emoticons
                elif tokens[index] == "...":
                    continue
                elif tokens[index]:
                    try:
                        str(tokens[index])
                        new_tokens.append(emoticonDictionary.select_emoticon(tokens[index]))
                    except Exception:
                        continue
                else:
                    new_tokens.append(emoticonDictionary.select_emoticon(tokens[index]))
                i += 1
            except IndexError:
                print "Error"
        else:
            flag = 'false'
            continue
    return new_tokens


def get_entity(text):
    entity_list = []
    text = map(lambda x: x.lower(), text.split())
    if any(st.lower() in text for st in actor) or 'act' in text:
        entity_list.append('ACTOR')
    if any(st in text for st in director):
        entity_list.append('DIR')
    if 'song' in text or 'soundtrack' in text:
        entity_list.append('SONG')
    return entity_list


if __name__ == '__main__':
    main()
