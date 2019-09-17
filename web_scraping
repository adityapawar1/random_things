#!/usr/bin/env python
import urllib.request

base1 = "https://www.dictionary.com/browse/{}"
base2 = "https://www.macmillandictionary.com/us/dictionary/american/{}"
base3 = "https://www.merriam-webster.com/dictionary/{}"

words = []
text = ""

while True:
    word = input("Enter the word you want the definition for. Enter done if done entering words: ")
    try:
        if word == "done":
            break
        else:
            word1 = word.split(" ")
            if len(word1) > 1:
                word = ""
                for c, w in enumerate(word1):
                    if c == 0:
                        word += w
                    else:
                        word += "+" + w
            u = urllib.request.urlopen(base3.format(word))  # The url you want to open
            words.append(word)

    except:
        print("Error: That is not a word, please enter a valid word. If you think the entered word is a word, check you internet.")

for word in words:
    try:
        u = urllib.request.urlopen(base3.format(word))  # The url you want to open
        data = u.read().decode("utf-8")
        # print(base3.format(word))
    except:
        print("Error on word: {} while looking for the link".format(word))
        print(base3.format(word))
    try:
        parsedtext = data.split('<meta name="description" content="'.format(word.title()))
        parsedtext = parsedtext[1].split("definition is -")
        definition = parsedtext[1].split('. How to use')[0]
        definition = definition.split('.">')[0]
        print(word + " -" + definition)
        text += word + " -" + definition + "\n"
    except:
        print("Error on word: '{}' while looking for the definition".format(word))
        print(data)

file = open("definitions.txt", "w+")
file.write(text)
file.close()



