from newspaper import Article

def pull_content_from_url(url:str):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

        