from dmc_api import *

print "Druga Attack: %.f"%max_stat_boosted(get_card('Druga'), 'Attack')
print "Druga Speed: %.f"%max_stat_boosted(get_card('Druga'), 'Speed')

print "RNM Attack: %.f"%max_stat_boosted(get_card('Red-nosed Minotaur'), 'Attack')
print "RNM Speed: %.f"%max_stat_boosted(get_card('Red-nosed Minotaur'), 'Speed')

#print get_card_buff_abilities(get_card('Liquid Metal'))
print "Druga:", buff_stats(get_card('Druga'))
print "RNM:", buff_stats(get_card('Red-nosed Minotaur'))
#print_sorted_by(get_all_five_stars(), "Speed")