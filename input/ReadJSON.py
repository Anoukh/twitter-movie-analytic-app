import json
from pprint import pprint
def main():
    tweets = []
    count = 0
    for line in open('/Users/anoukh/FYP/loveyouzindaginew.json', 'r'):
        lineObject = json.loads(line)
        tweetText = lineObject["text"]
        count = count + 1
    print count

if __name__ == '__main__':
    main()
