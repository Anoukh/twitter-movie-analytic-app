import json
# import csv
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import stopwords
import unicodecsv as csv
import emojiDictionary
import re

trackedHashTag = "dearzindagi"

def main():
    output_file = open('/Users/anoukh/FYP/tokenizedemoji.csv', "wb")
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',',
                        encoding="utf-8")
    count = 0
    output_twitter_array = []
    # Append Headings
    output_twitter_array.append("date")
    output_twitter_array.append("text")
    output_twitter_array.append("lat")
    output_twitter_array.append("long")
    # End Append Headings
    writer.writerow(output_twitter_array)
    for line in open('/Users/anoukh/FYP/Datasets/DearZindagi/emoji.json', 'r'):
        output_twitter_array = []
        line_object = json.loads(line)
        tweet_text = line_object["text"]
        # if(line_object["coordinates"] != None): Only process tweets with coordinates
        #     count = count + 1
        # try:
        #     tweet_text = unicode(tweet_text)
        # except UnicodeDecodeError:
        #     tweet_text = str(tweet_text).encode('string_escape')
        #     tweet_text = unicode(tweet_text)
        tokenized_tweets = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(tweet_text)
        # Remove Stop Words
        new_tokenized_tweets = [w for w in tokenized_tweets if w.lower() not in stopwords.words('english')]
        output_twitter_array.append(line_object["created_at"])
        coordinates_object = line_object['coordinates']

        # preProcessedTextUnicode = replaceUnneccassaryTokens(newTokenizedTweets)
        # my_list = [str(my_list[x]) for x in range(len(preProcessedTextUnicode))]
        # print my_list
        output_twitter_array.append(replace_unnecessary_tokens(new_tokenized_tweets))

        try:
            output_twitter_array.append(coordinates_object['coordinates'][0])
            output_twitter_array.append(coordinates_object['coordinates'][1])
        except TypeError:
            output_twitter_array.append(0.0)
            output_twitter_array.append(0.0)

        writer.writerow(output_twitter_array)
        # print outputTwitterArray

        # Break the loop at 10 for testing
        count += 1
        # if (count == 10):
        #     break
    print count


# TODO: Remove RT that have no location
# TODO: Detect Outliers
def replace_unnecessary_tokens(tokens):
    i = 0
    newTokens = []
    flag = 'false'
    pattern = re.compile(r'\w+(?:-\w+)+')
    for index in range(len(tokens)):
        if flag == 'false':
            if tokens[index] == u'\u2764' and tokens[index+1] == u'\ufe0f':
                newTokens.append("love")
                flag = 'true'
            elif tokens[index] == u'\ud83d':
                emojiWord = emojiDictionary.select_emoji(tokens[index+1])
                if emojiWord != 'unknown':
                    newTokens.append(emojiWord)
                flag = 'true'
            # Replace Ampersand
            elif tokens[index] == '&amp;':
                newTokens.append('and')
            # Replace "at" symbol
            elif tokens[index] == '@':
                newTokens.append('at')
            # Break Hyphenated Words
            elif pattern.match(tokens[index]):
                word = tokens[index].split('-')
                for w in word:
                    newTokens.append(w)
            # Emoticon
            elif tokens[index] == ':)' or tokens[index] == ':-)':
                newTokens.append('happy')
            elif tokens[index] == ':(' or tokens[index] == ':-(':
                newTokens.append('sad')
            else:
                newTokens.append(tokens[index])
            i += 1
        else:
            flag = 'false'
            continue
    return newTokens


if __name__ == '__main__':
    main()
