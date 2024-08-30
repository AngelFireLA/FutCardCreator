import os
import random

from PIL import Image

from fut_card_creator.utils import get_flag_image, get_club_logo, get_important_stats, get_card_stats_pos, \
    add_image_to_image, add_text_to_image, calculate_overall_ratings

current_folder = os.path.dirname(os.path.abspath(__file__))


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

    def weighted_random_choice(self, stats, weights):
        total_weight = sum(weights.values())
        random_choice = random.uniform(0, total_weight)
        cumulative_weight = 0
        for stat, weight in weights.items():
            cumulative_weight += weight
            if random_choice <= cumulative_weight:
                return stat
        return random.choice(list(stats.keys()))  # fallback

    def update_stats_based_on_overall(self, new_overall, calculate_type=3):
        overall_diff = new_overall - self.overall
        original_stats = True
        for stat in self.stats.keys():
            if stat not in self.default_stats:
                original_stats = False
        if not original_stats or self.position not in self.positions:
            calculate_type = 1
        if calculate_type == 1:
            for i in random.sample(self.stats.keys(), 3):
                self.stats[i] += random.randint(max(1, int(overall_diff / 2)), overall_diff * 2)
            for i in random.sample(self.stats.keys(), 3):
                self.stats[i] += random.randint(1, max(1, overall_diff))
        elif calculate_type == 2:
            stats_to_increase = random.sample(get_important_stats(self.position), 2)
            for stat in stats_to_increase:
                self.stats[stat] += random.randint(max(1, int(overall_diff / 2)), overall_diff * 2)
            other_stats_to_increase = random.sample(
                [stat for stat in self.stats.keys() if stat not in stats_to_increase], 2)
            for stat in other_stats_to_increase:
                self.stats[stat] += random.randint(1, max(1, overall_diff))
        elif calculate_type == 3:
            original_real_overall = calculate_overall_ratings(self.stats)[self.position]
            current_real_overall = original_real_overall

            # Create a weight mapping based on the position's formula
            position_weights = {
                "ST": {"SHO": 0.40, "PAC": 0.30, "DRI": 0.20, "PHY": 0.10},
                "RW": {"DRI": 0.35, "PAC": 0.30, "SHO": 0.25, "PAS": 0.10},
                "LW": {"DRI": 0.35, "PAC": 0.30, "SHO": 0.25, "PAS": 0.10},
                "CF": {"SHO": 0.40, "DRI": 0.30, "PAC": 0.20, "PAS": 0.10},
                "CAM": {"DRI": 0.35, "PAS": 0.35, "SHO": 0.25, "PAC": 0.05},
                "CM": {"PAS": 0.45, "DRI": 0.30, "DEF": 0.10, "SHO": 0.15},
                "CDM": {"DEF": 0.30, "PAS": 0.30, "PHY": 0.30, "DRI": 0.10},
                "RM": {"PAC": 0.35, "DRI": 0.25, "PAS": 0.25, "SHO": 0.15},
                "LM": {"PAC": 0.35, "DRI": 0.25, "PAS": 0.25, "SHO": 0.15},
                "LB": {"DEF": 0.30, "PAC": 0.35, "PHY": 0.10, "PAS": 0.25},
                "RB": {"DEF": 0.30, "PAC": 0.35, "PHY": 0.10, "PAS": 0.25},
                "CB": {"DEF": 0.45, "PHY": 0.40, "PAC": 0.15},
            }

            # Set a base weight for non-key stats
            base_weight = 0.05

            # Get the weight distribution for the position
            position_formula_weights = position_weights.get(self.position, {})

            # Initialize the weights with the base weight for all stats
            weights = {stat: base_weight for stat in self.stats.keys()}

            # Update the weights with the position-specific values
            for stat, weight in position_formula_weights.items():
                weights[stat] = weight

            while current_real_overall != original_real_overall + overall_diff:
                stat_to_change = self.weighted_random_choice(self.stats, weights)
                self.stats[stat_to_change] += 1
                self.stats[stat_to_change] = min(99, self.stats[stat_to_change])
                current_real_overall = calculate_overall_ratings(self.stats)[self.position]

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
        image_path = os.path.join(current_folder, f'images/card_templates/{self.card_type}.png')
        self.image = Image.open(image_path)
        font_path = os.path.join(current_folder, 'fonts/DINPro CondBold.otf')

        # Add name
        name_font_size = 95
        name_position = (356, 645)
        self.image = add_text_to_image(self.image, self.player.name.upper(), name_position, font_path, name_font_size,
                                       center=True)

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
        self.image = add_text_to_image(self.image, str(self.player.overall), overall_position, font_path,
                                       overall_font_size, center=True)

        # Add position
        position_font_size = 70
        position_position = (150, 275)
        self.image = add_text_to_image(self.image, self.player.position, position_position, font_path,
                                       position_font_size, center=True)

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
