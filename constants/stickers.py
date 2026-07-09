# --- à ajouter à la fin de constants/stickers.py (ne pas remplacer le fichier, juste append) ---

class WaStickers:
    STICKERS_PER_FILE = 30  # WhatsApp/Sticker Maker: max 30 stickers par fichier .wastickers
    STATIC_MAX_BYTES = 100 * 1024  # limite "soft" WhatsApp pour un sticker statique (100 KB)
    ANIMATED_MAX_BYTES = 480 * 1024  # limite WhatsApp pour un sticker anime (~500 KB, marge de securite)
    TRAY_ICON_MAX_BYTES = 50 * 1024  # limite de l'icone du tray (96x96 png)
    TRAY_ICON_SIZE = 96
    STICKER_SIZE = 512
    TITLE_MAX_LEN = 128
    AUTHOR_MAX_LEN = 128
