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

        self.found_path(id_img)

    def found_path(self,id_img):

        if id_img == 1 :

            self.size_img = (size.CELL_SIZE*size.SIZE_SPELL_GROUND,size.CELL_SIZE*size.SIZE_SPELL_GROUND)
            self.delta_size_bg = size.DELTA_SIZE_BG_SPELL*size.CELL_SIZE
            self.init_img(assets.ADD_SLOT_WEAPON,assets.ICONE_AUGMENT_WEAPON)

        elif id_img == 2 :

            self.size_img = (size.CELL_SIZE*size.SIZE_SPELL_GROUND,size.CELL_SIZE*size.SIZE_SPELL_GROUND)
            self.delta_size_bg = size.DELTA_SIZE_BG_SPELL*size.CELL_SIZE
            self.init_img(assets.ADD_2_SLOT_WEAPON,assets.ICONE_AUGMENT_WEAPON)

        else :
            print("Issue in client/ui/objects/object_type, id_img unknown for upgrade weapon : ",id_img)

class upgrade_life(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path()

    def found_path(self):

        self.size_img = (size.CELL_SIZE*size.SIZE_SPELL_GROUND,size.CELL_SIZE*size.SIZE_SPELL_GROUND)
        self.delta_size_bg = size.DELTA_SIZE_BG_SPELL*size.CELL_SIZE
        self.init_img(assets.ADD_LIFE,assets.ICONE_AUGMENT_WEAPON)

class upgrade_time(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path()

    def found_path(self):

        self.size_img = (size.CELL_SIZE*size.SIZE_SPELL_GROUND,size.CELL_SIZE*size.SIZE_SPELL_GROUND)
        self.delta_size_bg = size.DELTA_SIZE_BG_SPELL*size.CELL_SIZE
        self.init_img(assets.REDUCE_TIME,assets.ICONE_AUGMENT_WEAPON)

class chest(interactable):

    def __init__(self,id_img,pos_x,pos_y,price = 0):

        super().__init__(pos_x,pos_y,price)

        self.found_path(id_img)

    def found_path(self,id_img):

        self.size_img = (size.CELL_SIZE*size.CHEST_SIZE_WITH,size.CELL_SIZE*size.CHEST_SIZE_HEIGHT)

        if id_img == 1:
            self.init_img(assets.CHEST_SPELL_CLOSE)
            self.init_use_img(assets.CHEST_SPELL_OPEN)
        
        elif id_img==2:
            self.init_img(assets.CHEST_UPGRADE_CLOSE)
            self.init_use_img(assets.CHEST_UPGRADE_OPEN)

        elif id_img==3:
            self.init_img(assets.CHEST_SPELL_RARE_CLOSE)
            self.init_use_img(assets.CHEST_SPELL_RARE_OPEN)

        elif id_img == 4:
            self.init_img(assets.CHEST_SPELL_LEGENDARY_CLOSE)
            self.init_use_img(assets.CHEST_SPELL_LEGENDARY_OPEN)
        else :
            print("Unknown chest id in client/ui/object_type",id_img)