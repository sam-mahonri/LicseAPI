from .wiki_glue import WikipediaSummarizer



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