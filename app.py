import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Global Power Plant",
    layout="wide"
)

# Título
st.title("Análisis Exploratorio del Global Power Plant Database")

# Cargar datos
df = pd.read_csv("global_power_plant_database.csv")

# Eliminar registros nulos necesarios
df = df.dropna(subset=["primary_fuel", "capacity_mw"])

# =====================
# SIDEBAR - FILTROS
# =====================

st.sidebar.header("Filtros")

combustible = st.sidebar.multiselect(
    "Tipo de combustible",
    options=sorted(df["primary_fuel"].unique()),
    default=sorted(df["primary_fuel"].unique())
)

capacidad = st.sidebar.slider(
    "Capacidad (MW)",
    int(df["capacity_mw"].min()),
    int(df["capacity_mw"].max()),
    (
        int(df["capacity_mw"].min()),
        int(df["capacity_mw"].max())
    )
)

# Aplicar filtros
df_filtrado = df[
    (df["primary_fuel"].isin(combustible)) &
    (df["capacity_mw"].between(capacidad[0], capacidad[1]))
]

# =====================
# MÉTRICAS
# =====================

st.header("Exploración de Datos")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Cantidad de registros",
    len(df_filtrado)
)

col2.metric(
    "Media capacidad (MW)",
    round(df_filtrado["capacity_mw"].mean(), 2)
)

col3.metric(
    "Desviación estándar",
    round(df_filtrado["capacity_mw"].std(), 2)
)

# =====================
# TABLA
# =====================

st.subheader("Datos filtrados")

st.dataframe(df_filtrado)

# =====================
# VISUALIZACIÓN 1
# =====================

st.subheader("Distribución de la capacidad instalada")

fig1, ax1 = plt.subplots(figsize=(8,4))

sns.histplot(
    data=df_filtrado,
    x="capacity_mw",
    bins=30,
    kde=True,
    color="steelblue",
    ax=ax1
)

st.pyplot(fig1)

# =====================
# VISUALIZACIÓN 2
# =====================

st.subheader("Capacidad por tipo de combustible")

fig2, ax2 = plt.subplots(figsize=(10,5))

sns.boxplot(
    data=df_filtrado,
    x="primary_fuel",
    y="capacity_mw",
    ax=ax2
)

plt.xticks(rotation=45)

st.pyplot(fig2)

# =====================
# VISUALIZACIÓN 3
# =====================

st.subheader("Cantidad de plantas por combustible")

fig3, ax3 = plt.subplots(figsize=(8,4))

df_filtrado["primary_fuel"].value_counts().plot(
    kind="bar",
    color="cornflowerblue",
    ax=ax3
)

ax3.set_xlabel("Combustible")
ax3.set_ylabel("Cantidad")

st.pyplot(fig3)

# =====================
# VALIDACIÓN ESTADÍSTICA
# =====================

st.header("Validación Estadística")

st.write("""
La prueba estadística realizada en el análisis mostró que existen diferencias entre los grupos evaluados.
Esto indica que las variaciones observadas no parecen ocurrir únicamente por azar y sugieren que el tipo de combustible está asociado a diferencias en las características de las plantas analizadas.
""")

# =====================
# HALLAZGOS
# =====================

st.header("Hallazgos del análisis")

st.write("""
• Las plantas presentan diferencias importantes en su capacidad instalada según la fuente de energía utilizada.

• Algunos tipos de combustible concentran una mayor cantidad de plantas dentro del conjunto de datos.

• Se observan valores extremos de capacidad que reflejan la existencia de centrales de gran escala.

• Los filtros permiten analizar de forma interactiva el comportamiento de las plantas según el combustible y la capacidad instalada.
""")