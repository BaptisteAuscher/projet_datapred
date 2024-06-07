import requests

"""
keywords = []
while True: 
  keyword = input("Entrez des keywords")
  if keyword != "fin":
    keywords.append(keyword)
  else:
    break
"""

def requete(keywords, date_du_jour, clef_API="90c0bf04-d747-41a0-af03-47bfac6e9585") :  
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
    "apiKey": clef_API,
    "forceMaxDataTimeWindow": 31
  }, headers={"content-type" : "application/json"})

  articles = r.json()["articles"]["results"]

  with open("resultat.txt", "w") as f:
    for article in articles:
      f.write(article["title"] + "\n")
      f.write(article["url"] + "\n")
      f.write(article["body"] + "\n")
      f.write("\n")
    

