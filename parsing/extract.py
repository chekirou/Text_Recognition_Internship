import re


def extract_arrets(file_path):
    arrets = []
    with open(file_path) as file:
        content = file.read()
        L = re.findall("« ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —", content)
        for i in L:
            arrets.append(i[0])
    return arrets

def extract_datas(file_path):
    with open(file_path) as file:
        content = file.read()
        datas = []
        L = re.findall("(Audience du (.*?)\.(.*?) « ((La Cour|Le Tribunal) ; (.*?))\. » (.*?)) —",
                       content)
        for i in L:
            print("==================")
            for k, j in enumerate(i):
                print(k, "==>", j)
            print("==================")
            arret, president, date = i[4], i[1], i[2]
            datas.append((arret,president,date))
        return datas

def extract_all(file_path):
    with open(file_path) as file:
        datas = []
        content = file.read()
        L = re.findall(
            "(((COUR|TRIBUNAL).*?) (Présidence de ((.*?).)) (Audience du ((\d+) (\w+) (\d+\.)))) (.*?) « ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —",
            content)
        for i in L:
            print("====")
            juridiction = (i[1])
            president = (i[5])
            date = (i[6]).replace("Audience du ","")
            arret = (i[14])
            datas.append((president,date,juridiction,arret))
        return datas


print(extract_all("parsed/19110109.txt"))