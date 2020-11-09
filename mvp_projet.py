# Projet Python Groupe 2TL1-8
# Maxime Lits, Francois Charlier, Matthew Everard

#[["A1","A2","A3","A4"],
# ["B1","B2","B3","B4"],
# ["C1","C2","C3","C4"],
# ["D1","D2","D3","D4"]];

import random

plateau = [["A1","A2","A3","A4"],
            ["B1","B2","B3","B4"],
            ["C1","C2","C3","C4"],
            ["D1","D2","D3","D4"]];

joueur1= {"carre":2,
           "rond":2,
           "triangle":2,
           "croix":2
           };

joueur2 = {"carre":2,
           "rond":2,
           "triangle":2,
           "croix":2
           };

########################################################################

def testVictoire(joueur):
    # test lignes
    for i in plateau:
        if len(i[0]) > 2 and len(i[1]) > 2 and len(i[2]) > 2 and len(i[3]) > 2:
            ligne = 0
            for a in range(len(i)): 
                for a1 in range(len(i)):
                    if a != a1:
                        if i[a] == i[a1]: 
                            ligne = 1
            if ligne == 0:
                print("Victoire, GG au " + joueur)
                return True

    # test colonnes
    new_plateau_colonne = [[],[],[],[]]
    for i in plateau:
        new_plateau_colonne[0].append(i[0])
        new_plateau_colonne[1].append(i[1])
        new_plateau_colonne[2].append(i[2])
        new_plateau_colonne[3].append(i[3])
    
    for i in new_plateau_colonne:
        if len(i[0]) > 2 and len(i[1]) > 2 and len(i[2]) > 2 and len(i[3]) > 2:
            ligne = 0
            for a in range(len(i)): 
                for a1 in range(len(i)):
                    if a != a1:
                        if i[a] == i[a1]: 
                            ligne = 1
            if ligne == 0:
                print("Victoire, GG au " + joueur)
                return True
                
    # test zones
    new_plateau_zone = [[],[],[],[]]
    demi_plateau1 = [plateau[0], plateau[1]]
    demi_plateau2 = [plateau[2], plateau[3]]
    
    for i in demi_plateau1:
        new_plateau_zone[0].append(i[0])
        new_plateau_zone[0].append(i[1])
        new_plateau_zone[1].append(i[2])
        new_plateau_zone[1].append(i[3])
    for i in demi_plateau2:
        new_plateau_zone[2].append(i[0])
        new_plateau_zone[2].append(i[1])
        new_plateau_zone[3].append(i[2])
        new_plateau_zone[3].append(i[3])
    
    for i in new_plateau_zone:
        if len(i[0]) > 2 and len(i[1]) > 2 and len(i[2]) > 2 and len(i[3]) > 2:
            ligne = 0
            for a in range(len(i)): 
                for a1 in range(len(i)):
                    if a != a1:
                        if i[a] == i[a1]: 
                            ligne = 1
            if ligne == 0:
                print("Victoire, GG au " + joueur)
                return True
                
def joueur1_play():
    print("Au tour du joueur 1")
    print('Vous avez {} "carre", {} "rond", {} "triangle", {} "croix" '.format(joueur1["carre"], joueur1["rond"], joueur1["triangle"], joueur1["croix"] ))
    print("Insérer comme ceci : nom_de_la_piece, ID_de_la_case")
    placement_str = input()
    placement_list = placement_str.split(", ")
    if len(placement_list) != 2:
        while True:
            placement_str = input()
            placement_list = placement_str.split(", ")
            if len(placement_list) == 2 and len(placement_list[1]) == 2:
                break
            else:
                print("Veuiller respecter cette syntaxe : nom_de_la_piece, ID_de_la_case")
                
    if len(placement_list) == 2:
        if len(placement_list[1]) == 2: # doit etre différent de carre, rond, triangle, croix
            while True:
                if placement_list[0] in joueur1 and joueur1[placement_list[0]] > 0 and (placement_list[1] in plateau[0] or placement_list[1] in plateau[1] or placement_list[1] in plateau[2] or placement_list[1] in plateau[3]):
                    joueur1[placement_list[0]] = joueur1[placement_list[0]] - 1
                    break;
                else:
                    print("Vous avez tapé un mauvais nom de piece, un emplacement déjà pris, un mauvais id de case ou vous n'avez plus de {}, veuillez les réinsérer :".format(placement_list[0]))
                    placement_str = input()
                    placement_list = placement_str.split(", ")
             
            for i in plateau:
                if placement_list[1] in i:
                    position = i.index(placement_list[1])
                    i[position] = placement_list[0]
            
            print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(plateau[0], plateau[1], plateau[2], plateau[3]))

        
def joueur2_play():
    print("Au tour du joueur 2")
    print('Vous avez {} "carre", {} "rond", {} "triangle", {} "croix" '.format(joueur2["carre"], joueur2["rond"], joueur2["triangle"], joueur2["croix"] ))
    print("Insérer comme ceci : nom_de_la_piece, ID_de_la_case")
    placement_str = input()
    placement_list = placement_str.split(", ")
    if len(placement_list) != 2:
        while True:
            placement_str = input()
            placement_list = placement_str.split(", ")
            if len(placement_list) == 2 and len(placement_list[1]) == 2:
                break
            else:
                print("Veuiller respecter cette syntaxe : nom_de_la_piece, ID_de_la_case")
                
    if len(placement_list[1]) == 2: # doit etre différent de carre, rond, triangle, croix
        while True:
            if placement_list[0] in joueur2 and joueur2[placement_list[0]] > 0 and (placement_list[1] in plateau[0] or placement_list[1] in plateau[1] or placement_list[1] in plateau[2] or placement_list[1] in plateau[3]):
                joueur2[placement_list[0]] = joueur2[placement_list[0]] - 1
                break
            else:
                print("Vous avez tapé un mauvais nom de piece, un emplacement déjà pris, un mauvais id de case ou vous n'avez plus de {}, veuillez les réinsérer :".format(placement_list[0]))
                placement_str = input()
                placement_list = placement_str.split(", ")
         
        for i in plateau:
            if placement_list[1] in i:
                position = i.index(placement_list[1])
                i[position] = placement_list[0]
        
        print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(plateau[0], plateau[1], plateau[2], plateau[3]))
    
    
        
def deroulement(rand):
    if rand == 0:
        while True:
            joueur1_play()
            if testVictoire("joueur 1"):
                break;
            joueur2_play()
            if testVictoire("joueur 2"):
                break;
    if rand == 1:
        while True:
            joueur2_play()
            if testVictoire("joueur 2"):
                break;
            joueur1_play()
            if testVictoire("joueur 1"):
                break;

def debutPartie(): 
    print("Voici le plateau : \n{}\n{}\n{}\n{}\n".format(plateau[0], plateau[1], plateau[2], plateau[3]))
    rand = int(random.uniform(0, 2))
    
    if rand == 0:
        deroulement(rand)
    else:
        deroulement(rand)
###########################################################################
    
debutPartie()


