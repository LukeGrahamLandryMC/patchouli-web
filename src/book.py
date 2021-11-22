import json, os

class Book:
    def __init__(self, namespace, bookname):
        self.resource_path = resource_path
        self.namespace = namespace
        self.bookname = bookname
        self.lang = {}
        self.required_resources = []


    def readLang(self, language):
        with open(self.resource_path + "/assets/" + self.namespace + "/lang/" + language + ".json", "r") as f:
            self.lang[language] = json.loads("\n".join(f.readlines()))


    def getBookData(self):
        with open(self.resource_path + "/data/" + self.namespace + "/patchouli_books/" + self.bookname + "/book.json", "r") as f:
            book_info = json.loads("\n".join(f.readlines()))
            self.display_name = book_info["name"]
            self.landing_text = book_info["landing_text"]
            self.background_image_rl = book_info["background_image"]
    
    def findResource(self, rl):
        modid = rl.split(":")[0]
        path = ":".join(rl.split(":")[1:])


    
    def generateHTML(self):
        self.getBookData()
        return ""


    


if __name__ == "__main__":
    # book = Book("resources/Botania-master/src/main/resources", "botania")
    print(findBooks())

