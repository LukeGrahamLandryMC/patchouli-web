import json, os

class ResourceManager:
    lang = []

    def init():
        ResourceManager.readLang()

    def readLang():
        for namespace in os.listdir("../resources/assets"):
            for language in os.listdir("../resources/assets/{}/lang".format(namespace)):
                language = language.split(".")[0]
                with open("../resources/assets/{}/lang/{}.json".format(namespace, language), "r") as f:
                    if language not in ResourceManager.lang:
                        ResourceManager.lang[language] = {}

                    info = json.loads("\n".join(f.readlines()))

                    for key, value in info.items():
                        ResourceManager.lang[language][key] = value
    
    def translate(key, language="en_us"):
        if key in ResourceManager.lang[language]:
            return ResourceManager.lang[language][key]
        elif key in ResourceManager.lang["en_us"]:
            return ResourceManager.lang["en_us"][key]
        else:
            return key

    def findResource(rl):
        modid = rl.split(":")[0]
        path = ":".join(rl.split(":")[1:])

def readJsonFile(path):
    with open(path, "r") as f:
        return json.loads("\n".join(f.readlines()))

def loadTemplate(source, target, action):
    with open(source, "r") as f:
        template_html = "\n".join(f.readlines())

    with open(target, "r") as f:
        f.write(action(template_html))

class Book:
    def __init__(self, namespace, bookname):
        self.namespace = namespace
        self.bookname = bookname
        self.lang = {}
        self.required_resources = []
        self.base_path = "../resources/assets/data" + self.namespace + "/patchouli_books/" + self.bookname
        self.target_path = "../{}/{}".format(self.namespace, self.bookname)


    # loads book.json
    # walks categories and entries
    def getBookData(self):
        book_info = readJsonFile(self.base_path + "/book.json")
        self.display_name = book_info["name"]
        self.landing_text = book_info["landing_text"]
        self.background_image_rl = book_info["background_image"]

        self.categories = []
        self.entries = {}
        for category in os.listdir(self.base_path + "/categories"):
            self.categories.append(category.split(".")[0])
            self.entries[category] = []
            for entry in os.listdir(self.base_path + "/entries/" + category):
                self.entries[category].append(entry.split(".")[0])


    # uses templates/category.html
    def createCategory(self, category):
        category_data = readJsonFile(self.base_path + "/categories/" + category + ".json")

        out_html = ""

        for entry in self.entries[category]:
            self.createEntry(entry)

            # add link to <page_html>

    # uses templates/entry.html   
    def createEntry(self, category, entry):
        entry_data = readJsonFile("{}/entries/{}/{}.json".format(self.base_path, category, entry))

        entry_html = ""

        for page in entry_data["pages"]:
            entry_html += self.createPage(page)
        
        loadTemplate("templates/entry.html", "{}/{}/{}.html".format(self.target_path, category, entry), lambda template : template.replace("$ENTRY", entry_html))


    def createPage(self, data):
        out_html = ""

        if data["type"] == "text":
            pass

        elif data["type"] == "botania:lore":
            pass
            
        else:
            out_html = "<b> createPage Error: missing page type: {} </b>".format(data["type"])
            print(out_html) 

        return out_html

    # uses templates/book_home.html
    def createMain(self):
        pass

    # uses templates/entry_list.html
    def createEntryList(self):
        pass
       
    
    def generateHTML(self):
        self.getBookData()
        self.createMain()
        self.createEntryList()

        for category in self.categories:
            self.createCategory(category)
        
