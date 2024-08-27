import time

from PIL import Image, ImageDraw, ImageFont
from utils import *

import random


class Player:
    positions = ["ST", "RW", "LW", "CF", "CAM", "CM", "CDM", "RM", "LM", "LB", "CB", "RB"]
    default_stats = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]

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

    def update_stats_based_on_overall(self, new_overall):
        overall_diff = new_overall - self.overall
        original_stats = True
        for stat in self.stats.keys():
            if stat not in self.default_stats:
                original_stats = False
        if original_stats and self.position not in self.positions:
            for i in random.sample(self.stats.keys(), 3):
                self.stats[i] += overall_diff
            for i in random.sample(self.stats.keys(), 3):
                self.stats[i] += int(overall_diff/2)
        else:
            stats_to_increase = random.sample(get_important_stats(self.position), 2)
            for stat in stats_to_increase:
                self.stats[stat] += random.randint(1, overall_diff)
            other_stats_to_increase = random.sample([stat for stat in self.stats.keys() if stat not in stats_to_increase], 2)
            for stat in other_stats_to_increase:
                self.stats[stat] += int(overall_diff / 2)



    def update_overall(self, new_overall, update_stats=True):
        if update_stats:
            self.update_stats_based_on_overall(new_overall)
        self.overall = new_overall
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

    def update_overall(self, new_overall):
        self.player.update_overall(new_overall)





start_time = time.time()
player_stats = {"PAC": 80, "SHO": 87, "PAS": 90, "DRI": 94, "DEF": 34, "PHY": 64}
messi = Player("messi", "messi.png", "Paris Saint-Germain", "Argentina", 91, "RW", player_stats)
calculate_overall_ratings(player_stats)
card = Card(messi, "rare_gold")
card.create_image()
output_path = 'test.png'
card.export_image(output_path)
card.update_overall(94)
card.create_image()
output_path = 'test2.png'
card.export_image(output_path)

#messi
player_stats = {"PAC": 74, "SHO": 88, "PAS": 94, "DRI": 87, "DEF": 65, "PHY": 78}
calculate_overall_ratings(player_stats)

#kimmich
player_stats = {"PAC": 70, "SHO": 74, "PAS": 88, "DRI": 83, "DEF": 82, "PHY": 78}
calculate_overall_ratings(player_stats)

#balde
player_stats = {"PAC": 91, "SHO": 48, "PAS": 73, "DRI": 78, "DEF": 75, "PHY": 64}
calculate_overall_ratings(player_stats)

#alexander arnold
player_stats = {"PAC": 76, "SHO": 71, "PAS": 90, "DRI": 80, "DEF": 80, "PHY": 74}
calculate_overall_ratings(player_stats)

#de jong
player_stats = {"PAC": 79, "SHO": 56, "PAS": 75, "DRI": 74, "DEF": 89, "PHY": 80}
calculate_overall_ratings(player_stats)

#kroos
player_stats = {"PAC": 51, "SHO": 80, "PAS": 90, "DRI": 81, "DEF": 71, "PHY": 71}
calculate_overall_ratings(player_stats)

#haaland
player_stats = {"PAC": 89, "SHO": 93, "PAS": 68, "DRI": 81, "DEF": 45, "PHY": 88}
calculate_overall_ratings(player_stats)

#mbappé
player_stats = {"PAC": 97, "SHO": 90, "PAS": 80, "DRI": 92, "DEF": 36, "PHY": 78}
calculate_overall_ratings(player_stats)
