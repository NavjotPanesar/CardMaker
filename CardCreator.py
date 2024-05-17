import base64
from io import BytesIO
import json
from PIL import Image

from cardmaker.CardConstructor import CardConstructor

input_data = {
  "card": "synchro",
  "Title": "Swords of LightLigheeets",
  "attribute": "Dark",
  "Level": 9,
  "Type": "Curse/Removal",
  "Descripton": "When John wins an Aram, proving for once and for all aaaaaaaaaaaaaaaaaa that he is not the curse.",
  "Atk": "",
  "Def": ""
}

img_from_db_example = None
with open("./cardmaker/img/cards/Card-trap.png", "rb") as image:
  img_from_db_example = base64.b64encode(image.read())

input_data["image_card"] = Image.open(BytesIO(base64.b64decode(img_from_db_example)))

card1 = CardConstructor(input_data)

f = open("./output.png", "wb")
f.write((card1.generateCard()))
f.close