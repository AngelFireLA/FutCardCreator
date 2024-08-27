import os

import requests
from fuzzywuzzy import process
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def get_closest_country_name(query):
    response = requests.get("https://restcountries.com/v3.1/all")
    if response.status_code == 200:
        country_names = [country['name']['common'] for country in response.json()]
        closest_match = process.extractOne(query, country_names)
        return closest_match[0]
    else:
        return None


def get_flag_image(country_name):
    # Create cache directory if it doesn't exist
    cache_dir = "images/nation_cache"
    # Construct the file path for the cached image
    cache_file_path = os.path.join(cache_dir, f"{country_name}.png")

    # Check if the flag is already cached
    if os.path.exists(cache_file_path):
        return Image.open(cache_file_path)

    # Fetch the flag image from the API if not cached
    closest_country_name = get_closest_country_name(country_name)


    if closest_country_name:



        response = requests.get(f"https://restcountries.com/v3.1/name/{closest_country_name}")
        if response.status_code == 200:
            country_data = response.json()[0]
            flag_url = country_data['flags']['png']

            # Fetch the flag image from the URL
            image_response = requests.get(flag_url)
            if image_response.status_code == 200:
                image = Image.open(BytesIO(image_response.content))

                # Save the flag image to the cache
                image.save(cache_file_path)

                return image
    return None

def add_image_to_image(original_image, image, position, size=None, center=False):
    if size:
        image = image.resize(size)

    # Ensure the pasted image has an alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Ensure the original image is in a mode that supports alpha (if necessary)
    if original_image.mode != 'RGBA':
        original_image = original_image.convert('RGBA')

    if center:
        # Calculate the centered position
        image_width, image_height = image.size
        position = (position[0] - image_width // 2, position[1] - image_height // 2)

    # Paste the image onto the original image
    original_image.paste(image, position, image)

    return original_image

def add_text_to_image(image, text, position, font_path, font_size, center=False):
    # Initialize ImageDraw object
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    if not center:
        # Add text to the image
        draw.text(position, text, font=font, fill=(73, 57, 15))
    else:
        # Calculate text bounding box
        text_bbox = draw.textbbox(position, text, font=font)

        # Calculate centered position
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        centered_position = (position[0] - text_width // 2, position[1] - text_height // 2)

        # Add centered text to the image
        draw.text(centered_position, text, font=font, fill=(73, 57, 15))  # Black text


    return image

def get_card_stats_pos(stats:list=None):
    if not stats:
        stats = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
    left_x = 180
    right_x = 520
    basic_y = 750
    y_space = 80

    stat_text_space = 80
    num_y_offset = 5

    stats_text_pos_dict = {
        stats[0]: (left_x, basic_y),
        stats[1]: (left_x, basic_y + y_space),
        stats[2]: (left_x, basic_y + y_space * 2),
        stats[3]: (right_x, basic_y),
        stats[4]: (right_x, basic_y + y_space),
        stats[5]: (right_x, basic_y + y_space * 2)
    }
    stats_num_pos_dict = {
        stats[0]: (left_x - stat_text_space, basic_y - num_y_offset),
        stats[1]: (left_x - stat_text_space, basic_y + y_space - num_y_offset),
        stats[2]: (left_x - stat_text_space, basic_y + y_space * 2 - num_y_offset),
        stats[3]: (right_x - stat_text_space, basic_y - num_y_offset),
        stats[4]: (right_x - stat_text_space, basic_y + y_space - num_y_offset),
        stats[5]: (right_x - stat_text_space, basic_y + y_space * 2 - num_y_offset)
    }
    return stats_text_pos_dict, stats_num_pos_dict

def fetch_all_teams(api_key="3"):
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/search_all_teams.php?l="
    leagues = [
        "French Ligue 1",
        "French Ligue 2",
        "English Premier League",
        "English League Championship"
        "Spanish La Liga",
        "Italian Serie A",
        "German Bundesliga",
        "Dutch Eredivisie",
        "Portuguese Primeira Liga",
        "Belgian First Division A",
    ]

    teams = []

    for league in leagues:
        response = requests.get(url + league)
        if response.status_code == 200:
            league_data = response.json()
            if league_data['teams']:
                teams.extend(league_data['teams'])

    return teams

def get_important_stats(stat):
    important_stats = {
        "ST": ["SHO", "DRI", "PAC"],
        "RW": ["SHO", "DRI", "PAC"],
        "LW": ["SHO", "DRI", "PAC"],
        "LM": ["DRI", "PAC", "PAS"],
        "RM": ["DRI", "PAC", "PAS"],
        "CAM": ["SHO", "DRI", "PAC"],
        "CF": ["SHO", "DRI", "PAS"],
        "CM": ["SHO", "DRI", "PAS", "DEF"],
        "CDM": ["PHY", "DEF", "PAS"],
        "LB": ["DEF", "PAC", "PAS"],
        "RB": ["DEF", "PAC", "PAS"],
        "CB": ["DEF", "PHY", "PAC"]
    }
    if stat in important_stats:
        return important_stats[stat]
    else:
        return []

def get_closest_team_name(club_name, teams):
    team_names = [team['strTeam'] for team in teams]
    closest_match = process.extractOne(club_name, team_names)
    return closest_match[0]


def get_club_logo(club_name, api_key="3"):
    # Create cache directory if it doesn't exist
    cache_dir = "images/club_logo_cache"
    os.makedirs(cache_dir, exist_ok=True)

    # Construct the file path for the cached image
    cache_file_path = os.path.join(cache_dir, f"{club_name.lower().replace(' ', '_')}.png")

    # Check if the logo is already cached
    if os.path.exists(cache_file_path):
        return Image.open(cache_file_path)

    # Fetch all teams and find the closest match
    teams = fetch_all_teams(api_key)
    closest_team_name = get_closest_team_name(club_name, teams)

    # Fetch the club logo from the API if not cached
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/searchteams.php?t={closest_team_name}"
    response = requests.get(url)
    if response.status_code == 200:
        team_data = response.json()
        if team_data['teams']:
            if "strBadge" not in team_data['teams'][0]:
                logo_url = team_data['teams'][0]['strTeamBadge']
            else:
                logo_url = team_data['teams'][0]['strBadge']
            if logo_url:
                # Fetch the logo image from the URL
                image_response = requests.get(logo_url)
                if image_response.status_code == 200:
                    image = Image.open(BytesIO(image_response.content))

                    # Save the logo image to the cache
                    image.save(cache_file_path)

                    return image
    return None

def calculate_overall_ratings(stats):
    coeff_multiplier = 1.022
    formulas = {
        "ST": lambda s: (coeff_multiplier*0.40 * s["SHO"]) + (coeff_multiplier*0.30 * s["PAC"]) + (coeff_multiplier*0.20 * s["DRI"]) + (coeff_multiplier*0.10 * s["PHY"]),
        "RW": lambda s: (coeff_multiplier*0.35 * s["DRI"]) + (coeff_multiplier*0.30 * s["PAC"]) + (coeff_multiplier*0.25 * s["SHO"]) + (coeff_multiplier*0.10 * s["PAS"]),
        "LW": lambda s: (coeff_multiplier*0.35 * s["DRI"]) + (coeff_multiplier*0.30 * s["PAC"]) + (coeff_multiplier*0.25 * s["SHO"]) + (coeff_multiplier*0.10 * s["PAS"]),
        "CF": lambda s: (coeff_multiplier*0.40 * s["SHO"]) + (coeff_multiplier*0.30 * s["DRI"]) + (coeff_multiplier*0.20 * s["PAC"]) + (coeff_multiplier*0.10 * s["PAS"]),
        "CAM": lambda s: (coeff_multiplier*0.35 * s["DRI"]) + (coeff_multiplier*0.35 * s["PAS"]) + (coeff_multiplier*0.25 * s["SHO"]) + (coeff_multiplier*0.05 * s["PAC"]),
        "CM": lambda s: (coeff_multiplier*0.45 * s["PAS"]) + (coeff_multiplier*0.30 * s["DRI"]) + (coeff_multiplier*0.10 * s["DEF"]) + (coeff_multiplier*0.15 * s["SHO"]),
        "CDM": lambda s: (coeff_multiplier*0.30 * s["DEF"]) + (coeff_multiplier*0.30 * s["PAS"]) + (coeff_multiplier*0.30 * s["PHY"]) + (coeff_multiplier*0.10 * s["DRI"]),
        "RM": lambda s: (coeff_multiplier*0.35 * s["PAC"]) + (coeff_multiplier*0.25 * s["DRI"]) + (coeff_multiplier*0.25 * s["PAS"]) + (coeff_multiplier*0.15 * s["SHO"]),
        "LM": lambda s: (coeff_multiplier*0.35 * s["PAC"]) + (coeff_multiplier*0.25 * s["DRI"]) + (coeff_multiplier*0.25 * s["PAS"]) + (coeff_multiplier*0.15 * s["SHO"]),
        "LB": lambda s: (coeff_multiplier*0.30 * s["DEF"]) + (coeff_multiplier*0.35 * s["PAC"]) + (coeff_multiplier*0.10 * s["PHY"]) + (coeff_multiplier*0.25 * s["PAS"]),
        "RB": lambda s: (coeff_multiplier*0.30 * s["DEF"]) + (coeff_multiplier*0.35 * s["PAC"]) + (coeff_multiplier*0.10 * s["PHY"]) + (coeff_multiplier*0.25 * s["PAS"]),
        "CB": lambda s: (coeff_multiplier*0.45 * s["DEF"]) + (coeff_multiplier*0.40 * s["PHY"]) + (coeff_multiplier*0.15 * s["PAC"]),
    }

    for position, formula in formulas.items():
        ovr = formula(stats)
        print(f"{position}: {round(ovr)}")
    print()