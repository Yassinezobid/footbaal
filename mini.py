
import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Calcul Simple de Profit Net - Location de Terrains")

# Section Revenus
st.header("Revenus")
revenu = st.number_input(
    "Revenu mensuel total (DH)",
    min_value=0.0,
    step=100.0,
    value=0.0,
    key="revenu"
)

# Section Charges Mensuelles
st.header("Charges Mensuelles")
loyer = st.number_input(
    "Loyer mensuel (DH)",
    min_value=0.0,
    step=100.0,
    value=0.0,
    key="loyer"
)
employes = st.number_input(
    "Salaires employés (DH)",
    min_value=0.0,
    step=100.0,
    value=0.0,
    key="employes"
)
electricite = st.number_input(
    "Électricité (DH)",
    min_value=0.0,
    step=10.0,
    value=0.0,
    key="electricite"
)
eau = st.number_input(
    "Eau (DH)",
    min_value=0.0,
    step=10.0,
    value=0.0,
    key="eau"
)

# Section Charges d'Investissement (Lancement)
st.header("Charges d'investissement (lancement)")
investissement = st.number_input(
    "Total charges d'investissement (DH)",
    min_value=0.0,
    step=1000.0,
    value=0.0,
    key="investissement"
)

# Calculs
total_charges_mensuelles = loyer + employes + electricite + eau
profit_net = revenu - total_charges_mensuelles

# Affichage du récapitulatif
st.header("Récapitulatif")
summary = {
    "Revenu mensuel (DH)": [revenu],
    "Charges mensuelles (DH)": [total_charges_mensuelles],
    "Charges d'investissement (DH)": [investissement],
    "Profit net mensuel (DH)": [profit_net]
}
df_summary = pd.DataFrame(summary)
st.table(df_summary)
