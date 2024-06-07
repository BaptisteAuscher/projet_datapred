from eventregistry import *
import pandas as pd
er = EventRegistry(apiKey = "YOUR_API_KEY", allowUseOfArchive = False)

def get_articles(keywords=None, 
                 keywordsLoc="body", 
                 andOrKW="and", 
                 ignoreKeywords=None, 
                 andOrIKW="and", 
                 dataType="news", 
                 lang="eng", 
                 dateStart=None, 
                 dateEnd=None, 
                 maxRows=100) :
    """
    Description:
    Find articles based on specified criteria.

    Parameters:
    - keywords (str or list): Keywords to search for in articles. Can be a single string or a list of strings. The maximum length is 15.
    - keywordsLoc (str): Location in the article to search for keywords. Options: "body" (default), "title", or "body,title".
    - andOrKW (str): Operator to use for combining keywords. Options: "and" (default) for all keywords, "or" for any keyword.
    - ignoreKeywords (str or list): Keywords to ignore in articles.
    - andOrIKW (str): Operator to use for combining ignored keywords. Options: "and" (default) for all ignored keywords, "or" for any ignored keyword.
    - dataType (str or list): Types of data to search. Options: "news" (default) for news content, "pr" for press releases, or "blog". 
                              If multiple data types are desired, provide them in a list (e.g., ["news", "pr"]).
    - lang (str or list): Language(s) of articles to search for. If more than one language is specified, resulting articles can be written in any of the languages.
    - dateStart (str): Start date of the time interval to search for articles (format: "YYYY-MM-DD").
    - dateEnd (str): End date of the time interval to search for articles (format: "YYYY-MM-DD").
    - maxRows (int): Maximum number of articles to retrieve.

    Returns:
    pandas.DataFrame: DataFrame containing the requested articles.
    """

    if keywords != None :
        if andOrKW == "and" :
            keywords = QueryItems.AND(keywords)
        elif andOrKW == "or" :
            keywords = QueryItems.OR(keywords)
        else :
            print(f"Error, andOrKW must be 'and' or 'or' not {andOrKW}.")
            return None
    if ignoreKeywords != None :
        if andOrIKW == "and" :
            ignoreKeywords = QueryItems.AND(ignoreKeywords)
        elif andOrIKW == "or" :
            ignoreKeywords = QueryItems.OR(ignoreKeywords)
        else :
            print(f"Error, andOrIKW must be 'and' or 'or' not {andOrIKW}.")
            return None
    
    q = QueryArticlesIter (
        keywords=keywords,
        keywordsLoc=keywordsLoc,
        ignoreKeywords=ignoreKeywords,
        dataType=dataType,
        lang=lang,
        dateStart=dateStart,
        dateEnd=dateEnd)
    q_execQuery = q.execQuery(er, sortBy = "date", 
                               returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(concepts = True, categories = True)),
                               maxItems = maxRows)
    print(q_execQuery)
    df = pd.DataFrame()
    for article in q_execQuery :
        # Convertir l'article en ligne de DataFrame
        df_row = pd.DataFrame({
            'uri': [article.get('uri', None)],
            'lang': [article.get('lang', None)],
            'isDuplicate': [article.get('isDuplicate', None)],
            'date': [article.get('date', None)],
            'time': [article.get('time', None)],
            'dateTime': [article.get('dateTime', None)],
            'dateTimePub': [article.get('dateTimePub', None)],
            'dataType': [article.get('dataType', None)],
            'sim': [article.get('sim', None)],
            'url': [article.get('url', None)],
            'title': [article.get('title', None)],
            'body': [article.get('body', None)],
            'source_uri': [article['source']['uri']] if 'source' in article and 'uri' in article['source'] else [None],
            'source_dataType': [article['source']['dataType']] if 'source' in article and 'dataType' in article['source'] else [None],
            'source_title': [article['source']['title']] if 'source' in article and 'title' in article['source'] else [None],
            'authors': [', '.join([author['name'] for author in article.get('authors', [])])],
            'sentiment': [article.get('sentiment', None)],
            'wgt': [article.get('wgt', None)],
            'relevance': [article.get('relevance', None)],
            'image': [article.get('image', None)],
            'eventUri': [article.get('eventUri', None)]
        })
        df = pd.concat([df, df_row], ignore_index=True)
    return df
