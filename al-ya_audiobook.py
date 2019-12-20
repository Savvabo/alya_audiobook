from bs4 import BeautifulSoup
import requests
from gtts import gTTS


def get_all_articles():
    all_articles = []
    step = 0
    website = 'https://evo-lutio.livejournal.com/?skip={}'
    while True:
        print(step)
        response = requests.get(website.format(step))
        soup = BeautifulSoup(response.text, 'lxml')
        if not soup.find('div', id='page') or step == 50:
            return all_articles
        else:
            all_articles.append(soup)
            step += 50


def get_article_text(article_link):
    response = requests.get(article_link)
    soup = BeautifulSoup(response.text, 'lxml')
    article_text = soup.find('article', class_='b-singlepost-body').text
    return article_text
    # BeautifulSoup(requests.get(article.find('a', class_='subj-link')['href']).text, 'lxml').find('article', class_='b-singlepost-body').text


def score_article(article_text):
    tts = gTTS('{}'.format(article_text))
    scored_text = tts.save('article_text.mp3')
    return scored_text

def parse_articles(step):
    parsed_articles = []
    articles = step.find_all('dl', class_='entry hentry')
    for article in articles:
        article_data = dict()
        article_data['article_title'] = article.find('dt', class_='entry-title').text
        article_data['article_link'] = article.find('a', class_='subj-link')['href']
        article_data['article_text'] = get_article_text(article_data['article_link'])
        article_data['article_scoring'] = score_article(article_data['article_text'])
        parsed_articles.append(article_data)
    return parsed_articles


def format_to_string(parsed_article):
    template = "    1. {article_title}     \n " \
               "    2. {article_text}     \n " \
               "    3. {article_scoring}     \n " \
               "    4. {article_link}     \n "
    formatted_message = template.format(article_title=parsed_article['article_title'],
                                        article_text=parsed_article['article_text'],
                                        article_scoring=parsed_article['article_scoring'],
                                        article_link=parsed_article['article_link'])
    return formatted_message


def run():
    parsed_articles = []
    all_articles = get_all_articles()
    for step in all_articles:
        parsed_articles.extend(parse_articles(step))
    print(parsed_articles)
    for parsed_article in parsed_articles:
        formatted_articles = format_to_string(parsed_article)
        print(formatted_articles)


if __name__ == '__main__':
    run()
