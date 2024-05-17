# from _config import *
import os
from PIL import Image, ImageDraw, ImageFont
import random

from cardmaker.DrawImage import DrawImage
from cardmaker.DrawArtwork import DrawArtwork
from cardmaker.DrawAttribute import DrawAttribute
from cardmaker.DrawLevel import DrawLevel
import textwrap

import base64
from io import BytesIO

serial_id = random.randint(000000000, 999999999)


class CardConstructor:

   config = None
   card_img = None
   card_img_draw = None

   def __init__(self, json_card) -> None:
      self.loadConfig()

      if isinstance(json_card, dict):
         self.json_card = json_card
      
      self.getSources()
   
   def loadConfig(self):
      self.config = {
         'source_path': os.path.dirname(__file__)+"/img/",
         'path_cards': "cards/",
         'path_img':   "cardimages/",
         'path_attr':   "type/",
         'path_level': "lvl/",
         'i': 0,
         'areas': {
            'card_area': (0,0),
            'img_area':  (51,113),
            'attr_area': (355,29),
            'level_area': (380,76),
            'level_x': 380,
            'level_y': 76,
         },
         'text': {
            'title_xy': (30,28),
            'title_width': 320,
            'atk_xy': (265,557),
            'def_xy': (350,557),
            'type_xy': (35,460),
            'desc_xy': (35,480),
            'desc_width': 350,
            'fontsize48': 48,
            'fontsize38': 38,
            'fontsize30': 30,
            'fontsize23': 23,
            'fontsize15': 15,
            'fontsize12': 14,
            'fudge_y_small_title': 5,
            'fudge_y_xsmall_title': 8,
            'titleFont': os.path.dirname(__file__)+'/fonts/Yu-Gi-Oh! Matrix Regular Small Caps 2.ttf',
            'AttrFont': os.path.dirname(__file__)+"/fonts/Yu-Gi-Oh! ITC Stone Serif Small Caps Bold.ttf",
            'DescFont': os.path.dirname(__file__)+'/fonts/Yu-Gi-Oh! Matrix Book.ttf',
            'title_color': 'black',
            'title_color_xyz': 'white',
            'text_alignment': 'left'
         }
      }

   def getSources(self):
      self.source_card_path      = self.config['source_path'] + self.config['path_cards'] +'Card-' + self.json_card['card'].lower().replace(' ', '-') + '.png'
      self.attribute_path        = self.config['source_path'] + self.config['path_attr'] + self.json_card['attribute'] + '.png'
      self.level_path            = self.config['source_path'] + self.config['path_level'] + 'Level-Red.png'

      self.image                 = DrawImage(self.json_card['card'], self.config['areas']['card_area'], self.source_card_path).getimage()
      self.source_card1          = DrawImage(self.json_card['card'], self.config['areas']['card_area'], self.source_card_path).getSourceCard()

      self.artwork               = DrawArtwork(self.config['areas']['img_area'], self.json_card['image_card']).getArtwork()
      
      self.attribute             = DrawAttribute(self.json_card['attribute'], self.config['areas']['attr_area'], self.attribute_path).getAttribute()

      self.level                 = DrawLevel(self.json_card['Level'], self.config['areas']['level_area'], self.level_path).getLevel()

   def setLevel(self):
      for self.config['i'] in range(self.json_card['Level']):
        self.config['areas']['level_x'] = self.config['areas']['level_x'] - 27
        self.area = self.config['areas']['level_x'], self.config['areas']['level_y']
        self.source_card1.paste(self.level, self.area)

   def pasteImages(self):
      self.draw                  = ImageDraw.Draw(self.source_card1) 

      self.source_card1.paste(self.artwork, self.config['areas']['img_area'])
      self.source_card1.paste(self.attribute, self.config['areas']['attr_area']) 

   def linkArrows(self):
      pass

   def writeText(self):
      TitleFont                  = ImageFont.truetype(self.config['text']['titleFont'], self.config['text']['fontsize48'])
      TitleFontSmall                  = ImageFont.truetype(self.config['text']['titleFont'], self.config['text']['fontsize38'])
      TitleFontVerySmall                  = ImageFont.truetype(self.config['text']['titleFont'], self.config['text']['fontsize30'])
      ATKDEFFont                 = ImageFont.truetype(self.config['text']['titleFont'], self.config['text']['fontsize23'])
      AttrFont                   = ImageFont.truetype(self.config['text']['AttrFont'], self.config['text']['fontsize15'])
      DescFont                   = ImageFont.truetype(self.config['text']['DescFont'], self.config['text']['fontsize12'])
      
      title_color = self.config['text']['title_color_xyz'] if self.json_card['card'] == "XYZ" else self.config['text']['title_color']
      
      selected_title_font = TitleFont
      fudge = 0
      if not self.will_text_fit(self.json_card['Title'], self.config['text']['title_width'], selected_title_font):
         selected_title_font = TitleFontSmall
         fudge = self.config['text']['fudge_y_small_title']
         if not self.will_text_fit(self.json_card['Title'], self.config['text']['title_width'], selected_title_font):
            selected_title_font = TitleFontVerySmall
            fudge = self.config['text']['fudge_y_xsmall_title']
      title_xy = (self.config['text']['title_xy'][0], self.config['text']['title_xy'][1] + fudge)

      self.draw.text(title_xy, self.json_card['Title'], font=selected_title_font, fill=title_color, align=self.config['text']['text_alignment']) 

      self.draw.text((self.config['text']['atk_xy']), self.json_card['Atk'], font=ATKDEFFont, fill=self.config['text']['title_color'], align=self.config['text']['text_alignment'])
      self.draw.text((self.config['text']['def_xy']), self.json_card['Def'], font=ATKDEFFont, fill=self.config['text']['title_color'], align=self.config['text']['text_alignment'])
      self.draw.text((self.config['text']['type_xy']), "[" + self.json_card['Type'] + "]", font=AttrFont, fill=self.config['text']['title_color'], align=self.config['text']['text_alignment'])

      wrapped_desc = self.wrap_text(self.json_card['Descripton'], self.config['text']['desc_width'], DescFont)
      self.draw.text((self.config['text']['desc_xy']),  wrapped_desc, font=DescFont, fill=self.config['text']['title_color'], align=self.config['text']['text_alignment'])

   def wrap_text(self, text: str, width: int, font: ImageFont):
      text_lines = []
      text_line = []
      text = text.replace('\n', ' [br] ')
      words = text.split()

      for word in words:
         if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
         text_line.append(word)
         left, top, right, bottom = font.getbbox(' '.join(text_line))
         w = right-left
         if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

      if len(text_line) > 0:
         text_lines.append(' '.join(text_line))

      return "\n".join(text_lines)

   def will_text_fit(self, text: str, width: int, font: ImageFont):
      left, top, right, bottom = font.getbbox(text)
      w = right-left
      if w < width: 
         return True
      return False


   def outputCard(self):
      out = Image.alpha_composite(self.image,self.source_card1)
      # out.save("output/save.png")

      buffered = BytesIO()
      out.save(buffered, format="PNG")
      return (buffered.getvalue())

   def generateCard(self):
      self.getSources()
      self.pasteImages()
      self.writeText()
      self.setLevel()
      return self.outputCard()


