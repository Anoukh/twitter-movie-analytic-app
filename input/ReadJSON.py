import json
import re
import htmlentitydefs
import csv

def main():
    outputFile = open('/Users/anoukh/FYP/tokenizedloveyouzindaginew.csv', "wb")
    writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',')
    count = 0
    outputTwitterArray = []
    outputTwitterArray.append("date")
    outputTwitterArray.append("text")
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
        outputTwitterArray.append(lineObject["created_at"])
        outputTwitterArray.append(tokenizeTweets(tweetText))
        tokenizeTweets(tweetText)
        writer.writerow(outputTwitterArray)
        count += 1
        if (count == 6):
            break
    print count


def tokenizeTweets(tweetText): # TODO remove unnecessary tokens and combine together
    # Emoticons:
    emoticon_string = r"""
        (?:
          [<>]?
          [:;=8]                     # eyes
          [\-o\*\']?                 # optional nose
          [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
          |
          [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
          [\-o\*\']?                 # optional nose
          [:;=8]                     # eyes
          [<>]?
        )"""

    regex_strings = (

        # URLs
        r"""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""
        ,
        # Phone numbers:
        r"""
        (?:
          (?:            # (international)
            \+?[01]
            [\-\s.]*
          )?
          (?:            # (area code)
            [\(]?
            \d{3}
            [\-\s.\)]*
          )?
          \d{3}          # exchange
          [\-\s.]*
          \d{4}          # base
        )"""
        ,
        # Emoticons:
        emoticon_string
        ,
        # HTML tags:
        r"""<[^>]+>"""
        ,
        # Twitter username:
        r"""(?:@[\w_]+)"""
        ,
        # Twitter hashtags:
        r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
        ,
        # Remaining word types:
        r"""
        (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
        |
        (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
        |
        (?:[\w_]+)                     # Words without apostrophes or dashes.
        |
        (?:\.(?:\s*\.){1,})            # Ellipsis dots.
        |
        (?:\S)                         # Everything else that isn't whitespace.
        """
    )

    tokens_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
    emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)

    html_entity_digit_re = re.compile(r"&#\d+;")
    html_entity_alpha_re = re.compile(r"&\w+;")
    amp = "&amp;"
    # TODO: Convert this symbol to 'and'

    def tokenize(s):
        return tokens_re.findall(s)

    def preprocess(s, lowercase=False):
        s = __html2unicode(s)
        tokens = tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def __html2unicode(s):
        """
        Internal method that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
        ents = set(html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, unichr(entnum))
                except:
                    pass
        # Now the alpha versions:
        ents = set(html_entity_alpha_re.findall(s))
        ents = filter((lambda x: x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass
            s = s.replace(amp, " and ")
        return s

    # print(preprocess(tweetText))
    return preprocess(tweetText)

if __name__ == '__main__':
    main()
