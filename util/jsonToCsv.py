import unicodecsv as csv
import json


def main():
    output_file = open('/Users/anoukh/FYP/Datasets/Logan/logan.csv', "wb")
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',',
                        encoding="utf-8")

    output_twitter_array = ["total"]
    writer.writerow(output_twitter_array)

    twitter_array = []

    for line in open('/Users/anoukh/FYP/Datasets/Logan/logan.json', 'r'):
        line = json.loads(line)
        twitter_array.append([line["text"], line["created_at"], line["coordinates"], line['favorite_count',
                                                                                          line['retweet_count']]])
    print len(twitter_array)
    unique_tweet_set = dict((x[0], x[1:]) for x in twitter_array)
    print len(unique_tweet_set)
    for key in unique_tweet_set:
        output_twitter_array = [key]
        writer.writerow(output_twitter_array)


if __name__ == '__main__':
    main()
