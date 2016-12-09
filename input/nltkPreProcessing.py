import json
import re
import htmlentitydefs
import csv
from nltk.tokenize.casual import TweetTokenizer


def main():
    outputFile = open('/Users/anoukh/FYP/tokenizedloveyouzindaginew.csv', "wb")
    writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',')
    count = 0
    outputTwitterArray = []
    # Append Headings
    outputTwitterArray.append("date")
    outputTwitterArray.append("text")
    outputTwitterArray.append("lat")
    outputTwitterArray.append("long")
    # End Append Headings
    writer.writerow(outputTwitterArray)
    for line in open('/Users/anoukh/FYP/loveyouzindaginew.json', 'r'):
        outputTwitterArray = []
        lineObject = json.loads(line)
        tweetText = lineObject["text"]
        # if(lineObject["coordinates"] != None): Only process tweets with coordinates
        #     count = count + 1
        try:
            tweetText = unicode(tweetText)
        except UnicodeDecodeError:
            tweetText = str(tweetText).encode('string_escape')
            tweetText = unicode(tweetText)
        tokenizedTweets = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(tweetText)
        outputTwitterArray.append(lineObject["created_at"])
        coordinatesObject = lineObject['coordinates']

        outputTwitterArray.append(replaceUnneccassaryTokens(tokenizedTweets))
        try:
            outputTwitterArray.append(coordinatesObject['coordinates'][0])
            outputTwitterArray.append(coordinatesObject['coordinates'][1])
        except TypeError:
            outputTwitterArray.append(0.0)
            outputTwitterArray.append(0.0)
        # writer.writerow(outputTwitterArray)
        print tokenizedTweets
        count += 1
        if (count == 1):
            break
    print count


def replaceUnneccassaryTokens(tokens):
    i = 0
    for word in tokens:
        if word == '&amp;':
            word = 'and'
            tokens[i] = word
        if word == '@':
            word = 'at'
            tokens[i] = word
        if word[:1] == '#':
            word = word[1:]
            newString = ''.join(map(lambda x: x if x.islower() else " " + x, word))
            newToken = TweetTokenizer().tokenize(newString)
            # tokens[i:i] = newToken
            print tokens
            print newToken
            # TODO: Complete
        i += 1
    return tokens


if __name__ == '__main__':
    main()