
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# =====================================================
# 1. CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Mundial 2026 | Football Analytics",
    page_icon="⚽",
    layout="wide"
)

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
CSV_PATH = ROOT_DIR / "data" / "Data_Mundial_2026.csv"

# =====================================================
# 2. ESTILO VISUAL
# =====================================================

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }

    [data-testid="stMetric"] {
        background-color: #1b2533;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #34445a;
    }

    [data-testid="stMetricLabel"] {
        color: #b7c5d8;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    div[data-testid="stSidebar"] {
        background-color: #17212e;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. CARGA DE DATOS
# =====================================================

@st.cache_data
def cargar_datos():

    if not CSV_PATH.exists():
        st.error(
            f"No se encuentra el CSV en: {CSV_PATH}"
        )
        st.stop()

    df = pd.read_csv(CSV_PATH)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    columnas_numericas = [
        "home_score", "away_score",
        "home_possession", "away_possession",
        "home_sot", "away_sot",
        "home_total_shots", "away_total_shots",
        "home_saves", "away_saves",
        "home_cards_yellow", "away_cards_yellow",
        "home_cards_red", "away_cards_red",
        "home_fouls", "away_fouls",
        "home_corners", "away_corners",
        "home_crosses", "away_crosses",
        "home_interceptions", "away_interceptions"
    ]

    for col in columnas_numericas:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df


df = cargar_datos()


# =====================================================
# 4. PREPARACIÓN DE DATOS
# =====================================================

partidos = df.dropna(
    subset=["home_score", "away_score"]
).copy()


def crear_observaciones(partidos):

    local = pd.DataFrame({
        "partido": partidos.index,
        "fecha": partidos["date"],
        "fase": partidos["round"],
        "equipo": partidos["home_team"],
        "rival": partidos["away_team"],
        "condicion": "Local",
        "goles": partidos["home_score"],
        "goles_rival": partidos["away_score"],
        "posesion": partidos["home_possession"],
        "tiros": partidos["home_total_shots"],
        "tiros_puerta": partidos["home_sot"],
        "formacion": partidos["home_formation"],
        "corners": partidos["home_corners"],
        "faltas": partidos["home_fouls"],
        "amarillas": partidos["home_cards_yellow"],
        "rojas": partidos["home_cards_red"]
    })

    visitante = pd.DataFrame({
        "partido": partidos.index,
        "fecha": partidos["date"],
        "fase": partidos["round"],
        "equipo": partidos["away_team"],
        "rival": partidos["home_team"],
        "condicion": "Visitante",
        "goles": partidos["away_score"],
        "goles_rival": partidos["home_score"],
        "posesion": partidos["away_possession"],
        "tiros": partidos["away_total_shots"],
        "tiros_puerta": partidos["away_sot"],
        "formacion": partidos["away_formation"],
        "corners": partidos["away_corners"],
        "faltas": partidos["away_fouls"],
        "amarillas": partidos["away_cards_yellow"],
        "rojas": partidos["away_cards_red"]
    })

    datos = pd.concat(
        [local, visitante],
        ignore_index=True
    )

    datos["resultado"] = np.select(
        [
            datos["goles"] > datos["goles_rival"],
            datos["goles"] == datos["goles_rival"]
        ],
        [
            "Victoria",
            "Empate"
        ],
        default="Derrota"
    )

    datos["victoria"] = (
        datos["resultado"] == "Victoria"
    ).astype(int)

    return datos


datos = crear_observaciones(partidos)


# =====================================================
# 5. FILTROS
# =====================================================

st.sidebar.title("⚽ Filtros")

fases = ["Todas"] + sorted(
    datos["fase"].dropna().unique().tolist()
)

fase_seleccionada = st.sidebar.selectbox(
    "Fase del torneo",
    fases
)

equipos = ["Todos"] + sorted(
    datos["equipo"].dropna().unique().tolist()
)

equipo_seleccionado = st.sidebar.selectbox(
    "Equipo",
    equipos
)

condiciones = [
    "Ambos",
    "Local",
    "Visitante"
]

condicion_seleccionada = st.sidebar.selectbox(
    "Condición",
    condiciones
)

datos_filtrados = datos.copy()

if fase_seleccionada != "Todas":
    datos_filtrados = datos_filtrados[
        datos_filtrados["fase"] == fase_seleccionada
    ]

if equipo_seleccionado != "Todos":
    datos_filtrados = datos_filtrados[
        datos_filtrados["equipo"] == equipo_seleccionado
    ]

if condicion_seleccionada != "Ambos":
    datos_filtrados = datos_filtrados[
        datos_filtrados["condicion"] == condicion_seleccionada
    ]


# =====================================================
# 6. CABECERA Y KPIs
# =====================================================

st.title("⚽ MUNDIAL 2026")
st.subheader("Football Analytics Dashboard")

st.markdown(
    "Análisis táctico, estadístico y ofensivo "
    "del Mundial de Fútbol 2026."
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Partidos analizados",
    f"{datos_filtrados['partido'].nunique():,}"
)

col2.metric(
    "Observaciones",
    f"{len(datos_filtrados):,}"
)

col3.metric(
    "Goles anotados",
    f"{datos_filtrados['goles'].sum():.0f}"
)

col4.metric(
    "Posesión media",
    f"{datos_filtrados['posesion'].mean():.1f}%"
)

st.divider()


# =====================================================
# 7. PESTAÑAS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Resumen",
    "🧠 Formaciones",
    "⚽ Posesión",
    "🎯 Ataque",
    "🏟️ Local vs Visitante",
    "🔎 Partidos"
])


# =====================================================
# TAB 1: RESUMEN
# =====================================================

with tab1:

    st.header("Resumen general")

    col1, col2 = st.columns(2)

    with col1:

        resultados = (
            datos_filtrados["resultado"]
            .value_counts()
            .reindex(
                ["Victoria", "Empate", "Derrota"],
                fill_value=0
            )
            .reset_index()
        )

        resultados.columns = [
            "Resultado", "Cantidad"
        ]

        fig = px.pie(
            resultados,
            names="Resultado",
            values="Cantidad",
            hole=0.55,
            title="Distribución de resultados"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        goles_resultado = (
            datos_filtrados.groupby("resultado")["goles"]
            .mean()
            .reindex(
                ["Victoria", "Empate", "Derrota"]
            )
            .reset_index()
        )

        goles_resultado.columns = [
            "Resultado", "Goles medios"
        ]

        fig = px.bar(
            goles_resultado,
            x="Resultado",
            y="Goles medios",
            color="Resultado",
            title="Goles medios según resultado",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Estadísticas por resultado")

    resumen = (
        datos_filtrados.groupby("resultado")
        .agg(
            Observaciones=("equipo", "count"),
            Posesion_media=("posesion", "mean"),
            Tiros_medios=("tiros", "mean"),
            Tiros_puerta=("tiros_puerta", "mean"),
            Goles_medios=("goles", "mean")
        )
        .reindex(
            ["Victoria", "Empate", "Derrota"]
        )
        .reset_index()
    )

    st.dataframe(
        resumen.round(2),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TAB 2: FORMACIONES
# =====================================================

with tab2:

    st.header("Análisis táctico")

    st.write(
        "¿Qué sistemas tácticos presentan un mayor "
        "porcentaje de victorias?"
    )

    formaciones = (
        datos_filtrados
        .dropna(subset=["formacion"])
        .groupby("formacion")
        .agg(
            Apariciones=("equipo", "count"),
            Victorias=("victoria", "sum"),
            Posesion=("posesion", "mean")
        )
        .reset_index()
    )

    formaciones["Porcentaje_victorias"] = (
        formaciones["Victorias"] /
        formaciones["Apariciones"] * 100
    )

    minimo = st.slider(
        "Mínimo de apariciones por formación",
        min_value=1,
        max_value=20,
        value=4
    )

    formaciones_filtradas = formaciones[
        formaciones["Apariciones"] >= minimo
    ].sort_values(
        "Porcentaje_victorias"
    )

    fig = px.bar(
        formaciones_filtradas,
        x="Porcentaje_victorias",
        y="formacion",
        orientation="h",
        color="Porcentaje_victorias",
        text="Porcentaje_victorias",
        hover_data=["Apariciones", "Victorias"],
        title="Porcentaje de victorias por formación"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Posesión media por formación")

    fig = px.bar(
        formaciones.sort_values(
            "Posesion",
            ascending=False
        ),
        x="formacion",
        y="Posesion",
        color="Posesion",
        title="Posesión media según sistema táctico"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        formaciones.sort_values(
            "Porcentaje_victorias",
            ascending=False
        ).round(2),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TAB 3: POSESIÓN
# =====================================================

with tab3:

    st.header("Posesión y resultados")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.box(
            datos_filtrados,
            x="resultado",
            y="posesion",
            color="resultado",
            category_orders={
                "resultado": [
                    "Victoria",
                    "Empate",
                    "Derrota"
                ]
            },
            title="Distribución de posesión por resultado"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.scatter(
            datos_filtrados,
            x="posesion",
            y="goles",
            color="resultado",
            hover_data=["equipo", "rival"],
            title="Posesión y goles"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    correlacion = datos_filtrados[
        ["posesion", "goles", "victoria"]
    ].corr()

    st.subheader("Matriz de correlación")

    fig = px.imshow(
        correlacion,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlación de Pearson"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "La correlación muestra asociaciones estadísticas, "
        "no relaciones de causalidad."
    )


# =====================================================
# TAB 4: ATAQUE
# =====================================================

with tab4:

    st.header("Producción ofensiva")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.scatter(
            datos_filtrados,
            x="posesion",
            y="tiros_puerta",
            color="resultado",
            size="tiros",
            hover_data=["equipo", "rival"],
            title="Posesión frente a tiros a puerta"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        ataque = (
            datos_filtrados.groupby("resultado")
            .agg(
                Tiros_totales=("tiros", "mean"),
                Tiros_puerta=("tiros_puerta", "mean")
            )
            .reindex(
                ["Victoria", "Empate", "Derrota"]
            )
            .reset_index()
            .melt(
                id_vars="resultado",
                var_name="Tipo",
                value_name="Media"
            )
        )

        fig = px.bar(
            ataque,
            x="resultado",
            y="Media",
            color="Tipo",
            barmode="group",
            title="Volumen ofensivo según resultado"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Correlación ofensiva")

    correlacion_ataque = datos_filtrados[
        ["tiros_puerta", "tiros", "goles"]
    ].corr()

    st.dataframe(
        correlacion_ataque.round(2),
        use_container_width=True
    )


# =====================================================
# TAB 5: LOCAL VS VISITANTE
# =====================================================

with tab5:

    st.header("Ventaja de jugar en casa")

    localia = (
        datos_filtrados
        .groupby("condicion")
        .agg(
            Observaciones=("equipo", "count"),
            Victorias=("victoria", "sum"),
            Goles=("goles", "mean"),
            Posesion=("posesion", "mean"),
            Tiros=("tiros", "mean"),
            Tiros_puerta=("tiros_puerta", "mean")
        )
        .reset_index()
    )

    localia["Porcentaje_victorias"] = (
        localia["Victorias"] /
        localia["Observaciones"] * 100
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            localia,
            x="condicion",
            y="Porcentaje_victorias",
            color="condicion",
            text="Porcentaje_victorias",
            title="Porcentaje de victorias"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        comparativa = localia.melt(
            id_vars="condicion",
            value_vars=[
                "Goles",
                "Posesion",
                "Tiros",
                "Tiros_puerta"
            ],
            var_name="Estadística",
            value_name="Media"
        )

        fig = px.bar(
            comparativa,
            x="Estadística",
            y="Media",
            color="condicion",
            barmode="group",
            title="Comparativa estadística"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Datos de localía")

    st.dataframe(
        localia.round(2),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TAB 6: EXPLORADOR DE PARTIDOS
# =====================================================

with tab6:

    st.header("Explorador de partidos")

    partidos_explorar = partidos.copy()

    if fase_seleccionada != "Todas":
        partidos_explorar = partidos_explorar[
            partidos_explorar["round"] == fase_seleccionada
        ]

    if equipo_seleccionado != "Todos":
        partidos_explorar = partidos_explorar[
            (partidos_explorar["home_team"] == equipo_seleccionado) |
            (partidos_explorar["away_team"] == equipo_seleccionado)
        ]

    partidos_explorar["Marcador"] = (
        partidos_explorar["home_score"].astype(int).astype(str)
        + " - "
        + partidos_explorar["away_score"].astype(int).astype(str)
    )

    columnas_mostrar = [
        "date",
        "round",
        "home_team",
        "Marcador",
        "away_team",
        "home_formation",
        "away_formation",
        "home_possession",
        "away_possession"
    ]

    st.dataframe(
        partidos_explorar[columnas_mostrar].sort_values("date"),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Detalle de un partido")

    opciones = partidos_explorar.index.tolist()

    if opciones:

        partido_id = st.selectbox(
            "Selecciona un partido",
            opciones,
            format_func=lambda x: (
                f"{partidos.loc[x, 'home_team']} "
                f"vs {partidos.loc[x, 'away_team']}"
            )
        )

        partido = partidos.loc[partido_id]

        st.markdown(
            f"### {partido['home_team']} "
            f"{int(partido['home_score'])} - "
            f"{int(partido['away_score'])} "
            f"{partido['away_team']}"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                f"Posesión {partido['home_team']}",
                f"{partido['home_possession']}%"
            )

            st.metric(
                "Tiros a puerta",
                int(partido["home_sot"])
            )

            st.write(
                "Formación:",
                partido["home_formation"]
            )

        with c2:

            st.metric(
                f"Posesión {partido['away_team']}",
                f"{partido['away_possession']}%"
            )

            st.metric(
                "Tiros a puerta",
                int(partido["away_sot"])
            )

            st.write(
                "Formación:",
                partido["away_formation"]
            )

    else:
        st.warning(
            "No hay partidos para los filtros seleccionados."
        )


# =====================================================
# 8. PIE DE PÁGINA
# =====================================================

st.divider()

st.caption(
    "Mundial 2026 | Football Analytics | "
    "Proyecto de Data Analytics"
)

st.caption(
    "Fuente: Kaggle - 2026 FIFA World Cup Dataset. "
    "Análisis descriptivo; no implica causalidad."
)
