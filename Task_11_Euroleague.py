import streamlit as st

st.set_page_config(page_title="Euroleague Predictor", layout="wide")
st.title("Euroleague Simulator 2026 🏀")

# --- 1. ΑΡΧΙΚΑ ΔΕΔΟΜΕΝΑ (ΜΟΝΟ ΜΙΑ ΦΟΡΑ) ---
if 'standings' not in st.session_state:
    st.session_state.standings = {
        'Fener':23, 'Oly':23, 'Real':22, 'Hapoel':21, 'Valencia':22, 'Zalgiris':21, 
        'Pao': 20, 'Barca':20, 'Rstar': 19, 'Monaco': 19, 'Macabi': 18, 'Dubai':18, 
        'Armani': 0, 'Partizan': 0, 'Bayern': 0, 'Pari': 0, 'Bologna': 0, 
        'Baskonia': 0, 'Efes': 0, 'Asvel': 0, 'none': -10
    }

if 'h2h_results' not in st.session_state:
    # Εδώ κρατάμε τις νίκες H2H (1 για νίκη, 0 για ήττα)
    st.session_state.h2h_results = {
        tuple(sorted(('Fener', 'Oly'))): {'Fener': 1, 'Oly': 1},
        tuple(sorted(('Fener', 'Real'))): {'Fener': 0, 'Real': 1},
        tuple(sorted(('Oly', 'Real'))): {'Oly': 0, 'Real': 1},
        tuple(sorted(('Hapoel', 'Valencia'))): {'Hapoel': 1, 'Valencia': 1},
        tuple(sorted(('Hapoel', 'Zalgiris'))): {'Hapoel': 0, 'Zalgiris': 2},
        tuple(sorted(('Hapoel', 'Pao'))): {'Hapoel': 1, 'Pao': 1},
        tuple(sorted(('Hapoel', 'Barca'))): {'Hapoel': 2, 'Barca': 0},
        tuple(sorted(('Valencia', 'Zalgiris'))): {'Valencia': 1, 'Zalgiris': 1},
        tuple(sorted(('Valencia', 'Pao'))): {'Valencia': 1, 'Pao': 0},
        tuple(sorted(('Valencia', 'Barca'))): {'Valencia': 0, 'Barca': 2},
        tuple(sorted(('Zalgiris', 'Pao'))): {'Zalgiris': 0, 'Pao': 2},
        tuple(sorted(('Zalgiris', 'Barca'))): {'Zalgiris': 2, 'Barca': 0},
        tuple(sorted(('Pao', 'Barca'))): {'Pao': 0, 'Barca': 1},
        tuple(sorted(('Pao', 'Rstar'))): {'Pao': 1, 'Rstar': 1},
        tuple(sorted(('Pao', 'Monaco'))): {'Pao': 1, 'Monaco': 1},
        tuple(sorted(('Barca', 'Rstar'))): {'Barca': 2, 'Rstar': 0},
        tuple(sorted(('Barca', 'Monaco'))): {'Barca': 0, 'Monaco': 1},
        tuple(sorted(('Rstar', 'Monaco'))): {'Rstar': 2, 'Monaco': 0},
        tuple(sorted(('Rstar', 'Macabi'))): {'Rstar': 1, 'Macabi': 1},
        tuple(sorted(('Rstar', 'Dubai'))): {'Rstar': 1, 'Dubai': 1},
        tuple(sorted(('Monaco', 'Macabi'))): {'Monaco': 1, 'Macabi': 1},
        tuple(sorted(('Monaco', 'Dubai'))): {'Monaco': 1, 'Dubai': 1},
        tuple(sorted(('Macabi', 'Dubai'))): {'Macabi': 2, 'Dubai': 0},
		tuple(sorted(('Real', 'Valencia'))): {'Real': 1, 'Valencia': 1},
		tuple(sorted(('Real', 'Hapoel'))): {'Real': 2, 'Hapoel': 0},
		tuple(sorted(('Real', 'Zalgiris'))): {'Real': 1, 'Zalgiris': 1},
		tuple(sorted(('Real', 'Barcelona'))): {'Real': 2, 'Barcelona': 0},
		tuple(sorted(('Real', 'Pao'))): {'Real': 0, 'Pao': 2},
		tuple(sorted(('Fener', 'Valencia'))): {'Fener': 1, 'Valencia': 1},
		tuple(sorted(('Fener', 'Hapoel'))): {'Fener': 1, 'Hapoel': 0},
		tuple(sorted(('Fener', 'Zalgiris'))): {'Fener': 0, 'Zalgiris': 2},
		tuple(sorted(('Fener', 'Barcelona'))): {'Fener': 2, 'Barcelona': 0},
		tuple(sorted(('Fener', 'Pao'))): {'Fener': 1, 'Pao': 1}
    }

# --- 2. ΟΙ ΑΓΩΝΕΣ ---
all_matches = [('none','Hapoel', 'Fener'), ('none','Zalgiris', 'Dubai'), ('none','Rstar', 'Pari'), 
    ('none','Oly', 'Real'), ('none','Barca', 'Pao'), ('none','Valencia', 'Armani'), 
    ('none','Baskonia', 'Macabi'), ('none','Monaco', 'Asvel'), ('none','Hapoel', 'Oly'), ('none','Fener', 'Real'), ('none','Valencia', 'Pao'), ('none','Pari', 'Macabi'), ('none','Monaco', 'Barca'), 
				('none','Dubai', 'Efes'), ('none','Partizan', 'Zalgiris'), ('none','Asvel', 'Rstar'), ('none','Macabi', 'Hapoel'), ('none','Asvel','Fener'), ('none','Macabi','Bologna'), ('none','Oly','Armani'), ('none','Real','Rstar'), ('none','Dubai','Valencia'), 
				('none','Zalgiris','Pari'), ('none','Monaco','Hapoel'), ('none','Pao','Efes'), ('none','Barca','Bayern')
]

st.sidebar.header("Πρόβλεψη Αγώνων")
predictions = {}

# Δημιουργία των Selectboxes στο πλάι
for a, home, away in all_matches:
    predictions[(a, home, away)] = st.sidebar.selectbox(
        f"{home} vs {away}", 
        [a, home, away], 
        key=f"{home}_{away}"
    )

# --- 3. ΥΠΟΛΟΓΙΣΜΟΣ ΒΑΘΜΟΛΟΓΙΑΣ ---
# Ξεκινάμε από τις βασικές νίκες και προσθέτουμε τις προβλέψεις
current_standings = st.session_state.standings.copy()
current_h2h = {k: v.copy() for k, v in st.session_state.h2h_results.items()}

for (a, home, away), winner in predictions.items():
    current_standings[winner] += 1
    key = tuple(sorted((a, home, away)))
    if key not in current_h2h:
        current_h2h[key] = {a:0, home: 0, away: 0}
    current_h2h[key][winner] += 1

# --- 4. ΣΥΝΑΡΤΗΣΗ ΤΑΞΙΝΟΜΗΣΗΣ ---
def euroleague_sort(team):
    wins = current_standings[team]
    h2h_tie_wins = 0
    for other in current_standings:
        if other != team and current_standings[other] == wins:
            m_key = tuple(sorted((team, other)))
            if m_key in current_h2h:
                h2h_tie_wins += current_h2h[m_key].get(team, 0)
    return (wins, h2h_tie_wins)

# Ταξινόμηση
ranked_teams = sorted(current_standings.keys(), key=euroleague_sort, reverse=True)

# --- 5. ΕΜΦΑΝΙΣΗ ΠΙΝΑΚΑ ---
st.subheader("Τελική Κατάταξη")

table_data = []
for i, team in enumerate(ranked_teams, 1):
    w, h2h = euroleague_sort(team)
    table_data.append({
        "Θέση": i,
        "Ομάδα": team,
        "Νίκες": w,
        "H2H Wins": h2h
    })

st.table(table_data)

if st.button("Reset Simulator"):
    st.rerun()
