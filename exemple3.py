import requests

keywords = []
outputs = [] # in title, url, body, len
countries = []
sent = []
time = []
def get_wikipedia_link(location_name):
    base_url = "http://en.wikipedia.org/wiki/"
    formatted_location = location_name.replace(" ", "_")  # Remplacer les espaces par des underscores
    return f"{base_url}{formatted_location}"


while True: 
  keyword = input("Entrez des keywords")
  if keyword != "fin":
    keywords.append(keyword)
  else:
    break

while True : 
    output = input ("Entrer des formats de sortie parmi title, url, body, len")
    if output != "fin":
        outputs.append(output)
    else:
        break

time_input = input("Entrez l'intervalle de temps (format: YYYY-MM-DD YYYY-MM-DD), appuyez sur Entrée si non spécifié: ")
if time_input.strip():  # Check if the input is not empty
    start_date, end_date = map(str.strip, time_input.split())
    time = [start_date, end_date]

sent_input = input("Entrez l'intervalle de sentiments compris dans -1,1 (format : x y avec y>x) , appuyez sur Entrée si non spécifié: ")
if sent_input.strip():  # Check if the input is not empty
    min_sent, max_sent = map(str.strip, sent_input.split())
    sent = [float(min_sent), float(max_sent)]

while True:
    country = input("Entrez les pays d'origines (en Anglais)")
    if country != "fin":
        countries.append(get_wikipedia_link(country))
    else:
        break
        
keywordLoc = input ("Où localiser les keywords ? Taper title, body ou body,title")

r = requests.get("http://eventregistry.org/api/v1/article/getArticles", {
    "action": "getArticles",
    "keyword": keywords,
    "articlesPage": 1,
    "articlesCount": 100,
    "articlesSortBy": "date",
    "articlesSortByAsc": False,
    "articlesArticleBodyLen": -1,
    "resultType": "articles",
    "dataType": [
        "news",
        "pr"
    ],
    "apiKey": "562eab60-8961-4906-82d9-6a5cbd74589c",
    "forceMaxDataTimeWindow": 31,
    "dateStart": time[0] if len(time)>0 else None,
    "dateEnd": time[1] if len(time)>0 else None,
    "sourceLocationUri": countries if len(countries)>0 else None,
    "minSentiment" : min_sent if len(sent)>0 else None,
    "maxSentiment" : max_sent if len(sent)>0 else None,
    "keywordLoc" : keywordLoc
}, headers={"content-type": "application/json"})

articles = r.json()["articles"]["results"]
if "len" in outputs : 
    print("nombre d'articles" , len(articles))
    outputs.remove("len")

with open("resultat.txt", "w") as f:
    for article in articles:
        for x in outputs : 
            f.write(article[x] + "\n")
        f.write("\n")

# Faire une requête sans date et voir la date de l'article