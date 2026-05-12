from client.ui.objects.interactable_element import interactable
from client.config import assets,size_display as size

class spell_on_ground(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path(id_img)

    def found_path(self,id_img):

        self.size_img = (size.CELL_SIZE*size.SIZE_SPELL_GROUND,size.CELL_SIZE*size.SIZE_SPELL_GROUND)
        self.delta_size_bg = size.DELTA_SIZE_BG_SPELL*size.CELL_SIZE
        self.init_img(assets.SPELLS[id_img],assets.ICONE_SPELL)

class healer_spawn(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path()

    def found_path(self):

        self.size_img = (size.CELL_SIZE*8,size.CELL_SIZE*16)
        self.init_img(assets.HEALER,None,assets.HEALER_TRIGGER,0.1)

class upgrade_weapon(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path()

    def found_path(self):

        self.size_img = (size.CELL_SIZE*size.SIZE_SPELL_GROUND,size.CELL_SIZE*size.SIZE_SPELL_GROUND)
        self.delta_size_bg = size.DELTA_SIZE_BG_SPELL*size.CELL_SIZE
        self.init_img(assets.ADD_SLOT_WEAPON,assets.ICONE_AUGMENT_WEAPON)