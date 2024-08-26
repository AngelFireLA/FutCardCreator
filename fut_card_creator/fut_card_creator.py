import time

from PIL import Image, ImageDraw, ImageFont
from utils import *


class Player:
    def __init__(self, name, photo_path, club, nation, overall, position, stats):
        self.name = name
        self.photo_path = photo_path
        self.club = club
        self.nation = nation
        self.overall = overall
        self.position = position
        self.stats = stats

    def update_stat(self, stat, new_value):
        self.stats[stat] = new_value

class Card:
    def __init__(self, player, card_type):
        self.player = player
        self.card_type = card_type
        self.image = None

    def create_image(self):
        image_path = f'images/card_templates/{self.card_type}.png'
        self.image = Image.open(image_path)
        font_path = 'fonts/DINPro CondBold.otf'

        # Add name
        name_font_size = 95
        name_position = (356, 645)
        self.image = add_text_to_image(self.image, self.player.name.upper(), name_position, font_path, name_font_size, center=True)

        # Add club
        club_image = get_club_logo(self.player.club)
        club_position = (150, 520)
        club_size = (110, 110)
        self.image = add_image_to_image(self.image, club_image, club_position, club_size, center=True)

        # Add nation
        flag_image = get_flag_image(self.player.nation)
        flag_position = (150, 395)
        flag_size = (100, 60)
        self.image = add_image_to_image(self.image, flag_image, flag_position, flag_size, center=True)

        # Add overall
        overall_font_size = 150
        overall_position = (150, 150)
        self.image = add_text_to_image(self.image, str(self.player.overall), overall_position, font_path, overall_font_size, center=True)

        # Add position
        position_font_size = 70
        position_position = (150, 275)
        self.image = add_text_to_image(self.image, self.player.position, position_position, font_path, position_font_size, center=True)

        # Add photo
        if self.player.photo_path:
            photo = Image.open(self.player.photo_path)
            photo_size = (490, 490)
            photo_position = (450, 363)
            self.image = add_image_to_image(self.image, photo, photo_position, photo_size, center=True)

        # Add stats
        stats_text_pos, stats_num_pos = get_card_stats_pos()
        font_size = 70
        num_font_size = 75
        for stat in self.player.stats:
            text = stat
            position = stats_text_pos[text]  # x, y position of the text
            self.image = add_text_to_image(self.image, text, position, font_path, font_size)

            num = str(self.player.stats[stat])
            position = stats_num_pos[text]
            self.image = add_text_to_image(self.image, num, position, font_path, num_font_size)

    def update_stat(self, stat, new_value):
        self.player.update_stat(stat, new_value)

    def export_image(self, file_path):
        self.image.save(file_path)


start_time = time.time()
player = Player("messi", "messi.png", "Paris Saint-Germain", "Argentina", 91, "RW", {"PAC": 81, "SHO": 89, "PAS": 90, "DRI": 94, "DEF": 34, "PHY": 64})
card = Card(player, "rare_gold")
card.create_image()
output_path = 'test.png'
card.export_image(output_path)
print(time.time()-start_time)
