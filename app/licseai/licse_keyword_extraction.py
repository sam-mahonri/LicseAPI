import yake

def get_keywords(text, range=5):
    kw_extractor = yake.KeywordExtractor(lan="pt", n=2, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=range, features=None)
    keywords = kw_extractor.extract_keywords(text)

    return keywords