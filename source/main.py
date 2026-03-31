"""
OVERGROWTH: The Beginning of a New Era
Jeu d'horreur psychologique en Pygame
Style: Body Horror / Vision Nocturne / Esthétique TV Grainée
"""

import pygame  #si ne marche pas pip install pygame==2.1.3
import sys
import random
import math
import time
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# INITIALISATION

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

LARGEUR, HAUTEUR = 1024, 768
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("OVERGROWTH: The Beginning of a New Era")
horloge = pygame.time.Clock()


# PALETTE DE COULEURS (Vision nocturne / Body Horror)

NOIR          = (0, 0, 0)
VERT_NUIT     = (10, 30, 10)
VERT_SOMBRE   = (20, 50, 20)
VERT_MOYEN    = (40, 100, 40)
VERT_CLAIR    = (80, 160, 80)
VERT_VIF      = (100, 220, 100)
GRIS_SOMBRE   = (30, 35, 30)
GRIS_MOYEN    = (70, 80, 70)
GRIS_CLAIR    = (140, 150, 140)
BLANC_VERDATRE= (200, 220, 200)
ROUGE_PUCE    = (220, 30, 30)
ROUGE_SANG    = (150, 10, 10)
ORANGE_ALERTE = (200, 100, 0)
BLEU_ELECTRIQUE=(40, 80, 220)
TRANSPARENT   = (0, 0, 0, 0)


# POLICES

try:
    POLICE_MONO   = pygame.font.SysFont("Courier New", 18)
    POLICE_MONO_L = pygame.font.SysFont("Courier New", 28)
    POLICE_MONO_XL= pygame.font.SysFont("Courier New", 42)
    POLICE_TITRE  = pygame.font.SysFont("Courier New", 22, bold=True)
except:
    POLICE_MONO   = pygame.font.Font(None, 20)
    POLICE_MONO_L = pygame.font.Font(None, 30)
    POLICE_MONO_XL= pygame.font.Font(None, 45)
    POLICE_TITRE  = pygame.font.Font(None, 24)


# CHARGEMENT DES IMAGES (portraits personnages)


def charger_image_perso(nom_fichier, taille=(190, 260), filtre_nocturne=True):
    """
    Charge une image de personnage et applique le filtre vision nocturne.
    Cherche le fichier dans le même dossier que overgrowth.py ou dans assets/.
    Retourne None si introuvable — le portrait en code sera utilisé à la place.
    """
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemins = [
        os.path.join(dossier_script, nom_fichier),
        os.path.join(dossier_script, "assets", nom_fichier),
    ]
    chemin = next((c for c in chemins if os.path.exists(c)), None)
    if not chemin:
        print(f"[IMAGE] Introuvable : {nom_fichier} — portrait procédural utilisé.")
        return None
    try:
        surf = pygame.image.load(chemin).convert_alpha()
        surf = pygame.transform.smoothscale(surf, taille)
        if filtre_nocturne:
            surf = appliquer_filtre_nocturne(surf)
        print(f"[IMAGE] Chargée : {nom_fichier}")
        return surf
    except Exception as e:
        print(f"[IMAGE] Erreur {nom_fichier} : {e}")
        return None

def appliquer_filtre_nocturne(surface):
    """
    Filtre vision nocturne : désaturation + teinte vert sombre.
    Utilise numpy si disponible, sinon fallback simple.
    """
    try:
        import numpy as np
        resultat = surface.copy()
        arr = pygame.surfarray.pixels3d(resultat)
        lum = 0.299 * arr[:,:,0].astype(float) + \
              0.587 * arr[:,:,1].astype(float) + \
              0.114 * arr[:,:,2].astype(float)
        arr[:,:,0] = np.clip(lum * 0.22, 0, 255).astype(np.uint8)
        arr[:,:,1] = np.clip(lum * 0.82, 0, 255).astype(np.uint8)
        arr[:,:,2] = np.clip(lum * 0.28, 0, 255).astype(np.uint8)
        del arr
        return resultat
    except ImportError:
        # Sans numpy : teinte verte simple
        teinte = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        teinte.fill((0, 30, 0, 70))
        surface.blit(teinte, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return surface

# ── Chargement au démarrage ──
# Place tes fichiers images dans le même dossier que overgrowth.py
IMAGES_PERSOS = {}
IMAGES_PERSOS[2] = charger_image_perso("gouv-character.overgrowth.webp")  # Agent SURSUM
IMAGES_PERSOS[5] = charger_image_perso("vieux_qui_fume.png")              # Le Fumeur (vieux barbu)
IMAGES_PERSOS[7] = charger_image_perso("langue_trouer.png")               # Perso 7 — bouche/langue hybride
IMAGES_PERSOS[1] = charger_image_perso("insomniaque_1.png")      # L'Insomniaque
IMAGES_PERSOS[3] = charger_image_perso("vielle_chat_pixel.png")      # Mère & Enfant
IMAGES_PERSOS[4] = charger_image_perso("sdf-pixel.png")              # Le SDF
IMAGES_PERSOS[8] = charger_image_perso("hybride_grand.png")     # L'Ordinaire (hybride puce)
IMAGES_PERSOS[9] = charger_image_perso("hybride_femme.png")  # L'Enraciné (hybride racines)


# GÉNÉRATION SONORE (synthèse — pas de fichiers externes)


def generer_son_statique(duree_ms=500):
    """Bruit blanc pour l'effet TV statique."""
    freq_ech = 44100
    nb_samples = int(freq_ech * duree_ms / 1000)
    buf = bytearray()
    for _ in range(nb_samples):
        val = random.randint(-3000, 3000)
        buf += val.to_bytes(2, byteorder='little', signed=True)
        buf += val.to_bytes(2, byteorder='little', signed=True)
    son = pygame.mixer.Sound(buffer=bytes(buf))
    son.set_volume(0.15)
    return son

def generer_bourdonnement(freq=60, duree_ms=3000, volume=0.08):
    """Bourdonnement grave et inquiétant pour l'ambiance."""
    freq_ech = 44100
    nb_samples = int(freq_ech * duree_ms / 1000)
    buf = bytearray()
    for i in range(nb_samples):
        t = i / freq_ech
        # Superposition de plusieurs fréquences graves
        val = (
            math.sin(2 * math.pi * freq * t) * 8000 +
            math.sin(2 * math.pi * freq * 1.5 * t) * 3000 +
            math.sin(2 * math.pi * freq * 0.5 * t) * 5000 +
            random.randint(-500, 500)  # grain
        )
        val = max(-32767, min(32767, int(val)))
        buf += val.to_bytes(2, byteorder='little', signed=True)
        buf += val.to_bytes(2, byteorder='little', signed=True)
    son = pygame.mixer.Sound(buffer=bytes(buf))
    son.set_volume(volume)
    return son

def generer_battement_coeur(bpm=90, duree_ms=2000):
    """Battement de cœur pour la tension nocturne."""
    freq_ech = 44100
    nb_samples = int(freq_ech * duree_ms / 1000)
    buf = bytearray()
    intervalle = int(freq_ech * 60 / bpm)
    for i in range(nb_samples):
        pos = i % intervalle
        # Deux pics par battement (LUB-DUB)
        val = 0
        if pos < 800:
            val = int(math.sin(math.pi * pos / 800) * 25000)
        elif pos < 1600 and pos > 900:
            val = int(math.sin(math.pi * (pos-900) / 700) * 15000)
        val = max(-32767, min(32767, val))
        buf += val.to_bytes(2, byteorder='little', signed=True)
        buf += val.to_bytes(2, byteorder='little', signed=True)
    son = pygame.mixer.Sound(buffer=bytes(buf))
    son.set_volume(0.4)
    return son

def generer_cri_glitch(duree_ms=1500):
    """Cri strident glitché pour le jumpscare du Traqueur."""
    freq_ech = 44100
    nb_samples = int(freq_ech * duree_ms / 1000)
    buf = bytearray()
    for i in range(nb_samples):
        t = i / freq_ech
        progression = i / nb_samples
        freq_inst = 200 + random.randint(-50,50) + progression * 800
        val = (
            math.sin(2 * math.pi * freq_inst * t) * 20000 * (1 - progression) +
            random.randint(-10000, 10000)
        )
        val = max(-32767, min(32767, int(val)))
        buf += val.to_bytes(2, byteorder='little', signed=True)
        buf += val.to_bytes(2, byteorder='little', signed=True)
    son = pygame.mixer.Sound(buffer=bytes(buf))
    son.set_volume(0.9)
    return son


# PRÉ-CHARGEMENT DES SONS

print("Génération audio...")
SON_STATIQUE     = generer_son_statique(300)
SON_AMBIANCE     = generer_bourdonnement(55, 4000, 0.07)
SON_COEUR        = generer_battement_coeur(80, 2000)
SON_COEUR_RAPIDE = generer_battement_coeur(130, 1500)
SON_JUMPSCARE    = generer_cri_glitch(2000)
print("Audio prêt.")


# EFFETS VISUELS


def dessiner_scanlines(surface, alpha=60):
    """Filtre scanlines horizontales semi-transparentes."""
    scanline = pygame.Surface((LARGEUR, 2), pygame.SRCALPHA)
    scanline.fill((0, 0, 0, alpha))
    for y in range(0, HAUTEUR, 4):
        surface.blit(scanline, (0, y))

def dessiner_grain(surface, intensite=25):
    """Grain cinématographique — pixels aléatoires."""
    for _ in range(intensite * 30):
        x = random.randint(0, LARGEUR - 1)
        y = random.randint(0, HAUTEUR - 1)
        lum = random.randint(0, intensite)
        couleur = (lum, lum + random.randint(0,5), lum)
        surface.set_at((x, y), couleur)

def dessiner_vignette(surface):
    """Assombrissement des bords de l'écran (vignette)."""
    vignette = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
    cx, cy = LARGEUR // 2, HAUTEUR // 2
    for rayon in range(min(cx, cy), 0, -2):
        alpha = max(0, int(180 * (1 - rayon / min(cx, cy)) ** 1.5))
        couleur = (0, 0, 0, alpha)
        pygame.draw.ellipse(vignette, couleur,
                            (cx - rayon, cy - rayon * HAUTEUR // LARGEUR,
                             rayon * 2, rayon * 2 * HAUTEUR // LARGEUR), 2)
    surface.blit(vignette, (0, 0))

def effet_glitch(surface, intensite=5):
    """Décalage horizontal aléatoire de bandes de pixels (glitch)."""
    for _ in range(intensite):
        y = random.randint(0, HAUTEUR - 10)
        h = random.randint(2, 8)
        decalage = random.randint(-20, 20)
        bande = surface.subsurface((0, y, LARGEUR, h)).copy()
        surface.blit(bande, (decalage, y))

def dessiner_puce_rouge(surface, x, y, taille=8, pulse=0):
    """Dessine une puce rouge brillante (signature des hybrides)."""
    # Halo lumineux
    halo_alpha = 100 + int(50 * math.sin(pulse))
    halo = pygame.Surface((taille * 6, taille * 6), pygame.SRCALPHA)
    pygame.draw.ellipse(halo, (220, 30, 30, halo_alpha),
                        (0, 0, taille * 6, taille * 6))
    surface.blit(halo, (x - taille * 3, y - taille * 3))
    # Corps de la puce
    pygame.draw.rect(surface, ROUGE_PUCE, (x - taille//2, y - taille//4, taille, taille//2))
    # Petites pattes
    for i in range(3):
        px = x - taille//2 + i * (taille // 3)
        pygame.draw.line(surface, ROUGE_SANG, (px, y - taille//4), (px, y - taille//2), 1)
        pygame.draw.line(surface, ROUGE_SANG, (px, y + taille//4), (px, y + taille//2), 1)


# CLASSE PERSONNAGE


class Personnage:
    """
    Classe de base pour tous les personnages du jeu.
    Chaque personnage a des indices visuels, des dialogues,
    un type (humain/hybride) et une liste de signes suspects.
    """
    def __init__(self, id, nom, est_hybride, dialogues,
                 signes_visibles, signes_caches=None,
                 description_apparence="", couleur_portrait=None,
                 special=None):
        self.id                 = id
        self.nom                = nom
        self.est_hybride        = est_hybride
        self.dialogues          = dialogues          # Liste de strings
        self.signes_visibles    = signes_visibles    # Signes visibles d'emblée
        self.signes_caches      = signes_caches or []# Signes révélés par Scanner
        self.description        = description_apparence
        self.couleur_portrait   = couleur_portrait or GRIS_MOYEN
        self.special            = special            # Capacité spéciale (ex: "scanner")
        self.dialogue_idx       = 0
        self.pulse_timer        = 0                  # Pour animation puce
        self.a_ete_scan         = False

    def get_dialogue(self):
        """Retourne le prochain dialogue cyclique."""
        d = self.dialogues[self.dialogue_idx % len(self.dialogues)]
        self.dialogue_idx += 1
        return d

    def dessiner_portrait(self, surface, x, y, largeur=200, hauteur=260):
        """
        Dessine le portrait du personnage.
        Utilise l'image réelle si disponible dans IMAGES_PERSOS,
        sinon replie sur le portrait procédural en code.
        """
        # ── Vérifier si une image est disponible pour ce personnage ──
        img = IMAGES_PERSOS.get(self.id)
        if img is not None:
            # Redimensionner si nécessaire
            if img.get_size() != (largeur, hauteur):
                img = pygame.transform.smoothscale(img, (largeur, hauteur))
            # Fond noir derrière l'image
            pygame.draw.rect(surface, (5, 8, 5),
                             (x, y, largeur, hauteur), border_radius=4)
            surface.blit(img, (x, y))
            # Bordure verte par-dessus
            pygame.draw.rect(surface, VERT_CLAIR,
                             (x, y, largeur, hauteur), 2, border_radius=4)
            # Scanlines légères sur le portrait
            for sly in range(y, y + hauteur, 5):
                sl = pygame.Surface((largeur, 1), pygame.SRCALPHA)
                sl.fill((0, 0, 0, 35))
                surface.blit(sl, (x, sly))
            # Nom
            txt = POLICE_MONO.render(self.nom, True, VERT_VIF)
            surface.blit(txt, (x + largeur//2 - txt.get_width()//2, y + hauteur - 28))
            # Détails spéciaux par-dessus l'image
            self._dessiner_overlay_special(surface, x, y, largeur, hauteur)
            return

        # ── Portrait procédural (fallback si pas d'image) ──
        pygame.draw.rect(surface, self.couleur_portrait,
                         (x, y, largeur, hauteur), border_radius=4)
        pygame.draw.rect(surface, VERT_CLAIR,
                         (x, y, largeur, hauteur), 2, border_radius=4)

        # Silhouette tête
        cx = x + largeur // 2
        cy = y + hauteur // 3
        # Tête
        pygame.draw.ellipse(surface, (self.couleur_portrait[0]+20,
                                      self.couleur_portrait[1]+20,
                                      self.couleur_portrait[2]+20),
                            (cx - 40, cy - 50, 80, 90))
        # Corps
        pygame.draw.rect(surface, (self.couleur_portrait[0]+10,
                                   self.couleur_portrait[1]+10,
                                   self.couleur_portrait[2]+10),
                         (cx - 50, cy + 45, 100, 100), border_radius=5)

        # Effets spéciaux selon le personnage
        self._dessiner_details_special(surface, x, y, largeur, hauteur, cx, cy)

        # Nom du personnage
        txt = POLICE_MONO.render(self.nom, True, VERT_VIF)
        surface.blit(txt, (x + largeur//2 - txt.get_width()//2, y + hauteur - 30))

    def _dessiner_details_special(self, surface, x, y, larg, haut, cx, cy):
        """
        Portraits procéduraux inspirés du style des images fournies :
        fond sombre, traits esquissés, couleurs desaturées, détails corporels marqués.
        """
        self.pulse_timer += 0.05

        if self.id == 1:
            # ── L'Insomniaque ──
            # Fond sombre bleuté
            pygame.draw.rect(surface, (18, 22, 28), (x, y, larg, haut), border_radius=4)
            # Silhouette — buste
            pygame.draw.rect(surface, (25, 30, 38), (cx - 55, cy + 30, 110, 130), border_radius=6)
            # Veste sombre avec cols
            pygame.draw.polygon(surface, (20, 25, 32),
                                [(cx - 55, cy + 30), (cx - 20, cy + 30), (cx, cy + 60),
                                 (cx + 20, cy + 30), (cx + 55, cy + 30), (cx + 55, cy + 160),
                                 (cx - 55, cy + 160)])
            # Col de chemise
            pygame.draw.polygon(surface, (40, 48, 40),
                                [(cx - 18, cy + 30), (cx, cy + 55), (cx + 18, cy + 30)])
            # Cou
            pygame.draw.rect(surface, (38, 45, 38), (cx - 12, cy + 8, 24, 28))
            # Tête
            pygame.draw.ellipse(surface, (42, 50, 42), (cx - 42, cy - 55, 84, 72))
            # Cheveux très courts et sombres
            pygame.draw.ellipse(surface, (15, 18, 15), (cx - 42, cy - 55, 84, 35))
            # Traits du visage — regard fixe et malaisant
            # Yeux GRANDS ouverts — ne cligne jamais
            for dx, dy_eye in [(-18, 0), (18, 0)]:
                # Blanc de l'œil (surdimensionné)
                pygame.draw.ellipse(surface, (200, 215, 195),
                                    (cx + dx - 16, cy - 28, 32, 22))
                # Iris vert pâle
                pygame.draw.circle(surface, (60, 100, 60), (cx + dx, cy - 17), 8)
                # Pupille noire dilatée
                pygame.draw.circle(surface, (5, 5, 5), (cx + dx, cy - 17), 6)
                # Reflet (rend le regard encore plus fixe)
                pygame.draw.circle(surface, (160, 200, 160), (cx + dx + 3, cy - 20), 2)
                # Cernes profonds
                pygame.draw.ellipse(surface, (20, 28, 20),
                                    (cx + dx - 16, cy - 15, 32, 12))
            # Nez fin
            pygame.draw.line(surface, (30, 36, 30), (cx, cy - 12), (cx - 4, cy + 2), 1)
            pygame.draw.line(surface, (30, 36, 30), (cx, cy - 12), (cx + 4, cy + 2), 1)
            # Bouche fermée, tendue
            pygame.draw.line(surface, (35, 42, 35), (cx - 12, cy + 8), (cx + 12, cy + 8), 2)
            # Veinules sous les yeux (insomnie)
            pygame.draw.line(surface, (25, 35, 45), (cx - 28, cy - 8), (cx - 15, cy - 5), 1)
            pygame.draw.line(surface, (25, 35, 45), (cx + 28, cy - 8), (cx + 15, cy - 5), 1)
            # Étiquette indice
            fond_ind = pygame.Surface((larg - 10, 20), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 150))
            surface.blit(fond_ind, (x + 5, y + haut - 52))
            txt = POLICE_MONO.render("! Ne cligne pas des yeux", True, ORANGE_ALERTE)
            surface.blit(txt, (x + 6, y + haut - 51))

        elif self.id == 3:
            # ── Mère & Enfant ──
            # Fond verdâtre épuisé
            pygame.draw.rect(surface, (16, 24, 18), (x, y, larg, haut), border_radius=4)
            # MÈRE — à gauche, position 3/4
            # Corps mère (manteau usé)
            pygame.draw.rect(surface, (28, 38, 28), (cx - 55, cy + 20, 75, 140), border_radius=4)
            pygame.draw.rect(surface, (22, 32, 22), (cx - 55, cy + 20, 75, 140), 1, border_radius=4)
            # Tête mère
            pygame.draw.ellipse(surface, (45, 55, 42), (cx - 48, cy - 48, 70, 68))
            # Cheveux défaits
            pygame.draw.arc(surface, (18, 22, 18),
                            pygame.Rect(cx - 50, cy - 50, 74, 40), 0, math.pi, 3)
            for hi in range(-3, 3):
                pygame.draw.line(surface, (20, 25, 20),
                                 (cx - 13 + hi * 8, cy - 45),
                                 (cx - 18 + hi * 9, cy - 10), 1)
            # Yeux mère — épuisés
            pygame.draw.ellipse(surface, (130, 145, 125), (cx - 35, cy - 18, 22, 12))
            pygame.draw.ellipse(surface, (130, 145, 125), (cx - 8,  cy - 18, 22, 12))
            pygame.draw.circle(surface, (30, 38, 28), (cx - 24, cy - 12), 4)
            pygame.draw.circle(surface, (30, 38, 28), (cx + 3,  cy - 12), 4)
            # Cernes
            pygame.draw.ellipse(surface, (22, 30, 22), (cx - 35, cy - 8, 22, 8))
            pygame.draw.ellipse(surface, (22, 30, 22), (cx - 8,  cy - 8, 22, 8))
            # Bouche inquiète
            pygame.draw.arc(surface, (35, 45, 32),
                            pygame.Rect(cx - 15, cy + 2, 25, 12), math.pi, 2 * math.pi, 1)

            # ENFANT — à droite, en avant
            # Corps enfant
            pygame.draw.rect(surface, (32, 44, 30), (cx + 10, cy + 40, 50, 110), border_radius=4)
            # Tête enfant
            pygame.draw.ellipse(surface, (48, 58, 44), (cx + 8, cy, 52, 48))
            # Yeux enfant grands et innocents
            pygame.draw.ellipse(surface, (140, 160, 130), (cx + 14, cy + 10, 16, 12))
            pygame.draw.ellipse(surface, (140, 160, 130), (cx + 36, cy + 10, 16, 12))
            pygame.draw.circle(surface, (20, 28, 18), (cx + 22, cy + 16), 4)
            pygame.draw.circle(surface, (20, 28, 18), (cx + 44, cy + 16), 4)
            # Bras atrophié (malformation visible)
            pygame.draw.line(surface, (38, 50, 35), (cx + 10, cy + 55), (cx - 5, cy + 80), 3)
            pygame.draw.ellipse(surface, (35, 45, 32), (cx - 12, cy + 76, 12, 18))  # main atrophiée
            pygame.draw.line(surface, (28, 38, 25), (cx + 58, cy + 55), (cx + 62, cy + 90), 2)
            # Indice
            fond_ind = pygame.Surface((larg - 10, 20), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 150))
            surface.blit(fond_ind, (x + 5, y + haut - 52))
            txt = POLICE_MONO.render("Malformation (non infectieux)", True, ORANGE_ALERTE)
            surface.blit(txt, (x + 6, y + haut - 51))

        elif self.id == 4:
            # ── Le SDF ──
            # Fond très sombre, terne
            pygame.draw.rect(surface, (14, 16, 12), (x, y, larg, haut), border_radius=4)
            # Vêtements en lambeaux (superposition de couches)
            # Couche extérieure — manteau déchiré
            pygame.draw.polygon(surface, (22, 24, 18),
                                [(cx - 58, cy + 25), (cx + 58, cy + 25),
                                 (cx + 62, cy + 170), (cx - 62, cy + 170)])
            pygame.draw.polygon(surface, (28, 30, 22),
                                [(cx - 58, cy + 25), (cx + 58, cy + 25),
                                 (cx + 62, cy + 170), (cx - 62, cy + 170)], 1)
            # Déchirures dans le manteau
            for di in range(4):
                dx_d = cx - 40 + di * 22
                pygame.draw.line(surface, (10, 12, 8),
                                 (dx_d, cy + 60 + di * 15), (dx_d + 8, cy + 90 + di * 15), 1)
            # Sous-couche — pull
            pygame.draw.rect(surface, (18, 20, 15), (cx - 45, cy + 28, 90, 100))
            # Cou et tête
            pygame.draw.rect(surface, (40, 38, 28), (cx - 14, cy + 8, 28, 22))
            pygame.draw.ellipse(surface, (44, 40, 30), (cx - 44, cy - 52, 88, 70))
            # Barbe et cheveux négligés
            pygame.draw.ellipse(surface, (22, 20, 14), (cx - 38, cy - 8, 76, 58))  # barbe
            # Texture barbe
            for bi in range(12):
                bx = cx - 35 + bi * 6 + random.randint(-2, 2)
                by = cy - 5 + random.randint(-5, 20)
                pygame.draw.line(surface, (15, 14, 10), (bx, by), (bx + 2, by + 6), 1)
            # Yeux cernés, abattus
            pygame.draw.ellipse(surface, (90, 85, 65), (cx - 28, cy - 22, 18, 10))
            pygame.draw.ellipse(surface, (90, 85, 65), (cx + 10, cy - 22, 18, 10))
            pygame.draw.circle(surface, (35, 30, 20), (cx - 19, cy - 17), 3)
            pygame.draw.circle(surface, (35, 30, 20), (cx + 19, cy - 17), 3)
            # PIEDS SALES — très visibles en bas (signe distinctif)
            for pied_x, decal in [(cx - 38, 0), (cx + 5, 5)]:
                # Pied nu et terreux
                pygame.draw.ellipse(surface, (28, 20, 10), (pied_x, cy + 148, 38, 18))
                # Terre et crasse
                for ti in range(6):
                    pygame.draw.circle(surface, (18, 12, 5),
                                       (pied_x + 4 + ti * 5, cy + 155 + random.randint(-2, 2)), 2)
                # Orteils
                for oi in range(4):
                    pygame.draw.ellipse(surface, (25, 18, 8),
                                        (pied_x + 2 + oi * 8, cy + 145, 7, 6))
            # Indice
            fond_ind = pygame.Surface((larg - 10, 20), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 150))
            surface.blit(fond_ind, (x + 5, y + haut - 52))
            txt = POLICE_MONO.render("! Pieds nus et terreux", True, ORANGE_ALERTE)
            surface.blit(txt, (x + 6, y + haut - 51))

        elif self.id == 8:
            # ── L'Ordinaire (Hybride caché) ──
            # Apparence parfaitement banale — le plus dangereux
            pygame.draw.rect(surface, (18, 26, 18), (x, y, larg, haut), border_radius=4)
            # Tenue ordinaire — pull neutre
            pygame.draw.rect(surface, (30, 42, 30), (cx - 52, cy + 22, 104, 138), border_radius=5)
            pygame.draw.rect(surface, (36, 50, 35), (cx - 52, cy + 22, 104, 138), 1, border_radius=5)
            # Col en V
            pygame.draw.polygon(surface, (25, 36, 25),
                                [(cx - 16, cy + 22), (cx, cy + 50), (cx + 16, cy + 22)])
            # Cou normal
            pygame.draw.rect(surface, (45, 56, 42), (cx - 13, cy + 5, 26, 22))
            # Tête parfaitement normale
            pygame.draw.ellipse(surface, (48, 60, 44), (cx - 44, cy - 52, 88, 70))
            # Cheveux soignés
            pygame.draw.ellipse(surface, (20, 26, 18), (cx - 44, cy - 52, 88, 35))
            # Visage neutre et lisse — trop normal
            # Yeux normaux
            for dx_e in [-18, 18]:
                pygame.draw.ellipse(surface, (120, 140, 115),
                                    (cx + dx_e - 12, cy - 22, 24, 14))
                pygame.draw.circle(surface, (35, 45, 30), (cx + dx_e, cy - 15), 5)
                pygame.draw.circle(surface, (5, 5, 5), (cx + dx_e, cy - 15), 3)
                pygame.draw.circle(surface, (160, 200, 155), (cx + dx_e + 2, cy - 17), 1)
            # Sourire trop parfait
            pygame.draw.arc(surface, (38, 50, 35),
                            pygame.Rect(cx - 16, cy, 32, 16), math.pi, 2 * math.pi, 2)
            # Dents légèrement visibles
            pygame.draw.rect(surface, (170, 185, 165), (cx - 10, cy + 2, 20, 6))

            # PUCE DORSALE — visible seulement si scanné (coin haut droit)
            if self.a_ete_scan:
                dessiner_puce_rouge(surface, x + larg - 22, y + 22, 9, self.pulse_timer)
                fond_ind = pygame.Surface((larg - 10, 20), pygame.SRCALPHA)
                fond_ind.fill((0, 0, 0, 180))
                surface.blit(fond_ind, (x + 5, y + haut - 52))
                txt = POLICE_MONO.render("PUCE DORSALE DÉTECTÉE !", True, ROUGE_PUCE)
                surface.blit(txt, (x + 6, y + haut - 51))
            else:
                fond_ind = pygame.Surface((larg - 10, 20), pygame.SRCALPHA)
                fond_ind.fill((0, 0, 0, 130))
                surface.blit(fond_ind, (x + 5, y + haut - 52))
                txt = POLICE_MONO.render("Apparence normale...", True, GRIS_MOYEN)
                surface.blit(txt, (x + 6, y + haut - 51))

        elif self.id == 9:
            # ── L'Enraciné (Hybride végétal) ──
            pygame.draw.rect(surface, (10, 18, 8), (x, y, larg, haut), border_radius=4)
            # Vêtements déchirés avec racines qui percent
            pygame.draw.rect(surface, (16, 28, 12), (cx - 52, cy + 18, 104, 142), border_radius=5)
            # Racines qui traversent les vêtements
            for ri in range(8):
                rx = cx - 45 + ri * 12
                ry_start = cy + 60 + ri % 3 * 20
                ry_end = cy + 145 + ri % 4 * 10
                pygame.draw.line(surface, (18, 35, 8), (rx, ry_start), (rx + 5, ry_end), 2)
                # Ramifications
                pygame.draw.line(surface, (12, 25, 5),
                                 (rx + 3, (ry_start + ry_end) // 2),
                                 (rx + 14, (ry_start + ry_end) // 2 + 10), 1)
            # Cou avec veinures végétales
            pygame.draw.rect(surface, (35, 52, 25), (cx - 14, cy + 5, 28, 20))
            for vi in range(4):
                pygame.draw.line(surface, (20, 42, 10),
                                 (cx - 10 + vi * 6, cy + 5), (cx - 8 + vi * 5, cy + 22), 1)
            # Tête légèrement envahie de végétation
            pygame.draw.ellipse(surface, (38, 55, 28), (cx - 44, cy - 52, 88, 70))
            # Cheveux fusionnés avec petites racines
            pygame.draw.ellipse(surface, (15, 30, 8), (cx - 44, cy - 52, 88, 35))
            for hi in range(6):
                hx = cx - 35 + hi * 12
                pygame.draw.line(surface, (10, 25, 5),
                                 (hx, cy - 50), (hx + random.randint(-4, 4), cy - 35), 1)
            # Yeux hybrides — pupilles végétales allongées
            for dx_e in [-18, 18]:
                pygame.draw.ellipse(surface, (80, 120, 50),
                                    (cx + dx_e - 14, cy - 22, 28, 14))
                # Pupille en fente verticale
                pygame.draw.ellipse(surface, (5, 10, 3),
                                    (cx + dx_e - 3, cy - 22, 6, 14))
            # Bouche entrouverte — racine qui sort
            pygame.draw.ellipse(surface, (8, 14, 5), (cx - 16, cy + 4, 32, 14))
            pygame.draw.line(surface, (15, 30, 8), (cx, cy + 4), (cx - 5, cy + 25), 2)
            # PIEDS — racines et terre (signe le plus évident)
            pygame.draw.rect(surface, (10, 16, 5), (cx - 45, cy + 148, 90, 25))
            # Racines denses aux pieds
            for ri in range(10):
                rx = cx - 42 + ri * 9
                pygame.draw.line(surface, (14, 28, 6),
                                 (rx, cy + 155), (rx + random.randint(-8, 8), cy + 175), 2)
            # Terre et boue
            pygame.draw.ellipse(surface, (20, 15, 5), (cx - 48, cy + 158, 96, 18))
            for ti in range(15):
                pygame.draw.circle(surface, (12, 9, 3),
                                   (cx - 44 + ti * 6 + random.randint(-2, 2), cy + 162), 2)
            # Indice
            fond_ind = pygame.Surface((larg - 10, 20), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 150))
            surface.blit(fond_ind, (x + 5, y + haut - 52))
            txt = POLICE_MONO.render("! Pieds-racines + terre", True, ROUGE_PUCE)
            surface.blit(txt, (x + 6, y + haut - 51))

    def _dessiner_overlay_special(self, surface, x, y, largeur, hauteur):
        """
        Overlays dessinés PAR-DESSUS les images réelles.
        Ajoute les indicateurs d'indices et effets d'ambiance sur les sprites.
        """
        self.pulse_timer += 0.05

        if self.id == 2:
            # Agent SURSUM : halo bleu électrique + badge
            # Halo lumineux bleu autour du portrait
            halo_a = int(20 + 10 * math.sin(self.pulse_timer))
            halo = pygame.Surface((largeur + 20, hauteur + 20), pygame.SRCALPHA)
            pygame.draw.rect(halo, (40, 80, 220, halo_a), (0, 0, largeur + 20, hauteur + 20),
                             4, border_radius=6)
            surface.blit(halo, (x - 10, y - 10))
            # Badge SURSUM
            badge = pygame.Surface((largeur - 10, 24), pygame.SRCALPHA)
            badge.fill((15, 30, 150, 210))
            pygame.draw.rect(badge, (60, 110, 255, 255), (0, 0, largeur - 10, 24), 1)
            surface.blit(badge, (x + 5, y + hauteur - 52))
            txt_b = POLICE_MONO.render("▶ AGENT SURSUM — SCANNER", True, (130, 180, 255))
            surface.blit(txt_b, (x + 7, y + hauteur - 50))

        elif self.id == 5:
            # Fumeur : cigarette animée + indice langue
            # Fumée de cigarette
            for fi in range(3):
                fy = y + int(hauteur * 0.3) - (self.pulse_timer * 2 + fi * 15) % 50
                fa = max(0, 80 - int((self.pulse_timer * 2 + fi * 15) % 50) * 2)
                if fa > 0:
                    fume = pygame.Surface((8, 6), pygame.SRCALPHA)
                    fume.fill((100, 120, 100, int(fa)))
                    surface.blit(fume, (x + largeur - 35 + fi * 3, int(fy)))
            # Bandeau indice
            fond_ind = pygame.Surface((largeur - 10, 22), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 170))
            surface.blit(fond_ind, (x + 5, y + hauteur - 54))
            txt = POLICE_MONO.render("! Langue rongée (tabac ?)", True, ORANGE_ALERTE)
            surface.blit(txt, (x + 6, y + hauteur - 53))

        elif self.id == 7:
            # Hybride sans langue : veinures végétales pulsantes + indice
            pulse = int(self.pulse_timer * 2) % (largeur + 100)
            # Veinures vertes qui se propagent
            vein_surf = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
            for vi in range(5):
                vx = (pulse + vi * 30) % largeur
                pygame.draw.line(vein_surf, (20, 60, 15, 60),
                                 (vx, hauteur // 3), (vx + 10, hauteur * 2 // 3), 2)
            surface.blit(vein_surf, (x, y))
            # Halo rouge très subtil — signe de danger
            halo_r = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
            halo_r.fill((30, 5, 5, int(12 + 8 * math.sin(self.pulse_timer))))
            surface.blit(halo_r, (x, y))
            # Bandeau indice
            fond_ind = pygame.Surface((largeur - 10, 22), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 170))
            surface.blit(fond_ind, (x + 5, y + hauteur - 54))
            txt = POLICE_MONO.render("? Absence de langue", True, ROUGE_PUCE)
            surface.blit(txt, (x + 6, y + hauteur - 53))

        elif self.id == 8 and self.a_ete_scan:
            # Hybride puce : puce rouge pulsante visible après scan
            dessiner_puce_rouge(surface, x + largeur - 25, y + hauteur // 2, 11, self.pulse_timer)
            fond_ind = pygame.Surface((largeur - 10, 22), pygame.SRCALPHA)
            fond_ind.fill((0, 0, 0, 180))
            surface.blit(fond_ind, (x + 5, y + hauteur - 54))
            txt = POLICE_MONO.render("PUCE DORSALE !", True, ROUGE_PUCE)
            surface.blit(txt, (x + 6, y + hauteur - 53))


# BASE DE DONNÉES DES PERSONNAGES


def creer_personnages():
    """
    Retourne la liste de tous les personnages disponibles.
    Perso 10 (Traqueur) est géré séparément.
    """
    persos = [
        Personnage(
            id=1, nom="L'Insomniaque",
            est_hybride=False,
            dialogues=[
                "Je ne dors plus depuis... longtemps.",
                "Vous avez remarqué comme les nuits sont courtes ?",
                "Mes yeux s'adaptent mieux dans le noir maintenant.",
                "Vous me fixez ? Quelque chose ne va pas ?"
            ],
            signes_visibles=["Ne cligne jamais des yeux"],
            signes_caches=[],
            description_apparence="Un homme pâle aux yeux grands ouverts. Fixe tout sans jamais cligner.",
            couleur_portrait=(35, 45, 35),
            special=None
        ),
        Personnage(
            id=2, nom="Agent SURSUM",
            est_hybride=False,
            dialogues=[
                "Combinaison de protection, secteur 7.",
                "Si vous m'accueillez, je peux scanner vos autres invités.",
                "Mon équipement détecte les puces dorsales à 2 mètres.",
                "Le protocole exige une inspection immédiate."
            ],
            signes_visibles=["Combinaison bleu électrique", "Masque à gaz"],
            signes_caches=[],
            description_apparence="Agent en combinaison hermétique bleue. Offre le service de Scanner.",
            couleur_portrait=(20, 30, 80),
            special="scanner"
        ),
        Personnage(
            id=3, nom="Mère & Enfant",
            est_hybride=False,
            dialogues=[
                "Elle est née comme ça. C'est une malformation, rien d'autre.",
                "Les médecins ont confirmé. Ce n'est pas... l'épidémie.",
                "S'il vous plaît, elle a besoin de chaleur.",
                "Ne la regardez pas comme ça. Elle souffre assez."
            ],
            signes_visibles=["Malformation physique visible (enfant)"],
            signes_caches=["Génétique certifiée non-infectieuse"],
            description_apparence="Mère épuisée. L'enfant a un bras atrophié — malformation congénitale.",
            couleur_portrait=(40, 55, 40),
            special=None
        ),
        Personnage(
            id=4, nom="Le SDF",
            est_hybride=False,
            dialogues=[
                "S'il vous plaît, j'ai froid, je ne sens plus mes orteils.",
                "Juste une nuit. Je vous en supplie.",
                "Mes pieds... la rue est glacée.",
                "Je suis humain, je vous le jure sur tout."
            ],
            signes_visibles=["Pieds sales et nus"],
            signes_caches=["Humain, pauvre, non infecté"],
            description_apparence="SDF déguenillé, pieds nus et terreux. Signe ambigu mais humain.",
            couleur_portrait=(45, 40, 30),
            special=None
        ),
        Personnage(
            id=5, nom="Le Fumeur",
            est_hybride=False,
            dialogues=[
                "Vous auriez un feu ? Ma gorge me brûle.",
                "J'ai une langue, regardez — ah, elle saigne un peu...",
                "Le tabac... ça ronge tout. Même la langue.",
                "Ne vous inquiétez pas, c'est la cigarette. Que ça."
            ],
            signes_visibles=["Langue partiellement rongée (par le tabac)"],
            signes_caches=["Non-hybride, langue abîmée par tabagisme"],
            description_apparence="Fumeur invétéré. Sa langue abîmée peut tromper — ce n'est pas une mutation.",
            couleur_portrait=(50, 55, 40),
            special=None
        ),
        Personnage(
            id=7, nom="L'Inconnu",
            est_hybride=True,
            dialogues=[
                "Ouv... rez... Je suis... comme... vous...",
                "Froid... dehors... laissez...",
                "Nou... nous sommes... pareils...",
            ],
            signes_visibles=["Élocution fragmentée"],
            signes_caches=["Absence de langue", "Veinures végétales sous la peau"],
            description_apparence="Hybride. Parle avec difficulté — n'a plus de langue. Peau veinée de vert.",
            couleur_portrait=(30, 55, 30),
            special=None
        ),
        Personnage(
            id=8, nom="L'Ordinaire",
            est_hybride=True,
            dialogues=[
                "Bonsoir. Il fait froid ce soir.",
                "J'habite le quartier, vous me connaissez.",
                "Je cherche juste un endroit chaud.",
                "Vous n'avez pas à avoir peur."
            ],
            signes_visibles=["Apparence parfaitement normale"],
            signes_caches=["Puce dorsale active (détectable uniquement via Scanner)"],
            description_apparence="Hybride presque parfait. Seule la puce dans le dos le trahit.",
            couleur_portrait=(40, 60, 40),
            special=None
        ),
        Personnage(
            id=9, nom="L'Enraciné",
            est_hybride=True,
            dialogues=[
                "La terre est chaude. Laissez-moi entrer pour me planter.",
                "Mes racines cherchent... un foyer.",
                "Vous sentez la terre ? C'est moi. C'est... bien.",
                "Je dois m'ancrer. Vite."
            ],
            signes_visibles=["Pieds avec racines et terre visible", "Odeur de terre humide"],
            signes_caches=["Mutation végétale avancée"],
            description_apparence="Hybride végétal avancé. Pieds fusionnés avec des racines et de la terre.",
            couleur_portrait=(25, 45, 15),
            special=None
        ),
    ]
    return persos


# SÉQUENCE INTRO (Breaking News)


class IntroBreakingNews:
    """
    Écran d'intro style vieille télévision avec défilement de texte.
    """
    MESSAGES = [
        "2174 : ÉPIDÉMIE SURSUM-VIRET. MUTATION PLANTE/IA DÉTECTÉE.",
        "DANGER : LES HYBRIDES ATTAQUENT LES PERSONNES SEULES.",
        "ORDRE : HÉBERGEZ DES CITOYENS POUR NE PAS RESTER ISOLÉ.",
        "SIGNES : PIEDS SALES, ABSENCE DE LANGUE, PUCES DORSALES.",
        "ALERTE : À MINUIT, LE TRAQUEUR 10 SORT. DORMEZ IMPÉRATIVEMENT.",
    ]

    def __init__(self):
        self.timer         = 0
        self.msg_idx       = 0
        self.char_idx      = 0          # Pour l'effet machine à écrire
        self.texte_affiché = ""
        self.vitesse_frappe= 3          # frames par caractère
        self.frame_frappe  = 0
        self.delai_entre   = 120        # frames avant le message suivant
        self.delai_counter = 0
        self.en_delai      = False
        self.terminé       = False
        self.alpha_static  = 0
        self.pulse_rouge   = 0
        # Lignes de "static" TV
        self.static_lignes = [(random.randint(0, HAUTEUR),
                               random.randint(2, 8),
                               random.randint(20, 80)) for _ in range(8)]

    def mettre_a_jour(self):
        self.timer += 1
        self.pulse_rouge = math.sin(self.timer * 0.05) * 0.5 + 0.5

        # Mise à jour des lignes statiques
        if self.timer % 15 == 0:
            self.static_lignes = [(random.randint(0, HAUTEUR),
                                   random.randint(2, 8),
                                   random.randint(20, 80)) for _ in range(8)]

        if self.en_delai:
            self.delai_counter += 1
            if self.delai_counter >= self.delai_entre:
                self.en_delai      = False
                self.delai_counter = 0
                self.msg_idx      += 1
                self.char_idx      = 0
                self.texte_affiché = ""
                if self.msg_idx >= len(self.MESSAGES):
                    self.terminé = True
        else:
            # Effet machine à écrire
            self.frame_frappe += 1
            if self.frame_frappe >= self.vitesse_frappe:
                self.frame_frappe = 0
                msg = self.MESSAGES[self.msg_idx]
                if self.char_idx < len(msg):
                    self.texte_affiché += msg[self.char_idx]
                    self.char_idx      += 1
                else:
                    self.en_delai = True

    def dessiner(self, surface):
        # Fond TV sombre
        surface.fill((5, 8, 5))

        # Bordure TV
        pygame.draw.rect(surface, (20, 25, 20),
                         (60, 80, LARGEUR - 120, HAUTEUR - 160), border_radius=20)
        pygame.draw.rect(surface, (40, 50, 40),
                         (60, 80, LARGEUR - 120, HAUTEUR - 160), 4, border_radius=20)

        # Zone écran TV
        ecran_rect = (90, 110, LARGEUR - 180, HAUTEUR - 220)
        pygame.draw.rect(surface, (8, 15, 8), ecran_rect, border_radius=10)

        # "BREAKING NEWS" en haut
        bn_texte = POLICE_MONO_L.render("■ BREAKING NEWS", True,
                                        (int(200 * self.pulse_rouge), 30, 30))
        surface.blit(bn_texte, (110, 125))

        # Ligne rouge
        rouge_lum = int(150 + 100 * self.pulse_rouge)
        pygame.draw.rect(surface, (rouge_lum, 20, 20), (90, 155, LARGEUR - 180, 3))

        # Numéro du message
        num_txt = POLICE_MONO.render(f"[{self.msg_idx + 1}/{len(self.MESSAGES)}]",
                                     True, GRIS_MOYEN)
        surface.blit(num_txt, (LARGEUR - 160, 125))

        # Texte défilant avec retour à la ligne automatique
        self._dessiner_texte_wrap(surface, self.texte_affiché,
                                  110, 180, LARGEUR - 200, VERT_VIF, POLICE_MONO_L)

        # Curseur clignotant
        if self.timer % 60 < 30 and not self.en_delai:
            cur_x = 110 + POLICE_MONO_L.size(self.texte_affiché.split('\n')[-1])[0]
            cur_y = 180 + (self.texte_affiché.count('\n')) * 35
            pygame.draw.rect(surface, VERT_VIF, (cur_x, cur_y, 12, 26))

        # Lignes de static TV
        for (ly, lh, lalpha) in self.static_lignes:
            ligne_s = pygame.Surface((LARGEUR - 180, lh), pygame.SRCALPHA)
            ligne_s.fill((200, 220, 200, lalpha))
            surface.blit(ligne_s, (90, ly))

        # Bande info en bas
        pygame.draw.rect(surface, (15, 25, 15),
                         (90, HAUTEUR - 140, LARGEUR - 180, 30))
        info = POLICE_MONO.render(
            "RÉSEAU URGENCE-VIRET  |  SIGNAL: 94%  |  ÉMISSION EN COURS",
            True, VERT_MOYEN)
        surface.blit(info, (100, HAUTEUR - 136))

        # Appuyez sur Entrée
        if self.en_delai and self.delai_counter > 30:
            cont = POLICE_MONO.render(
                "[ ENTRÉE : continuer ]" if self.msg_idx < len(self.MESSAGES) - 1
                else "[ ENTRÉE : commencer ]",
                True, (100 + int(100 * self.pulse_rouge), 120, 100))
            surface.blit(cont, (LARGEUR//2 - cont.get_width()//2, HAUTEUR - 100))

        # Effets post-process
        dessiner_scanlines(surface, 40)
        dessiner_grain(surface, 15)

    def _dessiner_texte_wrap(self, surface, texte, x, y, largeur_max,
                              couleur, police, interligne=35):
        """Découpe le texte en lignes selon la largeur max."""
        mots  = texte.split(' ')
        ligne = ""
        ligne_y = y
        for mot in mots:
            test = ligne + mot + " "
            if police.size(test)[0] > largeur_max:
                if ligne:
                    rendu = police.render(ligne.strip(), True, couleur)
                    surface.blit(rendu, (x, ligne_y))
                    ligne_y += interligne
                ligne = mot + " "
            else:
                ligne = test
        if ligne:
            rendu = police.render(ligne.strip(), True, couleur)
            surface.blit(rendu, (x, ligne_y))

    def gerer_evenement(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.en_delai:
                self.delai_counter = self.delai_entre  # Sauter le délai


# GESTIONNAIRE DE SALLES


SALLES = {
    "SALON":   {"touche": pygame.K_z, "label": "Z - SALON   (Télévision)"},
    "COULOIR": {"touche": pygame.K_q, "label": "Q - COULOIR (Porte/Judas)"},
    "CUISINE": {"touche": pygame.K_s, "label": "S - CUISINE (Invités)"},
    "CHAMBRE": {"touche": pygame.K_d, "label": "D - CHAMBRE (Lit)"},
}

class SalleManager:
    """Gère les salles et dessine leur contenu."""

    def __init__(self):
        self.salle_actuelle = "SALON"

    def changer_salle(self, nom_salle):
        self.salle_actuelle = nom_salle

    def dessiner(self, surface, jeu):
        """Dessine la salle actuelle."""
        surface.fill(VERT_NUIT)
        salle = self.salle_actuelle

        if salle == "SALON":
            self._dessiner_salon(surface, jeu)
        elif salle == "COULOIR":
            self._dessiner_couloir(surface, jeu)
        elif salle == "CUISINE":
            self._dessiner_cuisine(surface, jeu)
        elif salle == "CHAMBRE":
            self._dessiner_chambre(surface, jeu)

        # HUD commun
        self._dessiner_hud(surface, jeu)

    def _dessiner_salon(self, surface, jeu):
        t = jeu.timer_global
        # ── Plafond ──
        pygame.draw.rect(surface, (8, 14, 8), (0, 0, LARGEUR, 60))
        # Liseré plafond/mur
        pygame.draw.rect(surface, (18, 30, 18), (0, 58, LARGEUR, 4))

        # ── Mur principal avec papier peint dégradé ──
        for y in range(60, 490):
            intensite = 12 + int(6 * (y - 60) / 430)
            pygame.draw.line(surface, (intensite, intensite + 8, intensite), (0, y), (LARGEUR, y))
        # Motif papier peint — lignes verticales très subtiles
        for x in range(0, LARGEUR, 60):
            pygame.draw.line(surface, (14, 22, 14), (x, 60), (x, 490), 1)
        # Motif horizontal du papier peint
        for y in range(100, 490, 60):
            pygame.draw.line(surface, (14, 22, 14), (0, y), (LARGEUR, y), 1)

        # ── Sol parquet ──
        for y in range(490, HAUTEUR - 40):
            intensite = 10 + int(4 * (y - 490) / 240)
            pygame.draw.line(surface, (intensite, intensite + 5, intensite - 2), (0, y), (LARGEUR, y))
        # Lames de parquet
        for x in range(0, LARGEUR, 80):
            decal = (x // 80 % 2) * 40
            pygame.draw.line(surface, (16, 24, 12), (x, 490 + decal), (x, HAUTEUR - 40), 1)
        # Plinthe
        pygame.draw.rect(surface, (20, 32, 18), (0, 488, LARGEUR, 6))

        # ── Lampe de plafond ──
        lx = LARGEUR // 2
        # Fil
        pygame.draw.line(surface, (25, 40, 25), (lx, 0), (lx, 68), 2)
        # Abat-jour
        pygame.draw.polygon(surface, (22, 35, 22),
                            [(lx - 30, 68), (lx + 30, 68), (lx + 18, 95), (lx - 18, 95)])
        pygame.draw.polygon(surface, (35, 55, 35),
                            [(lx - 30, 68), (lx + 30, 68), (lx + 18, 95), (lx - 18, 95)], 1)
        # Halo lumineux (pulse lent)
        halo_a = 18 + int(8 * math.sin(t * 0.03))
        halo = pygame.Surface((200, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(halo, (60, 100, 60, halo_a), (0, 0, 200, 120))
        surface.blit(halo, (lx - 100, 80))

        # ── Meubles gauche : étagère ──
        # Montants
        pygame.draw.rect(surface, (18, 30, 18), (30, 150, 8, 300))
        pygame.draw.rect(surface, (18, 30, 18), (178, 150, 8, 300))
        # Planches
        for ey in [150, 220, 290, 360, 430]:
            pygame.draw.rect(surface, (22, 36, 20), (30, ey, 156, 10))
            pygame.draw.rect(surface, (30, 48, 28), (30, ey, 156, 10), 1)
        # Objets sur étagère — livres stylisés
        livres_couleurs = [(20,45,20),(18,35,30),(25,40,15),(30,30,20),(15,40,25)]
        lx_livre = 40
        for lc in livres_couleurs:
            largeur_l = random.randint(12, 22)
            pygame.draw.rect(surface, lc, (lx_livre, 225, largeur_l, 55))
            pygame.draw.rect(surface, (lc[0]+8,lc[1]+8,lc[2]+8), (lx_livre, 225, largeur_l, 55), 1)
            lx_livre += largeur_l + 3
        # Petite plante malade sur étagère
        pygame.draw.rect(surface, (25, 18, 10), (140, 290, 20, 15))  # pot
        for i in range(3):
            angle = -math.pi/2 + (i-1) * 0.5
            lx2 = 150 + int(math.cos(angle) * 18)
            ly2 = 285 + int(math.sin(angle) * 12)
            pygame.draw.line(surface, (20, 50, 15), (150, 290), (lx2, ly2), 2)
        # Cadre photo (vide, noir)
        pygame.draw.rect(surface, (25, 38, 22), (50, 360, 70, 55))
        pygame.draw.rect(surface, (35, 55, 30), (50, 360, 70, 55), 2)
        pygame.draw.rect(surface, (5, 8, 5), (55, 365, 60, 45))

        # ── Télévision centrale ──
        tv_x, tv_y, tv_l, tv_h = LARGEUR//2 - 170, 110, 340, 220
        # Meuble TV
        pygame.draw.rect(surface, (16, 26, 16), (tv_x - 40, tv_y + tv_h, tv_l + 80, 50),
                         border_radius=4)
        pygame.draw.rect(surface, (25, 40, 22), (tv_x - 40, tv_y + tv_h, tv_l + 80, 50), 1,
                         border_radius=4)
        # Petites jambes meuble TV
        for jx in [tv_x - 20, tv_x + tv_l - 10]:
            pygame.draw.rect(surface, (20, 32, 18), (jx, tv_y + tv_h + 50, 12, 15))
        # Câbles derrière la TV
        for i in range(3):
            cx_c = tv_x + tv_l//2 + (i-1) * 15
            pygame.draw.line(surface, (15, 22, 15),
                             (cx_c, tv_y + tv_h + 10), (cx_c + (i-1)*8, tv_y + tv_h + 55), 2)
        # Cadre TV
        pygame.draw.rect(surface, (12, 18, 12), (tv_x - 12, tv_y - 10, tv_l + 24, tv_h + 20),
                         border_radius=6)
        pygame.draw.rect(surface, (28, 45, 26), (tv_x - 12, tv_y - 10, tv_l + 24, tv_h + 20),
                         2, border_radius=6)
        # Écran (légèrement incurvé visuellement)
        pygame.draw.rect(surface, (4, 10, 4), (tv_x, tv_y, tv_l, tv_h), border_radius=3)
        # Lueur verte de l'écran
        lueur_tv = pygame.Surface((tv_l, tv_h), pygame.SRCALPHA)
        lueur_tv.fill((0, 0, 0, 0))
        lueur_a = 30 + int(15 * math.sin(t * 0.04))
        pygame.draw.rect(lueur_tv, (30, 80, 30, lueur_a), (0, 0, tv_l, tv_h))
        surface.blit(lueur_tv, (tv_x, tv_y))
        # Scanlines TV
        for sly in range(tv_y + 2, tv_y + tv_h - 2, 5):
            pygame.draw.line(surface, (8, 20, 8), (tv_x + 2, sly), (tv_x + tv_l - 2, sly))
        # Contenu écran
        txt_tv = POLICE_MONO.render("▶ SIGNAL URGENCE VIRET-7", True, VERT_MOYEN)
        surface.blit(txt_tv, (tv_x + 14, tv_y + 18))
        txt_tv2 = POLICE_MONO.render(f"  JOUR {jeu.jour_actuel}/5  ░ SURVIVANTS: ???",
                                     True, (50, 110, 50))
        surface.blit(txt_tv2, (tv_x + 14, tv_y + 42))
        barre_prog = int(jeu.progression_heure() * 22)
        barre = "█" * barre_prog + "░" * (22 - barre_prog)
        txt_barre = POLICE_MONO.render(f"  [{barre}]", True, (40, 90, 40))
        surface.blit(txt_barre, (tv_x + 14, tv_y + 66))
        txt_heure = POLICE_MONO_L.render(jeu.get_heure_str(), True, VERT_VIF)
        surface.blit(txt_heure, (tv_x + tv_l//2 - txt_heure.get_width()//2, tv_y + 100))
        # Bruit statique sur les bords de l'écran
        for _ in range(40):
            sx = random.randint(tv_x, tv_x + tv_l - 1)
            sy = random.randint(tv_y, tv_y + tv_h - 1)
            lum = random.randint(5, 25)
            surface.set_at((sx, sy), (lum, lum + 5, lum))
        # Bouton power TV
        pygame.draw.circle(surface, (18, 30, 18), (tv_x + tv_l - 20, tv_y + tv_h + 6), 5)
        tv_led_col = (0, 180, 0) if t % 120 < 100 else (0, 80, 0)
        pygame.draw.circle(surface, tv_led_col, (tv_x + tv_l - 20, tv_y + tv_h + 6), 3)

        # ── Canapé ──
        canape_x = LARGEUR//2 - 220
        canape_y = HAUTEUR - 260
        # Pieds
        for px in [canape_x + 15, canape_x + 405]:
            pygame.draw.rect(surface, (15, 24, 14), (px, canape_y + 130, 12, 30))
        # Assise
        pygame.draw.rect(surface, (20, 36, 20), (canape_x, canape_y + 55, 440, 80),
                         border_radius=6)
        pygame.draw.rect(surface, (28, 46, 26), (canape_x, canape_y + 55, 440, 80), 1,
                         border_radius=6)
        # Dossier
        pygame.draw.rect(surface, (22, 40, 20), (canape_x, canape_y, 440, 60), border_radius=8)
        pygame.draw.rect(surface, (32, 52, 28), (canape_x, canape_y, 440, 60), 1, border_radius=8)
        # Accoudoirs
        for ax in [canape_x - 18, canape_x + 422]:
            pygame.draw.rect(surface, (20, 36, 20), (ax, canape_y + 10, 22, 110), border_radius=5)
            pygame.draw.rect(surface, (30, 48, 26), (ax, canape_y + 10, 22, 110), 1, border_radius=5)
        # Coussins
        for ci, cx_c in enumerate([canape_x + 30, canape_x + 185, canape_x + 330]):
            pygame.draw.rect(surface, (25, 42, 23), (cx_c, canape_y + 58, 110, 70), border_radius=5)
            pygame.draw.rect(surface, (34, 55, 30), (cx_c, canape_y + 58, 110, 70), 1, border_radius=5)
            # Pli central du coussin
            pygame.draw.line(surface, (18, 30, 18),
                             (cx_c + 55, canape_y + 62), (cx_c + 55, canape_y + 124), 1)

        # ── Table basse ──
        pygame.draw.rect(surface, (14, 22, 14), (LARGEUR//2 - 110, canape_y + 140, 220, 50),
                         border_radius=3)
        pygame.draw.rect(surface, (22, 35, 20), (LARGEUR//2 - 110, canape_y + 140, 220, 50),
                         1, border_radius=3)
        # Tasse sur table
        pygame.draw.ellipse(surface, (20, 32, 20), (LARGEUR//2 - 20, canape_y + 148, 28, 14))
        pygame.draw.rect(surface, (18, 28, 18), (LARGEUR//2 - 18, canape_y + 150, 24, 22))
        pygame.draw.arc(surface, (25, 40, 22),
                        pygame.Rect(LARGEUR//2 + 6, canape_y + 153, 10, 12),
                        -math.pi/2, math.pi/2, 1)
        # Vapeur tasse
        if t % 40 < 20:
            for vi in range(2):
                vy_off = (t % 40) * 2
                vapeur = pygame.Surface((20, 30), pygame.SRCALPHA)
                pygame.draw.line(vapeur, (40, 60, 40, 60),
                                 (6 + vi*8, 25 - vy_off % 25), (8 + vi*6, 0), 1)
                surface.blit(vapeur, (LARGEUR//2 - 10, canape_y + 125))

        # ── Mur droit : fenêtre condamnée ──
        fen_x = LARGEUR - 200
        pygame.draw.rect(surface, (10, 16, 10), (fen_x, 150, 140, 200))
        pygame.draw.rect(surface, (22, 35, 20), (fen_x, 150, 140, 200), 2)
        # Planches clouées
        for pi in range(5):
            py_p = 165 + pi * 35
            pygame.draw.rect(surface, (16, 25, 14), (fen_x - 5, py_p, 150, 12))
            pygame.draw.rect(surface, (22, 35, 20), (fen_x - 5, py_p, 150, 12), 1)
            # Clous
            for cxi in [fen_x + 10, fen_x + 120]:
                pygame.draw.circle(surface, (30, 45, 28), (cxi, py_p + 6), 3)
        # Lumière qui filtre (très faible)
        lueur_fen = pygame.Surface((140, 200), pygame.SRCALPHA)
        lueur_fen.fill((20, 35, 20, 12))
        surface.blit(lueur_fen, (fen_x, 150))

        # ── Ombre portée du canapé sur le sol ──
        ombre_c = pygame.Surface((440, 20), pygame.SRCALPHA)
        ombre_c.fill((0, 0, 0, 60))
        surface.blit(ombre_c, (canape_x, canape_y + 156))

        # Label salle
        txt_s = POLICE_TITRE.render("[ SALON ]", True, VERT_MOYEN)
        surface.blit(txt_s, (20, 20))

    def _dessiner_couloir(self, surface, jeu):
        t = jeu.timer_global
        cx = LARGEUR // 2

        # ── Plafond ──
        pygame.draw.rect(surface, (6, 10, 6), (0, 0, LARGEUR, 55))
        pygame.draw.rect(surface, (14, 22, 14), (0, 53, LARGEUR, 4))

        # ── Mur de fond (perspective) ──
        for y in range(55, 490):
            intensite = 8 + int(5 * (y - 55) / 435)
            pygame.draw.line(surface, (intensite, intensite + 6, intensite), (0, y), (LARGEUR, y))

        # ── Sol ──
        for y in range(490, HAUTEUR - 40):
            intensite = 9 + int(3 * (y - 490) / 240)
            pygame.draw.line(surface, (intensite, intensite + 3, intensite - 1), (0, y), (LARGEUR, y))
        # Plinthe
        pygame.draw.rect(surface, (16, 26, 14), (0, 487, LARGEUR, 6))

        # ── Lignes de perspective (tunnel) ──
        nb_lignes = 10
        for i in range(nb_lignes):
            alpha_l = 30 + i * 15
            larg_p = LARGEUR // 2 - i * (LARGEUR // (nb_lignes * 2))
            haut_p = HAUTEUR - 100 - i * 35
            rect_p = pygame.Rect(cx - larg_p, 55 + i * 25, larg_p * 2, haut_p)
            s_ligne = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
            pygame.draw.rect(s_ligne, (25, 45, 25, alpha_l), rect_p, 1)
            surface.blit(s_ligne, (0, 0))

        # ── Murs latéraux avec texture ──
        # Gauche
        pygame.draw.rect(surface, (10, 16, 10), (0, 55, 200, 435))
        for wy in range(55, 490, 40):
            pygame.draw.line(surface, (13, 20, 13), (0, wy), (200, wy + 10), 1)
        # Droite
        pygame.draw.rect(surface, (10, 16, 10), (LARGEUR - 200, 55, 200, 435))
        for wy in range(55, 490, 40):
            pygame.draw.line(surface, (13, 20, 13), (LARGEUR, wy), (LARGEUR - 200, wy + 10), 1)

        # ── Ampoule nue au plafond ──
        pygame.draw.line(surface, (20, 32, 20), (cx, 0), (cx, 60), 2)
        pygame.draw.circle(surface, (22, 38, 22), (cx, 65), 10)
        pygame.draw.circle(surface, (35, 60, 35), (cx, 65), 10, 1)
        # Filament clignotant
        if t % 200 < 180:
            ampoule_lum = 40 + int(20 * math.sin(t * 0.05))
            pygame.draw.circle(surface, (ampoule_lum, ampoule_lum + 20, ampoule_lum), (cx, 65), 5)
            halo_a = pygame.Surface((120, 80), pygame.SRCALPHA)
            pygame.draw.ellipse(halo_a, (30, 60, 30, 18), (0, 0, 120, 80))
            surface.blit(halo_a, (cx - 60, 60))
        else:
            # Scintillement — ampoule qui vacille
            pygame.draw.circle(surface, (15, 20, 15), (cx, 65), 5)

        # ── Mur de fond avec papier peint décollé ──
        # Papier peint — bandes verticales
        for px in range(250, LARGEUR - 250, 30):
            pygame.draw.line(surface, (14, 22, 14), (px, 130), (px, 490), 1)
        # Coins décollés du papier peint
        for dcx, dcy in [(cx - 80, 140), (cx + 50, 200)]:
            pygame.draw.polygon(surface, (12, 18, 12),
                                [(dcx, dcy), (dcx + 25, dcy), (dcx + 15, dcy + 30)])
            pygame.draw.polygon(surface, (18, 28, 18),
                                [(dcx, dcy), (dcx + 25, dcy), (dcx + 15, dcy + 30)], 1)

        # ── Porte principale ──
        porte_x, porte_y = cx - 90, 130
        porte_l, porte_h = 180, 290

        # Encadrement
        pygame.draw.rect(surface, (22, 36, 20),
                         (porte_x - 14, porte_y - 10, porte_l + 28, porte_h + 14), border_radius=2)
        # Ombre intérieure encadrement
        pygame.draw.rect(surface, (10, 16, 10),
                         (porte_x - 10, porte_y - 6, porte_l + 20, porte_h + 10), border_radius=2)

        # Corps de la porte
        for col_y in range(porte_y, porte_y + porte_h):
            intensite = 14 + int(4 * (col_y - porte_y) / porte_h)
            pygame.draw.line(surface, (intensite, intensite + 6, intensite - 2),
                             (porte_x, col_y), (porte_x + porte_l, col_y))
        # Panneaux moulurés
        for panel in [(porte_x + 10, porte_y + 10, porte_l - 20, 110),
                      (porte_x + 10, porte_y + 135, porte_l - 20, 110),
                      (porte_x + 10, porte_y + 260, porte_l - 20, 22)]:
            pygame.draw.rect(surface, (20, 32, 18), panel, 1, border_radius=2)
        # Bordure lumineuse de la porte (visiteur présent = plus intense)
        bord_intensite = 35 if jeu.visiteur_en_attente else 22
        pygame.draw.rect(surface, (bord_intensite, bord_intensite + 15, bord_intensite),
                         (porte_x, porte_y, porte_l, porte_h), 2, border_radius=1)

        # Poignée de porte
        pygame.draw.circle(surface, (28, 45, 26), (porte_x + porte_l - 22, porte_y + 160), 8)
        pygame.draw.circle(surface, (38, 60, 35), (porte_x + porte_l - 22, porte_y + 160), 8, 1)
        pygame.draw.rect(surface, (22, 36, 20),
                         (porte_x + porte_l - 26, porte_y + 155, 3, 30), border_radius=1)

        # ── Judas ──
        judas_x, judas_y = cx, porte_y + 95
        pygame.draw.circle(surface, (8, 14, 8), (judas_x, judas_y), 14)
        pygame.draw.circle(surface, (30, 50, 28), (judas_x, judas_y), 14, 2)
        pygame.draw.circle(surface, (18, 30, 18), (judas_x, judas_y), 8)
        # Reflet judas
        pygame.draw.circle(surface, (35, 55, 33), (judas_x - 4, judas_y - 4), 3)

        # ── Sonnette ──
        pygame.draw.rect(surface, (20, 32, 18),
                         (porte_x + porte_l + 18, porte_y + 80, 24, 40), border_radius=4)
        pygame.draw.rect(surface, (28, 45, 25),
                         (porte_x + porte_l + 18, porte_y + 80, 24, 40), 1, border_radius=4)
        txt_sonn = POLICE_MONO.render("↑", True, VERT_MOYEN)
        surface.blit(txt_sonn, (porte_x + porte_l + 23, porte_y + 90))

        # ── Côtés mur avec détails ──
        # Gauche : porte-manteau
        for ei_y in [200, 260, 310]:
            pygame.draw.line(surface, (20, 32, 18), (60, ei_y - 5), (60, ei_y + 5), 3)
            pygame.draw.circle(surface, (25, 40, 22), (60, ei_y), 5)
            pygame.draw.circle(surface, (35, 55, 30), (60, ei_y), 5, 1)
        # Vêtement suspendu (forme)
        pygame.draw.line(surface, (16, 26, 16), (60, 205), (48, 260), 2)
        pygame.draw.line(surface, (16, 26, 16), (60, 205), (72, 260), 2)
        pygame.draw.rect(surface, (16, 26, 16), (48, 260, 24, 55))

        # Droite : boîte aux lettres / interphone
        pygame.draw.rect(surface, (18, 28, 18), (LARGEUR - 130, 240, 70, 100), border_radius=3)
        pygame.draw.rect(surface, (28, 45, 25), (LARGEUR - 130, 240, 70, 100), 1, border_radius=3)
        txt_inter = POLICE_MONO.render("INTER", True, GRIS_MOYEN)
        surface.blit(txt_inter, (LARGEUR - 122, 250))
        pygame.draw.rect(surface, (10, 16, 10), (LARGEUR - 120, 268, 50, 18))
        # LED interphone
        led_c = (0, 120, 0) if not jeu.visiteur_en_attente else (180, 20, 20)
        pygame.draw.circle(surface, led_c, (LARGEUR - 75, 310), 5)

        # ── Lumière sous la porte (si visiteur) ──
        if jeu.visiteur_en_attente:
            v = jeu.visiteur_en_attente
            couleur_signal = ROUGE_PUCE if v.est_hybride else VERT_VIF
            alpha_sig = 80 + int(60 * math.sin(t * 0.08))
            lueur_porte = pygame.Surface((porte_l - 20, 5), pygame.SRCALPHA)
            lueur_porte.fill((*couleur_signal, alpha_sig))
            surface.blit(lueur_porte, (porte_x + 10, porte_y + porte_h))
            # Ombre silhouette sous la porte
            ombre_s = pygame.Surface((porte_l, 12), pygame.SRCALPHA)
            pygame.draw.ellipse(ombre_s, (0, 0, 0, 70), (0, 0, porte_l, 12))
            surface.blit(ombre_s, (porte_x, porte_y + porte_h + 2))

            # Frappe à la porte — animation vibration
            if t % 90 < 5:
                effet_glitch(surface, 1)

            txt_v = POLICE_MONO.render(f"On frappe à la porte — {v.nom}", True, VERT_CLAIR)
            surface.blit(txt_v, (cx - txt_v.get_width()//2, porte_y + porte_h + 22))
            self._bouton(surface, cx - 180, porte_y + porte_h + 52, "[ O ] Ouvrir", VERT_MOYEN)
            self._bouton(surface, cx - 180, porte_y + porte_h + 78, "[ J ] Regarder au judas", GRIS_MOYEN)
            self._bouton(surface, cx - 180, porte_y + porte_h + 104, "[ R ] Refuser", ROUGE_SANG)
        else:
            txt_calme = POLICE_MONO.render("Couloir calme. Personne dehors.", True, GRIS_MOYEN)
            surface.blit(txt_calme, (cx - txt_calme.get_width()//2, porte_y + porte_h + 22))

        txt_s = POLICE_TITRE.render("[ COULOIR — PORTE D'ENTRÉE ]", True, VERT_MOYEN)
        surface.blit(txt_s, (20, 20))

    def _dessiner_cuisine(self, surface, jeu):
        t = jeu.timer_global

        # ── Plafond ──
        pygame.draw.rect(surface, (7, 12, 7), (0, 0, LARGEUR, 55))
        pygame.draw.rect(surface, (16, 26, 16), (0, 53, LARGEUR, 4))

        # ── Murs ──
        for y in range(55, 490):
            intensite = 10 + int(5 * (y - 55) / 435)
            pygame.draw.line(surface, (intensite, intensite + 7, intensite), (0, y), (LARGEUR, y))
        # Carreaux de faïence en haut (derrière plan de travail)
        for cy_t in range(55, 280, 30):
            for cx_t in range(0, LARGEUR, 30):
                pygame.draw.rect(surface, (12, 20, 12), (cx_t, cy_t, 29, 29), 1)

        # ── Sol carrelé ──
        for ty in range(490, HAUTEUR - 40, 35):
            for tx in range(0, LARGEUR, 35):
                col = (11, 18, 11) if (tx // 35 + ty // 35) % 2 == 0 else (9, 14, 9)
                pygame.draw.rect(surface, col, (tx, ty, 34, 34))
                pygame.draw.rect(surface, (14, 22, 12), (tx, ty, 34, 34), 1)
        pygame.draw.rect(surface, (18, 28, 16), (0, 487, LARGEUR, 6))

        # ── Placard haut gauche ──
        pygame.draw.rect(surface, (14, 22, 12), (0, 60, 220, 160))
        pygame.draw.rect(surface, (22, 35, 20), (0, 60, 220, 160), 2)
        # Portes du placard
        pygame.draw.rect(surface, (16, 26, 14), (5, 65, 100, 150), border_radius=2)
        pygame.draw.rect(surface, (16, 26, 14), (110, 65, 105, 150), border_radius=2)
        pygame.draw.rect(surface, (20, 32, 18), (5, 65, 100, 150), 1, border_radius=2)
        pygame.draw.rect(surface, (20, 32, 18), (110, 65, 105, 150), 1, border_radius=2)
        # Poignées placards
        pygame.draw.rect(surface, (25, 40, 22), (55, 138, 20, 8), border_radius=2)
        pygame.draw.rect(surface, (25, 40, 22), (148, 138, 20, 8), border_radius=2)

        # ── Placard haut droit ──
        pygame.draw.rect(surface, (14, 22, 12), (LARGEUR - 220, 60, 220, 160))
        pygame.draw.rect(surface, (22, 35, 20), (LARGEUR - 220, 60, 220, 160), 2)
        pygame.draw.rect(surface, (16, 26, 14),
                         (LARGEUR - 215, 65, 100, 150), border_radius=2)
        pygame.draw.rect(surface, (16, 26, 14),
                         (LARGEUR - 110, 65, 105, 150), border_radius=2)
        pygame.draw.rect(surface, (20, 32, 18),
                         (LARGEUR - 215, 65, 100, 150), 1, border_radius=2)
        pygame.draw.rect(surface, (20, 32, 18),
                         (LARGEUR - 110, 65, 105, 150), 1, border_radius=2)
        pygame.draw.rect(surface, (25, 40, 22), (LARGEUR - 170, 138, 20, 8), border_radius=2)
        pygame.draw.rect(surface, (25, 40, 22), (LARGEUR - 75, 138, 20, 8), border_radius=2)

        # ── Plan de travail gauche ──
        pygame.draw.rect(surface, (18, 30, 16), (0, 280, 280, 18))
        pygame.draw.rect(surface, (26, 42, 24), (0, 280, 280, 18), 1)
        # Meuble sous le plan
        pygame.draw.rect(surface, (12, 20, 12), (0, 298, 280, 195))
        pygame.draw.rect(surface, (18, 28, 16), (0, 298, 280, 195), 1)
        # Porte meuble
        pygame.draw.rect(surface, (14, 22, 14), (5, 303, 130, 180), border_radius=2)
        pygame.draw.rect(surface, (14, 22, 14), (140, 303, 130, 180), border_radius=2)
        pygame.draw.rect(surface, (20, 30, 18), (5, 303, 130, 180), 1, border_radius=2)
        pygame.draw.rect(surface, (20, 30, 18), (140, 303, 130, 180), 1, border_radius=2)
        pygame.draw.rect(surface, (22, 36, 20), (55, 390, 20, 8), border_radius=2)
        pygame.draw.rect(surface, (22, 36, 20), (170, 390, 20, 8), border_radius=2)

        # ── Évier ──
        pygame.draw.rect(surface, (15, 25, 14), (50, 230, 160, 50), border_radius=3)
        pygame.draw.rect(surface, (22, 38, 20), (50, 230, 160, 50), 2, border_radius=3)
        pygame.draw.rect(surface, (6, 10, 6), (60, 235, 140, 38), border_radius=2)
        # Robinet
        pygame.draw.rect(surface, (20, 32, 20), (118, 210, 8, 25))
        pygame.draw.rect(surface, (22, 36, 22), (105, 206, 34, 8), border_radius=3)
        # Goutte d'eau
        if t % 80 < 40:
            gy = 240 + (t % 80) * 2
            if gy < 280:
                pygame.draw.circle(surface, (20, 45, 30), (122, gy), 2)

        # ── Plan de travail droit ──
        pygame.draw.rect(surface, (18, 30, 16), (LARGEUR - 280, 280, 280, 18))
        pygame.draw.rect(surface, (26, 42, 24), (LARGEUR - 280, 280, 280, 18), 1)
        pygame.draw.rect(surface, (12, 20, 12), (LARGEUR - 280, 298, 280, 195))
        pygame.draw.rect(surface, (18, 28, 16), (LARGEUR - 280, 298, 280, 195), 1)
        pygame.draw.rect(surface, (14, 22, 14), (LARGEUR - 275, 303, 130, 180), border_radius=2)
        pygame.draw.rect(surface, (14, 22, 14), (LARGEUR - 140, 303, 130, 180), border_radius=2)
        pygame.draw.rect(surface, (20, 30, 18), (LARGEUR - 275, 303, 130, 180), 1, border_radius=2)
        pygame.draw.rect(surface, (20, 30, 18), (LARGEUR - 140, 303, 130, 180), 1, border_radius=2)

        # ── Table centrale avec chaises ──
        table_x = LARGEUR//2 - 160
        table_y = 350
        # Pieds table
        for px in [table_x + 15, table_x + 285]:
            pygame.draw.rect(surface, (14, 22, 14), (px, table_y + 30, 10, 130))
        # Plateau
        pygame.draw.rect(surface, (16, 28, 14), (table_x, table_y, 320, 30), border_radius=2)
        pygame.draw.rect(surface, (24, 40, 22), (table_x, table_y, 320, 30), 1, border_radius=2)
        # Chaises (simplifiées)
        for chx in [table_x - 40, table_x + 300]:
            pygame.draw.rect(surface, (12, 20, 12), (chx, table_y + 20, 35, 6))
            pygame.draw.rect(surface, (12, 20, 12), (chx + 5, table_y + 26, 5, 80))
            pygame.draw.rect(surface, (12, 20, 12), (chx + 25, table_y + 26, 5, 80))
            pygame.draw.rect(surface, (12, 20, 12), (chx, table_y - 30, 35, 6))
            pygame.draw.line(surface, (14, 22, 14), (chx + 5, table_y - 30), (chx + 5, table_y + 20), 1)
            pygame.draw.line(surface, (14, 22, 14), (chx + 30, table_y - 30), (chx + 30, table_y + 20), 1)

        # ── Lampe de plafond cuisine ──
        pygame.draw.rect(surface, (18, 30, 18),
                         (LARGEUR//2 - 60, 0, 120, 10))
        pygame.draw.rect(surface, (20, 34, 20),
                         (LARGEUR//2 - 50, 10, 100, 25), border_radius=3)
        lueur_k = 20 + int(8 * math.sin(t * 0.04))
        halo_k = pygame.Surface((300, 150), pygame.SRCALPHA)
        pygame.draw.ellipse(halo_k, (30, 60, 30, lueur_k), (0, 0, 300, 150))
        surface.blit(halo_k, (LARGEUR//2 - 150, 30))

        # ── Zone invités (milieu bas) ──
        txt_s = POLICE_TITRE.render("[ CUISINE — INVITÉS HÉBERGÉS ]", True, VERT_MOYEN)
        surface.blit(txt_s, (20, 20))

        if jeu.invites_actuels:
            nb = len(jeu.invites_actuels)
            espacement = min(230, (LARGEUR - 80) // max(nb, 1))
            zone_y = 60
            for i, inv in enumerate(jeu.invites_actuels):
                px = 40 + i * espacement
                # Fond de portrait légèrement différencié
                fond_inv = pygame.Surface((200, 310), pygame.SRCALPHA)
                fond_inv.fill((5, 12, 5, 160))
                surface.blit(fond_inv, (px - 5, zone_y - 5))
                inv.dessiner_portrait(surface, px, zone_y, 190, 260)
                # Boutons
                agent_present = any(p.id == 2 for p in jeu.invites_actuels)
                if agent_present and inv.id != 2:
                    txt_scan = POLICE_MONO.render(f"[{i+1}] Scanner", True, BLEU_ELECTRIQUE)
                    surface.blit(txt_scan, (px, zone_y + 268))
                    txt_ex = POLICE_MONO.render(f"[E+{i+1}] Examiner", True, VERT_CLAIR)
                    surface.blit(txt_ex, (px, zone_y + 288))
                else:
                    txt_ex = POLICE_MONO.render(f"[{i+1}] Examiner", True, VERT_CLAIR)
                    surface.blit(txt_ex, (px, zone_y + 268))
            self._bouton(surface, 20, HAUTEUR - 80,
                         "[ X ] Expulser un invité (puis son numéro)", ROUGE_SANG)
        else:
            fond_vide = pygame.Surface((500, 60), pygame.SRCALPHA)
            fond_vide.fill((0, 0, 0, 100))
            surface.blit(fond_vide, (LARGEUR//2 - 250, HAUTEUR//2 - 70))
            txt_vide = POLICE_MONO.render("Aucun invité hébergé pour l'instant.", True, GRIS_MOYEN)
            surface.blit(txt_vide, (LARGEUR//2 - txt_vide.get_width()//2, HAUTEUR//2 - 55))

    def _dessiner_chambre(self, surface, jeu):
        t = jeu.timer_global
        heure = jeu.get_heure()

        # ── Plafond ──
        couleur_plafond = (5, 9, 5) if heure >= 22 else (7, 12, 7)
        pygame.draw.rect(surface, couleur_plafond, (0, 0, LARGEUR, 55))
        pygame.draw.rect(surface, (14, 22, 14), (0, 53, LARGEUR, 4))

        # ── Murs (plus sombres la nuit) ──
        intensite_mur = 6 if heure >= 23 else 10
        for y in range(55, 490):
            iv = intensite_mur + int(4 * (y - 55) / 435)
            pygame.draw.line(surface, (iv, iv + 5, iv), (0, y), (LARGEUR, y))

        # ── Sol ──
        for y in range(490, HAUTEUR - 40):
            iv = 8 + int(3 * (y - 490) / 240)
            pygame.draw.line(surface, (iv, iv + 3, iv - 1), (0, y), (LARGEUR, y))
        # Tapis sous le lit
        tapis_surf = pygame.Surface((460, 120), pygame.SRCALPHA)
        tapis_surf.fill((12, 20, 10, 180))
        pygame.draw.rect(tapis_surf, (18, 30, 16, 200), (0, 0, 460, 120), 2)
        surface.blit(tapis_surf, (LARGEUR//2 - 230, 420))
        # Motif tapis
        for ti in range(3):
            pygame.draw.rect(surface, (15, 24, 13),
                             (LARGEUR//2 - 210 + ti * 70, 430, 60, 100), 1, border_radius=2)
        pygame.draw.rect(surface, (16, 28, 14), (0, 487, LARGEUR, 6))

        # ── Lit ──
        lit_x = LARGEUR//2 - 210
        lit_y = 220
        # Tête de lit
        pygame.draw.rect(surface, (14, 24, 12),
                         (lit_x - 10, lit_y - 60, 430, 75), border_radius=6)
        pygame.draw.rect(surface, (22, 36, 20),
                         (lit_x - 10, lit_y - 60, 430, 75), 2, border_radius=6)
        # Panneaux moulurés tête de lit
        for pi_l in range(3):
            pygame.draw.rect(surface, (18, 30, 16),
                             (lit_x + pi_l * 135, lit_y - 55, 120, 60), 1, border_radius=3)
        # Cadre du lit
        pygame.draw.rect(surface, (12, 20, 10), (lit_x - 10, lit_y, 430, 230), border_radius=5)
        pygame.draw.rect(surface, (20, 34, 18), (lit_x - 10, lit_y, 430, 230), 2, border_radius=5)
        # Matelas
        pygame.draw.rect(surface, (16, 28, 14), (lit_x, lit_y + 5, 410, 220), border_radius=4)
        # Couverture (dégradé)
        for cy_lit in range(lit_y + 5, lit_y + 160):
            iv_lit = 14 + int(6 * (cy_lit - lit_y - 5) / 155)
            pygame.draw.line(surface, (iv_lit, iv_lit + 8, iv_lit),
                             (lit_x, cy_lit), (lit_x + 410, cy_lit))
        # Plis couverture
        for pli in [60, 130, 200, 280, 360]:
            pygame.draw.line(surface, (18, 30, 16),
                             (lit_x + pli, lit_y + 5), (lit_x + pli + 15, lit_y + 160), 1)
        # Bord couverture
        pygame.draw.rect(surface, (22, 38, 20), (lit_x, lit_y + 5, 410, 160), 1, border_radius=4)
        # Oreillers
        for oi, ox in enumerate([lit_x + 20, lit_x + 215]):
            pygame.draw.rect(surface, (20, 34, 18), (ox, lit_y + 10, 170, 70), border_radius=8)
            pygame.draw.rect(surface, (28, 46, 26), (ox, lit_y + 10, 170, 70), 1, border_radius=8)
            # Pli central oreiller
            pygame.draw.line(surface, (16, 28, 14),
                             (ox + 85, lit_y + 14), (ox + 85, lit_y + 76), 1)
        # Pied de lit
        pygame.draw.rect(surface, (14, 24, 12),
                         (lit_x - 10, lit_y + 228, 430, 18), border_radius=4)
        # Pieds métalliques
        for fx in [lit_x + 5, lit_x + 395]:
            pygame.draw.rect(surface, (18, 28, 16), (fx, lit_y + 242, 12, 25))

        # ── Table de nuit gauche ──
        pygame.draw.rect(surface, (12, 20, 12), (lit_x - 90, lit_y + 20, 75, 100), border_radius=3)
        pygame.draw.rect(surface, (18, 28, 16), (lit_x - 90, lit_y + 20, 75, 100), 1, border_radius=3)
        pygame.draw.rect(surface, (14, 22, 14), (lit_x - 88, lit_y + 50, 71, 45), border_radius=2)
        pygame.draw.rect(surface, (18, 28, 16), (lit_x - 88, lit_y + 50, 71, 45), 1, border_radius=2)
        pygame.draw.rect(surface, (18, 30, 16), (lit_x - 72, lit_y + 65, 20, 8), border_radius=2)
        # Lampe de chevet
        pygame.draw.rect(surface, (14, 22, 14), (lit_x - 68, lit_y - 5, 6, 30))
        pygame.draw.polygon(surface, (18, 30, 16),
                            [(lit_x - 80, lit_y - 5), (lit_x - 54, lit_y - 5),
                             (lit_x - 60, lit_y + 18), (lit_x - 74, lit_y + 18)])
        # Halo lampe chevet (orange la nuit)
        if heure >= 21:
            halo_chevet = pygame.Surface((100, 80), pygame.SRCALPHA)
            alpha_ch = 15 + int(8 * math.sin(t * 0.03))
            pygame.draw.ellipse(halo_chevet, (60, 40, 10, alpha_ch), (0, 0, 100, 80))
            surface.blit(halo_chevet, (lit_x - 120, lit_y - 20))
        # Réveil sur table de nuit
        pygame.draw.rect(surface, (14, 22, 14), (lit_x - 82, lit_y + 25, 32, 22), border_radius=2)
        pygame.draw.rect(surface, (20, 32, 18), (lit_x - 82, lit_y + 25, 32, 22), 1, border_radius=2)
        rev_txt = POLICE_MONO.render(jeu.get_heure_str(), True, ROUGE_PUCE)
        rev_txt_s = pygame.transform.scale(rev_txt, (30, 12))
        surface.blit(rev_txt_s, (lit_x - 81, lit_y + 30))

        # ── Table de nuit droite ──
        pygame.draw.rect(surface, (12, 20, 12),
                         (lit_x + 420, lit_y + 20, 75, 100), border_radius=3)
        pygame.draw.rect(surface, (18, 28, 16),
                         (lit_x + 420, lit_y + 20, 75, 100), 1, border_radius=3)
        # Verre d'eau
        pygame.draw.rect(surface, (10, 18, 14), (lit_x + 440, lit_y + 22, 16, 22))
        pygame.draw.rect(surface, (18, 35, 25), (lit_x + 440, lit_y + 22, 16, 22), 1)
        pygame.draw.ellipse(surface, (15, 30, 22), (lit_x + 439, lit_y + 20, 18, 6))

        # ── Armoire ──
        arm_x = LARGEUR - 170
        pygame.draw.rect(surface, (10, 18, 10), (arm_x, 60, 150, 430))
        pygame.draw.rect(surface, (18, 28, 16), (arm_x, 60, 150, 430), 2)
        # Portes armoire
        pygame.draw.rect(surface, (12, 20, 12), (arm_x + 5, 65, 66, 415), border_radius=2)
        pygame.draw.rect(surface, (12, 20, 12), (arm_x + 76, 65, 66, 415), border_radius=2)
        pygame.draw.rect(surface, (16, 26, 14), (arm_x + 5, 65, 66, 415), 1, border_radius=2)
        pygame.draw.rect(surface, (16, 26, 14), (arm_x + 76, 65, 66, 415), 1, border_radius=2)
        # Poignées armoire
        pygame.draw.rect(surface, (20, 32, 18), (arm_x + 60, 270, 8, 30), border_radius=2)
        pygame.draw.rect(surface, (20, 32, 18), (arm_x + 80, 270, 8, 30), border_radius=2)
        # Miroir sur armoire (reflet sombre)
        pygame.draw.rect(surface, (6, 10, 6), (arm_x + 15, 120, 120, 160))
        pygame.draw.rect(surface, (20, 30, 18), (arm_x + 15, 120, 120, 160), 1)
        # Reflet fantomatique dans le miroir
        reflet_a = 12 + int(5 * math.sin(t * 0.02))
        pygame.draw.ellipse(surface, (25, 40, 25),
                            (arm_x + 55, 145, 40, 110))
        reflet = pygame.Surface((120, 160), pygame.SRCALPHA)
        pygame.draw.ellipse(reflet, (30, 50, 30, reflet_a), (40, 20, 40, 120))
        surface.blit(reflet, (arm_x + 15, 120))

        # ── Fenêtre avec rideaux ──
        fen_x = 30
        fen_y = 90
        # Rideau gauche
        pygame.draw.polygon(surface, (14, 22, 12),
                            [(fen_x, fen_y), (fen_x + 60, fen_y),
                             (fen_x + 45, fen_y + 200), (fen_x, fen_y + 200)])
        # Rideau droit
        pygame.draw.polygon(surface, (14, 22, 12),
                            [(fen_x + 120, fen_y), (fen_x + 160, fen_y),
                             (fen_x + 160, fen_y + 200), (fen_x + 115, fen_y + 200)])
        # Carreau fenêtre
        pygame.draw.rect(surface, (5, 10, 5), (fen_x + 60, fen_y, 60, 200))
        # Lumière extérieure (verte la nuit = éclairage urbain)
        if heure >= 20:
            lueur_ext = pygame.Surface((60, 200), pygame.SRCALPHA)
            la = 8 + int(4 * math.sin(t * 0.02))
            lueur_ext.fill((10, 30, 10, la))
            surface.blit(lueur_ext, (fen_x + 60, fen_y))
        # Tringle rideau
        pygame.draw.rect(surface, (20, 32, 18), (fen_x - 5, fen_y - 4, 175, 5))

        # ── Tension nocturne ──
        txt_s = POLICE_TITRE.render("[ CHAMBRE ]", True, VERT_MOYEN)
        surface.blit(txt_s, (20, 20))

        if heure >= 23.5:
            # Overlay rouge pulsant
            overlay_r = pygame.Surface((LARGEUR, HAUTEUR - 40), pygame.SRCALPHA)
            pulsation = int(20 + 15 * math.sin(t * 0.12))
            overlay_r.fill((pulsation, 0, 0, pulsation // 2))
            surface.blit(overlay_r, (0, 0))

            alerte = POLICE_MONO_L.render("⚠ DORMEZ ! MINUIT APPROCHE...", True, ROUGE_PUCE)
            surface.blit(alerte, (LARGEUR//2 - alerte.get_width()//2, HAUTEUR - 130))
            self._bouton(surface, LARGEUR//2 - 110, HAUTEUR - 90, "[ Entrée ] Fermer les yeux",
                         VERT_VIF)
        elif heure >= 22.0:
            # Suggestion de dormir
            conseil = POLICE_MONO.render(
                f"Il est {jeu.get_heure_str()}. Vous pourriez dormir bientôt...", True, GRIS_MOYEN)
            surface.blit(conseil, (LARGEUR//2 - conseil.get_width()//2, HAUTEUR - 90))
            self._bouton(surface, LARGEUR//2 - 110, HAUTEUR - 65, "[ Entrée ] Dormir",
                         VERT_MOYEN)
        else:
            txt_trop_tot = POLICE_MONO.render(
                f"Il est {jeu.get_heure_str()}. Trop tôt pour dormir.", True, GRIS_MOYEN)
            surface.blit(txt_trop_tot,
                         (LARGEUR//2 - txt_trop_tot.get_width()//2, HAUTEUR - 75))

    def _bouton(self, surface, x, y, texte, couleur):
        txt = POLICE_MONO.render(texte, True, couleur)
        surface.blit(txt, (x, y))

    def _dessiner_hud(self, surface, jeu):
        """HUD en bas — heure, jour, invités, tension."""
        # Bande HUD
        pygame.draw.rect(surface, (5, 12, 5), (0, HAUTEUR - 40, LARGEUR, 40))
        pygame.draw.line(surface, VERT_MOYEN, (0, HAUTEUR - 40), (LARGEUR, HAUTEUR - 40))

        heure_txt = POLICE_TITRE.render(
            f"JOUR {jeu.jour_actuel}/5  |  {jeu.get_heure_str()}  |  "
            f"Invités: {len(jeu.invites_actuels)}/3  |  "
            f"Salle: {jeu.salle_manager.salle_actuelle}",
            True, VERT_CLAIR)
        surface.blit(heure_txt, (10, HAUTEUR - 32))

        # Navigation en haut à droite
        nav_x = LARGEUR - 350
        for i, (nom, info) in enumerate(SALLES.items()):
            couleur = VERT_VIF if nom == jeu.salle_manager.salle_actuelle else GRIS_MOYEN
            txt_nav = POLICE_MONO.render(info["label"], True, couleur)
            surface.blit(txt_nav, (nav_x, 10 + i * 20))

        # Tension sonore — barre rouge si nuit avancée
        heure = jeu.get_heure()
        if heure >= 23.5:
            tension_alpha = int(128 + 127 * math.sin(jeu.timer_global * 0.1))
            alerte_surf = pygame.Surface((LARGEUR, 4), pygame.SRCALPHA)
            alerte_surf.fill((220, 30, 30, tension_alpha))
            surface.blit(alerte_surf, (0, HAUTEUR - 44))

# BOÎTE DE DIALOGUE


class DialogueBox:
    """Affiche les dialogues des personnages avec effet machine à écrire."""

    def __init__(self):
        self.actif       = False
        self.texte_total = ""
        self.texte_affiché = ""
        self.char_idx    = 0
        self.timer_frappe= 0
        self.vitesse     = 2
        self.locuteur    = ""
        self.couleur_loc = VERT_VIF
        self.signes      = []
        self.terminé     = False
        self.image_detail = None  # Image optionnelle affichée dans la boîte

    def afficher(self, locuteur, texte, signes=None, couleur=VERT_VIF, image_detail=None):
        self.actif        = True
        self.locuteur     = locuteur
        self.texte_total  = texte
        self.texte_affiché= ""
        self.char_idx     = 0
        self.timer_frappe = 0
        self.couleur_loc  = couleur
        self.signes       = signes or []
        self.terminé      = False
        self.image_detail = image_detail  # Surface pygame ou None

    def mettre_a_jour(self):
        if not self.actif:
            return
        self.timer_frappe += 1
        if self.timer_frappe >= self.vitesse:
            self.timer_frappe = 0
            if self.char_idx < len(self.texte_total):
                self.texte_affiché += self.texte_total[self.char_idx]
                self.char_idx += 1
            else:
                self.terminé = True

    def dessiner(self, surface):
        if not self.actif:
            return
        # Fond dialogue
        boite = pygame.Surface((LARGEUR - 40, 200), pygame.SRCALPHA)
        boite.fill((5, 15, 5, 220))
        surface.blit(boite, (20, HAUTEUR - 250))
        pygame.draw.rect(surface, VERT_MOYEN,
                         (20, HAUTEUR - 250, LARGEUR - 40, 200), 2, border_radius=4)

        # Locuteur
        txt_loc = POLICE_TITRE.render(f"[ {self.locuteur} ]", True, self.couleur_loc)
        surface.blit(txt_loc, (35, HAUTEUR - 242))

        # Texte
        mots = self.texte_affiché.split(' ')
        ligne, ly = "", HAUTEUR - 215
        for mot in mots:
            test = ligne + mot + " "
            if POLICE_MONO.size(test)[0] > LARGEUR - 80:
                rendu = POLICE_MONO.render(ligne, True, BLANC_VERDATRE)
                surface.blit(rendu, (35, ly))
                ly += 22
                ligne = mot + " "
            else:
                ligne = test
        if ligne:
            rendu = POLICE_MONO.render(ligne, True, BLANC_VERDATRE)
            surface.blit(rendu, (35, ly))

        # Signes visibles
        if self.signes:
            sy = HAUTEUR - 95
            for signe in self.signes:
                couleur_s = ROUGE_PUCE if "!" in signe else ORANGE_ALERTE
                txt_s = POLICE_MONO.render(f"  ► {signe}", True, couleur_s)
                surface.blit(txt_s, (35, sy))
                sy += 20

        # Indicateur de fin
        if self.terminé:
            cont = POLICE_MONO.render("[ Entrée / Espace ]", True, GRIS_MOYEN)
            surface.blit(cont, (LARGEUR - cont.get_width() - 35, HAUTEUR - 65))

    def fermer(self):
        self.actif = False
        self.terminé = False


# ÉCRANS DE FIN


def ecran_victoire(surface, horloge):
    """Cinématique de victoire : flash blanc, annonce radio."""
    timer = 0
    texte_final = [
        "TRANSMISSION D'URGENCE — RÉSEAU VIRET",
        "",
        "Épidémie Sursum-Viret : CONTENUE.",
        "Les hybrides ont été neutralisés.",
        "",
        "Vous avez survécu... mais la paranoïa reste.",
        "",
        "Chaque visage dans la rue vous semble suspect.",
        "Vous vérifiez les pieds de chacun.",
        "Vous cherchez les yeux qui ne cillent pas.",
        "",
        "Est-ce vraiment terminé ?",
    ]
    son_vic = generer_bourdonnement(440, 3000, 0.15)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        timer += 1

        # Flash blanc initial
        if timer < 30:
            alpha = int(255 * (1 - timer / 30))
            surface.fill((alpha, alpha, alpha))
        else:
            surface.fill((5, 10, 5))
            # Texte qui apparaît progressivement
            for i, ligne in enumerate(texte_final):
                delai = 30 + i * 40
                if timer > delai:
                    prog = min(1.0, (timer - delai) / 20)
                    alpha_t = int(255 * prog)
                    if i == 0:
                        rendu = POLICE_MONO_L.render(ligne, True, VERT_VIF)
                    elif "Épidémie" in ligne or "survécu" in ligne:
                        rendu = POLICE_MONO_L.render(ligne, True, VERT_CLAIR)
                    elif "paranoïa" in ligne or "terminé" in ligne:
                        rendu = POLICE_MONO_L.render(ligne, True, ORANGE_ALERTE)
                    else:
                        rendu = POLICE_MONO.render(ligne, True, GRIS_CLAIR)
                    rendu.set_alpha(alpha_t)
                    surface.blit(rendu, (LARGEUR//2 - rendu.get_width()//2, 80 + i * 48))

        if timer == 30:
            son_vic.play()

        dessiner_scanlines(surface, 30)
        dessiner_grain(surface, 8)
        pygame.display.flip()
        horloge.tick(60)

def ecran_defaite(surface, horloge, raison="minuit"):
    """Cinématique de défaite : écran noir, sons de racines."""
    timer = 0
    texte_defaite = [
        "ERREUR SYSTÈME",
        "",
        "Hôte compromis détecté.",
        "Intégration Sursum-Viret : EN COURS...",
        "",
        "L'infection est en vous.",
        "Vous faites partie du système désormais.",
        "",
        "██████████ 100%",
        "",
        "RECYCLAGE TERMINÉ.",
    ]
    if raison == "minuit":
        texte_defaite.insert(1, "Hôte seul détecté à 00:00.")
    elif raison == "hybride":
        texte_defaite.insert(1, "Hybride infiltré — votre logement est compromis.")

    son_racines = generer_bourdonnement(30, 4000, 0.2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        timer += 1

        if timer < 20:
            surface.fill(NOIR)
        else:
            surface.fill((2, 3, 2))
            for i, ligne in enumerate(texte_defaite):
                delai = 20 + i * 50
                if timer > delai:
                    prog = min(1.0, (timer - delai) / 15)
                    alpha_t = int(255 * prog)
                    if "ERREUR" in ligne or "RECYCLAGE" in ligne:
                        couleur = ROUGE_PUCE
                        rendu = POLICE_MONO_XL.render(ligne, True, couleur)
                    elif "██" in ligne:
                        couleur = ROUGE_SANG
                        rendu = POLICE_MONO_L.render(ligne, True, couleur)
                    else:
                        couleur = GRIS_MOYEN
                        rendu = POLICE_MONO.render(ligne, True, couleur)
                    rendu.set_alpha(alpha_t)
                    surface.blit(rendu, (LARGEUR//2 - rendu.get_width()//2, 60 + i * 55))

        if timer == 20:
            son_racines.play()

        if timer % 30 == 0:
            effet_glitch(surface, random.randint(2, 6))

        dessiner_grain(surface, 20)
        dessiner_scanlines(surface, 50)
        pygame.display.flip()
        horloge.tick(60)

def ecran_jumpscare(surface, horloge):
    """Jumpscare du Traqueur de Minuit (Perso 10)."""
    SON_JUMPSCARE.play()
    timer = 0
    running = True
    while running and timer < 180:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        timer += 1
        progression = timer / 180

        # Fond qui pulse entre noir et rouge sombre
        r = int(20 * math.sin(timer * 0.3) + 10)
        surface.fill((r, 0, 0))

        # Silhouette du Traqueur (dessinée procéduralement)
        _dessiner_traqueur(surface, timer)

        # Message système
        if timer > 30:
            alpha = min(255, (timer - 30) * 10)
            msg1 = POLICE_MONO_XL.render("ERREUR SYSTÈME", True, ROUGE_PUCE)
            msg1.set_alpha(alpha)
            surface.blit(msg1, (LARGEUR//2 - msg1.get_width()//2, HAUTEUR//2 + 120))
        if timer > 60:
            alpha = min(255, (timer - 60) * 8)
            msg2 = POLICE_MONO_L.render("Hôte seul détecté. Recyclage en cours...",
                                         True, GRIS_CLAIR)
            msg2.set_alpha(alpha)
            surface.blit(msg2, (LARGEUR//2 - msg2.get_width()//2, HAUTEUR//2 + 165))

        # Glitch intense
        if timer < 60:
            effet_glitch(surface, 10)

        dessiner_scanlines(surface, 80)
        dessiner_grain(surface, 40)
        pygame.display.flip()
        horloge.tick(60)

def _dessiner_traqueur(surface, timer):
    """
    Dessine la silhouette procédurale du Traqueur de Minuit.
    REMPLACE PAR TON IMAGE : surface.blit(img_traqueur, (cx - img.get_width()//2, 50))
    """
    cx, cy = LARGEUR // 2, HAUTEUR // 2 - 80
    t = timer * 0.05

    # Corps principal (silhouette noire filiforme)
    # Tête
    pygame.draw.ellipse(surface, (15, 5, 5), (cx - 50, cy - 160, 100, 120))
    # Yeux — orbites avec racines
    for dx in [-20, 20]:
        # Orbite
        pygame.draw.ellipse(surface, (5, 0, 0), (cx + dx - 12, cy - 120, 24, 18))
        # Racines qui sortent des yeux
        for i in range(5):
            angle = -math.pi/2 + (i - 2) * 0.3 + math.sin(t + i) * 0.1
            longueur = 20 + i * 8
            ex = cx + dx + math.cos(angle) * longueur
            ey = cy - 111 + math.sin(angle) * longueur
            pygame.draw.line(surface, (40, 10, 5), (cx + dx, cy - 111), (int(ex), int(ey)), 1)

    # Corps long et fin
    pygame.draw.rect(surface, (10, 3, 3), (cx - 20, cy - 40, 40, 280))

    # Bras filiformes avec excroissances
    for signe_bras, longueur_bras in [(-1, 180), (1, 160)]:
        bx = cx + signe_bras * 20
        # Bras principal
        bx2 = cx + signe_bras * (20 + longueur_bras + int(10 * math.sin(t * 1.3)))
        by2 = cy + 80 + int(20 * math.sin(t))
        pygame.draw.line(surface, (8, 2, 2), (bx, cy + 40), (bx2, by2), 3)
        # Câbles-doigts (épines)
        for j in range(4):
            angle = (j / 3 * math.pi * signe_bras) + math.sin(t + j) * 0.2
            longueur_d = 30 + j * 10
            dx2 = bx2 + math.cos(angle) * longueur_d
            dy2 = by2 + math.sin(angle) * longueur_d
            pygame.draw.line(surface, (50, 10, 10), (bx2, by2), (int(dx2), int(dy2)), 1)
            # Épine à la pointe
            pygame.draw.circle(surface, ROUGE_SANG, (int(dx2), int(dy2)), 2)

    # Jambes filiformes
    for signe_j in [-1, 1]:
        jx = cx + signe_j * 15
        jx2 = cx + signe_j * (15 + 40 + int(5 * math.sin(t * 0.7 + signe_j)))
        jy2 = cy + 350
        pygame.draw.line(surface, (8, 2, 2), (jx, cy + 240), (jx2, jy2), 2)
        # Racines aux pieds
        for k in range(6):
            angle = math.pi/2 + (k - 3) * 0.25
            longueur_r = 15 + k * 5
            rx = jx2 + math.cos(angle) * longueur_r
            ry = jy2 + math.sin(angle) * longueur_r
            pygame.draw.line(surface, (30, 15, 5), (jx2, jy2), (int(rx), int(ry)), 1)


# ÉTAT DU JEU PRINCIPAL


class EtatJeu:
    """
    Classe centrale qui gère toute la logique du jeu :
    - Cycle jour/nuit
    - Visites aléatoires
    - Invités hébergés
    - Conditions de victoire/défaite
    """
    DUREE_JOUR_SEC  = 7 * 60  # 7 minutes en secondes IRL
    HEURE_DEBUT     = 9.0     # 09h00
    HEURE_FIN       = 24.0    # 00h00 (minuit)
    HEURE_ALERTE    = 23.5    # 23h30 — battement cœur

    MAX_INVITES     = 3
    NB_JOURS        = 5
    VISITES_PAR_JOUR= 2

    def __init__(self):
        self.tous_persos     = creer_personnages()
        self.jour_actuel     = 1
        self.temps_debut_jour= time.time()
        self.invites_actuels = []           # Personnages hébergés
        self.visiteur_en_attente = None     # Personne qui frappe
        self.hybrides_infiltres  = 0        # Compteur hybrides acceptés
        self.timer_global    = 0
        self.salle_manager   = SalleManager()
        self.dialogue_box    = DialogueBox()
        self.son_coeur_joue  = False
        self.son_ambiance_canal = pygame.mixer.Channel(0)
        self.son_coeur_canal    = pygame.mixer.Channel(1)
        self.son_ambiance_canal.play(SON_AMBIANCE, loops=-1)
        self.persos_visites        = set()  # IDs déjà visités (pas deux fois le même)
        self._planifier_visites()
        self.visites_restantes    = list(self.visites_du_jour)
        self.derniere_visite_temps= 0
        self.agent_present         = False  # Agent SURSUM est-il dans la cuisine ?
        self.mode_expulsion        = False
        self.mode_scanner          = False
        self.scanner_cible_idx     = -1

    def _planifier_visites(self):
        """Choisit 2 personnages aléatoires qui ne se répètent pas d'un jour à l'autre."""
        disponibles = [p for p in self.tous_persos if p.id not in self.persos_visites]
        if len(disponibles) < self.VISITES_PAR_JOUR:
            # Réinitialise si on a épuisé tout le monde
            self.persos_visites = set()
            disponibles = list(self.tous_persos)
        choisis = random.sample(disponibles, min(self.VISITES_PAR_JOUR, len(disponibles)))
        # Mélanger les heures de visite
        heures = sorted(random.uniform(10, 22) for _ in choisis)
        self.visites_du_jour = list(zip(heures, choisis))
        for p in choisis:
            self.persos_visites.add(p.id)

    def get_heure(self):
        """Retourne l'heure actuelle (9.0 à 24.0)."""
        elapsed  = time.time() - self.temps_debut_jour
        fraction = elapsed / self.DUREE_JOUR_SEC
        heure    = self.HEURE_DEBUT + fraction * (self.HEURE_FIN - self.HEURE_DEBUT)
        return min(heure, 24.0)

    def get_heure_str(self):
        h = self.get_heure()
        heures   = int(h) % 24
        minutes  = int((h % 1) * 60)
        return f"{heures:02d}:{minutes:02d}"

    def progression_heure(self):
        """Retourne 0.0 à 1.0 selon l'avancement du jour."""
        h = self.get_heure()
        return (h - self.HEURE_DEBUT) / (self.HEURE_FIN - self.HEURE_DEBUT)

    def mettre_a_jour(self):
        self.timer_global += 1
        self.dialogue_box.mettre_a_jour()

        heure = self.get_heure()

        # Battement de cœur après 23h30
        if heure >= self.HEURE_ALERTE and not self.son_coeur_joue:
            self.son_coeur_joue = True
            self.son_coeur_canal.play(SON_COEUR_RAPIDE, loops=-1)
        elif heure < self.HEURE_ALERTE and self.son_coeur_joue:
            self.son_coeur_joue = False
            self.son_coeur_canal.stop()

        # Vérifier les visites planifiées
        if not self.visiteur_en_attente and self.visites_restantes:
            h_visite, perso = self.visites_restantes[0]
            if heure >= h_visite:
                self.visiteur_en_attente = perso
                self.visites_restantes.pop(0)

    def verifier_minuit(self):
        """Vérifie si minuit est atteint et si le joueur est bien couché."""
        return self.get_heure() >= 24.0

    def passer_au_jour_suivant(self):
        """Passage au jour suivant (appelé quand le joueur dort)."""
        self.jour_actuel += 1
        self.temps_debut_jour = time.time()
        self.son_coeur_joue = False
        self.son_coeur_canal.stop()
        self._planifier_visites()
        self.visites_restantes = list(self.visites_du_jour)
        # Les invités quittent entre les jours
        self.invites_actuels = []
        self.visiteur_en_attente = None
        self.agent_present = False

    def accepter_visiteur(self):
        """Accepte le visiteur en attente dans le logement."""
        if self.visiteur_en_attente and len(self.invites_actuels) < self.MAX_INVITES:
            perso = self.visiteur_en_attente
            self.invites_actuels.append(perso)
            if perso.id == 2:
                self.agent_present = True
            self.visiteur_en_attente = None
            # Dialogue d'accueil
            self.dialogue_box.afficher(
                perso.nom,
                perso.get_dialogue(),
                perso.signes_visibles,
                couleur=BLEU_ELECTRIQUE if perso.id == 2 else VERT_CLAIR
            )
        elif len(self.invites_actuels) >= self.MAX_INVITES:
            self.dialogue_box.afficher(
                "SYSTÈME", "Logement plein. Refusez quelqu'un d'abord.", [], ROUGE_SANG)
            self.visiteur_en_attente = None

    def refuser_visiteur(self):
        """Refuse et renvoie le visiteur."""
        if self.visiteur_en_attente:
            self.dialogue_box.afficher(
                "SYSTÈME",
                f"Vous refusez {self.visiteur_en_attente.nom}. La nuit continue.",
                [], GRIS_MOYEN)
            self.visiteur_en_attente = None

    def regarder_judas(self):
        """Inspecte le visiteur par le judas — révèle signes visibles."""
        if self.visiteur_en_attente:
            v = self.visiteur_en_attente
            self.dialogue_box.afficher(
                f"[JUDAS] {v.nom}",
                v.description,
                v.signes_visibles,
                couleur=ROUGE_PUCE if v.est_hybride else VERT_CLAIR
            )

    def scanner_invite(self, idx):
        """Utilise le Scanner de l'Agent sur un invité."""
        if not self.agent_present:
            self.dialogue_box.afficher(
                "SYSTÈME", "L'Agent SURSUM n'est pas présent.", [], ROUGE_SANG)
            return
        if 0 <= idx < len(self.invites_actuels):
            cible = self.invites_actuels[idx]
            cible.a_ete_scan = True
            if cible.signes_caches:
                signes_tous = cible.signes_visibles + cible.signes_caches
                self.dialogue_box.afficher(
                    "AGENT SURSUM — SCAN",
                    f"Analyse de {cible.nom} terminée.",
                    signes_tous,
                    couleur=BLEU_ELECTRIQUE)
            else:
                self.dialogue_box.afficher(
                    "AGENT SURSUM — SCAN",
                    f"{cible.nom} : Aucune anomalie détectée par le scanner.",
                    ["Aucune puce détectée"],
                    couleur=BLEU_ELECTRIQUE)

    def examiner_invite(self, idx):
        """Examine de près un invité — dialogue + signes."""
        if 0 <= idx < len(self.invites_actuels):
            inv = self.invites_actuels[idx]
            signes = inv.signes_visibles[:]
            if inv.a_ete_scan:
                signes += inv.signes_caches
            self.dialogue_box.afficher(
                inv.nom, inv.get_dialogue(), signes,
                couleur=ROUGE_PUCE if inv.est_hybride else VERT_CLAIR)

    def expulser_invite(self, idx):
        """Expulse un invité du logement."""
        if 0 <= idx < len(self.invites_actuels):
            expulsé = self.invites_actuels.pop(idx)
            if expulsé.id == 2:
                self.agent_present = False
            self.dialogue_box.afficher(
                "SYSTÈME",
                f"{expulsé.nom} a été expulsé.",
                [], ROUGE_SANG)

    def compter_hybrides_presents(self):
        return sum(1 for p in self.invites_actuels if p.est_hybride)


# BOUCLE PRINCIPALE


def boucle_principale():
    try:
        # ---- Intro ----
        intro = IntroBreakingNews()
        while not intro.terminé:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                intro.gerer_evenement(event)
            intro.mettre_a_jour()
            intro.dessiner(ecran)
            pygame.display.flip()
            horloge.tick(60)

        print("Intro terminée. Initialisation du jeu...")
        # ---- Jeu ----
        jeu = EtatJeu()
        print(f"Jeu initialisé. Jour {jeu.jour_actuel}, Heure: {jeu.get_heure_str()}")
        game_running = True
        resultat = None   # "victoire", "defaite_minuit", "defaite_hybride"
    except Exception as e:
        print(f"ERREUR lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit()

    while game_running:
        try:
            dt = horloge.tick(60)

            # -- Évènements --
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:

                    # Fermer dialogue
                    if jeu.dialogue_box.actif and jeu.dialogue_box.terminé:
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            jeu.dialogue_box.fermer()
                        continue

                    # Mode expulsion
                    if jeu.mode_expulsion:
                        for k, val in enumerate([pygame.K_1, pygame.K_2, pygame.K_3]):
                            if event.key == val:
                                jeu.expulser_invite(k)
                        jeu.mode_expulsion = False
                        continue

                    # Mode scanner
                    if jeu.mode_scanner:
                        for k, val in enumerate([pygame.K_1, pygame.K_2, pygame.K_3]):
                            if event.key == val:
                                jeu.scanner_invite(k)
                        jeu.mode_scanner = False
                        continue

                    # Navigation (ZQSD — AZERTY)
                    salle = jeu.salle_manager.salle_actuelle
                    if event.key == pygame.K_z:
                        jeu.salle_manager.changer_salle("SALON")
                    elif event.key == pygame.K_q:
                        jeu.salle_manager.changer_salle("COULOIR")
                    elif event.key == pygame.K_s:
                        jeu.salle_manager.changer_salle("CUISINE")
                    elif event.key == pygame.K_d:
                        jeu.salle_manager.changer_salle("CHAMBRE")

                    # Actions en COULOIR
                    elif event.key == pygame.K_o and salle == "COULOIR":
                        jeu.accepter_visiteur()
                    elif event.key == pygame.K_j and salle == "COULOIR":
                        jeu.regarder_judas()
                    elif event.key == pygame.K_r and salle == "COULOIR":
                        jeu.refuser_visiteur()

                    # Actions en CUISINE
                    elif event.key == pygame.K_x and salle == "CUISINE":
                        jeu.mode_expulsion = True
                        jeu.dialogue_box.afficher(
                            "SYSTÈME", "Expulser qui ? Appuyez sur 1, 2 ou 3.", [], ROUGE_SANG)
                    elif (event.key in (pygame.K_1, pygame.K_2, pygame.K_3)
                          and salle == "CUISINE"):
                        idx = [pygame.K_1, pygame.K_2, pygame.K_3].index(event.key)
                        # E + chiffre → examiner
                        touches = pygame.key.get_pressed()
                        if touches[pygame.K_e]:
                            jeu.examiner_invite(idx)
                        else:
                            # Chiffre seul → scanner si agent présent
                            if jeu.agent_present:
                                jeu.scanner_invite(idx)
                            else:
                                jeu.examiner_invite(idx)

                    # Dormir en CHAMBRE
                    elif event.key == pygame.K_RETURN and salle == "CHAMBRE":
                        heure = jeu.get_heure()
                        if heure >= 23.5 or heure >= 22.0:
                            # Vérifier les hybrides
                            nb_hybrides = jeu.compter_hybrides_presents()
                            if nb_hybrides > 0:
                                if jeu.jour_actuel >= jeu.NB_JOURS:
                                    resultat = "defaite_hybride"
                                    game_running = False
                                else:
                                    jeu.passer_au_jour_suivant()
                            elif jeu.jour_actuel >= jeu.NB_JOURS:
                                resultat = "victoire"
                                game_running = False
                            else:
                                jeu.passer_au_jour_suivant()
                                jeu.dialogue_box.afficher(
                                    "SYSTÈME",
                                    f"Jour {jeu.jour_actuel}. Vous avez survécu encore une nuit.",
                                    [], VERT_VIF)
                        else:
                            jeu.dialogue_box.afficher(
                                "SYSTÈME",
                                f"Il est {jeu.get_heure_str()}. Attendez 23h30 pour dormir.",
                                [], GRIS_MOYEN)

            # -- Mise à jour --
            jeu.mettre_a_jour()

            # Vérification minuit
            if jeu.get_heure() >= 24.0:
                if jeu.salle_manager.salle_actuelle != "CHAMBRE":
                    # JUMPSCARE
                    ecran_jumpscare(ecran, horloge)
                    resultat = "defaite_minuit"
                    game_running = False
                else:
                    # Joueur était couché — passer au jour suivant automatiquement
                    nb_hybrides = jeu.compter_hybrides_presents()
                    if nb_hybrides > 0 and jeu.jour_actuel >= jeu.NB_JOURS:
                        resultat = "defaite_hybride"
                        game_running = False
                    elif jeu.jour_actuel >= jeu.NB_JOURS:
                        resultat = "victoire"
                        game_running = False
                    else:
                        jeu.passer_au_jour_suivant()
                        jeu.dialogue_box.afficher(
                            "SYSTÈME",
                            f"Jour {jeu.jour_actuel}. Une nouvelle journée commence.",
                            [], VERT_MOYEN)

            # -- Dessin --
            jeu.salle_manager.dessiner(ecran, jeu)
            jeu.dialogue_box.dessiner(ecran)

            # Post-process global
            dessiner_vignette(ecran)
            dessiner_scanlines(ecran, 35)
            if jeu.timer_global % 90 < 3:  # Glitch aléatoire occasionnel
                effet_glitch(ecran, 2)

            pygame.display.flip()

        except Exception as e:
            print(f"ERREUR dans la boucle de jeu: {e}")
            import traceback
            traceback.print_exc()
            game_running = False

    # ---- Cinématique de fin ----
    if resultat == "victoire":
        ecran_victoire(ecran, horloge)
    elif resultat in ("defaite_minuit", "defaite_hybride"):
        raison = "minuit" if resultat == "defaite_minuit" else "hybride"
        ecran_defaite(ecran, horloge, raison)

    # ---- Retour au menu ou quitter ----
    ecran.fill(NOIR)
    txt_fin = POLICE_MONO_L.render("[ Entrée : rejouer | Échap : quitter ]",
                                    True, VERT_MOYEN)
    ecran.blit(txt_fin, (LARGEUR//2 - txt_fin.get_width()//2, HAUTEUR//2))
    pygame.display.flip()

    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_attente = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    boucle_principale()  # Rejouer
                    en_attente = False
                elif event.key == pygame.K_ESCAPE:
                    en_attente = False


# POINT D'ENTRÉE


if __name__ == "__main__":
    boucle_principale()
    pygame.quit()
    sys.exit()
