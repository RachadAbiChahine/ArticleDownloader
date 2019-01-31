import json
import logging
from newspaper import Article

separator = "*********************************************************************" + '\n'

filename = 'articleUri.txt'
file = open(filename, "r")
output = open("result-Fr", "w")
cmpUrlWellProcessed = 0
cmpUriInError = 0
uriInError = []
for line in file:
    if line.strip().endswith(".pdf"):
        print("ispdf")
    else:
        try:
            article = Article(line.strip())
            article.download()
            article.parse()
            article.nlp()

            output.write(line + '\n')
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
