import json
# import csv
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import unicodecsv as csv
import emojiDictionary
import emoticonDictionary
import re
import string

trackedHashTag = "dearzindagi"

def main():
    output_file = open('/Users/anoukh/FYP/tokenizeddearzindagifinal.csv', "wb")
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
    # End Append Headings
    writer.writerow(output_twitter_array)

    '''
    twitter_array = []
    counter = 0
    for line in open('/Users/anoukh/FYP/Datasets/DearZindagi/dearzindagifinal.json', 'r'):
        line = json.loads(line)
        twitter_array.append([line["text"], line["created_at"], line["coordinates"]])
        counter += 1
        print counter

    print len(twitter_array)
    L_dict = dict((x[0], x[1:]) for x in twitter_array)
    print len(L_dict)

    '''
    for line in open('/Users/anoukh/FYP/Datasets/DearZindagi/dearzindagifinal.json', 'r'):
        output_twitter_array = []
        line_object = json.loads(line)
        tweet_text = line_object["text"]
        # if(line_object["coordinates"] != None): Only process tweets with coordinates
        #     count = count + 1
        tokenized_tweets = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(tweet_text)
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
        new_tokenized_tweets = [word for word in tokenized_tweets if word.lower() not in stopwords_punctuations]
        output_twitter_array.append(line_object["created_at"])
        coordinates_object = line_object['coordinates']
        # output_twitter_array.append(replace_unnecessary_tokens(new_tokenized_tweets))

        output_twitter_array.append(" ".join(map(str, replace_unnecessary_tokens(new_tokenized_tweets))))

        try:
            output_twitter_array.append(coordinates_object['coordinates'][0])
            output_twitter_array.append(coordinates_object['coordinates'][1])
        except TypeError:
            output_twitter_array.append(0.0)
            output_twitter_array.append(0.0)

        writer.writerow(output_twitter_array)
        # print output_twitter_array

        # Break the loop at 10 for testing
        count += 1
        print count
        # if (count == 10):
        #     break
    print count


# TODO: Remove RT that have no location
# TODO: Detect Outliers
def replace_unnecessary_tokens(tokens):
    i = 0
    newTokens = []
    flag = 'false'
    hyphen_pattern = re.compile(r'\w+(?:-\w+)+')
    url_pattern = rtext = re.compile(r'^https?:\/\/.*[\r\n]*')
    for index in range(len(tokens)):
        if flag == 'false':
            try:
                if tokens[index] == u'\u2026':
                    continue
                elif tokens[index] == u'\u2764':
                    newTokens.append("love")
                    flag = 'true'
                elif tokens[index] == u'\ud83d':
                    emojiWord = emojiDictionary.select_emoji(tokens[index+1])
                    if emojiWord != 'unknown':
                        newTokens.append(emojiWord)
                    flag = 'true'
                # Remove Hashtags and Mentions
                elif tokens[index][:1] == '#' or tokens[index][:1] == '@':
                    continue
                # Break Hyphenated Words
                elif hyphen_pattern.match(tokens[index]):
                    word = tokens[index].split('-')
                    for w in word:
                        newTokens.append(w)
                # URL removal
                elif url_pattern.match(tokens[index]):
                    continue
                # # Emoticon
                # elif tokens[index] == ':)' or tokens[index] == ':-)':
                #     newTokens.append('happy')
                # elif tokens[index] == ':(' or tokens[index] == ':-(':
                #     newTokens.append('sad')
                elif tokens[index]:
                    try:
                        str(tokens[index])
                        newTokens.append(emoticonDictionary.select_emoticon(tokens[index]))
                    except Exception:
                        print "error"
                        continue
                else:
                    newTokens.append(emoticonDictionary.select_emoticon(tokens[index]))
                i += 1
            except IndexError:
                print "Error"
        else:
            flag = 'false'
            continue
    return newTokens


if __name__ == '__main__':
    main()
