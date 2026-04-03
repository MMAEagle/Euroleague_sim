standings = {'Fener':23, 'Oly':22, 'Real':22, 'Hapoel':21, 'Valencia':21, 'Zalgiris':21, 'Pao': 20, 'Barca':20, 'Rstar': 19, 'Monaco': 19, 'Macabi': 18, 'Dubai':18, 
			'Armani': 0, 'Partizan': 0, 'Bayern': 0, 'Pari': 0, 'Bologna': 0, 'Baskonia': 0, 'Efes': 0, 'Asvel': 0}

matches_35 = [('Asvel', 'Oly'), ('Baskonia', 'Real'), ('Bologna', 'Valencia')]

matches_36 = [('Hapoel', 'Fener'), ('Zalgiris', 'Dubai'), ('Rstar', 'Pari'), ('Oly', 'Real'), ('Barca', 'Pao'),
				('Valencia', 'Armani'), ('Baskonia', 'Macabi'), ('Monaco', 'Asvel')
]

matches_37 = [('Hapoel', 'Oly'), ('Fener', 'Real'), ('Valencia', 'Pao'), ('Pari', 'Macabi'), ('Monaco', 'Barca'), 
				('Dubai', 'Efes'), ('Partizan', 'Zalgiris'), ('Asvel', 'Rstar') 

]

matches_30 = [('Macabi', 'Hapoel')]

matches_38 = [('Asvel','Fener'), ('Macabi','Bologna'), ('Oly','Armani'), ('Real','Rstar'), ('Dubai','Valencia'), 
				('Zalgiris','Pari'), ('Monaco','Hapoel'), ('Pao','Efes'), ('Barca','Bayern')
]

h2h_results={
	tuple(sorted(('Fener', 'Oly'))) : {'Fener': 1, 'Oly': 1},
	tuple(sorted(('Fener', 'Real'))) : {'Fener': 0, 'Real': 1},
	tuple(sorted(('Oly', 'Real'))) :{'Oly': 0, 'Real': 1},
	tuple(sorted(('Hapoel', 'Valencia'))) :{'Hapoel':1, 'Valencia': 1},
	tuple(sorted(('Hapoel', 'Zalgiris'))) :{'Hapoel':0, 'Zalgiris': 2},
	tuple(sorted(('Hapoel', 'Pao'))) :{'Hapoel':1, 'Pao': 1},
	tuple(sorted(('Hapoel', 'Barca'))) :{'Hapoel': 2, 'Barca': 0},
	tuple(sorted(('Valencia', 'Zalgiris'))) :{'Valencia':1, 'Zalgiris': 1},
	tuple(sorted(('Valencia', 'Pao'))) :{'Valencia':1, 'Pao': 0},
	tuple(sorted(('Valencia', 'Barca'))) :{'Valencia': 0, 'Barca': 2},
	tuple(sorted(('Zalgiris', 'Pao'))) :{'Zalgiris': 0, 'Pao': 2},
	tuple(sorted(('Zalgiris', 'Barca'))) :{'Zalgiris':2, 'Barca': 0},
	tuple(sorted(('Pao', 'Barca'))) :{'Pao':0, 'Barca': 1},
	tuple(sorted(('Pao', 'Rstar'))) :{'Pao':1, 'Rstar': 1},
	tuple(sorted(('Pao', 'Monaco'))) :{'Pao':1, 'Monaco': 1},
	tuple(sorted(('Barca', 'Rstar'))) :{'Barca':2, 'Rstar': 0},
	tuple(sorted(('Barca', 'Monaco'))) :{'Barca':0, 'Monaco': 1},
	tuple(sorted(('Rstar', 'Monaco'))) :{'Rstar': 2, 'Monaco': 0},
	tuple(sorted(('Rstar', 'Macabi'))) :{'Rstar':1, 'Macabi': 1},
	tuple(sorted(('Rstar', 'Dubai'))) :{'Rstar':1, 'Dubai': 1},
	tuple(sorted(('Monaco', 'Macabi'))) :{'Monaco': 1, 'Macabi': 1},
	tuple(sorted(('Monaco', 'Dubai'))) :{'Monaco':1, 'Dubai': 1},
	tuple(sorted(('Macabi', 'Dubai'))) :{'Macabi':2, 'Dubai': 0}
}

all_rounds = [matches_35, matches_36, matches_37, matches_30, matches_38]

for round_matches in all_rounds:
	print(f'\n----ΝΕΑ ΑΓΩΝΙΣΤΙΚΗ----')
	for home, away in round_matches:
		winner = ''
		while winner not in [home, away]:
			winner = input(f'Ποιος θα ειναι ο Νικητής στον αγώνα {home} - {away}; ')
			if winner not in [home, away]:
				print(f"Λάθος! Πρέπει να γράψεις είτε {home} είτε {away}.")

	
		standings[winner] += 1

		key = tuple(sorted((home, away)))
		if key not in h2h_results:
			h2h_results[key] = {home: 0, away: 0}

		h2h_results[key][winner] += 1




team_list = list(standings.keys())

def compare_teams(team):
	return standings[team]


total_h2h_diff = {team: 0 for team in standings.keys()}

def euroleague_sort(team):
    # 1ο Κριτήριο: Συνολικές Νίκες (π.χ. 25)
    total_wins = standings[team]
    
    # 2ο Κριτήριο: Νίκες ΜΟΝΟ απέναντι σε αυτούς που έχουν τις ίδιες συνολικές νίκες
    h2h_wins_in_tie = 0
    for other_team in standings:
        if other_team != team and standings[other_team] == total_wins:
            # Ψάχνουμε αν έχουν παίξει μεταξύ τους στο h2h_results
            match_key = tuple(sorted((team, other_team)))
            if match_key in h2h_results:
                # Προσθέτουμε μόνο τις νίκες απέναντι στον συγκεκριμένο ισόβαθμο
                h2h_wins_in_tie += h2h_results[match_key].get(team, 0)
    
    # Επιστρέφουμε ένα tuple. Η Python θα ταξινομήσει πρώτα με το 1ο και μετά με το 2ο
    return (total_wins, h2h_wins_in_tie)

# Η νέα ταξινόμηση χρησιμοποιεί τη συνάρτηση που φτιάξαμε
ranked = sorted(team_list, key=euroleague_sort, reverse=True)
print("\n" + "="*55)
print(f"{'ΘΕΣΗ':<6} {'ΟΜΑΔΑ':<15} {'ΝΙΚΕΣ':<10} {'+/- H2H':<10}")
print("-" * 55)

for i, team in enumerate(ranked, 1):
    # Παίρνουμε τα αποτελέσματα κατευθείαν από τη συνάρτηση που φτιάξαμε
    wins, h2h_tie_wins = euroleague_sort(team)
    print(f"{i:<6} {team:<15} {wins:<10} {h2h_tie_wins:<10}")