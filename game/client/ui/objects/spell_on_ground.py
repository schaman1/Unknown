from client.ui.objects.interactable_element import interactable
from client.config import assets,size_display as size

class spell_on_ground(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path(id_img)

    def found_path(self,id_img):

        self.size_img = (size.CELL_SIZE*4,size.CELL_SIZE*4)
        self.init_img(assets.SPELLS[id_img])