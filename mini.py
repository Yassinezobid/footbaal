import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="SimuProfit - Business Plan Mini Football",
    page_icon="⚽",
    layout="wide"
)

# Fonction pour ajouter un style CSS personnalisé
def local_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2196F3;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .chart-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Titre principal de l'application
st.markdown('<p class="main-header">⚽ SimuProfit - Business Plan Mini Football</p>', unsafe_allow_html=True)
st.markdown("### Simulez la rentabilité de vos terrains de mini football en quelques clics")

# Initialisation des variables de session si elles n'existent pas déjà
if 'prix_vente' not in st.session_state:
    # Seulement le service de location
    st.session_state.prix_vente = 200.0
    st.session_state.cout_unitaire = 50.0
    st.session_state.commandes_jour = 8
    
    # Initialisation des paramètres d'activité
    st.session_state.jours_activite = 26
    st.session_state.taux_impot = 20.0
    st.session_state.nb_associes = 2
    st.session_state.nb_terrains = 1
    
    # Initialisation des charges mensuelles
    st.session_state.charges_mensuelles = {
        "Loyer": 8000.0,
        "Électricité et eau": 3500.0,
        "Employés": 6000.0
    }
    
    # Initialisation des charges d'investissement
    st.session_state.charges_investissement = {
        "Avance de terrain": 40000.0,
        "Construction": 150000.0,
        "Gazon": 250000.0,
        "Publicités": 20000.0,
        "Stock initial": 15000.0,
        "Social Media et App": 10000.0,
        "Caméras de surveillance": 5000.0,
        "Caméras de filmage": 10000.0,
        "Divers": 5000.0,
        "Création d'association": 5000.0
    }

# Dictionnaire des emojis pour les charges
charges_emojis = {
    "Loyer": "🏢",
    "Électricité et eau": "⚡",
    "Employés": "👨‍💼"
}

# Fonction pour calculer les indicateurs financiers
def calculer_indicateurs():
    # Calcul des revenus et coûts pour la location
    revenu_par_terrain = st.session_state.prix_vente * st.session_state.commandes_jour * st.session_state.jours_activite
    cout_par_terrain = st.session_state.cout_unitaire * st.session_state.commandes_jour * st.session_state.jours_activite
    marge_par_terrain = revenu_par_terrain - cout_par_terrain
    
    # Calcul pour tous les terrains
    revenu_brut = revenu_par_terrain * st.session_state.nb_terrains
    cout_variable = cout_par_terrain * st.session_state.nb_terrains
    cout_fixe = sum(st.session_state.charges_mensuelles.values())
    cout_total = cout_variable + cout_fixe
    benefice_brut = revenu_brut - cout_total
    impot = benefice_brut * (st.session_state.taux_impot / 100) if benefice_brut > 0 else 0
    profit_net = benefice_brut - impot
    profit_par_associe = profit_net / st.session_state.nb_associes if st.session_state.nb_associes > 0 else 0
    
    # Calcul du total des investissements
    investissement_specifique_terrain = (
        st.session_state.charges_investissement["Avance de terrain"] +
        st.session_state.charges_investissement["Construction"] +
        st.session_state.charges_investissement["Gazon"] +
        st.session_state.charges_investissement["Caméras de surveillance"] +
        st.session_state.charges_investissement["Caméras de filmage"]
    )
    
    investissement_commun = (
        st.session_state.charges_investissement["Publicités"] +
        st.session_state.charges_investissement["Stock initial"] +
        st.session_state.charges_investissement["Social Media et App"] +
        st.session_state.charges_investissement["Divers"] +
        st.session_state.charges_investissement["Création d'association"]
    )
    
    total_investissement = investissement_specifique_terrain * st.session_state.nb_terrains + investissement_commun
    
    # Calcul du seuil de rentabilité
    if revenu_brut > 0:
        seuil_rentabilite = cout_fixe / (1 - (cout_variable / revenu_brut))
        marge_cout_variable = (1 - (cout_variable / revenu_brut)) * 100
    else:
        seuil_rentabilite = 0
        marge_cout_variable = 0
    
    # Calcul du ROI
    if total_investissement > 0 and profit_net > 0:
        roi_mensuel = profit_net / total_investissement * 100
        roi_annuel = roi_mensuel * 12
        temps_retour = total_investissement / profit_net
    else:
        roi_mensuel = 0
        roi_annuel = 0
        temps_retour = float('inf')
    
    return {
        'revenu_par_terrain': revenu_par_terrain,
        'cout_par_terrain': cout_par_terrain,
        'marge_par_terrain': marge_par_terrain,
        'revenu_brut': revenu_brut,
        'cout_variable': cout_variable,
        'cout_fixe': cout_fixe,
        'cout_total': cout_total,
        'benefice_brut': benefice_brut,
        'impot': impot,
        'profit_net': profit_net,
        'profit_par_associe': profit_par_associe,
        'total_investissement': total_investissement,
        'seuil_rentabilite': seuil_rentabilite,
        'marge_cout_variable': marge_cout_variable,
        'roi_mensuel': roi_mensuel,
        'roi_annuel': roi_annuel,
        'temps_retour': temps_retour
    }

# Calculer les indicateurs financiers
indicateurs = calculer_indicateurs()

# Contenu principal
# 1. Affichage du résumé financier
st.markdown("## 💰 Résumé financier")
col_profit1, col_profit2, col_profit3 = st.columns(3)
with col_profit1:
    st.metric(label="Profit Net Total", value=f"{indicateurs['profit_net']:.2f} DH",
            delta=f"{indicateurs['profit_net']:.1f} DH" if indicateurs['profit_net'] > 0 else f"-{abs(indicateurs['profit_net']):.1f} DH")
with col_profit2:
    st.metric(label="Par Associé", value=f"{indicateurs['profit_par_associe']:.2f} DH")
with col_profit3:
    st.metric(label="ROI annuel", value=f"{indicateurs['roi_annuel']:.2f}%")

# 2. Paramètres d'activité généraux
st.markdown('<p class="sub-header">📆 Paramètres d\'activité</p>', unsafe_allow_html=True)
params_col1, params_col2, params_col3, params_col4 = st.columns(4)

with params_col1:
    jours_activite = st.number_input(
        "Nombre de jours d'activité par mois",
        min_value=1,
        max_value=31,
        value=st.session_state.jours_activite,
        step=1,
        key="jours_activite_input"
    )
    st.session_state.jours_activite = jours_activite

with params_col2:
    taux_impot = st.number_input(
        "Taux d'impôt (%)",
        min_value=0.0,
        max_value=50.0,
        value=st.session_state.taux_impot,
        step=0.5,
        key="taux_impot_input"
    )
    st.session_state.taux_impot = taux_impot

with params_col3:
    nb_associes = st.number_input(
        "Nombre d'associés",
        min_value=1,
        value=st.session_state.nb_associes,
        step=1,
        key="nb_associes_input"
    )
    st.session_state.nb_associes = nb_associes

with params_col4:
    nb_terrains = st.number_input(
        "Nombre de terrains",
        min_value=1,
        value=st.session_state.nb_terrains,
        step=1,
        key="nb_terrains_input"
    )
    st.session_state.nb_terrains = nb_terrains

# 3. Paramètres du service de location
st.markdown('<p class="sub-header">⚽ Paramètres de location</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    prix_location = st.number_input(
        "Prix de location par heure (DH)",
        min_value=0.0,
        value=st.session_state.prix_vente,
        step=10.0,
        key="prix_location_input"
    )
    st.session_state.prix_vente = prix_location

with col2:
    cout_location = st.number_input(
        "Coût par heure de location (DH)",
        min_value=0.0,
        value=st.session_state.cout_unitaire,
        step=5.0,
        key="cout_location_input"
    )
    st.session_state.cout_unitaire = cout_location

with col3:
    commandes_jour = st.number_input(
        "Nombre de locations par jour",
        min_value=0.0,
        value=st.session_state.commandes_jour,
        step=1.0,
        key="commandes_jour_input"
    )
    st.session_state.commandes_jour = commandes_jour

# 4. Tableau récapitulatif du service de location
st.markdown('<p class="sub-header">📊 Détails des revenus</p>', unsafe_allow_html=True)

# Calculs pour le tableau
revenu_mensuel = indicateurs['revenu_par_terrain'] * st.session_state.nb_terrains
cout_mensuel = indicateurs['cout_par_terrain'] * st.session_state.nb_terrains
marge_mensuelle = revenu_mensuel - cout_mensuel

# Création du tableau
details_data = {
    "Indicateur": ["Prix par heure", "Coût par heure", "Marge par heure", 
                  "Locations par jour", "Jours d'activité", "Nombre de terrains",
                  "Revenu mensuel", "Coût variable mensuel", "Marge brute mensuelle"],
    "Valeur": [
        f"{st.session_state.prix_vente:.2f} DH",
        f"{st.session_state.cout_unitaire:.2f} DH",
        f"{(st.session_state.prix_vente - st.session_state.cout_unitaire):.2f} DH",
        st.session_state.commandes_jour,
        st.session_state.jours_activite,
        st.session_state.nb_terrains,
        f"{revenu_mensuel:.2f} DH",
        f"{cout_mensuel:.2f} DH",
        f"{marge_mensuelle:.2f} DH"
    ]
}

df_details = pd.DataFrame(details_data)
st.dataframe(df_details, use_container_width=True)

# 5. Tableau des charges mensuelles
st.markdown('<p class="sub-header">💸 Charges mensuelles</p>', unsafe_allow_html=True)

with st.form(key="charges_form"):
    # Table éditable pour les charges
    charges_data = []
    
    # Utiliser des colonnes pour organiser les champs de formulaire
    col1, col2, col3 = st.columns(3)
    
    with col1:
        loyer = st.number_input(
            "🏢 Loyer (DH)",
            min_value=0.0,
            value=st.session_state.charges_mensuelles["Loyer"],
            step=100.0,
            format="%.2f",
            key="charge_loyer"
        )
        st.session_state.charges_mensuelles["Loyer"] = loyer
    
    with col2:
        electricite = st.number_input(
            "⚡ Électricité et eau (DH)",
            min_value=0.0,
            value=st.session_state.charges_mensuelles["Électricité et eau"],
            step=100.0,
            format="%.2f",
            key="charge_electricite"
        )
        st.session_state.charges_mensuelles["Électricité et eau"] = electricite
    
    with col3:
        employes = st.number_input(
            "👨‍💼 Employés (DH)",
            min_value=0.0,
            value=st.session_state.charges_mensuelles["Employés"],
            step=100.0,
            format="%.2f",
            key="charge_employes"
        )
        st.session_state.charges_mensuelles["Employés"] = employes
    
    # Bouton pour soumettre les modifications
    charges_submitted = st.form_submit_button("Mettre à jour les calculs")
    if charges_submitted:
        st.success("Valeurs mises à jour! Les calculs ont été recalculés.")
        indicateurs = calculer_indicateurs()  # Recalculer les indicateurs

# Tableau récapitulatif des charges
charges_data = {
    "Charge": ["🏢 Loyer", "⚡ Électricité et eau", "👨‍💼 Employés", "📊 TOTAL"],
    "Montant (DH)": [
        f"{st.session_state.charges_mensuelles['Loyer']:.2f} DH",
        f"{st.session_state.charges_mensuelles['Électricité et eau']:.2f} DH",
        f"{st.session_state.charges_mensuelles['Employés']:.2f} DH",
        f"{sum(st.session_state.charges_mensuelles.values()):.2f} DH"
    ]
}

df_charges = pd.DataFrame(charges_data)
st.dataframe(df_charges, use_container_width=True)

# 6. Tableau des charges d'investissement
st.markdown('<p class="sub-header">🏗️ Charges d\'investissement (Lancement)</p>', unsafe_allow_html=True)

# Regroupement des investissements par catégorie
investissements_categories = {
    "Par terrain": [
        "Avance de terrain", "Construction", "Gazon", "Caméras de surveillance", "Caméras de filmage"
    ],
    "Communs": [
        "Publicités", "Stock initial", "Social Media et App", "Divers", "Création d'association"
    ]
}

# Création du tableau d'investissement
inv_data = []
for categorie, items in investissements_categories.items():
    subtotal = 0
    for item in items:
        montant = st.session_state.charges_investissement.get(item, 0.0)
        subtotal += montant
        inv_data.append({
            "Catégorie": categorie,
            "Investissement": item,
            "Montant (DH)": f"{montant:.2f} DH"
        })
    
    if categorie == "Par terrain":
        montant_total = subtotal * st.session_state.nb_terrains
        inv_data.append({
            "Catégorie": categorie,
            "Investissement": f"Sous-total ({st.session_state.nb_terrains} terrain{'s' if st.session_state.nb_terrains > 1 else ''})",
            "Montant (DH)": f"{montant_total:.2f} DH"
        })
    else:
        inv_data.append({
            "Catégorie": categorie,
            "Investissement": "Sous-total",
            "Montant (DH)": f"{subtotal:.2f} DH"
        })

# Ajouter une ligne de total pour les investissements
inv_data.append({
    "Catégorie": "",
    "Investissement": "📊 TOTAL INVESTISSEMENT",
    "Montant (DH)": f"{indicateurs['total_investissement']:.2f} DH"
})

df_inv = pd.DataFrame(inv_data)
st.dataframe(df_inv, use_container_width=True)

# 7. Rentabilité et Analyse financière
st.markdown('<p class="sub-header">📈 Résumé financier</p>', unsafe_allow_html=True)

# Tableau récapitulatif financier
data_resume = {
    "Indicateur": ["Revenu mensuel", "Coût variable", "Coût fixe (charges)",
                  "Coût total mensuel", "Bénéfice avant impôt", f"Impôt ({st.session_state.taux_impot}%)",
                  "Profit net mensuel", f"Profit par associé ({st.session_state.nb_associes})"],
    "Montant (DH)": [
        f"{indicateurs['revenu_brut']:.2f} DH",
        f"{indicateurs['cout_variable']:.2f} DH",
        f"{indicateurs['cout_fixe']:.2f} DH",
        f"{indicateurs['cout_total']:.2f} DH",
        f"{indicateurs['benefice_brut']:.2f} DH",
        f"{indicateurs['impot']:.2f} DH",
        f"{indicateurs['profit_net']:.2f} DH",
        f"{indicateurs['profit_par_associe']:.2f} DH"
    ]
}

df_resume = pd.DataFrame(data_resume)
st.dataframe(df_resume, use_container_width=True)

# Graphique simplifié
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['Revenu', 'Coût total', 'Profit net']
values = [indicateurs['revenu_brut'], indicateurs['cout_total'], indicateurs['profit_net']]

bars = ax.bar(labels, values, color=['#4CAF50', '#FF9800', '#2196F3'])

# Ajouter les valeurs au-dessus des barres
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 500, f'{height:.0f} DH', ha='center', va='bottom')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.title('Aperçu financier mensuel')

# Affichage du graphique
with st.container():
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# 8. Analyse de rentabilité
st.markdown('<p class="sub-header">⏱️ Analyse de rentabilité</p>', unsafe_allow_html=True)

col_rentab1, col_rentab2 = st.columns(2)

with col_rentab1:
    st.markdown("### 🏁 Seuil de rentabilité")
    st.metric(
        label="Seuil de rentabilité mensuel",
        value=f"{indicateurs['seuil_rentabilite']:.2f} DH"
    )
    st.write(f"Vous devez générer au moins **{indicateurs['seuil_rentabilite']:.2f} DH** de revenus mensuels pour couvrir tous vos coûts.")

with col_rentab2:
    st.markdown("### 💰 Retour sur investissement")
    
    if indicateurs['profit_net'] > 0:
        st.metric(
            label="Temps de retour sur investissement",
            value=f"{indicateurs['temps_retour']:.1f} mois"
        )
        annees = int(indicateurs['temps_retour'] // 12)
        mois_restants = int(indicateurs['temps_retour'] % 12)
        if annees > 0:
            st.write(f"Votre investissement total de **{indicateurs['total_investissement']:.2f} DH** sera rentabilisé en **{annees} ans et {mois_restants} mois**.")
        else:
            st.write(f"Votre investissement total de **{indicateurs['total_investissement']:.2f} DH** sera rentabilisé en **{mois_restants} mois**.")
    else:
        st.error("❌ Avec les paramètres actuels, votre activité n'est pas rentable.")

# 9. Comparaison avec différents nombres de terrains (tableau simplifié)
st.markdown('<p class="sub-header">🔄 Comparaison par nombre de terrains</p>', unsafe_allow_html=True)

# Calculer les indicateurs pour différents nombres de terrains
max_terrains = 5
comparaison_terrains = []

for n_terrains in range(1, max_terrains + 1):
    # Sauvegarde temporaire du nombre actuel de terrains
    nombre_terrains_actuel = st.session_state.nb_terrains
    
    # Définir temporairement le nombre de terrains pour le calcul
    st.session_state.nb_terrains = n_terrains
    comp_indicateurs = calculer_indicateurs()
    
    # Restaurer le nombre de terrains d'origine
    st.session_state.nb_terrains = nombre_terrains_actuel
    
    comparaison_terrains.append({
        "Nombre de terrains": n_terrains,
        "Revenu mensuel": f"{comp_indicateurs['revenu_brut']:.2f} DH",
        "Profit net": f"{comp_indicateurs['profit_net']:.2f} DH",
        "Profit par associé": f"{comp_indicateurs['profit_par_associe']:.2f} DH",
        "Investissement": f"{comp_indicateurs['total_investissement']:.2f} DH",
        "Temps de retour (mois)": f"{comp_indicateurs['temps_retour']:.1f}" if comp_indicateurs['profit_net'] > 0 else "N/A"
    })

df_comparaison = pd.DataFrame(comparaison_terrains)
st.dataframe(df_comparaison, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### ⚽ SimuProfit - Business Plan Mini Football")
st.markdown("Une application pour simuler et optimiser la rentabilité de vos terrains de mini football.")
