import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="SimuProfit - Business Plan Mini Football",
    page_icon="⚽",
    layout="wide"
)

# Style personnalisé simplifié
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
st.markdown('<p class="main-header">⚽ SimuProfit - Business Plan Mensuel Mini Football</p>', unsafe_allow_html=True)
st.markdown("### Simulez la rentabilité de vos terrains de mini football")

# Initialisation des variables de session
if 'prix_location' not in st.session_state:
    # Initialisation des paramètres
    st.session_state.prix_location = 200.0
    st.session_state.cout_location = 50.0
    st.session_state.commandes_jour = 8  # Défini comme entier
    
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

# Fonction pour calculer les indicateurs financiers
def calculer_indicateurs():
    # Calcul des revenus et coûts pour la location
    revenu_location = st.session_state.prix_location * st.session_state.commandes_jour * st.session_state.jours_activite * st.session_state.nb_terrains
    cout_location = st.session_state.cout_location * st.session_state.commandes_jour * st.session_state.jours_activite * st.session_state.nb_terrains
    marge_location = revenu_location - cout_location
    
    # Calcul des totaux
    revenu_brut = revenu_location
    cout_variable = cout_location
    cout_fixe = sum(st.session_state.charges_mensuelles.values())
    cout_total = cout_variable + cout_fixe
    benefice_brut = revenu_brut - cout_total
    impot = benefice_brut * (st.session_state.taux_impot / 100) if benefice_brut > 0 else 0
    profit_net = benefice_brut - impot
    charge_amelioration = profit_net * 0.3
    profit_net_final = profit_net - charge_amelioration
    profit_par_associe = profit_net_final / st.session_state.nb_associes if st.session_state.nb_associes > 0 else 0
    
    # Calcul des investissements
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
    
    # Calcul du ROI et temps de retour
    if total_investissement > 0 and profit_net_final > 0:
        roi_mensuel = profit_net_final / total_investissement * 100
        roi_annuel = roi_mensuel * 12
        temps_retour = total_investissement / profit_net_final
    else:
        roi_mensuel = 0
        roi_annuel = 0
        temps_retour = float('inf')
    
    return {
        'revenu_location': revenu_location,
        'cout_location': cout_location,
        'marge_location': marge_location,
        'revenu_brut': revenu_brut,
        'cout_variable': cout_variable,
        'cout_fixe': cout_fixe,
        'cout_total': cout_total,
        'benefice_brut': benefice_brut,
        'impot': impot,
        'profit_net': profit_net,
        'charge_amelioration': charge_amelioration,
        'profit_net_apres_amelioration': profit_net_final,
        'profit_par_associe': profit_par_associe,
        'total_investissement': total_investissement,
        'roi_mensuel': roi_mensuel,
        'roi_annuel': roi_annuel,
        'temps_retour': temps_retour
    }
indicateurs = calculer_indicateurs()

# Affichage du résumé financier
st.markdown("## 💰 Résumé financier")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Profit Net Total", value=f"{indicateurs['profit_net']:.2f} DH",
            delta=f"{indicateurs['profit_net']:.1f} DH" if indicateurs['profit_net'] > 0 else f"-{abs(indicateurs['profit_net']):.1f} DH")
with col2:
    st.metric(label="Par Associé", value=f"{indicateurs['profit_par_associe']:.2f} DH")
with col3:
    st.metric(label="ROI annuel", value=f"{indicateurs['roi_annuel']:.2f}%")

# 1. Paramètres d'activité généraux
st.markdown('<p class="sub-header">📆 Paramètres d\'activité</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    jours_activite = st.number_input(
        "Nombre de jours d'activité par mois",
        min_value=1,
        max_value=31,
        value=int(st.session_state.jours_activite),  # Conversion explicite en entier
        step=1
    )
    st.session_state.jours_activite = jours_activite

with col2:
    taux_impot = st.number_input(
        "Taux d'impôt (%)",
        min_value=0.0,
        max_value=50.0,
        value=float(st.session_state.taux_impot),  # Conversion explicite en flottant
        step=0.5,
        format="%.1f"
    )
    st.session_state.taux_impot = taux_impot

with col3:
    nb_associes = st.number_input(
        "Nombre d'associés",
        min_value=1,
        value=int(st.session_state.nb_associes),  # Conversion explicite en entier
        step=1
    )
    st.session_state.nb_associes = nb_associes

with col4:
    nb_terrains = st.number_input(
        "Nombre de terrains",
        min_value=1,
        value=int(st.session_state.nb_terrains),  # Conversion explicite en entier
        step=1
    )
    st.session_state.nb_terrains = nb_terrains

# 2. Détails de la location de terrain
st.markdown('<p class="sub-header">⚽ Service de location de terrain</p>', unsafe_allow_html=True)

with st.form(key="location_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prix_location = st.number_input(
            "Prix de location (DH/heure)",
            min_value=0.0,
            value=float(st.session_state.prix_location),  # Conversion explicite en flottant
            step=10.0,
            format="%.1f"
        )
    
    with col2:
        cout_location = st.number_input(
            "Coût de location (DH/heure)",
            min_value=0.0,
            value=float(st.session_state.cout_location),  # Conversion explicite en flottant
            step=5.0,
            format="%.1f"
        )
    
    with col3:
        commandes_jour = st.number_input(
            "Locations par jour",
            min_value=0,
            value=int(st.session_state.commandes_jour),  # Conversion explicite en entier
            step=1
        )
    
    # Mettre à jour les valeurs en session
    st.session_state.prix_location = prix_location
    st.session_state.cout_location = cout_location
    st.session_state.commandes_jour = commandes_jour
    
    submitted = st.form_submit_button("Mettre à jour les calculs")
    if submitted:
        st.success("Valeurs mises à jour!")
        indicateurs = calculer_indicateurs()

# Affichage du tableau de la location
location_data = {
    "Indicateur": ["Prix de location (DH/heure)", "Coût de location (DH/heure)", "Marge unitaire (DH/heure)",
                  "Locations par jour", "Revenu mensuel (DH)", "Coût mensuel (DH)", "Marge mensuelle (DH)"],
    "Valeur": [
        f"{st.session_state.prix_location:.2f} DH",
        f"{st.session_state.cout_location:.2f} DH",
        f"{(st.session_state.prix_location - st.session_state.cout_location):.2f} DH",
        st.session_state.commandes_jour,
        f"{indicateurs['revenu_location']:.2f} DH",
        f"{indicateurs['cout_location']:.2f} DH",
        f"{indicateurs['marge_location']:.2f} DH"
    ]
}

df_location = pd.DataFrame(location_data)
st.dataframe(df_location, use_container_width=True)

# 3. Charges mensuelles
st.markdown('<p class="sub-header">💸 Charges mensuelles</p>', unsafe_allow_html=True)

with st.form(key="charges_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        loyer = st.number_input(
            "Loyer (DH)",
            min_value=0.0,
            value=float(st.session_state.charges_mensuelles["Loyer"]),  # Conversion explicite en flottant
            step=100.0,
            format="%.1f"
        )
        st.session_state.charges_mensuelles["Loyer"] = loyer
    
    with col2:
        electricite_eau = st.number_input(
            "Électricité et eau (DH)",
            min_value=0.0,
            value=float(st.session_state.charges_mensuelles["Électricité et eau"]),  # Conversion explicite en flottant
            step=100.0,
            format="%.1f"
        )
        st.session_state.charges_mensuelles["Électricité et eau"] = electricite_eau
    
    with col3:
        employes = st.number_input(
            "Employés (DH)",
            min_value=0.0,
            value=float(st.session_state.charges_mensuelles["Employés"]),  # Conversion explicite en flottant
            step=100.0,
            format="%.1f"
        )
        st.session_state.charges_mensuelles["Employés"] = employes
    
    charges_submitted = st.form_submit_button("Mettre à jour les charges")
    if charges_submitted:
        st.success("Charges mises à jour!")
        indicateurs = calculer_indicateurs()

# Tableau des charges mensuelles
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

# 4. Tableau de bord financier
st.markdown('<p class="sub-header">📊 Bilan financier mensuel</p>', unsafe_allow_html=True)

# Tableau résumé des indicateurs financiers
data_resume = {
    "Indicateur": [
        "Revenu brut mensuel",
        "Coût variable (location)",
        "Coût fixe (charges)",
        "Coût total mensuel",
        "Bénéfice avant impôt",
        f"Impôt ({st.session_state.taux_impot}%)",
        "Profit net mensuel",
        "Amélioration projet (30%)",
        f"Profit par associé ({st.session_state.nb_associes})"
    ],
    "Montant (DH)": [
        f"{indicateurs['revenu_brut']:.2f} DH",
        f"{indicateurs['cout_variable']:.2f} DH",
        f"{indicateurs['cout_fixe']:.2f} DH",
        f"{indicateurs['cout_total']:.2f} DH",
        f"{indicateurs['benefice_brut']:.2f} DH",
        f"{indicateurs['impot']:.2f} DH",
        f"{indicateurs['profit_net']:.2f} DH",
        f"{indicateurs['charge_amelioration']:.2f} DH",
        f"{(indicateurs['profit_net_apres_amelioration'] / st.session_state.nb_associes) if st.session_state.nb_associes > 0 else 0:.2f} DH"
    ]
}

df_resume = pd.DataFrame(data_resume)
st.dataframe(df_resume, use_container_width=True)

# Formulaire pour ajuster les charges d'investissement
with st.form(key="investissement_form"):
    st.markdown('<p class="sub-header">🏗️ Ajuster les charges d\'investissement initial</p>', unsafe_allow_html=True)
    for key in st.session_state.charges_investissement:
        st.session_state.charges_investissement[key] = st.number_input(
            f"{key} (DH)",
            min_value=0.0,
            value=float(st.session_state.charges_investissement[key]),
            step=1000.0,
            format="%.1f"
        )
    inv_submitted = st.form_submit_button("Mettre à jour les charges d'investissement")
    if inv_submitted:
        st.success("Charges d'investissement mises à jour!")
        indicateurs = calculer_indicateurs()

# 5. Charges d'investissement
st.markdown('<p class="sub-header">🏗️ Charges d\'investissement initial</p>', unsafe_allow_html=True)

# Regroupement des investissements
investissements_categories = {
    "Par terrain": [
        "Avance de terrain", "Construction", "Gazon", "Caméras de surveillance", "Caméras de filmage"
    ],
    "Communs": [
        "Publicités", "Stock initial", "Social Media et App", "Divers", "Création d'association"
    ]
}

# Tableau des investissements
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
    
    # Sous-total pour chaque catégorie
    if categorie == "Par terrain":
        montant_total = subtotal * st.session_state.nb_terrains
        inv_data.append({
            "Catégorie": categorie,
            "Investissement": f"Sous-total ({st.session_state.nb_terrains} terrains)",
            "Montant (DH)": f"{montant_total:.2f} DH"
        })
    else:
        inv_data.append({
            "Catégorie": categorie,
            "Investissement": "Sous-total",
            "Montant (DH)": f"{subtotal:.2f} DH"
        })

# Ligne de total pour les investissements
inv_data.append({
    "Catégorie": "",
    "Investissement": "📊 TOTAL INVESTISSEMENT",
    "Montant (DH)": f"{indicateurs['total_investissement']:.2f} DH"
})

df_inv = pd.DataFrame(inv_data)
st.dataframe(df_inv, use_container_width=True)

# 6. Analyse de rentabilité
st.markdown('<p class="sub-header">📈 Analyse de rentabilité</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="ROI mensuel",
        value=f"{indicateurs['roi_mensuel']:.2f}%"
    )

with col2:
    if indicateurs['profit_net'] > 0:
        st.metric(
            label="Temps de retour sur investissement",
            value=f"{indicateurs['temps_retour']:.1f} mois"
        )
        annees = int(indicateurs['temps_retour'] // 12)
        mois_restants = int(indicateurs['temps_retour'] % 12)
        if annees > 0:
            st.write(f"**{annees} ans et {mois_restants} mois** pour rentabiliser l'investissement.")
        else:
            st.write(f"**{mois_restants} mois** pour rentabiliser l'investissement.")
    else:
        st.error("❌ Avec les paramètres actuels, l'activité n'est pas rentable.")

# 7. Graphique de profit net par nombre de terrains
st.markdown('<p class="sub-header">🔄 Impact du nombre de terrains</p>', unsafe_allow_html=True)

# Calculer les profits pour différents nombres de terrains
max_terrains = 5
profits_par_terrain = []

for n in range(1, max_terrains + 1):
    nb_terrains_original = st.session_state.nb_terrains
    st.session_state.nb_terrains = n
    indicateurs_temp = calculer_indicateurs()
    profits_par_terrain.append(indicateurs_temp['profit_net'])
    st.session_state.nb_terrains = nb_terrains_original

# Créer le graphique
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(range(1, max_terrains + 1), profits_par_terrain, color='#2196F3')
ax.set_xlabel('Nombre de terrains')
ax.set_ylabel('Profit net mensuel (DH)')
ax.set_title('Évolution du profit net en fonction du nombre de terrains')
ax.set_xticks(range(1, max_terrains + 1))

# Ajouter les valeurs sur les barres
for i, profit in enumerate(profits_par_terrain):
    ax.text(i + 1, profit + 100, f'{profit:.2f} DH', ha='center')

st.pyplot(fig)

# 8. Conclusion
st.markdown('<p class="sub-header">🎯 Conclusion</p>', unsafe_allow_html=True)

if indicateurs['profit_net'] > 0:
    st.success(f"✅ Votre projet est rentable avec un profit net mensuel de {indicateurs['profit_net']:.2f} DH.")
    st.write(f"Vous pouvez rentabiliser votre investissement en environ {indicateurs['temps_retour']:.1f} mois.")
    
    # Trouver le nombre optimal de terrains
    nb_optimal = profits_par_terrain.index(max(profits_par_terrain)) + 1
    if nb_optimal != st.session_state.nb_terrains:
        st.info(f"💡 Conseil: {nb_optimal} terrain(s) pourrait maximiser votre profit net.")
else:
    st.error("❌ Avec les paramètres actuels, votre projet n'est pas rentable.")
    st.write("Essayez d'ajuster les paramètres pour améliorer la rentabilité:")
    st.write("- Augmenter le prix de location")
    st.write("- Augmenter le nombre de locations par jour")
    st.write("- Réduire les coûts fixes ou variables")
