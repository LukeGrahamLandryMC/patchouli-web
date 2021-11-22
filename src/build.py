from book import Book

import os, shutil, requests, zipfile, json

def mergeFolders(source, target):
    if not os.path.isdir(source):
        raise FileNotFoundError("Directory does not exist: " + source)
    if not os.path.isdir(target):
        raise FileNotFoundError("Directory does not exist: " + target)
    
    for root, dirs, files in os.walk(source, topdown=True):
        for dir in dirs:
            base = root.split(source)[1]
            if not os.path.isdir(target + base + "/" + dir):
                 os.mkdir(target + base + "/" + dir) 

        for file in files:
            base = root.split(source)[1]
            shutil.copy(root + "/" + file, target + base + "/" + file)

def gatherModResources():
    if not os.path.isdir("../mods"):
        print("no mods directory. skipping gatherModResources")
        return

    if not os.path.isdir("../resources/assets"):
        os.mkdir("../resources/assets")
    if not os.path.isdir("../resources/data"):
        os.mkdir("../resources/data")

    for root, dirs, files in os.walk("../mods", topdown=True):
        for folder in dirs:
            print("merging assets", folder)
            mergeFolders("../mods/" + folder + "/src/main/resources/assets", "../resources/assets")
            print("merging data", folder)
            mergeFolders("../mods/" + folder + "/src/main/resources/data", "../resources/data")
            print("clearing mods/", folder)
            shutil.rmtree("../mods/" + folder)
        break

def getFromGithub(username, repository, branch):
    url = "https://github.com/{}/{}/archive/refs/heads/{}.zip".format(username, repository, branch)

    print("downloading", username, repository, branch)
    with open("../mods/temp.zip", 'wb') as handler:
        handler.write(requests.get(url).content)
    
    print("extracting zip")
    with zipfile.ZipFile("../mods/temp.zip","r") as zip_ref:
        zip_ref.extractall("../mods")

    os.remove("../mods/temp.zip")

# downloads all mods listed in /src/mods.json and puts them in /mods
# then moves data and assets directories into /resources (correctly combining same namespace folders from different mods)
# then empties /mods
def getMods(mods):
    os.mkdir("../mods")

    for mod in mods:
        getFromGithub(*mod)
    gatherModResources()

    os.rmdir("../mods")

# deletes any files in /resources that are not listed in <used_resources>
def clearUnusedResources(used_resources):
    print("optimizing /resources")
    for root, dirs, files in os.walk("../resources", topdown=False):
        path = root.split("../resources")[1] # ex. /assets/minecraft/path/to/dir

        for file in files:
            isUsed = (path + "/" + file) in used_resources
            if not isUsed:
                os.remove(root + "/" + file)
        
        for dir in dirs:
            if len(os.listdir(root + "/" + dir)) == 0:
                os.rmdir(root + "/" + dir)

# finds all the valid patchouli book paths in ./resources
def findBooks():
    results = {}

    mods = os.listdir("../resources/data")
    for namespace in mods:
        path = "../resources/data/" + namespace + "/patchouli_books"
        if os.path.isdir(path) and namespace != "patchouli":
            results[namespace] = os.listdir(path)

    return results

# generates the html pages for all books in ./resources
def loadBooks():
    bookData = [] # used to generate index file
    used_resources = []

    for namespace, booknames in findBooks().items():
        for bookname in booknames:
            book = Book(namespace, bookname)

            bookData.append({
                "name": book.display_name,
                "location": namespace + "/" + bookname
            })

            used_resources += book.used_resources

            # TODO: generate html files

    clearUnusedResources(used_resources)
    
    return bookData


def main():
    with open("mods.json", "r") as f:
        mods = json.loads("\n".join(f.readlines()))
    getMods(mods)
    books = loadBooks()
    # generateIndexFile(books) # TODO

clearUnusedResources([])