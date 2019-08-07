from pymongo import MongoClient

client = MongoClient()

db = client.sefaria.texts

# TeshuvotMaharshal = db.find_one({"versionTitle": "Teshuvot Maharshal, Lublin, 1574"})
# test = TeshuvotMaharshal["chapter"][26]
#
# file = open("testResponsaShabbos2.txt", "w", encoding='utf-16')
# for line in test:
#     file.write(line + "\n")
# file.close()

NBY = db.find_one({"title": "Noda BiYhudah I"})
test = NBY["chapter"]["Orach Chaim"][2]

file = open("NBYprayer.txt", "w", encoding='utf-8')
for line in test:
    file.write(line + "\n")
file.close()