words = []
with open("wordlist.txt", encoding="latin-1") as FileObj:
    for lines in FileObj:
        words.append(lines.strip())

# words = ["bat", "rats", "god", "dog", "cat", "arts", "star"]
sort_words = {}
for word in words:
    sort_words[word] = "".join(sorted(word))

anagrams = []
for i in range(len(words)):
    ana = [words[i]]
    for j in range(i + 1, len(words)):
        if sort_words[words[i]] == sort_words[words[j]]:
            ana.append(words[j])
    if len(ana) != 1:
        anagrams.append(ana)

with open("anagrams.txt", "w") as f:
    for items in anagrams:
        f.write("%s\n" % " ".join(i for i in items))
