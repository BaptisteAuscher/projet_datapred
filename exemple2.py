import requests

keywords = []
outputs = [] # in title, url, body, len
countries = []

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

while True:
    countries = input("Entrez les pays d'origines")
    if output.lower() != "fin":
        outputs.append(output)
    else:
        break


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
    "apiKey": "90c0bf04-d747-41a0-af03-47bfac6e9585",
    "forceMaxDataTimeWindow": 31,
    "dateStart": time[0] if time else None,
    "dateEnd": time[1] if time else None,
    "sourceLocationUri": countries if countries else None
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