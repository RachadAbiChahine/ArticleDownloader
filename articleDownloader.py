import json
import logging
import sys
import nltk
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from urllib.request import urlopen
from tika import parser



from newspaper import Article
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

separator = "*********************************************************************" + '\n'

filename = sys.argv[1]
file = open(filename, "r")
output = open(sys.argv[2], "w")
cmpUrlWellProcessed = 0
cmpUriInError = 0
uriInError = []
for line in file:
    if line.strip().endswith(".pdf"):
        pdf = urlopen(line.strip()).read()
        pdfFile = open("tmp.pdf", 'wb')
        pdfFile.write(pdf)
        pdfFile.close()
        raw = parser.from_file("tmp.pdf")

        output.write(separator+raw['content']+separator)

    else:
        try:
            article = Article(line.strip())
            article.download()
            article.parse()
            article.nlp()

            output.write("Url : " + line + '\n')
            output.write(article.title + '\n')
            try:
                output.write(article.publish_date.strftime("%Y-%m-%d %H:%M:%S") + '\n')
            except:
                output.write("Unknown date" + '\n')
            output.write(article.text + '\n')
            output.write(separator)
            output.write(','.join(article.additional_data))
            additionalData = article.meta_data
            data = json.loads(json.dumps(additionalData))
            if 'keywords' in data:
                output.write("keywords: ")
                output.write(data['keywords'])
            else:
                if 'news_keywords' in data:
                    output.write("keywords: ")
                    output.write(data['news_keywords'])
                else:
                    logging.info("no keyword found")
            output.write("tags: ")
            output.write(','.join(article.tags))
            output.write('\n')
            output.write(separator)
            cmpUrlWellProcessed += 1
        except Exception as e:
            cmpUriInError += 1
            logging.error(e)
            uriInError.append(line)

print(separator)
print("number of Url processed: ", cmpUrlWellProcessed, '\n')
print("number of Url in error: ", cmpUriInError, '\n')
for uri in uriInError:
    print(uri)
