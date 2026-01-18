import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_FONCE = (50, 50, 50)

# Couleurs du drapeau du Senegal (ma voiture)
VERT_SENEGAL = (0, 155, 72)
JAUNE_SENEGAL = (252, 209, 22)
ROUGE_SENEGAL = (206, 17, 38)

# Couleurs du drapeau du Maroc (obstacles)
ROUGE_MAROC = (193, 39, 45)
VERT_MAROC = (0, 98, 51)

# Creation de la fenetre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption(" Senegal vs Maroc  - Finale!")
horloge = pygame.time.Clock()

# Classe pour la voiture du Senegal (joueur)
class VoitureSenegal:
    def __init__(self):
        self.largeur = 50
        self.hauteur = 90
        self.x = LARGEUR // 2 - self.largeur // 2
        self.y = HAUTEUR - 120
        self.vitesse = 7
        
    def dessiner(self):
        # Voiture aux couleurs du Senegal (vert, jaune, rouge en bandes verticales)
        # Bande verte (gauche)
        pygame.draw.rect(ecran, VERT_SENEGAL, (self.x, self.y, 17, self.hauteur))
        # Bande jaune (milieu)
        pygame.draw.rect(ecran, JAUNE_SENEGAL, (self.x + 17, self.y, 16, self.hauteur))
        # Bande rouge (droite)
        pygame.draw.rect(ecran, ROUGE_SENEGAL, (self.x + 33, self.y, 17, self.hauteur))
        
        # Toit de la voiture
        pygame.draw.rect(ecran, VERT_SENEGAL, (self.x + 5, self.y - 20, self.largeur - 10, 25))
        
        # Fenetres
        pygame.draw.rect(ecran, (100, 150, 255), (self.x + 10, self.y - 15, 12, 15))
        pygame.draw.rect(ecran, (100, 150, 255), (self.x + 28, self.y - 15, 12, 15))
        
        # Roues noires
        pygame.draw.circle(ecran, NOIR, (self.x + 10, self.y + 15), 8)
        pygame.draw.circle(ecran, NOIR, (self.x + 40, self.y + 15), 8)
        pygame.draw.circle(ecran, NOIR, (self.x + 10, self.y + 70), 8)
        pygame.draw.circle(ecran, NOIR, (self.x + 40, self.y + 70), 8)
        
        # Etoile du Senegal au centre
        self.dessiner_etoile(self.x + 25, self.y + 45, 8, VERT_SENEGAL)
        
    def dessiner_etoile(self, x, y, taille, couleur):
        # Dessine une petite etoile à 5 branches
        points = []
        for i in range(5):
            angle = i * 144 - 90
            px = x + taille * pygame.math.Vector2(1, 0).rotate(angle).x
            py = y + taille * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((px, py))
        pygame.draw.polygon(ecran, couleur, points)
        
    def deplacer(self, direction):
        if direction == "GAUCHE" and self.x > 50:
            self.x -= self.vitesse
        elif direction == "DROITE" and self.x < LARGEUR - self.largeur - 50:
            self.x += self.vitesse

# Classe pour les voitures du Maroc (obstacles)
class VoitureMaroc:
    def __init__(self):
        self.largeur = 50
        self.hauteur = 90
        self.x = random.choice([100, 250, 400, 550])
        self.y = -100
        self.vitesse = 5
        
    def dessiner(self):
        # Voiture rouge du Maroc
        pygame.draw.rect(ecran, ROUGE_MAROC, (self.x, self.y, self.largeur, self.hauteur))
        
        # Toit
        pygame.draw.rect(ecran, ROUGE_MAROC, (self.x + 5, self.y + self.hauteur, self.largeur - 10, 20))
        
        # Etoile verte du Maroc au centre
        self.dessiner_etoile(self.x + 25, self.y + 45, 12, VERT_MAROC)
        
        # Roues
        pygame.draw.circle(ecran, NOIR, (self.x + 10, self.y + 20), 8)
        pygame.draw.circle(ecran, NOIR, (self.x + 40, self.y + 20), 8)
        pygame.draw.circle(ecran, NOIR, (self.x + 10, self.y + 70), 8)
        pygame.draw.circle(ecran, NOIR, (self.x + 40, self.y + 70), 8)
    
    def dessiner_etoile(self, x, y, taille, couleur):
        # Dessine une etoile à 5 branches
        points = []
        for i in range(5):
            angle = i * 144 - 90
            px = x + taille * pygame.math.Vector2(1, 0).rotate(angle).x
            py = y + taille * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((px, py))
        pygame.draw.polygon(ecran, couleur, points)
        
    def deplacer(self):
        self.y += self.vitesse
        
    def hors_ecran(self):
        return self.y > HAUTEUR

# Fonction pour dessiner la route
def dessiner_route(offset):
    # Fond vert (pelouse de stade)
    ecran.fill((34, 139, 34))
    
    # Route grise
    pygame.draw.rect(ecran, GRIS_FONCE, (50, 0, LARGEUR - 100, HAUTEUR))
    
    # Lignes blanches au centre
    for i in range(-1, 15):
        y = (i * 80 + offset) % HAUTEUR
        pygame.draw.rect(ecran, BLANC, (LARGEUR // 2 - 5, y, 10, 50))
    
    # Bordures de route
    pygame.draw.rect(ecran, BLANC, (50, 0, 10, HAUTEUR))
    pygame.draw.rect(ecran, BLANC, (LARGEUR - 60, 0, 10, HAUTEUR))

# Fonction pour verifier les collisions
def collision(voiture_senegal, voiture_maroc):
    if (voiture_senegal.x < voiture_maroc.x + voiture_maroc.largeur and
        voiture_senegal.x + voiture_senegal.largeur > voiture_maroc.x and
        voiture_senegal.y < voiture_maroc.y + voiture_maroc.hauteur and
        voiture_senegal.y + voiture_senegal.hauteur > voiture_maroc.y):
        return True
    return False

# Fonction principale du jeu
def jeu():
    voiture_senegal = VoitureSenegal()
    voitures_maroc = []
    score = 0
    offset_route = 0
    compteur_obstacle = 0
    
    en_cours = True
    while en_cours:
        horloge.tick(FPS)
        
        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Controles
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            voiture_senegal.deplacer("GAUCHE")
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            voiture_senegal.deplacer("DROITE")
        
        # Animation de la route
        offset_route += 5
        if offset_route >= 80:
            offset_route = 0
        
        # Creation des voitures marocaines
        compteur_obstacle += 1
        if compteur_obstacle > 60:
            voitures_maroc.append(VoitureMaroc())
            compteur_obstacle = 0
        
        # Déplacement des voitures marocaines
        for voiture in voitures_maroc[:]:
            voiture.deplacer()
            if voiture.hors_ecran():
                voitures_maroc.remove(voiture)
                score += 1
            if collision(voiture_senegal, voiture):
                en_cours = False
        
        # Augmentation de la difficulte
        if score > 0 and score % 10 == 0:
            for voiture in voitures_maroc:
                voiture.vitesse = 5 + score // 10
        
        # Dessin
        dessiner_route(offset_route)
        voiture_senegal.dessiner()
        for voiture in voitures_maroc:
            voiture.dessiner()
        
        # Affichage du score
        font = pygame.font.Font(None, 48)
        texte_score = font.render(f"🇸🇳 Score: {score}", True, BLANC)
        ecran.blit(texte_score, (10, 10))
        
        # Message d'encouragement
        font_petit = pygame.font.Font(None, 32)
        texte_encouragement = font_petit.render("Evitez les voitures marocaines!", True, JAUNE_SENEGAL)
        ecran.blit(texte_encouragement, (LARGEUR // 2 - 180, HAUTEUR - 30))
        
        pygame.display.flip()
    
    # Ecran de fin
    ecran_fin(score)

# Ecran de fin de jeu
def ecran_fin(score):
    ecran.fill(NOIR)
    font_grand = pygame.font.Font(None, 72)
    font_moyen = pygame.font.Font(None, 48)
    
    if score >= 20:
        texte_fin = font_grand.render("VICTOIRE SENEGAL!", True, VERT_SENEGAL)
    else:
        texte_fin = font_grand.render("GAME OVER!", True, ROUGE_MAROC)
    
    texte_score = font_moyen.render(f"Score Final: {score}", True, BLANC)
    texte_rejouer = font_moyen.render("Appuyez sur ESPACE pour rejouer", True, JAUNE_SENEGAL)
    
    ecran.blit(texte_fin, (LARGEUR // 2 - texte_fin.get_width() // 2, 150))
    ecran.blit(texte_score, (LARGEUR // 2 - texte_score.get_width() // 2, 250))
    ecran.blit(texte_rejouer, (LARGEUR // 2 - texte_rejouer.get_width() // 2, 350))
    
    pygame.display.flip()
    
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jeu()

# Lancement du jeu
if __name__ == "__main__":
    jeu()