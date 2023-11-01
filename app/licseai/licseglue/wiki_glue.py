import wikipediaapi

from . import summarize

from dotenv import load_dotenv, find_dotenv
import os


class WikipediaSummarizer:
    def __init__(self):
        self.headers = {
            'User-Agent': os.getenv('LICSE_WIKIPEDIA_USER')
        }
        self.wiki_wiki = wikipediaapi.Wikipedia(user_agent='Licse', language='pt', extract_format=wikipediaapi.ExtractFormat.WIKI, headers=self.headers)

    def extract_keyword(self, text):
        result = summarize.extract_keyword(text)
        return result

    def summarize_article(self, search_keyword, num_summary_sentences=5):
        search_results = self.wiki_wiki.page(search_keyword)

        if search_results.exists():
            article_text = search_results.text
            print(article_text)
            result = summarize.summarize_article(article_text, num_summary_sentences)
        else:
            result = None
        return result

if __name__ == "__main__":
    summarizer = WikipediaSummarizer()
    search_query = input('Digite sua consulta: ')

    search_keyword = summarizer.extract_keyword(search_query)

    if not search_keyword:
        search_keyword = search_query.split()[0]

    summary = summarizer.summarize_article(search_keyword)
    
    if summary:
        greeting = f"Olá! Aqui está um resumo sobre '{search_keyword}':\n\n"
        print(greeting + summary)
    else:
        print(f"Artigo contendo a palavra-chave '{search_keyword}' não encontrado na Wikipedia em português.")
