from snownlp import sentiment

sentiment.train('neg-all.txt', 'pos-all.txt')
sentiment.save('sentiment.marshal')