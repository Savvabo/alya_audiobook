from bs4 import BeautifulSoup
import requests
from gtts import gTTS
import telebot
import os

bot = telebot.TeleBot('992312685:AAHqVknW9e0taMmhx04j7bZPsxXCCNUbD4Q')


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


def parse_articles(step):
    parsed_articles = []
    articles = step.find_all('dl', class_='entry hentry')
    for article in articles:
        article_data = dict()
        article_data['article_title'] = article.find('a', class_='subj-link').text
        article_data['article_link'] = article.find('a', class_='subj-link')['href']
        article_data['article_text'] = get_article_text(article_data['article_link'])
        parsed_articles.append(article_data)
    return parsed_articles


def format_article(parsed_article):
    template = "    ✏ {article_title}     \n " \
               "    🔗 {article_link}      \n "
    formatted_message = template.format(article_title=parsed_article['article_title'],
                                        article_link=parsed_article['article_link'])
    tts = gTTS(text=parsed_article['article_text'], lang="ru")
    try:
        audio = '{}.mp3'.format(parsed_article['article_title'])
    except OSError:
        audio = 'evo_audio.mp3'
    tts.save(audio)
    send_audio = bot.send_audio(chat_id=334755342, audio=open(audio, 'rb'))
    del_audio = lambda var: os.remove('{}'.format(var))
    return formatted_message, send_audio, del_audio(audio)


def run():
    parsed_articles = []
    all_articles = get_all_articles()
    for step in all_articles:
        parsed_articles.extend(parse_articles(step))
    for parsed_article in parsed_articles:
        formatted_article = format_article(parsed_article)
        bot.send_message(334755342, formatted_article)
        print(formatted_article)


if __name__ == '__main__':
    run()
