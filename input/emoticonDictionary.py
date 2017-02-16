def select_emoticon(x):
    return {
        ":)": 'happy',
        ":(": 'sad',
        ":o": 'surprised'

    }.get(x, x)
