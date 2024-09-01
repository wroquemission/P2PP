import json

IMAGES = {
    'sakura-multiple': 'Images/sakura_multiple.svg',
    'sakura-single': 'Images/sakura_single.svg',
    'torii-gate': 'Images/torii_gate.svg',
    'shovel': 'Images/shovel.svg',
    'link': 'Images/link.svg',
    'logo': 'Images/logo.svg'
}

LABELS = {
    'eng': {
        'Invitation to Baptism': 'Data/{lang}/baptismal-invitation-{lang}.json',
        'Lesson 1': 'Data/{lang}/lesson-1-{lang}.json',
        'Lesson 2': 'Data/{lang}/lesson-2-{lang}.json',
        'Lesson 3': 'Data/{lang}/lesson-3-{lang}.json',
        'Lesson 4': 'Data/{lang}/lesson-4-{lang}.json',
        'Baptismal Questions': 'Data/{lang}/baptismal-questions-{lang}.json'
    }
}

def generate_content(data, level=1):
    content = ''
    
    for item in data:
        match item['type']:
            case 'paragraph':
                element = '<p class="content-paragraph">{}</p>'
                content += element.format(item['content'])
            case 'header':
                element = '<h{level} class="content-header">{title}</h{level}>'
                content += element.format(
                    level=level,
                    title=item['content']
                )
            case 'list':
                element = '<ul class="content-list">{}</ul>'
                content += element.format(
                    generate_content(item['content'], level)
                )
            case 'item':
                element = '<li class="content-list-item>{}</li>'
                
                first, *rest = item['content'].split('\n\n\n')
                
                if len(rest) > 0:
                    inner_list = ({'type': 'item', 'content': list_item} for list_item in rest)

                    content += element.format(
                        element.format(first) + generate_content(
                            [{'type': 'list', 'content': inner_list}],
                            level
                        )
                    )
                else:
                    content += element.format(first)
            case 'section':
                element = '<div class="content-section">{}</div>'
                content += element.format(
                    generate_content(item['content'], level + 1)
                )
                
    return content

def get_data(label_language, content_language):
    data = {}
    
    labels = LABELS[label_language]
    
    for label in labels:
        path = labels[label].format(lang=content_language)

        with open(path, 'r', encoding='utf-8') as f:
            data[label] = json.loads(f.read())
            
    return data

def fill_template(data, image_paths, template_path, output_path):
    images = {}
    
    for image in image_paths:
        with open(image_paths[image], 'r') as f:
            images[image] = f.read()

    with open(template_path, 'r') as f:
        template = f.read()
        output = template.replace(
            'DATA',
            json.dumps(data)
        ).replace(
            'IMAGES',
            json.dumps(images)
        )
        
    with open(output_path, 'w') as f:
        f.write(output)

TEMPLATE = 'template.html'
LABEL_LANG = 'eng'

data = {}

for lang in ('jpn', 'rom', 'eng', 'por'):
    data[lang] = get_data(LABEL_LANG, lang)

fill_template(data, IMAGES, TEMPLATE, 'Dist/P2PP.html')