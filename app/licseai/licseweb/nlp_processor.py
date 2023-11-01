import spacy

class NLPProcessor:
    def __init__(self, text):
        self.nlp = spacy.load("pt_core_news_lg")
        self.doc = self.nlp(text)

    def extract_topics(self):
        topics = []
        for chunk in self.doc.noun_chunks:
            topics.append(chunk.text)
        return topics

    def extract_summary(self):
        sentences = list(self.doc.sents)
        summary = ' '.join(map(str, sentences[:10]))  # Gera um resumo com as três primeiras sentenças.
        return summary
