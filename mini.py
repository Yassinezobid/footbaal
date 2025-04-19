# Voici la version modifiée du code :
# - Suppression de tous les services sauf "Location 1 heure"
# - Simplification des tableaux
# - Seules les charges mensuelles influencent le profit net

import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="SimuProfit - Location Terrains Mini Football",
    page_icon="⚽",
    layout="centered"
)

# Initialisation des données
if 'prix_location' not in st.session_state:
    st.session_state.prix_location = 200.0
    st.session_state.cout_unitaire = 50.0
    st.session_state.commandes_jour = 8
    st.session_state.jours_activite = 26
    st.session_state.nb_terrains = 1
    st.session_state.taux_impot = 20.0
    st.session_state.nb_associes = 2

    st.session_state.charges_mensuelles = {
        "Loyer": 8000.0,
        "Électricité et eau": 3500.0,
        "Employés": 6000.0
    }

    st.session_state.charges_investissement = {
        "Avance de terrain": 40000.0,
        "Construction": 150000.0,
        "Gazon": 250000.0,
        "Publicités": 20000.0,
        "App et réseaux sociaux": 10000.0,
        "Divers": 10000.0
    }

# Calcul des revenus et coûts
revenu_mensuel = st.session_state.prix_location * st.session_state.commandes_jour * st.session_state.jours_activite * st.session_state.nb_terrains
cout_variable = st.session_state.cout_unitaire * st.session_state.commandes_jour * st.session_state.jours_activite * st.session_state.nb_terrains
cout_fixe = sum(st.session_state.charges_mensuelles.values())
cost_total = cout_variable + cout_fixe
benefice_brut = revenu_mensuel - cost_total
impot = benefice_brut * st.session_state.taux_impot / 100 if benefice_brut > 0 else 0
profit_net = benefice_brut - impot
profit_par_associe = profit_net / st.session_state.nb_associes

# Calcul de l'investissement total
total_investissement = (
    (st.session_state.charges_investissement["Avance de terrain"] +
     st.session_state.charges_investissement["Construction"] +
     st.session_state.charges_investissement["Gazon"]) * st.session_state.nb_terrains +
    st.session_state.charges_investissement["Publicités"] +
    st.session_state.charges_investissement["App et réseaux sociaux"] +
    st.session_state.charges_investissement["Divers"]
)

roi_mensuel = profit_net / total_investissement * 100 if total_investissement > 0 else 0
temps_retour = total_investissement / profit_net if profit_net > 0 else float('inf')

# Interface utilisateur
st.title("⚽ SimuProfit - Location Terrains")
st.markdown("### Rentabilité mensuelle d'un terrain de mini football")

# Résumé financier
st.subheader("💸 Résumé Financier")
st.write(pd.DataFrame({
    "Indicateur": [
        "Revenu mensuel",
        "Coût variable",
        "Coût fixe",
        "Bénéfice brut",
        "Impôt",
        "Profit net",
        "Profit par associé",
        "Investissement total",
        "Temps de retour (mois)"
    ],
    "Montant (DH)": [
        f"{revenu_mensuel:.2f}",
        f"{cout_variable:.2f}",
        f"{cout_fixe:.2f}",
        f"{benefice_brut:.2f}",
        f"{impot:.2f}",
        f"{profit_net:.2f}",
        f"{profit_par_associe:.2f}",
        f"{total_investissement:.2f}",
        f"{temps_retour:.1f}" if temps_retour != float('inf') else "N/A"
    ]
}))

# Formulaire pour modifier les paramètres
st.subheader("⚙️ Paramètres")
with st.form("form_params"):
    st.session_state.commandes_jour = st.number_input("Commandes par jour", value=st.session_state.commandes_jour, min_value=0.0)
    st.session_state.prix_location = st.number_input("Prix location 1h (DH)", value=st.session_state.prix_location, min_value=0.0)
    st.session_state.cout_unitaire = st.number_input("Coût unitaire (DH)", value=st.session_state.cout_unitaire, min_value=0.0)
    st.session_state.jours_activite = st.number_input("Jours d'activité par mois", value=st.session_state.jours_activite, min_value=1, max_value=31)
    st.session_state.nb_terrains = st.number_input("Nombre de terrains", value=st.session_state.nb_terrains, min_value=1)
    st.session_state.nb_associes = st.number_input("Nombre d'associés", value=st.session_state.nb_associes, min_value=1)
    st.session_state.taux_impot = st.number_input("Taux d'impôt (%)", value=st.session_state.taux_impot, min_value=0.0, max_value=100.0)
    st.form_submit_button("Mettre à jour")
