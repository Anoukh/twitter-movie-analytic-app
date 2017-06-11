import unicodecsv as csv

actor = ['hugh', 'jackman', 'patrick', 'stewart', 'wolverine', 'dafne', 'keen']
director = ['james', 'mangold']


def main():
    count = 0
    output_file = open('/Users/anoukh/FYP/Datasets/Yashoda/LoganWithEntity.csv', "wb")
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar=',',
                        encoding="utf-8")

    with open('/Users/anoukh/FYP/Datasets/Yashoda/LoganPreProcessed.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            count += 1
            output_array = [row[0], row[1], find_entity(text=row[1])]
            writer.writerow(output_array)


def find_entity(text):
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
