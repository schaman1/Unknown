

class interactable_object:

    def __init__(self,id_categorie,pos_x,pos_y,price,unique_use = True):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.price = price
        self.id_cat = id_categorie
        self.unique_use = unique_use
