from bs4 import BeautifulSoup
doc = "test2.html"
file = open(doc, "r")
soup = BeautifulSoup(file , "html.parser")
count = 1
for ligne in soup.select("hr"):
    sup = soup.new_tag('p')
    sup.string = "**PAGE:"+ str(count)+"**"
    ligne.insert_after(sup)
    count += 1
df = pd.DataFrame(columns=["page", "arrêt", "date", "juridiction"])
text = soup.text
m = re.findall(r"(\*\*PAGE:(\d{1,3})\*\*.+?)?ARRÊT\..+?LA COUR.+?([A-Za-z].+?)\. Du(.+?\d{3}.+?)\.?\s?(—|-)(.+?)\.?(—|,)", text)
for _, page, arret, date, _,region,_ in m:
    df = df.append({'page' : page, 'arrêt' : arret , "date": date, "juridiction" : region},ignore_index=True)
df["page"] = df["page"].replace("",None)
df["page"] = df["page"].interpolate(method='pad')
df.to_csv(f"{index_directories}/{doc[:-5]}.csv")