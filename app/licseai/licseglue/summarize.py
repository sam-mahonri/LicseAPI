import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from yake import KeywordExtractor
import random

from dotenv import load_dotenv, find_dotenv
import os

nltk.download('punkt')
nltk.download('stopwords')


def extract_keyword(text):
    extractor = KeywordExtractor(lan="pt", top=1)
    keywords = extractor.extract_keywords(text)
    return keywords[0][0] if keywords else None

def summarize_article(article_text, num_summary_sentences=5):

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Zá-úÁ-Ú]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = sent_tokenize(article_text, language='portuguese')
    stop_words = set(stopwords.words('portuguese'))

    word_frequencies = {}
    for word in word_tokenize(formatted_article_text, language='portuguese'):
        if word.lower not in stop_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies:
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    sentence_scores = {}
    for sentence in sentence_list:
        for word in word_tokenize(sentence, language='portuguese'):
            if word in word_frequencies:
                if len(sentence.split()) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    import heapq

    summary_sentences = heapq.nlargest(num_summary_sentences, sentence_scores, key=sentence_scores.get)
    print(summary_sentences)
    summary = ' '.join(summary_sentences)
    return summary
