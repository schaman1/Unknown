from serv.domain.weapon.upgrades import UPGRADES

OBJECTS_ADDING = []
add = 500
i = 0

for id,el in UPGRADES.items():

    OBJECTS_ADDING.append(("SPELL",id,30000+i*add,26100,0))

    i+=1

for i in range(5):
    OBJECTS_ADDING.append(("UpgradeWeapon",2,30000+i*add,25100,0)) #21 bcs +2 slot for weapon

WEAPONS_ADDING = [[2,3,4,5,6],[],[32],[41]]