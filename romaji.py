import cutlet
import json
import re

labels = ['baptismal-invitation', 'lesson-1', 'lesson-2', 'lesson-3', 'lesson-4', 'baptismal-questions']

katsu = cutlet.Cutlet()
katsu.use_foreign_spelling = False

slash_pattern = re.compile(r'(\w+)/(\w+)')

def convert(source):
    for item in source:
        if isinstance(item['content'], list):
            convert(item['content'])
        else:
            item['content'] = slash_pattern.sub(r'\1 \2', katsu.romaji(item['content']))

for label in labels:
    with open('Data/jpn/{}-jpn.json'.format(label), 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        convert(data)
        
    with open('Data/rom/{}-rom.json'.format(label), 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))