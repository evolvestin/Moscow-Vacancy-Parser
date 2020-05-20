import re
import random
import _thread
import gspread
import requests
from time import sleep
from telebot import types
from telegraph import upload
from bs4 import BeautifulSoup
from datetime import datetime
from docs import moscow_vars as docs
from PIL import Image, ImageFont, ImageDraw
from additional.objects import thread_exec as executive
from oauth2client.service_account import ServiceAccountCredentials
from additional.objects import bold, code, under, query, \
    italic, printer, stamper, log_time, start_message, start_main_bot

stamp1 = int(datetime.now().timestamp())
allowed_head_elements = ['условия', 'требования']
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
starting = ['title', 'place', 'tags', 'geo', 'money', 'org_name', 'schedule', 'employment', 'short_place',
            'experience', 'education', 'contact', 'numbers', 'description', 'email', 'metro', 'tag_picture']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
emoji_list = '([💻🏙🏅🎓💸📔🚇💼🔋])'
emoji = {
    '💻': Image.open('emoji/comp.png'),
    '🏙': Image.open('emoji/city.png'),
    '🏅': Image.open('emoji/star.png'),
    '🎓': Image.open('emoji/edu.png'),
    '💸': Image.open('emoji/money.png'),
    '📔': Image.open('emoji/note.png'),
    '🚇': Image.open('emoji/metro.png'),
    '💼': Image.open('emoji/case.png'),
    '➡': Image.open('emoji/arrow.png'),
    '🔋': Image.open('emoji/empty.png')
}
e_post = '✉'
idMe = 396978030
idMain = docs.idMain
idDocs = docs.idDocs
idInstagram = docs.idInstagram
allowed_persons = [idMe, 470292601, 457209276, 574555477]
# =================================================================


def google(sheet, action, option):
    global creds5
    global client5
    global data5
    try:
        data5 = client5.open('scheduled').worksheet(sheet)
    except IndexError and Exception:
        creds5 = ServiceAccountCredentials.from_json_keyfile_name('person5.json', scope)
        client5 = gspread.authorize(creds5)
        data5 = client5.open('scheduled').worksheet(sheet)

    if action == 'col_values':
        try:
            values = data5.col_values(option)
        except IndexError and Exception:
            creds5 = ServiceAccountCredentials.from_json_keyfile_name('person5.json', scope)
            client5 = gspread.authorize(creds5)
            data5 = client5.open('scheduled').worksheet(sheet)
            values = data5.col_values(option)
    elif action == 'insert':
        try:
            values = data5.insert_row([option], 1)
        except IndexError and Exception:
            creds5 = ServiceAccountCredentials.from_json_keyfile_name('person5.json', scope)
            client5 = gspread.authorize(creds5)
            data5 = client5.open('scheduled').worksheet(sheet)
            values = data5.insert_row([option], 1)
        sleep(2)
    elif action == 'append':
        try:
            values = data5.append_row(option)
        except IndexError and Exception:
            creds5 = ServiceAccountCredentials.from_json_keyfile_name('person5.json', scope)
            client5 = gspread.authorize(creds5)
            data5 = client5.open('scheduled').worksheet(sheet)
            values = data5.append_row(option)
        sleep(2)
    elif action == 'delete':
        try:
            values = data5.delete_row(option)
        except IndexError and Exception:
            creds5 = ServiceAccountCredentials.from_json_keyfile_name('person5.json', scope)
            client5 = gspread.authorize(creds5)
            data5 = client5.open('scheduled').worksheet(sheet)
            try:
                values = data5.delete_row(option)
            except Exception as e:
                search_exception = re.search('You can\'t delete all the rows on the sheet', str(e))
                if search_exception:
                    values = data5.update_cell(1, 1, '')
                else:
                    values = None
        sleep(3)
    else:
        values = None
    sleep(1)
    return values


bot = start_main_bot('non-sync', docs.tkn)
used_array = google('moscow-growing', 'col_values', 1)
start_search = query('https://t.me/UsefullCWLinks/' + str(docs.start_link), 'd: (.*) :d')
if start_search:
    last_date = stamper(start_search.group(1)) - 3 * 60 * 60
    start_message('moscow-worker', stamp1)
else:
    last_date = '\nОшибка с нахождением номера поста. ' + bold('Бот выключен')
    start_message('moscow-worker', stamp1, last_date)
    _thread.exit()
# ====================================================================================


def hour():
    stack = int(datetime.now().timestamp())
    return int(datetime.utcfromtimestamp(int(stack) + 3 * 60 * 60).strftime('%H'))


def post_keys(em):
    posts_row = types.InlineKeyboardMarkup(row_width=1)
    button = [types.InlineKeyboardButton(text=em, callback_data='post')]
    posts_row.add(*button)
    return posts_row


def numeric_replace(number):
    number_string = str(number)
    if number >= 10000:
        number_string = number_string[:-3] + '.' + number_string[-3:]
    if number >= 1000000:
        number_string = number_string[:-7] + '.' + number_string[-7:]
    return number_string


def fonts(font_weight, font_size):
    if font_weight == 'regular':
        return ImageFont.truetype('fonts/Roboto-Regular.ttf', font_size)
    elif font_weight == 'bold':
        return ImageFont.truetype('fonts/Roboto-Bold.ttf', font_size)
    else:
        return ImageFont.truetype('fonts/RobotoCondensed-Bold.ttf', font_size)


def height_indent(row_text, font_weight, font_size):
    size = ImageFont.ImageFont.getsize(fonts(font_weight, font_size), row_text)
    text_height = size[1][1]
    return text_height


def width(emoji_parameter, row_text, font_weight, font_size):
    family = fonts(font_weight, font_size)
    if emoji_parameter:
        for f in emoji_parameter:
            if f in ['💻', '💸', '📔', '🔋']:
                family = fonts('bold', font_size)
    size = ImageFont.ImageFont.getsize(family, row_text)
    text_width = size[0][0]
    return text_width


def height(emoji_parameter, row_text, font_weight, font_size):
    family = fonts(font_weight, font_size)
    if emoji_parameter:
        for f in emoji_parameter:
            if f in ['💻', '💸', '📔', '🔋']:
                family = fonts('bold', font_size)
    size = ImageFont.ImageFont.getsize(family, row_text)
    text_height = size[0][1]
    return text_height


def search_emoji(text):
    search = re.search(emoji_list, text)
    if search:
        array = [[search.group(1)]]
    else:
        array = [False]
    if '➡' in text:
        if array[0]:
            array[0].append('➡')
        else:
            array[0] = ['➡']
    array.append(re.sub(emoji_list, '', text))
    return array


def instagram_former(growing):
    for i in growing:
        if str(type(growing.get(i))) == "<class 'str'>":
            growing[i] = re.sub('➡', '—', growing.get(i))
    array = []
    if growing['title'] != 'none':
        array.append('💻' + growing['title'])
    if growing['place'] != 'none':
        array.append('🏙' + growing['place'])
    if growing['experience'] != 'none':
        array.append('🏅Опыт работы ➡ ' + growing['experience'])
    if growing['education'] != 'none':
        array.append('🎓Образование ➡ ' + growing['education'])
    if growing['money'] != 'none':
        more = ''
        if growing['money'][1] != 'none':
            more += '+'
        array.append('💸З/П ' + growing['money'][0] + more + ' руб.')
    array.append(' ')
    array.append('📔Контакты')
    if growing['org_name'] != 'none':
        array.append(growing['org_name'])
    if growing['contact'] != 'none':
        array.append(growing['contact'])
    if growing['numbers'] != 'none':
        numbers = growing['numbers'].split('\n')
        array.append(numbers[0])
    if growing['email'] != 'none':
        array.append(growing['email'] + ' ➡ Резюме')
    if growing['email'] == 'none' and growing['numbers'] == 'none':
        array.append('🔋Источник в нашем telegram канале ➡ Ссылка в профиле')
    if growing['metro'] != 'none':
        array.append('🚇' + growing['metro'])
    return array


def image(image_text, image_text_price, background_coefficient):
    left = 100
    left_price = 60
    original_width = 550
    original_height = 280
    more_font_price = 200
    color = (256, 256, 256)
    original_width_price = 450
    original_height_price = 75
    img = Image.open('images/logo' + background_coefficient + '.png')
    draw = ImageDraw.Draw(img)
    while width(None, image_text_price, 'bold', more_font_price) > original_width_price:
        more_font_price -= 1
    left_price += (original_width_price - width(None, image_text_price, 'bold', more_font_price)) // 2
    top = 430 - height_indent(image_text_price, 'bold', more_font_price)
    top += (original_height_price - height(None, image_text_price, 'bold', more_font_price)) // 2
    draw.text((left_price, top), image_text_price, color, fonts('bold', more_font_price))

    if width(None, image_text, 'bold', 70) <= original_width:
        more_font = 200
        while width(None, image_text, 'bold', more_font) > original_width:
            more_font -= 1
        left += (original_width - width(None, image_text, 'bold', more_font)) // 2
        top = 120 - height_indent(image_text, 'bold', more_font)
        top += (original_height - height(None, image_text, 'bold', more_font)) // 2
        draw.text((left, top), image_text, color, fonts('bold', more_font))
    else:
        layer = 1
        drop_text = ''
        layer_array = []
        full_height = 0
        temp_text_array = re.sub('\s+', ' ', image_text.strip()).split(' ')
        for i in range(0, len(temp_text_array)):
            if width(None, temp_text_array[i], 'bold', 70) <= original_width:
                if width(None, (drop_text + ' ' + temp_text_array[i]).strip(), 'bold', 70) <= original_width:
                    drop_text = (drop_text + ' ' + temp_text_array[i]).strip()
                else:
                    if drop_text != '' and len(layer_array) < 3:
                        layer_array.append(drop_text)
                        full_height += height(None, drop_text, 'bold', 70)
                    drop_text = ''
                    drop_text = (drop_text + ' ' + temp_text_array[i]).strip()
                if i == len(temp_text_array) - 1:
                    if drop_text != '' and len(layer_array) < 3:
                        layer_array.append(drop_text)
                        full_height += height(None, drop_text, 'bold', 70)
        additional_height = 0
        if len(layer_array) > 0:
            indent_height = int(full_height / len(layer_array) + 0.15 * (full_height / len(layer_array)))
        else:
            indent_height = int(full_height + 0.15 * full_height)
        mod = int((original_height - len(layer_array) * indent_height) / 2)
        for i in layer_array:
            text_position = (left + (original_width - width(None, i, 'bold', 70)) // 2, 120 + mod + additional_height)
            additional_height += indent_height
            draw.text(text_position, i, color, fonts('bold', 70))
            layer += 1
    img.save('images/bot_edited.png')
    doc = open('images/bot_edited.png', 'rb')
    uploaded = upload.upload_file(doc)
    uploaded_link = '<a href="https://telegra.ph' + uploaded[0] + '">​​</a>️'
    return uploaded_link


def instagram_image(text_array, background_coefficient):
    background = Image.open('images/logo_instagram' + background_coefficient + '.png')
    img = Image.new('RGBA', (1080, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    original_height = 980
    original_width = 980
    color = (256, 256, 256)
    layer_array = []
    more_font = 200
    height_coefficient = False
    while height_coefficient is False:
        while len(layer_array) != len(text_array):
            for t in text_array:
                array = search_emoji(t)
                emoji_factor = 0
                if array[0]:
                    emoji_factor += int(more_font + more_font * 0.35) * len(array[0])
                if width(array[0], array[1], 'regular', more_font) + emoji_factor <= original_width:
                    layer_array.append(array)
                else:
                    temp_text_array = re.sub('\s+', ' ', array[1]).split(' ')
                    array = [array[0]]
                    drop_text = ''
                    for i in range(0, len(temp_text_array)):
                        if width(array[0], (drop_text + ' ' + temp_text_array[i]).strip(), 'regular', more_font) \
                                + emoji_factor <= original_width:
                            drop_text = (drop_text + ' ' + temp_text_array[i]).strip()
                        else:
                            if drop_text != '' and len(array) < 3:
                                array.append(drop_text)
                            else:
                                break
                            drop_text = temp_text_array[i]
                        if i == len(temp_text_array) - 1:
                            if drop_text != '' and len(array) < 3:
                                array.append(drop_text)
                                layer_array.append(array)
                            else:
                                break
            if len(layer_array) != len(text_array):
                more_font -= 1
                layer_array.clear()
        layer_count = 0
        additional_height = 0
        for i in layer_array:
            layer_count += len(i) - 1
        indent_height = int(more_font + 0.15 * more_font)
        if layer_count * indent_height <= original_height:
            mod = 50 + int((original_height - layer_count * indent_height) / 2)
            pic = mod + int(0.1 * more_font)
            previous_arrow_array = None
            for array in layer_array:
                for i in array:
                    if array.index(i) != 0:
                        left = 0
                        arrow_split = False
                        family = fonts('regular', more_font)
                        if array[0]:
                            for f in array[0]:
                                if f in ['💻', '💸', '📔', '🔋']:
                                    family = fonts('bold', more_font)
                                if f in ['💻', '🏙', '🏅', '🎓', '💸', '📔', '🚇', '💼', '🔋']:
                                    left += int(more_font + more_font * 0.35)
                                    if array.index(i) == 1:
                                        foreground = emoji[f].resize((more_font, more_font), Image.ANTIALIAS)
                                        background.paste(foreground, (50, pic + additional_height), foreground)
                                if f == '➡':
                                    arrow_split = True
                        if arrow_split is False:
                            text_position = (50 + left, mod + additional_height)
                            draw.text(text_position, i, color, family)
                        else:
                            text = i
                            arrow_indent = 50 + left
                            arrow_array = i.split('➡')
                            foreground = emoji['➡'].resize((more_font, more_font), Image.ANTIALIAS)
                            if len(arrow_array) > 1:
                                text = arrow_array[1]
                                previous_arrow_array = arrow_array
                                text_position = (arrow_indent, mod + additional_height)
                                arrow_indent += width(array[0], arrow_array[0], 'regular', more_font)
                                draw.text(text_position, arrow_array[0], color, family)
                                if text != '':
                                    background.paste(foreground, (arrow_indent, pic + additional_height), foreground)
                            if len(arrow_array) == 1 and previous_arrow_array:
                                if previous_arrow_array[0] == '' and previous_arrow_array[1] == '':
                                    background.paste(foreground, (arrow_indent, pic + additional_height), foreground)
                                    previous_arrow_array = None
                                elif previous_arrow_array[1] == '':
                                    background.paste(foreground, (arrow_indent, pic + additional_height), foreground)
                                    arrow_indent += int(more_font * 0.35)
                                    previous_arrow_array = None
                                else:
                                    arrow_indent -= more_font
                            text_position = (arrow_indent + more_font, mod + additional_height)
                            draw.text(text_position, text, color, family)
                        additional_height += indent_height
            height_coefficient = True
        else:
            more_font -= 1
            layer_array.clear()

    background.paste(img, (0, 0), img)
    background.save('images/bot_edited.png')
    doc = open('images/bot_edited.png', 'rb')
    uploaded = upload.upload_file(doc)
    uploaded_link = '<a href="https://telegra.ph' + uploaded[0] + '">​​</a>️'
    return uploaded_link


def hh_quest(pub_link):
    req = requests.get(pub_link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    growing = {}
    for i in starting:
        growing[i] = 'none'

    title = soup.find('div', class_='vacancy-title')
    if title is not None:
        if title.find('h1') is not None:
            tag = ''
            headline = re.sub('\s+', ' ', title.find('h1').get_text())
            growing['title'] = headline
            headline = re.sub('/', ' / ', headline)
            headline = re.sub('\(.*?\)|[+.,/]|г\.', '', headline.lower())
            headline = re.sub('e-mail', 'email', re.sub('\s+', ' ', headline))
            headline = re.sub('[\s-]', '_', headline.strip().capitalize())
            headline = re.sub('_+', '_', headline)
            for i in re.split('(_)', headline):
                if len(tag) <= 20:
                    tag += i
            if tag.endswith('_'):
                tag = tag[:-1]
            growing['tags'] = [tag]

    place = soup.find('div', class_='vacancy-address-text')
    if place is not None:
        metro = ''
        metro_array = place.find_all('span', class_='metro-station')
        for i in metro_array:
            metro += re.sub('\s+', ' ', i.get_text().strip() + ', ')
        if metro != '':
            growing['metro'] = metro[:-2]
        growing['place'] = re.sub(metro, '', re.sub('\s+', ' ', place.get_text()).strip())

    short_place = soup.find_all('span')
    if short_place is not None:
        for i in short_place:
            if str(i).find('vacancy-view-raw-address') != -1:
                search = re.search('<!-- -->(.*?)<!-- -->', str(i))
                if search:
                    growing['short_place'] = re.sub('\s+', ' ', search.group(1).capitalize().strip())
                    break
        if growing['short_place'] == 'none':
            short_place = soup.find('div', class_='vacancy-company')
            if short_place is not None:
                short_place = short_place.find('p')
                if short_place is not None:
                    growing['short_place'] = re.sub('\s+', ' ', short_place.get_text().capitalize().strip())

    geo_search = re.search('{"lat": (.*?), "lng": (.*?), "zoom"', str(soup))
    if geo_search:
        growing['geo'] = re.sub('\s', '', geo_search.group(1)) + ',' + re.sub('\s', '', geo_search.group(2))

    money = soup.find('p', class_='vacancy-salary')
    if money is not None:
        money_array = []
        money = re.sub('\s', '', money.get_text().lower())
        search_currency = re.search('(eur|бел\.)', money)
        search_ot = re.search('от(\d+)', money)
        search_do = re.search('до(\d+)', money)
        if search_do:
            money_array.append(search_do.group(1))
            money_array.append('none')
        elif search_ot:
            money_array.append(search_ot.group(1))
            money_array.append('more')
        else:
            money_array = 'none'
        if search_currency:
            if search_currency.group(1) == 'eur':
                money_array.append(' евро.')
            else:
                money_array.append(' бел. руб.')
        else:
            money_array.append(' руб.')
        growing['money'] = money_array

    org_name = soup.find('a', {'data-qa': 'vacancy-company-name'})
    if org_name is not None:
        growing['org_name'] = re.sub('\s+', ' ', org_name.get_text().strip())

    description = soup.find('div', class_='g-user-content')
    if description is not None:
        description = description.find_all(['p', 'ul', 'strong'])
        memory = []
        main = ''
        for i in description:
            text = ''
            lists = i.find_all('li')
            if len(lists) != 0 and len(memory) != 0:
                if memory[len(memory) - 1] in allowed_head_elements:
                    for g in lists:
                        list_element = re.sub('\n', '', g.get_text())
                        if len(list_element) > 1:
                            text += '🔹 '
                            list_element = re.sub(',', ', ', list_element)
                            list_element = re.sub('<', '&#60;', list_element)
                            list_element = re.sub('\s+', ' ', list_element).strip()
                            list_element = re.sub('\s*?,\s*?', ',', list_element)
                            list_element = re.sub('\s*?;\s*?', ';', list_element)
                            list_element = re.sub('\s*?\.\s*?', '.', list_element)
                            list_element = list_element[:1].capitalize() + list_element[1:]
                            if list_element.endswith(';') is False:
                                list_element += ';'
                            if list_element not in memory:
                                text += list_element + '\n'
                                memory.append(list_element)
                    text = re.sub('\.+', '.', text[:-2] + '.\n')
            else:
                head_element = re.sub('\s', '_', i.get_text()).lower()
                head_element = re.sub('\W', '', head_element)
                head_element = re.sub('_+', ' ', head_element)
                head_element = re.sub('<', '&#60;', head_element)
                if head_element in allowed_head_elements and head_element not in memory:
                    text += '\n✅ ' + bold(head_element.capitalize() + ':\n')
                    memory.append(head_element)
            main += text
        growing['description'] = main

    numbers = ''
    items = soup.find_all(['p', 'a', 'span'])
    for i in items:
        search = re.search('data-qa="vacancy-view-employment-mode"', str(i))
        if search:
            schedule_text = ''
            schedule = i.find('span')
            if schedule is not None:
                schedule_text = re.sub('\s+', ' ', schedule.get_text().strip())
                growing['schedule'] = re.sub('график', '', schedule_text).strip().capitalize()
            employment = re.sub('\s+', ' ', i.get_text().lower())
            employment = re.sub(',|занятость|' + schedule_text, '', employment).strip().capitalize()
            growing['employment'] = employment

        search = re.search('data-qa="vacancy-experience"', str(i))
        if search:
            growing['experience'] = re.sub('\s+', ' ', i.get_text().strip())

        search = re.search('data-qa="vacancy-contacts__fio"', str(i))
        if search:
            growing['contact'] = re.sub('\s+', ' ', i.get_text().strip())

        search = re.search('data-qa="vacancy-contacts__email"', str(i))
        if search:
            growing['email'] = re.sub('\s+', ' ', i.get_text().strip())

        search = re.search('data-qa="vacancy-contacts__phone"', str(i))
        if search:
            if numbers.find(re.sub('\s+', ' ', i.get_text().strip())) == -1:
                numbers += re.sub('\s+', ' ', i.get_text().strip()) + '\n'
    if numbers != '':
        growing['numbers'] = numbers[:-1]
    return [growing, pub_link]


def former(growing, pub_link, background_coefficient):
    text = ''
    money = None
    keys = post_keys(e_post)
    if growing['title'] != 'none':
        text_to_image = re.sub('/', ' / ', growing['title'])
        text_to_image = re.sub('\(.*?\)|[—.,]|г\.', '', text_to_image)
        text_to_image = re.sub('e-mail', 'email', re.sub('\s+', ' ', text_to_image))
        if growing['money'] != 'none':
            more = ''
            if growing['money'][1] != 'none':
                more += '+'
            money = numeric_replace(int(growing['money'][0])) + more
            if growing['money'][2] == ' евро.':
                money += u' \u20AC '
            elif growing['money'][2] == ' бел. руб.':
                money += ' бел. руб. '
            else:
                money += u' \u20BD '
        growing['tag_picture'] = image(re.sub('[—\s-]', ' ', text_to_image.strip()), money, background_coefficient)
        text = growing['tag_picture'] + '👨🏻‍💻 ' + bold(growing['title']) + '\n'
    if growing['experience'] != 'none':
        text += '🏅 Опыт работы ➡ ' + growing['experience'].capitalize() + '\n'
    if growing['education'] != 'none':
        text += '👨‍🎓 Образование ➡ ' + growing['education'].capitalize() + '\n'
    if money:
        text += '💸 ' + bold('З/П ') + str(money) + '\n'
    if growing['description'] != 'none':
        text += '{}\n'
    text += bold('📔 Контакты\n')
    if growing['org_name'] != 'none':
        text += growing['org_name'] + '\n'
    if growing['contact'] != 'none':
        text += growing['contact'] + '\n'
    if growing['numbers'] != 'none':
        text += growing['numbers'] + '\n'
    if growing['email'] != 'none':
        text += growing['email'] + ' ➡ Резюме\n'
    if growing['metro'] != 'none':
        text += '🚇 ' + growing['metro'] + '\n'

    if growing['geo'].lower() != 'none':
        text += '\n📍 http://maps.yandex.ru/?text=' + growing['geo'] + '\n'
    text += '\n🔎 ' + pub_link + '\n'

    if growing['tags'] != 'none':
        text += italic('\n💼ТЕГИ: ')
        for i in growing['tags']:
            text += '#' + i + ' '
        text = text[:-1] + '\n'

    if growing['description'] != 'none':
        len_text = 4094 - len(text)
        if len_text - len(growing['description']) >= 0:
            text = text.format(growing['description'])
        else:
            text = text.format(growing['description'][:len_text])

    text += '————\nРазместить вакансию @Superworksbot'
    text += instagram_image(instagram_former(growing), background_coefficient)

    if growing['short_place'] == 'none' or growing['money'] == 'none' or growing['title'] == 'none':
        text = pub_link

    return [text, keys, pub_link, growing]


def poster(id_forward, array):
    global last_date
    if array[0] != array[2]:
        message = bot.send_message(id_forward, array[0], reply_markup=array[1], parse_mode='HTML')
        if id_forward == idMain:
            if last_date < message.date:
                last_date = message.date
                start_editing = code('Последний пост на канале Superwork\n') + \
                    bold('d: ') + log_time(last_date + 3 * 60 * 60, code, 0, 'channel') + bold(' :d')
                try:
                    bot.edit_message_text(start_editing, -1001471643258, docs.start_link, parse_mode='HTML')
                except IndexError and Exception:
                    error = '<b>Проблемы с измением стартового ' \
                            'сообщения на канале @UsefullCWLinks</b>\n\n' + start_editing
                    bot.send_message(idMe, error, parse_mode='HTML', disable_web_page_preview=True)
    else:
        if array[3]:
            text = array[3]['tag_picture'] + 'Что-то пошло не так: {\n' + under(bold('link')) + ': ' + array[2] + '\n'
            for i in array[3]:
                if i == 'short_place' or i == 'money' or i == 'title':
                    text += under(bold(i)) + ': ' + re.sub('<', '&#60;', str(array[3].get(i))) + '\n'
                elif i != 'description':
                    text += str(i) + ': ' + re.sub('<', '&#60;', str(array[3].get(i))) + '\n'
            bot.send_message(idMe, text + '}', parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    try:
        if call.data == 'post' and call.from_user.id in allowed_persons:
            if call.message.text:
                text_list = list(call.message.text)
                if call.message.entities:
                    position = 0
                    for i in text_list:
                        true_lenght = len(i.encode('utf-16-le')) // 2
                        while true_lenght > 1:
                            text_list.insert(position + 1, '')
                            true_lenght -= 1
                        position += 1
                    entities_raw = call.message.entities
                    entities = []
                    for i in entities_raw:
                        entities.append(i)
                    entities.reverse()
                    for i in entities:
                        if i.type == 'bold':
                            tag = 'b'
                        elif i.type == 'italic':
                            tag = 'i'
                        elif i.type == 'text_link':
                            tag = None
                            if i.offset == 0:
                                search_telegraph = re.search('telegra.ph', i.url)
                                if search_telegraph:
                                    text_list.insert(0, '<a href="' + i.url + '">​​</a>')
                            else:
                                bot.send_message(idInstagram, '<a href="' + i.url + '">​​</a>️', parse_mode='HTML')
                                bot.send_document(idInstagram, i.url)
                        else:
                            tag = None
                        if tag:
                            text_list.insert(i.offset + i.length, '</' + tag + '>')
                            text_list.insert(i.offset, '<' + tag + '>')
                for i in text_list:
                    if i == '<':
                        text_list[text_list.index(i)] = '&#60;'
                text = ''.join(text_list)
                search_source = re.search('🔎(.*)', text)
                search_map = re.search('📍(.*)', text)
                if search_source:
                    link = search_source.group(1).strip()
                    text = text.replace(link, '<a href="' + link + '">Источник</a>')
                if search_map:
                    link = search_map.group(1).strip()
                    text = text.replace(link, '<a href="' + link + '">На карте</a>')
                google('moscow-schedule', 'append', [text])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

            bot.answer_callback_query(call.id, text='')
    except IndexError and Exception:
        executive(str(call))


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    try:
        if message.chat.id in allowed_persons:
            if message.text.startswith('https://'):
                site_search = re.search('hh\.ru', message.text)
                if site_search:
                    post = hh_quest(message.text)
                else:
                    post = hh_quest(message.text)
                poster(message.chat.id, former(post[0], post[1], str(random.randint(1, 2))))
            elif message.text.startswith('/pic'):
                subbed = re.sub('/pic', '', message.text).strip()
                split = subbed.split('/')
                if len(split) > 1:
                    background_coefficient = str(random.randint(1, 2))
                    text = image(split[0], split[1], background_coefficient)
                else:
                    text = 'Или блять нормально вводи или блять иди нахуй просто уебан'
                bot.send_message(message.chat.id, text, parse_mode='HTML')
            elif message.text.startswith('/base'):
                doc = open('log.txt', 'rt')
                bot.send_document(message.chat.id, doc)
                doc.close()
            else:
                bot.send_message(message.chat.id, bold('ссылка не подошла, пошел нахуй'), parse_mode='HTML')
    except IndexError and Exception:
        executive(str(message))


def checker(address, main_sep, link_sep, quest):
    global used_array
    sleep(3)
    text = requests.get(address, headers=headers)
    soup = BeautifulSoup(text.text, 'html.parser')
    posts_raw = soup.find_all('div', class_=main_sep)
    posts = []
    for i in posts_raw:
        link = i.find('a', class_=link_sep)
        if link is not None:
            posts.append(link.get('href'))
    for i in posts:
        if i not in used_array:
            google('moscow-growing', 'insert', i)
            used_array.insert(0, i)
            post = quest(i)
            poster(idDocs, former(post[0], post[1], str(random.randint(1, 2))))
            printer(i + ' сделано')
            sleep(3)


def main_posting():
    while True:
        try:
            sleep(20)
            scheduled = google('moscow-schedule', 'col_values', 1)
            if len(scheduled) > 0 and (13 <= hour() < 21):
                if len(scheduled[0]) > 0 and (last_date + 60 * 60) < stamper(log_time(gmt=0, form='channel')):
                    poster(idMain, [scheduled[0], None, None, None])
                    printer('запостил')
                    google('moscow-schedule', 'delete', 1)
        except IndexError and Exception:
            executive()


def hh_checker():
    while True:
        try:
            sleep(20)
            checker('https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&only_with_salary=true&'
                    'order_by=publication_time&schedule=remote&from=cluster_schedule&showClusters=true',
                    'vacancy-serp-item', 'bloko-link', hh_quest)
        except IndexError and Exception:
            executive()


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except IndexError and Exception:
        bot.stop_polling()
        sleep(1)
        telepol()


if __name__ == '__main__':
    gain = []
    if docs.floater == 1:
        gain = [hh_checker, main_posting]
    elif docs.idMain == idMe:
        gain = [hh_checker, main_posting]
    for thread_element in gain:
        _thread.start_new_thread(thread_element, ())
    telepol()
