# ==========================================================
# REPORTE DIARIO DE TERMINALES
# SER COMUNICACIONES S.A.S
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image
from pathlib import Path

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(
    page_title="Reporte Diario de Terminales",
    page_icon="📱",
    layout="wide"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background-color:#F5F7FA;
}

h1{
    color:#C00000;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:15px;
    border-left:6px solid #C00000;
    box-shadow:0px 2px 8px rgba(0,0,0,.15);
}

section[data-testid="stSidebar"]{
    background:#F0F2F6;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# CARGAR ARCHIVO
# ==========================================================

@st.cache_data
def cargar():

    ruta = Path(__file__).parent / "ventas.xlsx"

    df = pd.read_excel(
        ruta,
        sheet_name="Detallado"
    )

    df.columns = df.columns.str.strip()

    return df

df = cargar()

# ==========================================================
# FECHA
# ==========================================================

if "Fecha" in df.columns:
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# ==========================================================
# TERMINALES
# ==========================================================

df["ProductoDeVenta"] = (
    df["ProductoDeVenta"]
    .astype(str)
    .str.upper()
    .str.strip()
)

filtro_terminales = (
    df["ProductoDeVenta"].str.contains(
        "KIT PREPAGO|FINANCIAMIENTO|EQUIPOS REPOSIC|POSTPAGO|KIT FINANCIADO",
        regex=True,
        na=False
    )
)

df = df[filtro_terminales].copy()

df["Producto"] = "TERMINALES"

# ==========================================================
# CAMBIAR NOMBRE A TERMINALES
# ==========================================================

df["Producto"] = "TERMINALES"

# ==========================================================
# ENCABEZADO
# ==========================================================

col1,col2 = st.columns([1,6])

with col1:

    if Path("logo.png").exists():
        st.image("logo.png", width=130)

with col2:

    st.markdown("""
    <h1 style='margin-bottom:0'>
    REPORTE DIARIO DE TERMINALES DEL 1 AL 30 DE JULIO
    </h1>

    <h4 style='color:gray;margin-top:0'>
    SER COMUNICACIONES S.A.S.
    </h4>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Filtros")

# ==========================================================
# FECHA
# ==========================================================

if "Fecha" in df.columns:

    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

    fecha_min = df["Fecha"].min().date()
    fecha_max = df["Fecha"].max().date()

    rango = st.sidebar.date_input(
        "📅 Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

    if len(rango) == 2:
        inicio, fin = rango

        df = df[
            (df["Fecha"].dt.date >= inicio) &
            (df["Fecha"].dt.date <= fin)
        ]

# ==========================
# SUCURSAL
# ==========================

opciones = ["Todas"] + sorted(df["Sucursal"].dropna().unique().tolist())

sucursal = st.sidebar.selectbox(
    "🏢 Sucursal",
    opciones
)

if sucursal != "Todas":
    df = df[df["Sucursal"] == sucursal]

# Rol

opciones = ["Todos"] + sorted(df["Rol"].dropna().unique().tolist())

rol = st.sidebar.selectbox(
    "👤 Rol",
    opciones
)

if rol != "Todos":
    df = df[df["Rol"] == rol]


# Marca
opciones = ["Todas"] + sorted(df["Marca"].dropna().unique().tolist())

marca = st.sidebar.selectbox(
    "📱 Marca",
    opciones
)

if marca != "Todas":
    df = df[df["Marca"] == marca]

# Vendedor
opciones = ["Todos"] + sorted(df["NombreVendedor"].dropna().unique().tolist())

vendedor = st.sidebar.selectbox(
    "👤 Vendedor",
    opciones
)

if vendedor != "Todos":
    df = df[df["NombreVendedor"] == vendedor]

# ==========================================================
# KPIs
# ==========================================================

equipos = int(df["Cantidad"].sum())

valor = float(df["ValorNeto"].sum())

marcas = df["Marca"].nunique()

referencias = df["Referencia"].nunique()

vendedores = df["NombreVendedor"].nunique()

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "📱 Equipos",
    f"{equipos:,}"
)

c2.metric(
    "💰 Valor",
    f"${valor:,.0f}"
)

c3.metric(
    "🏷️ Marcas",
    marcas
)

c4.metric(
    "📦 Referencias",
    referencias
)

c5.metric(
    "👤 Vendedores",
    vendedores
)

#st.divider()

#st.info("✅ Dashboard cargado correctamente. En la siguiente parte agregaremos los gráficos y las tablas dinámicas.")

#st.divider()

# ==========================================================
# GRAFICOS
# ==========================================================

st.subheader("📊 Resumen General")

col1, col2 = st.columns(2)

ventas_marca = (
    df.groupby("Marca", as_index=False)["Cantidad"]
    .sum()
    .sort_values("Cantidad", ascending=False)
)

fig1 = px.bar(
    ventas_marca,
    x="Marca",
    y="Cantidad",
    text="Cantidad",
    color="Cantidad",
    color_continuous_scale="Reds",
    title="Ventas por Marca"
)

fig1.update_traces(

    texttemplate="%{text:,.0f}",
    textposition="outside",

    textfont=dict(
        size=18,
        color="black",
        family="Arial Black"
    ),

    cliponaxis=False

)

fig1.update_yaxes(

    range=[0, ventas_marca["Cantidad"].max()*1.20],
    title="Cantidad",
    title_font=dict(size=18,color="black"),
    tickfont=dict(size=14,color="black")

)

fig1.update_xaxes(

    tickfont=dict(
        size=14,
        color="black"
    )

)

fig1.update_layout(

    height=480,

    showlegend=False,

    title=dict(

        text="📱 Ventas por Marca",

        x=0.5,

        font=dict(
            size=22,
            color="black"
        )

    ),

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(
        size=15,
        color="black"
    ),

    margin=dict(
        t=80,
        l=30,
        r=30,
        b=30
    )
)

col1.plotly_chart(fig1, use_container_width=True)

ventas_rol = (
    df.groupby("Rol", as_index=False)["Cantidad"]
    .sum()
    .sort_values("Cantidad", ascending=False)
)

fig2 = px.bar(
    ventas_rol,
    x="Rol",
    y="Cantidad",
    text="Cantidad",
    color="Cantidad",
    color_continuous_scale="Blues",
    title="Ventas por Rol"
)

fig2.update_traces(

    texttemplate="%{text:,.0f}",

    textposition="outside",

    textfont=dict(

        size=18,

        color="black",

        family="Arial Black"

    ),

    cliponaxis=False

)

fig2.update_yaxes(

    range=[0, ventas_rol["Cantidad"].max()*1.20],

    title="Cantidad",

    title_font=dict(size=18,color="black"),

    tickfont=dict(size=14,color="black")

)

fig2.update_xaxes(

    tickfont=dict(

        size=14,

        color="black"

    )

)

fig2.update_layout(

    height=480,

    showlegend=False,

    title=dict(

        text="👥 Ventas por Rol",

        x=0.5,

        font=dict(

            size=22,

            color="black"

        )

    ),

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(

        size=15,

        color="black"

    ),

    margin=dict(

        t=80,

        l=30,

        r=30,

        b=30

    )

)


col2.plotly_chart(fig2, use_container_width=True)

st.divider()

# ==========================================================
# TABLA 1
# REFERENCIA vs ROL
# ==========================================================

st.subheader("📋 Cantidad de Terminales por Referencia y Rol")

# Orden que siempre tendrán los roles
# Obtener todos los roles existentes en el archivo
orden_roles = (
    df.groupby("Rol")["Cantidad"]
      .sum()
      .sort_values(ascending=False)
      .index
      .tolist()
)

# Crear tabla dinámica
tabla_ref = pd.pivot_table(
    df,
    values="Cantidad",
    index="Referencia",
    columns="Rol",
    aggfunc="sum",
    fill_value=0
)

# Agregar columnas que no existan
for rol in orden_roles:
    if rol not in tabla_ref.columns:
        tabla_ref[rol] = 0

# Reordenar columnas
# Solo deja los roles que realmente existen
columnas = [c for c in orden_roles if c in tabla_ref.columns]

tabla_ref = tabla_ref[columnas]

# Total
tabla_ref["TOTAL"] = tabla_ref.sum(axis=1)

# Ordenar por Total
tabla_ref = tabla_ref.sort_values(
    by="TOTAL",
    ascending=False
)

# Total General
fila_total = pd.DataFrame(
    tabla_ref.sum()
).T

fila_total.index = ["TOTAL GENERAL"]

tabla_ref = pd.concat([tabla_ref, fila_total])

# Formatear números
tabla_mostrar = tabla_ref.copy()

for col in tabla_mostrar.columns:
    tabla_mostrar[col] = tabla_mostrar[col].map(lambda x: f"{x:,.0f}")

st.table(tabla_mostrar)


