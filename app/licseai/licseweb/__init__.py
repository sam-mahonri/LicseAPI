from web_scraper import WebScraper
from nlp_processor import NLPProcessor

class WebPageReader:
    def __init__(self, url):
        self.url = url
        self.process_page()

    def process_page(self):
        web_scraper = WebScraper(self.url)
        links = web_scraper.extract_links()
        text = web_scraper.extract_text()

        nlp_processor = NLPProcessor(text)
        topics = nlp_processor.extract_topics()
        summary = nlp_processor.extract_summary()

        print("\nLinks Relacionados:")
        for link in links:
            print(link)

        print("\nTópicos no Site:")
        for topic in topics:
            print(topic)

        print("\nResumo do Site:")
        print(summary)

if __name__ == "__main__":
    url = input("Digite o URL da página web: ")
    web_page_reader = WebPageReader(url)
