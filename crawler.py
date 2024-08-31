import requests
from bs4 import BeautifulSoup
import json

URLs = {
    'baptismal-invitation': 'https://www.churchofjesuschrist.org/study/manual/preach-my-gospel-2023/04-chapter-3/07-chapter-3-invite?lang={}',
    'lesson-1': 'https://www.churchofjesuschrist.org/study/manual/preach-my-gospel-2023/04-chapter-3/08-chapter-3-lesson-1?lang={}',
    'lesson-2': 'https://www.churchofjesuschrist.org/study/manual/preach-my-gospel-2023/04-chapter-3/09-chapter-3-lesson-2?lang={}',
    'lesson-3': 'https://www.churchofjesuschrist.org/study/manual/preach-my-gospel-2023/04-chapter-3/10-chapter-3-lesson-3?lang={}',
    'lesson-4': 'https://www.churchofjesuschrist.org/study/manual/preach-my-gospel-2023/04-chapter-3/11-chapter-3-lesson-4?lang={}',
    'baptismal-questions': 'https://www.churchofjesuschrist.org/study/manual/preach-my-gospel-2023/20-chapter-12?lang={}'
}

lesson = input('LESSON> ')
lang = input('LANG> ')

URL = URLs[lesson].format(lang)
path = 'Data/{}/{}-{}.json'.format(lang, lesson, lang)

res = requests.get(URL)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, features='html.parser')
body = soup.find_all(class_='body-block')[0]
tag = body.find_all('section')

def create_element(element):
    elements = []

    for child in element:
        if child.name == "p":
            elements.append({'type': 'paragraph', 'content': child.text.strip()})
        elif child.name == 'header':
            elements.append({'type': 'header', 'content': child.text.strip().split('\n')[-1]})
        elif child.name in ['ul', 'ol']:
            elements.append({'type': 'list', 'content': create_element(child)})
        elif child.name == 'li':
            elements.append({'type': 'item', 'content': child.text.strip()})   
        elif child.name == 'section':
            elements.append({'type': 'section', 'content': create_element(child)})

    return elements

with open(path, 'w', encoding='utf-8') as f:
      json.dump(create_element(body), f, ensure_ascii=False, indent=4)