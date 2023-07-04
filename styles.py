# Styles
RESET = "\x1b[0m"  # Réinitialisation des styles
BOLD = "\x1b[1m"  # Texte en gras
ITALIC = "\x1b[3m"  # Texte en italique
UNDERLINE = "\x1b[4m"  # Texte souligné
CROSSED = "\x1b[9m"  # Texte barré
DOUBLE_UNDERLINE = "\x1b[21m"  # Double soulignement

# Couleurs
GREY = "\x1b[90m"  # Texte gris
RED = "\x1b[31m"  # Texte rouge
GREEN = "\x1b[32m"  # Texte vert
YELLOW = "\x1b[33m"  # Texte jaune
BLUE = "\x1b[34m"  # Texte bleu
MAGENTA = "\x1b[35m"  # Texte magenta
CYAN = "\x1b[36m"  # Texte cyan

# Couleurs de fond
BG_RED = "\x1b[41m"  # Fond rouge
BG_GREEN = "\x1b[42m"  # Fond vert
BG_YELLOW = "\x1b[43m"  # Fond jaune
BG_BLUE = "\x1b[44m"  # Fond bleu
BG_MAGENTA = "\x1b[45m"  # Fond magenta
BG_CYAN = "\x1b[46m"  # Fond cyan
BG_WITHE = "\x1b[47m"  # Fond blanc




def get_color_of_mood(mood: int):
    # You can customize your palette here
    if mood == 1:
        return RED
    elif mood == 2:
        return RED
    elif mood == 3:
        return YELLOW
    elif mood == 4:
        return GREEN
    elif mood == 5:
        return GREEN