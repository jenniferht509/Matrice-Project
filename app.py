import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("📊 Modèl Popilasyon Pòtoprens")
st.markdown("""
**Etidyan : Léa Jennifer Mondésir**  
**Fakilte Syans Enfòmatik**

---

### Eksplikasyon pwojè a 

Nou ap itilize **Chèn Markov** pou modèlize kijan popilasyon Pòtoprens ka chanje chak ane.  
- Chak **eta** reprezante yon kategori sosyal: Travay, Chomaj, Komèsan, Lekòl, Jèn deyò lekòl, Bandi.  
- **Matrice tranzisyon an** montre pwobabilite pou yon moun pase soti nan yon eta pou ale nan yon lòt.  
- **Eta inisyal la** se distribisyon popilasyon an nan premye ane a.  
- Fòmil la se: `X_{k+1} = P × X_k`  
- Lè nou repete kalkil la, nou ka prevwa evolisyon popilasyon an sou plizyè ane.  
""")

categories = ["Travay", "Chomaj", "Komèsan", "Lekòl", "Deyò lekòl", "Bandi"]

default_matrix = np.array([
    [0.70, 0.20, 0.05, 0.03, 0.01, 0.01],
    [0.30, 0.50, 0.10, 0.05, 0.03, 0.02],
    [0.10, 0.15, 0.60, 0.05, 0.05, 0.05],
    [0.05, 0.05, 0.05, 0.70, 0.10, 0.05],
    [0.10, 0.20, 0.05, 0.10, 0.45, 0.10],
    [0.05, 0.10, 0.05, 0.05, 0.05, 0.70]
])

default_X0 = np.array([0.25, 0.35, 0.10, 0.15, 0.10, 0.05])

population = st.slider("Popilasyon total Pòtoprens", 500000, 1500000, 1000000)
years = st.slider("Konbyen ane pou simile", 1, 20, 10)

st.subheader("📐 Matrice tranzisyon (ou ka modifye)")
P = []
for i, cat in enumerate(categories):
    row = []
    cols = st.columns(len(categories))
    for j, target in enumerate(categories):
        val = cols[j].number_input(
            f"{cat} → {target}",
            min_value=0.0, max_value=1.0,
            value=float(default_matrix[i][j]),
            step=0.01, key=f"{i}-{j}"
        )
        row.append(val)
    row = np.array(row)
    row = row / row.sum()
    P.append(row)
P = np.array(P)

st.write("✅ Matrice aktyèl:", P)

st.subheader("📌 Eta inisyal (proportion)")
X0 = []
cols = st.columns(len(categories))
for i, cat in enumerate(categories):
    val = cols[i].number_input(
        f"{cat}",
        min_value=0.0, max_value=1.0,
        value=float(default_X0[i]),
        step=0.01, key=f"init-{i}"
    )
    X0.append(val)
X0 = np.array(X0)
X0 = X0 / X0.sum()

states = [X0]
for _ in range(years):
    states.append(np.dot(states[-1], P))
states = np.array(states) * population

fig = go.Figure()
for i, cat in enumerate(categories):
    fig.add_trace(go.Scatter(
        x=list(range(years+1)),
        y=states[:, i],
        mode="lines+markers",
        name=cat
    ))

fig.update_layout(
    title="Evolisyon popilasyon Pòtoprens pa kategori",
    xaxis_title="Ane",
    yaxis_title="Nimewo moun",
    template="plotly_dark",
    legend=dict(title="Kategori")
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Rezilta final apre simulation")
for i, cat in enumerate(categories):
    st.write(f"{cat} : {int(states[-1][i])} moun")
