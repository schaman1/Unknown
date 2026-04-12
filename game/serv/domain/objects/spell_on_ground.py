from serv.domain.objects.interactable_object import interactable_object

class spell_on_ground(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price)