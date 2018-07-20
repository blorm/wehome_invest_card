#coding: utf-8
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import re
import datetime

CIRCLE_NUMBER = u'0①②③④⑤⑥⑦⑧⑨⑩⑪⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
LINE_COLOR = (74, 74, 74)
FONT = ImageFont.truetype('PingFang.ttc', 24, index=2)

card = Image.open('invest_card_template.jpg')
draw = ImageDraw.Draw(card)

date_font = ImageFont.truetype('PingFang.ttc', 20, index=6)
date = str(datetime.date.today() + datetime.timedelta(days=1)).replace('-', '.')
draw.text((590, 80), date, (187, 187, 187), date_font)

LINE_SPACING = 50
# text = ''
# input_text = '0'
# while input_text:
#   input_text = raw_input()
#   print [input_text]
#   text += input_text + '\n'

info_no = 1
line_count = 0
word_file = open('word.txt', 'r')

text = word_file.readline().strip()
while text:
  text = unicode(text, 'UTF-8')
  
  if len(text) > 2 and re.findall('\w\.', text):
    text = CIRCLE_NUMBER[info_no] + text[2:]
  first_line = 1
  while text:
    x = 92 - 30 * first_line
    y = 176 + LINE_SPACING * line_count
    display_length = 25 + 2 * first_line
    print text[:10], draw.textsize(text[:display_length], FONT)
    while draw.textsize(text[:display_length], FONT)[0] < 590 and display_length < len(text) and text[display_length] in u'，。.%%；0123456789':
      display_length += 1                                             # Todo: 优化末尾长度 数字等
    print text[:10], draw.textsize(text[:display_length], FONT)
    draw.text((x, y), text[:display_length], LINE_COLOR, FONT)
    text = text[display_length:]
    first_line = 0 if first_line else 0
    line_count += 1
  text = word_file.readline().strip()
  info_no += 1

head_height = 176
body_height = LINE_SPACING * line_count
tail_height = 230
tail = card.crop((0, 1500 - tail_height, 750, 1500))
card.paste(tail, (0, head_height + body_height, 750, head_height + body_height + tail_height))
card = card.crop((0, 0, 750, head_height + body_height + tail_height))

card.show()
card.save(date + '.jpg')