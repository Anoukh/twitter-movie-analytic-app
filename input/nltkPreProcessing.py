import json
# import csv
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import stopwords
import unicodecsv as csv
import emojiDictionary
import re

trackedHashTag = "dearzindagi"

def main():
    outputFile = open('/Users/anoukh/FYP/tokenizedemoji.csv', "wb")
    writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',',
                        encoding="utf-8")
    count = 0
    outputTwitterArray = []
    # Append Headings
    outputTwitterArray.append("date")
    outputTwitterArray.append("text")
    outputTwitterArray.append("lat")
    outputTwitterArray.append("long")
    # End Append Headings
    writer.writerow(outputTwitterArray)
    for line in open('/Users/anoukh/FYP/Datasets/DearZindagi/emoji.json', 'r'):
        outputTwitterArray = []
        lineObject = json.loads(line)
        tweetText = lineObject["text"]
        # if(lineObject["coordinates"] != None): Only process tweets with coordinates
        #     count = count + 1
        # try:
        #     tweetText = unicode(tweetText)
        # except UnicodeDecodeError:
        #     tweetText = str(tweetText).encode('string_escape')
        #     tweetText = unicode(tweetText)
        tokenizedTweets = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(tweetText)
        # Remove Stop Words
        newTokenizedTweets = [w for w in tokenizedTweets if w.lower() not in stopwords.words('english')]
        outputTwitterArray.append(lineObject["created_at"])
        coordinatesObject = lineObject['coordinates']

        # preProcessedTextUnicode = replaceUnneccassaryTokens(newTokenizedTweets)
        # my_list = [str(my_list[x]) for x in range(len(preProcessedTextUnicode))]
        # print my_list
        outputTwitterArray.append(replaceUnneccassaryTokens(newTokenizedTweets))

        try:
            outputTwitterArray.append(coordinatesObject['coordinates'][0])
            outputTwitterArray.append(coordinatesObject['coordinates'][1])
        except TypeError:
            outputTwitterArray.append(0.0)
            outputTwitterArray.append(0.0)

        writer.writerow(outputTwitterArray)
        # print outputTwitterArray

        # Break the loop at 10 for testing
        count += 1
        # if (count == 10):
        #     break
    print count


# TODO: Remove RT that have no location
# TODO: Detect Outliers
def replaceUnneccassaryTokens(tokens):
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
