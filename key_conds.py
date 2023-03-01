""" The available keys, if executed generate "all_conditions.json" """

key_to_conditions = {'21': 'Byvind', '39': 'Daggpunktstemperatur',
                     '11': 'Global Irradians (svenska stationer)',
                     '22': 'Lufttemperatur_M', '26': 'Lufttemperatur_D_min2',
                     '27': 'Lufttemperatur_D_max2', '19': 'Lufttemperatur_D_min1',
                     '1': 'Lufttemperatur_H', '2': 'Lufttemperatur_D_medel',
                     '20': 'Lufttemperatur_D_max1',
                     '9': 'Lufttryck reducerat havsytans nivå',
                     '24': 'Långvågs-Irradians',
                     '40': 'Markens tillstånd',
                     '25': 'Max av MedelVindhastighet',
                     '28': 'Molnbas_H_lägsta', '30': 'Molnbas_H_andra',
                     '32': 'Molnbas_H_tredje', '34': 'Molnbas_H_fjärde',
                     '29': 'Molnmängd_H_lägsta', '31': 'Molnmängd_H_andra',
                     '33': 'Molnmängd_H_tredje', '35': 'Molnmängd_H_fjärde',
                     '17': 'Nederbörd_12H', '18': 'Nederbörd_D',
                     '15': 'Nederbördsintensitet_15m_max',
                     '38': 'Nederbördsintensitet_15m_medel',
                     '23': 'Nederbördsmängd_M', '14': 'Nederbördsmängd_15m',
                     '5': 'Nederbördsmängd_D', '7': 'Nederbördsmängd_H',
                     '6': 'Relativ Luftfuktighet', '13': 'Rådande väder',
                     '12': 'Sikt', '8': 'Snödjup', '10': 'Solskenstid',
                     '16': 'Total molnmängd', '4': 'Vindhastighet',
                     '3': 'Vindriktning'}

condition_to_key = {value: key for key, value in key_to_conditions.items()}

if __name__ == "__main__":
    import json
    with open("all_conditions.json", "w") as file:
        json.dump(list(key_to_conditions.values()), file, ensure_ascii=False)
