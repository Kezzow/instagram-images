#!/usr/bin/env python3
"""
INSTAGRAM CARROUSEL + STORIES - Flux Meta officiel
4 comptes actifs | Stories automatiques 30s après chaque post
"""

import requests
import json
import base64
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PARIS_TZ = ZoneInfo("Europe/Paris")
from PIL import Image, ImageDraw, ImageFont
import random
import time
import logging
import sys

# ================= CONFIGURATION =================

GITHUB_TOKEN  = "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"
GITHUB_REPO   = "Kezzow/instagram-images"
GITHUB_BRANCH = "main"

DESCRIPTION_DEFAULT = """⚠️ STOP ! Ce message va CHANGER TA VIE si tu veux enfin devenir une femme forte, libre et inarrêtable.
Tu en as MARRE des relations qui te détruisent ? Des doutes, des angoisses, du manque de confiance ?
Il est temps de dire OUI à toi-même.
Ce que tu veux, tu peux l'avoir… Et ce pack est le premier pas.

✨ LE PACK ULTIME pour révéler la femme PUISSANTE en toi :
6 GUIDES TRANSFORMATEURS pour :
✅ Guérir d'une rupture sans souffrir pendant des mois
🚩 Détecter les red flags AVANT qu'il soit trop tard
💖 Reprendre confiance et t'aimer à 100%
🧘‍♀️ Apaiser ton anxiété et retrouver la paix intérieure
🌈 Être heureuse peu importe les circonstances
⚡️ Devenir magnétique et attirer le MEILLEUR

🎁 Et la meilleure partie ?
Tu profites d'une grosse réduction en prenant le pack complet !
Chaque guide coûte plus cher séparément…
Mais en pack, tu fais des économies ET tu as tout ce qu'il te faut pour ta transformation.

🔥Des milliers de femmes l'ont déjà adopté et vivent une véritable renaissance.
✨Elles brillent, elles s'aiment, elles OSENT. Et toi, tu attends quoi ?

Clique sur le lien dans ma bio pour commencer TA métamorphose aujourd'hui !👆✨

#femme #confianceensoi #developpementpersonnel"""

ACCOUNTS = [

    # ─── COMPTE 1 : @femmeforteindependante ───
    # Couleurs : Rose saumon (#FFB6C1) / Blanc
    {
        "name":               "femmes_fortes_independante",
        "quotes_file":        "quotes_relations_amoureuses.txt",
        "instagram_token":    "IGAANwbWz8TDJBZAGJSNnRGTzA5Q0E3aGJNeFhRYVhNMG4zeWpqZA2trVDg5MWVWZA0E4VDhtMVZALUm9VSnJlTFJtOW80R0FZAWjVLR09SbktJUTcybXBQUVcwaS1aSTRiLWtMOGhCMW9DNS1WWkVOdl95ZADl2YXVXd1lOYl8yMWlmUQZDZD",
        "instagram_user_id":  "26400533312969632",
        "bg_color":           "#FFB6C1",
        "text_color":         "#FFFFFF",
        "handle":             "@femmeforteindependante",
        "description":        DESCRIPTION_DEFAULT,
        "posting_schedule": [
            {"window": "midi", "target_hour": 12, "target_minute": 30, "variation": 5},
            {"window": "soir", "target_hour": 19, "target_minute": 30, "variation": 5},
        ],
        "promo_image_url": "https://raw.githubusercontent.com/Kezzow/instagram-images/main/promo_image.jpg",
    },

    # ─── COMPTE 2 : @femmefortepuissante ───
    # Couleurs : Noir (#000000) / Blanc
    {
        "name":               "femmes_fortes_puissante",
        "quotes_file":        "quotes_healing_trauma.txt",
        "instagram_token":    "IGAAUgf2BfEthBZAGIwaml1cENXWHJ6N0tmMXQyZAUNwbnRxal9fSkxSNHQ5ZAnlUelVSTXZA6LU9NLWZA0cWQwVzRtRjlTRWoweU1KUmx3alZAaaVREV1JWSmJtMHptVU1lZA1JDdUdTb1hGNk9aOHJ2NS1FQnhjZAXZADMG04WWdvNDMyawZDZD",
        "instagram_user_id":  "26341921652165010",
        "bg_color":           "#000000",
        "text_color":         "#FFFFFF",
        "handle":             "@femmefortepuissante",
        "description":        DESCRIPTION_DEFAULT,
        "posting_schedule": [
            {"window": "midi", "target_hour": 12, "target_minute": 45, "variation": 5},
            {"window": "soir", "target_hour": 19, "target_minute": 45, "variation": 5},
        ],
        "promo_image_url": "https://raw.githubusercontent.com/Kezzow/instagram-images/main/promo_image.jpg",
    },

    # ─── COMPTE 3 : @femme.forte.puissante ───
    # Niche : Femme independante & Ambition | Couleurs : Blanc (#FFFFFF) / Noir
    {
        "name":               "femme_forte_puissante",
        "quotes_file":        "quotes_femme_independante_ambition.txt",
        "instagram_token":    "IGAAUgf2BfEthBZAFk3bWZAHNHVabHV1VUV4amJsaVp5SDN5MzFJb0s1UTQ5eVJTdGIxSWtnbFNISVA0VFFuWjc3UW11YlFfc3F4dDZAZAbXE5VmhFMmJna05VVnNKbVZABZAkpub0FpWVJUUTAwVDBiMk5pcDE4Y25NNldJdE9GY25wNAZDZD",
        "instagram_user_id":  "26257611453889348",
        "bg_color":           "#FFFFFF",
        "text_color":         "#000000",
        "handle":             "@femme.forte.puissante",
        "description":        DESCRIPTION_DEFAULT,
        "posting_schedule": [
            {"window": "midi", "target_hour": 12, "target_minute": 0,  "variation": 5},
            {"window": "soir", "target_hour": 19, "target_minute": 0,  "variation": 5},
        ],
        "promo_image_url": "https://raw.githubusercontent.com/Kezzow/instagram-images/main/promo_image.jpg",
    },

    # ─── COMPTE 4 : @femme.forte.confiante ───
    # Niche : Glow Up & Self-Worth | Couleurs : Noir (#000000) / Blanc
    {
        "name":               "femme_forte_confiante",
        "quotes_file":        "quotes_glow_up_self_worth.txt",
        "instagram_token":    "IGAAUgf2BfEthBZAFo0N0MyM0NuVVgtNWJiWU1VZA2YyZAjRUM3BROXNZAUDBaZAFNMdnF0cjE2eHFaNHZAkcndHSk5TOVFJSjNZAeEE3a2w0TnlWcGRYbG4zc0xFUEs5UnFNeVE2dG1sb0lQVjVLNWZAHSHpsTElkVS1VQktORFlBMEZAWMAZDZD",
        "instagram_user_id":  "26320342537598995",
        "bg_color":           "#000000",
        "text_color":         "#FFFFFF",
        "handle":             "@femme.forte.confiante",
        "description":        DESCRIPTION_DEFAULT,
        "posting_schedule": [
            {"window": "midi", "target_hour": 12, "target_minute": 15, "variation": 5},
            {"window": "soir", "target_hour": 19, "target_minute": 15, "variation": 5},
        ],
        "promo_image_url": "https://raw.githubusercontent.com/Kezzow/instagram-images/main/promo_image.jpg",
    },

]

# ================= FONCTIONS UTILITAIRES =================

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('instagram_carousel_meta.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def get_font(size: int):
    """Charge une police serif avec fallback multi-OS (Ubuntu, Windows, macOS)"""
    candidates = [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
        "C:/Windows/Fonts/times.ttf",
        "times.ttf",
        "Times New Roman.ttf",
        "/Library/Fonts/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/dejavu/DejaVuSerif.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    logger.warning(f"⚠️ Aucune police trouvée pour taille {size}, utilisation du fallback PIL")
    return ImageFont.load_default()


def load_quotes(account_config: dict) -> list:
    """
    Charge les citations depuis le fichier associé au compte.
    Fallback sur les citations par défaut si fichier manquant.
    """
    quotes_file = account_config.get("quotes_file", f"quotes_{account_config['name']}.txt")

    if os.path.exists(quotes_file):
        with open(quotes_file, "r", encoding="utf-8") as f:
            quotes = [line.strip() for line in f if line.strip()]
        if quotes:
            logger.info(f"📖 Citation chargée depuis {quotes_file} ({len(quotes)} citations disponibles)")
            return quotes

    logger.warning(f"⚠️ Fichier manquant ({quotes_file}), utilisation des citations par défaut")
    return [
        "La confiance en soi est le premier secret du succès.",
        "Chaque jour est une nouvelle opportunité de briller.",
        "Le courage n'est pas l'absence de peur, mais la décision d'avancer malgré elle.",
        "Une femme forte ne suit pas la foule, elle la guide.",
        "Ton plus grand pouvoir est ta capacité à choisir.",
        "Sois la femme que tu aurais voulu rencontrer.",
        "Ta valeur ne diminue pas parce que quelqu'un ne peut pas la voir.",
        "Le succès est la somme de petits efforts répétés chaque jour.",
    ]


# ================= CRÉATION D'IMAGES =================

def create_citation_image(quote: str, account_config: dict, output_path: str) -> str:
    """Crée une image citation carrée 1080x1080"""
    width, height = 1080, 1080
    bg_color      = account_config.get("bg_color",   "#FFFFFF")
    text_color    = account_config.get("text_color",  "#000000")

    image = Image.new('RGB', (width, height), color=bg_color)
    draw  = ImageDraw.Draw(image)

    font        = get_font(58)
    handle_font = get_font(24)

    words        = quote.split()
    lines        = []
    current_line = []

    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 22:
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    line_height       = 85
    total_text_height = len(lines) * line_height
    y_position        = (height - total_text_height) // 2

    for line in lines:
        text_bbox  = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x_position = (width - text_width) // 2
        draw.text((x_position, y_position), line, fill=text_color, font=font)
        y_position += line_height

    # Handle en bas à droite — couleur identique au texte du compte
    handle = account_config["handle"]
    draw.text((width - 50, height - 40), handle, fill=text_color, font=handle_font, anchor="ra")

    image.save(output_path, 'JPEG', quality=95, optimize=True)
    return output_path


def create_story_image(citation_image_path: str, account_config: dict, output_path: str) -> str:
    """
    Crée une image story verticale 1080x1920 :
    - Image citation 960x960 centree avec bordure arrondie
    - Texte "NOUVEAU POST" 80px au-dessus de l'image
    - Pas de handle, pas d'emoji, pas de texte supplementaire
    """
    story_w, story_h = 1080, 1920
    bg_color         = account_config.get("bg_color",  "#FFFFFF")
    text_color       = account_config.get("text_color", "#000000")

    # La bordure contraste avec le fond
    border_color = "#FFFFFF" if bg_color.upper() == "#000000" else "#000000"

    story = Image.new('RGB', (story_w, story_h), color=bg_color)
    draw  = ImageDraw.Draw(story)

    # Charger et redimensionner l'image citation en 960x960
    embed_size   = 960
    citation_img = Image.open(citation_image_path).convert("RGB")
    citation_img = citation_img.resize((embed_size, embed_size), Image.LANCZOS)

    # Position centrée (légèrement remontée pour laisser de la place au texte au-dessus)
    img_x = (story_w - embed_size) // 2          # 60
    img_y = (story_h - embed_size) // 2           # 480

    # Bordure arrondie autour de l'image (dessinée avant de coller l'image)
    border_width  = 5
    border_radius = 20
    draw.rounded_rectangle(
        [img_x - border_width,
         img_y - border_width,
         img_x + embed_size + border_width,
         img_y + embed_size + border_width],
        radius=border_radius,
        outline=border_color,
        width=border_width
    )

    # Coller l'image citation
    story.paste(citation_img, (img_x, img_y))

    # Texte "NOUVEAU POST" centré, 80px au-dessus de l'image
    label_font = get_font(64)
    label_text = "NOUVEAU POST"
    label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
    label_w    = label_bbox[2] - label_bbox[0]
    label_h    = label_bbox[3] - label_bbox[1]
    label_x    = (story_w - label_w) // 2
    label_y    = img_y - 80 - label_h
    draw.text((label_x, label_y), label_text, fill=text_color, font=label_font)

    story.save(output_path, 'JPEG', quality=95, optimize=True)
    return output_path


# ================= UPLOAD GITHUB =================

def upload_to_github(image_path: str, filename: str) -> str:
    """Upload une image sur GitHub et retourne l'URL publique"""
    logger.info(f"📤 Upload GitHub: {filename}")

    with open(image_path, 'rb') as f:
        content_base64 = base64.b64encode(f.read()).decode('utf-8')

    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept":        "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Auto upload: {filename}",
        "content": content_base64,
        "branch":  GITHUB_BRANCH
    }

    response = requests.put(api_url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        download_url = response.json()['content']['download_url']
        logger.info(f"✅ Upload réussi: {download_url}")
        return download_url
    else:
        logger.error(f"❌ Erreur GitHub {response.status_code}: {response.text}")
        raise Exception(f"Erreur GitHub: {response.text}")




# ================= VALIDATION URL + PROMO IMAGE =================

def create_promo_image(account_config: dict, output_path: str) -> str:
    """
    Génère une image CTA 1080x1080 quand promo_image_url est indisponible.
    Design minimaliste : texte "LIEN EN BIO" centré + flèche, même charte graphique que la citation.
    """
    width, height = 1080, 1080
    bg_color   = account_config.get("bg_color",   "#FFFFFF")
    text_color = account_config.get("text_color",  "#000000")

    image = Image.new('RGB', (width, height), color=bg_color)
    draw  = ImageDraw.Draw(image)

    font_cta    = get_font(88)
    font_sub    = get_font(46)
    font_arrow  = get_font(120)

    # Ligne décorative haut
    draw.line([(120, 360), (960, 360)], fill=text_color, width=4)

    # Texte principal "LIEN EN BIO"
    cta_text = "LIEN EN BIO"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    cta_w    = cta_bbox[2] - cta_bbox[0]
    draw.text(((width - cta_w) // 2, 400), cta_text, fill=text_color, font=font_cta)

    # Sous-titre
    sub_lines = ["Pour acceder au", "pack complet"]
    y_sub = 530
    for line in sub_lines:
        b = draw.textbbox((0, 0), line, font=font_sub)
        draw.text(((width - (b[2] - b[0])) // 2, y_sub), line, fill=text_color, font=font_sub)
        y_sub += 60

    # Ligne décorative bas
    draw.line([(120, 700), (960, 700)], fill=text_color, width=4)

    # Flèche
    arrow = "↑"
    a_bbox = draw.textbbox((0, 0), arrow, font=font_arrow)
    draw.text(((width - (a_bbox[2] - a_bbox[0])) // 2, 740), arrow, fill=text_color, font=font_arrow)

    image.save(output_path, 'JPEG', quality=95, optimize=True)
    logger.info(f"🖼️  Image CTA générée : {output_path}")
    return output_path

# ================= FLUX META : CARROUSEL =================

def create_carousel_item(account_config: dict, image_url: str) -> str:
    """Étape 1 carrousel — crée un item image (sans caption)"""
    url  = f"https://graph.instagram.com/v20.0/{account_config['instagram_user_id']}/media"
    data = {
        "access_token":     account_config["instagram_token"],
        "image_url":        image_url,
        "media_type":       "IMAGE",
        "is_carousel_item": "true",
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Erreur item carrousel: {response.text}")
    item_id = response.json()['id']
    logger.info(f"✅ Item carrousel créé: {item_id}")
    return item_id


def wait_for_container_ready(account_config: dict, container_id: str, max_attempts: int = 10) -> bool:
    """Attend que le container soit en statut FINISHED"""
    for attempt in range(max_attempts):
        response = requests.get(
            f"https://graph.instagram.com/{container_id}",
            params={"access_token": account_config["instagram_token"], "fields": "status_code"}
        )
        if response.status_code == 200:
            status = response.json().get('status_code')
            if status == "FINISHED":
                logger.info(f"✅ Container FINISHED (tentative {attempt + 1})")
                return True
            elif status == "ERROR":
                logger.error(f"❌ Container ERROR: {response.json()}")
                return False
            logger.info(f"⏳ Container status: {status} (tentative {attempt + 1})")
        time.sleep(5)
    logger.warning("⚠️ Timeout attente container")
    return False


def create_carousel_container(account_config: dict, item_ids: list, caption: str) -> str:
    """Étape 2 carrousel — crée le container CAROUSEL avec caption"""
    url  = f"https://graph.instagram.com/v20.0/{account_config['instagram_user_id']}/media"
    data = {
        "access_token": account_config["instagram_token"],
        "media_type":   "CAROUSEL",
        "children":     json.dumps(item_ids),
        "caption":      caption,
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Erreur container carrousel: {response.text}")
    container_id = response.json()['id']
    logger.info(f"✅ Container carrousel créé: {container_id}")
    return container_id


def publish_carousel(account_config: dict, container_id: str) -> str:
    """Étape 3 carrousel — publie le carrousel"""
    if not wait_for_container_ready(account_config, container_id):
        logger.warning("⚠️ Container pas FINISHED, tentative de publication quand même")
    time.sleep(5)

    url  = f"https://graph.instagram.com/v20.0/{account_config['instagram_user_id']}/media_publish"
    data = {
        "access_token": account_config["instagram_token"],
        "creation_id":  container_id,
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Erreur publication carrousel: {response.text}")
    post_id = response.json()['id']
    logger.info(f"✅ CARROUSEL PUBLIÉ ! Post ID: {post_id}")
    return post_id


# ================= FLUX META : STORY =================

def create_story_container(account_config: dict, image_url: str) -> str:
    """Étape 1 story — crée le container STORIES"""
    url  = f"https://graph.instagram.com/v20.0/{account_config['instagram_user_id']}/media"
    data = {
        "access_token": account_config["instagram_token"],
        "media_type":   "STORIES",
        "image_url":    image_url,
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Erreur container story: {response.text}")
    container_id = response.json()['id']
    logger.info(f"✅ Container story créé: {container_id}")
    return container_id


def publish_story(account_config: dict, container_id: str) -> str:
    """Étape 2 story — publie la story"""
    if not wait_for_container_ready(account_config, container_id):
        logger.warning("⚠️ Story container pas FINISHED, tentative de publication quand même")
    time.sleep(3)

    url  = f"https://graph.instagram.com/v20.0/{account_config['instagram_user_id']}/media_publish"
    data = {
        "access_token": account_config["instagram_token"],
        "creation_id":  container_id,
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Erreur publication story: {response.text}")
    story_id = response.json()['id']
    logger.info(f"✅ STORY PUBLIEE ! Story ID: {story_id}")
    return story_id


# ================= ORCHESTRATION =================

def post_carousel_now(account_config: dict) -> bool:
    """
    Publie un carrousel + une story pour le compte donné.
    Flux complet :
      1. Citation aléatoire depuis le fichier du compte
      2. Création image carrousel (1080x1080) + image story (1080x1920)
      3. Upload des 2 images sur GitHub
      4. Post carrousel (3 étapes Meta)
      5. Attente 30s puis post story (2 étapes Meta)
      6. Nettoyage fichiers locaux
    """
    logger.info(f"{'=' * 50}")
    logger.info(f"🎯 DÉMARRAGE POST: {account_config['handle']}")

    timestamp        = datetime.now().strftime("%Y%m%d_%H%M%S")
    carousel_path    = f"carousel_{account_config['name']}_{timestamp}.jpg"
    promo_upload     = None
    story_path       = f"story_{account_config['name']}_{timestamp}.jpg"
    carousel_github  = f"carousel_{account_config['name']}_{timestamp}.jpg"
    story_github     = f"story_{account_config['name']}_{timestamp}.jpg"

    try:
        # ── 1. Citation ──
        quotes = load_quotes(account_config)
        quote  = random.choice(quotes)
        logger.info(f"💬 Citation sélectionnée: \"{quote}\"")

        # ── 2. Création des images ──
        logger.info("🖼️  Création image carrousel...")
        create_citation_image(quote, account_config, carousel_path)

        logger.info("🖼️  Création image story...")
        create_story_image(carousel_path, account_config, story_path)

        # ── 3. Upload GitHub ──
        logger.info("📤 Upload images sur GitHub...")
        carousel_url = upload_to_github(carousel_path, carousel_github)
        story_url    = upload_to_github(story_path,    story_github)

        # ── 4. Post carrousel (3 étapes Meta) ──
        # ── Slide 2 : promo image re-uploadée avec nom timestampé ──
        # Meta ne peut fetcher que des URLs fraîches (pas de CDN cache GitHub).
        # Solution : re-uploader le fichier promo local avec un nom unique à chaque post.
        promo_source = account_config.get("promo_image_path", "promo_image.jpg")
        promo_upload = f"promo_{account_config['name']}_{timestamp}.jpg"

        if os.path.exists(promo_source):
            logger.info(f"📤 Re-upload promo image depuis fichier local : {promo_source}")
            promo_url = upload_to_github(promo_source, promo_upload)
        else:
            logger.warning(
                f"⚠️ Fichier promo local introuvable ({promo_source})\n"
                f"   → Génération d'une image CTA de substitution..."
            )
            create_promo_image(account_config, promo_upload)
            promo_url = upload_to_github(promo_upload, promo_upload)
            if os.path.exists(promo_upload):
                os.remove(promo_upload)

        logger.info("📦 [CARROUSEL] Création des items...")
        item1_id = create_carousel_item(account_config, carousel_url)
        time.sleep(2)
        item2_id = create_carousel_item(account_config, promo_url)

        logger.info("📦 [CARROUSEL] Création du container...")
        time.sleep(3)
        container_id = create_carousel_container(
            account_config, [item1_id, item2_id], account_config["description"]
        )

        logger.info("🚀 [CARROUSEL] Publication...")
        post_id = publish_carousel(account_config, container_id)
        logger.info(f"✅ CARROUSEL PUBLIÉ: {post_id}")

        # ── 5. Story 30 secondes après ──
        logger.info("⏳ Attente 30 secondes avant publication story...")
        time.sleep(30)

        logger.info("📸 [STORY] Création container story...")
        story_container_id = create_story_container(account_config, story_url)

        logger.info("🚀 [STORY] Publication...")
        story_id = publish_story(account_config, story_container_id)
        logger.info(f"✅ STORY PUBLIÉE: {story_id}")

        # ── 6. Nettoyage ──
        for path in [carousel_path, promo_upload, story_path]:
            if path and os.path.exists(path):
                os.remove(path)
        logger.info("🧹 Images locales supprimées")

        logger.info(f"✅ POST COMPLET: carrousel={post_id} | story={story_id}")
        return True

    except Exception as e:
        logger.error(f"❌ ERREUR post {account_config['handle']}: {e}")
        import traceback
        traceback.print_exc()
        for path in [carousel_path, promo_upload, story_path]:
            if path and os.path.exists(path):
                os.remove(path)
        return False


# ================= BOUCLE PRINCIPALE =================

def main_loop():
    """Boucle 24/7 — vérifie toutes les minutes si un créneau de post est atteint"""
    logger.info("🔄 Démarrage boucle 24/7 (carrousels + stories)...")
    posted_windows = {}

    while True:
        now = datetime.now(PARIS_TZ)
        logger.info(f"⏰ {now.strftime('%H:%M')} (Paris)")

        for account_config in ACCOUNTS:
            key = account_config["handle"]
            if key not in posted_windows:
                posted_windows[key] = {}

            for schedule in account_config.get("posting_schedule", []):
                target_time = now.replace(
                    hour=schedule["target_hour"],
                    minute=schedule["target_minute"],
                    second=0, microsecond=0
                )
                window_start     = target_time - timedelta(minutes=schedule["variation"])
                window_end       = target_time + timedelta(minutes=schedule["variation"])
                window_today_key = f"{now.date().isoformat()}_{schedule['window']}"

                if window_start <= now <= window_end and window_today_key not in posted_windows[key]:
                    logger.info(f"🎯 Créneau atteint: {key} ({schedule['window']})")
                    success = post_carousel_now(account_config)
                    if success:
                        posted_windows[key][window_today_key] = True

        time.sleep(60)


# ================= MODE TEST =================

def test_carousel_now():
    """Mode test interactif — poste immédiatement sur tous les comptes"""
    print("\n" + "=" * 60)
    print("🤖 TEST CARROUSEL + STORY META")
    print("=" * 60)
    print("\n💡 Flux pour chaque compte :")
    print("  1. Lire citation depuis fichier .txt")
    print("  2. Créer image carrousel 1080x1080")
    print("  3. Créer image story 1080x1920 (NOUVEAU POST + bordure)")
    print("  4. Upload 2 images GitHub")
    print("  5. Post carrousel (3 étapes Meta)")
    print("  6. Attendre 30s → Post story (2 étapes Meta)")

    print(f"\n📱 Comptes configurés ({len(ACCOUNTS)}) :")
    for acc in ACCOUNTS:
        print(f"  • {acc['handle']:<30} | bg={acc['bg_color']} | fichier={acc['quotes_file']}")

    print("\n❓ Continuer ? (oui/non): ", end="")
    if input().lower() != "oui":
        print("❌ Annulé")
        return

    results = []
    for account_config in ACCOUNTS:
        print(f"\n{'─' * 50}")
        print(f"📱 COMPTE: {account_config['handle']}")
        success = post_carousel_now(account_config)
        results.append((account_config["handle"], success))

    print("\n" + "=" * 60)
    print("📊 RÉSULTATS")
    print("=" * 60)
    success_count = sum(1 for _, s in results if s)
    for handle, success in results:
        print(f"  {'✅' if success else '❌'} {handle}")
    print(f"\n{'✅ SUCCÈS TOTAL' if success_count == len(ACCOUNTS) else '⚠️ PARTIEL'} : {success_count}/{len(ACCOUNTS)} comptes")
    print("💡 Vérifie tes comptes Instagram !")


# ================= MAIN =================

def main():
    global logger
    logger = setup_logging()
    logger.info("INSTAGRAM CARROUSEL + STORY META - Démarrage (4 comptes)")

    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--test":
            test_carousel_now()
        else:
            main_loop()
    except KeyboardInterrupt:
        logger.info("\n⏹️ Service interrompu par l'utilisateur")
    except Exception as e:
        logger.error(f"💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        logger.info("🔄 Redémarrage dans 5 minutes...")
        time.sleep(300)
        main()


if __name__ == "__main__":
    main()
