import pickle

with open('./dict_idf.pickle', 'rb') as file:
    dict_idf = pickle.load(file)

dict_embedding = {}
file = open("./sgns.weibo.bigram-char")
information = file.readline()
print(information)
count_words = information.split(' ')[0]
print(int(count_words))

for _ in range(int(count_words)):
    line = file.readline()
    line = line.split(' ')
    word = line[0]
    vector = []
    if word in dict_idf:
        for i in range(300):
            vector.append(float(line[i + 1]))
        dict_embedding[word] = vector
        print(word, vector)

file = open('embedding.pickle', 'wb')
pickle.dump(dict_embedding, file)
file.close()
