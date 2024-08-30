import time

from fut_card_creator.fut_card_creator import *

start_time = time.time()
player_stats = {"PAC": 80, "SHO": 87, "PAS": 90, "DRI": 94, "DEF": 34, "PHY": 64}
messi = Player("messi", "messi.png", "Paris Saint-Germain", "Argentina", 90, "RW", player_stats)
calculate_overall_ratings(player_stats, debug=True)
card = Card(messi, "future_star")
card.create_image()
output_path = 'test.png'
card.export_image(output_path)
card.update_overall(95)
calculate_overall_ratings(player_stats, debug=True)
card.create_image()
output_path = 'test2.png'
card.export_image(output_path)

# #messi
# player_stats = {"PAC": 74, "SHO": 88, "PAS": 94, "DRI": 87, "DEF": 65, "PHY": 78}
# calculate_overall_ratings(player_stats)
#
# #kimmich
# player_stats = {"PAC": 70, "SHO": 74, "PAS": 88, "DRI": 83, "DEF": 82, "PHY": 78}
# calculate_overall_ratings(player_stats)
#
# #balde
# player_stats = {"PAC": 91, "SHO": 48, "PAS": 73, "DRI": 78, "DEF": 75, "PHY": 64}
# calculate_overall_ratings(player_stats)
#
# #alexander arnold
# player_stats = {"PAC": 76, "SHO": 71, "PAS": 90, "DRI": 80, "DEF": 80, "PHY": 74}
# calculate_overall_ratings(player_stats)
#
# #de jong
# player_stats = {"PAC": 79, "SHO": 56, "PAS": 75, "DRI": 74, "DEF": 89, "PHY": 80}
# calculate_overall_ratings(player_stats)
#
# #kroos
# player_stats = {"PAC": 51, "SHO": 80, "PAS": 90, "DRI": 81, "DEF": 71, "PHY": 71}
# calculate_overall_ratings(player_stats)
#
# #haaland
# player_stats = {"PAC": 89, "SHO": 93, "PAS": 68, "DRI": 81, "DEF": 45, "PHY": 88}
# calculate_overall_ratings(player_stats)
#
# #mbappé
# player_stats = {"PAC": 97, "SHO": 90, "PAS": 80, "DRI": 92, "DEF": 36, "PHY": 78}
# calculate_overall_ratings(player_stats)
