from PIL import Image

class DrawArtwork():
   def __init__(self, artarea, art_image) -> None:
      self.artarea = artarea
      self.art_image = art_image
      self.art_image1 = self.art_image.resize((320,320),Image.Resampling.LANCZOS)

   def getArtwork(self):
      return self.art_image1