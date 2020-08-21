def letters(word):
    i = 0
    while i < len(word):
        yield word[i]
        i += 1
