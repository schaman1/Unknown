from serv.domain.weapon.upgrades import UPGRADES

OBJECTS_ADDING = []
add = 500
i = 0

for id,el in UPGRADES.items():

    OBJECTS_ADDING.append(("SPELL",id,30000+i*add,26100,0))

    i+=1