from pymongo import MongoClient

client = MongoClient()

db = client.sefaria.texts

# get Beit Yosef Orach Chayim
BeitYosef = db.find_one({"versionTitle": "Tur Orach Chaim, Vilna, 1923", 'title': 'Beit Yosef'})
OrachChaim = BeitYosef["chapter"]["OrachChaim"]

simanNum = 1
for siman in range(0, len(OrachChaim)):
   file = open("by" + str(simanNum) + ".txt", "w", encoding='utf-16')
   for seif in OrachChaim[siman]:
       for line in seif:
           if line != []:
               file.write(line + "\n")
   file.close()
   simanNum+=1

#
# # get Shulchan Aruch Orach Chayim
# OrachChayim = db.find_one({"title": "Shulchan Arukh, Orach Chayim"})
#
# simanNum = 1
# for siman in range(0, len(OrachChayim["chapter"])):
#    file = open(str(simanNum) + ".txt", "w")
#    for seif in OrachChayim["chapter"][siman]:
#        file.write(seif)
#    simanNum+=1

# get a responsa