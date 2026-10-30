# ⚽ EDA Mundial de Fútbol 2026
## Formaciones, posesión, producción ofensiva y localía

Proyecto de **Análisis Exploratorio de Datos (EDA)** para estudiar la relación entre el rendimiento de los equipos y sus resultados en una muestra de partidos del Mundial de Fútbol 2026.

El análisis se centra en cuatro dimensiones: **formaciones tácticas, posesión, producción ofensiva y condición de local o visitante**. El objetivo es identificar patrones estadísticos asociados a la victoria, sin asumir que una asociación implique causalidad.

> **Informe final:** `Informe_Ejecutivo_EDA_Mundial_Futbol_2026.pdf` contiene el análisis, los gráficos, la interpretación de resultados y las limitaciones del estudio.

---

## 🎯 Objetivos

- Comparar el porcentaje de victorias según la formación táctica.
- Analizar la posesión según el resultado.
- Estudiar la relación entre posesión y tiros a puerta.
- Comparar el volumen de tiros totales y tiros a puerta según el resultado.
- Explorar la producción goleadora como indicador descriptivo de fuerza ofensiva.
- Comparar el rendimiento de los equipos locales y visitantes.
- Comunicar los resultados mediante gráficos y conclusiones interpretables.

## ❓ Preguntas de investigación

1. ¿Qué formaciones presentan un mayor porcentaje de victorias?
2. ¿Tener más posesión está asociado a obtener un mejor resultado?
3. ¿Existe relación entre posesión y tiros a puerta?
4. ¿Los equipos que ganan realizan más tiros?
5. ¿Cómo se distribuyen los goles por equipo y partido?
6. ¿Qué diferencias se observan entre jugar como local o visitante?
7. ¿Las formaciones muestran diferencias en la posesión media?

## 📊 Datos utilizados

- **Dataset:** [2026 FIFA World Cup — Kaggle](https://www.kaggle.com/datasets/mann14/2026-fifa-world-cup)
- **Archivo de trabajo:** `Data_Mundial_2026.csv`

### Tamaño de la muestra

| Indicador | Valor |
|---|---:|
| Partidos incluidos en el CSV | 104 |
| Partidos con ambos goles disponibles | 100 |
| Partidos excluidos del análisis de resultados por marcador incompleto | 4 |
| Observaciones equipo-partido analizadas | 200 |
| Columnas del CSV original | 42 |

### Unidad de análisis

La unidad de análisis es la **observación equipo-partido**: una fila representa las estadísticas de un equipo en un encuentro concreto. Cada partido genera dos observaciones, una por equipo. Por tanto, las 200 observaciones proceden de 100 partidos; no equivalen a 200 partidos independientes.

### Tratamiento de los datos

- Para analizar resultados se utilizan los partidos con ambos marcadores disponibles.
- El resultado se determina comparando los goles del equipo local y del visitante.
- No se imputan los marcadores ausentes.
- Los porcentajes por formación se interpretan junto con el número de apariciones.
- Las observaciones de ambos equipos del mismo partido están relacionadas.

## 🔎 Metodología

1. **Inspección:** revisión de la estructura, variables y disponibilidad de los marcadores.
2. **Preparación:** transformación de los datos al formato equipo-partido para comparar local y visitante.
3. **Indicadores:** cálculo del resultado, porcentajes de victorias y medidas descriptivas de goles y tiros.
4. **Análisis exploratorio:** comparación de distribuciones, medias, medianas y correlaciones.
5. **Visualización:** creación de gráficos para identificar patrones y diferencias.
6. **Interpretación:** elaboración de conclusiones considerando la muestra y sus limitaciones.

La correlación de Pearson resume asociaciones lineales, pero **no demuestra que una variable provoque otra**.

## 📈 Principales resultados

Los resultados siguientes describen exclusivamente la muestra analizada.

### 1. Formaciones y porcentaje de victorias

| Formación | Apariciones | Victorias | % de victorias |
|---|---:|---:|---:|
| 4-2-3-1 | 66 | 33 | 50,0 % |
| 4-1-4-1 | 49 | 24 | 49,0 % |
| 4-2-2-2 | 35 | 15 | 42,9 % |
| 3-4-3 | 15 | 2 | 13,3 % |
| 5-4-1 | 18 | 2 | 11,1 % |
| 5-3-2 | 7 | 0 | 0,0 % |

La formación 4-2-3-1 presenta el mayor porcentaje de victorias entre los sistemas mostrados. Esto no prueba que sea la causa del éxito: pueden influir la calidad del equipo, los rivales, el marcador y la localía.

### 2. Posesión según el resultado

| Resultado | Posesión media | Posesión mediana |
|---|---:|---:|
| Victoria | 56,3 % | 57,5 % |
| Empate | 50,0 % | 50,0 % |
| Derrota | 43,9 % | 42,5 % |

Los equipos que ganan presentan una posesión media superior en esta muestra. Sin embargo, **tener más posesión no garantiza ganar**: el control del balón debe interpretarse junto con la creación de ocasiones, los tiros y la eficacia.

### 3. Posesión y tiros a puerta

La correlación entre posesión y tiros a puerta es **0,52**, lo que indica una asociación lineal positiva en la muestra. No significa que aumentar la posesión provoque necesariamente más tiros a puerta en todos los partidos.

### 4. Volumen ofensivo según el resultado

| Resultado | Tiros totales medios | Tiros a puerta medios | Mediana de tiros a puerta |
|---|---:|---:|---:|
| Victoria | 14,88 | 6,04 | 5,5 |
| Empate | 13,43 | 4,12 | 3,0 |
| Derrota | 9,43 | 2,66 | 2,0 |

Los equipos ganadores registran, de media, más tiros totales y tiros a puerta. La correlación entre tiros a puerta y goles es **0,62**, frente a **0,44** entre tiros totales y goles. Esto muestra una asociación descriptiva entre la producción ofensiva y los goles, aunque no todos los disparos tienen la misma calidad.

### 5. Producción goleadora

La categoría más frecuente es **un gol por equipo-partido**, con 65 observaciones (32,5 %), seguida de los registros sin goles, con 53 observaciones (26,5 %).

En conjunto, el 59 % de las observaciones corresponden a equipos que anotaron uno o ningún gol. Los registros con cuatro goles o más representan el 9 % de la muestra.

### 6. Localía

| Condición | Victorias | Empates | Derrotas | % de victorias |
|---|---:|---:|---:|---:|
| Local | 50 | 20 | 30 | 50,0 % |
| Visitante | 30 | 20 | 50 | 30,0 % |

En esta muestra, los equipos locales presentan un porcentaje de victorias superior al de los visitantes. Los locales promedian 1,76 goles frente a 1,26 de los visitantes. Es un patrón descriptivo, no una estimación universal del efecto de jugar en casa.

### 7. Formaciones y posesión

La posesión media varía entre las formaciones analizadas. Estas diferencias también pueden depender de la identidad y el estilo de los equipos, la calidad de los rivales y el estado del marcador. Las formaciones con pocas apariciones requieren especial cautela.

## Aplicación interactiva con Streamlit

Como ampliación del análisis exploratorio de datos (EDA), se ha desarrollado una aplicación interactiva utilizando **Streamlit**, que permite visualizar y explorar los datos del Mundial de Fútbol 2026 de una forma dinámica.

El objetivo es transformar los resultados del análisis en un dashboard interactivo, facilitando la consulta de estadísticas, comparativas y patrones de comportamiento de los equipos.

### Funcionalidades del dashboard

La aplicación está organizada en diferentes secciones:

- **Resumen general:** indicadores principales, distribución de resultados y estadísticas generales.
- **Análisis de formaciones:** comparación de sistemas tácticos y porcentajes de victorias.
- **Posesión:** relación entre posesión del balón, goles y resultados.
- **Producción ofensiva:** análisis de tiros totales, tiros a puerta y correlaciones.
- **Local vs visitante:** comparación del rendimiento según la condición del equipo.
- **Explorador de partidos:** consulta de encuentros, marcadores y estadísticas individuales.

## 🧰 Herramientas

- **Python** para preparar y analizar los datos.
- **Pandas** y **NumPy** para manipulación y cálculo.
- **Matplotlib** para visualizaciones.
- **Jupyter Notebook** para documentar y ejecutar el análisis.
- **Git y GitHub** para control de versiones y publicación.
- **Kaggle** como fuente del dataset.
- **Streamlit** para dashboar interactivo.

## 📁 Estructura del proyecto

Una organización recomendada para el repositorio es:

```text
EDA-Mundial-2026/
├── data/
│   └── Data_Mundial_2026.csv
├── notebooks/
│   └── EDA_Mundial_2026.ipynb
├── informes/
│   └── Informe_Ejecutivo_EDA_Mundial_Futbol_2026.pdf
├── Streamlit/
│   ├── app.py
│   └── requirements.txt
├── README.md
└── requirements.txt
```

Adapta los nombres y rutas a los archivos reales del repositorio; no añadas rutas que no existan.

## ⚠️ Limitaciones

- Se analizan 100 partidos con ambos marcadores disponibles, de los 104 registros del CSV.
- La muestra puede no representar todos los partidos del torneo; no debe generalizarse sin comprobar su cobertura.
- Las observaciones de local y visitante proceden del mismo encuentro y están relacionadas.
- Los porcentajes por formación pueden ser inestables cuando hay pocas apariciones.
- Los tiros a puerta no miden por completo la calidad de las ocasiones; no se dispone aquí de una medida completa de goles esperados (xG).
- Las asociaciones observadas no prueban causalidad ni controlan por sí solas la calidad del equipo, la fuerza del rival, la fase del torneo o el contexto del marcador.

## ✅ Conclusiones

En esta muestra, las victorias aparecen asociadas a una mayor posesión media y, especialmente, a un mayor volumen de tiros a puerta. También se observan diferencias en los porcentajes de victorias según la formación y la condición de local o visitante.

Ninguna de estas variables garantiza por sí sola la victoria. La lectura más útil combina posesión, tiros, goles, formación y localía, considerando el tamaño de la muestra y el contexto de cada encuentro.

Como futuras líneas de trabajo, se propone incorporar xG, distinguir las fases del torneo y controlar por la fortaleza de los equipos y sus rivales.

---

## 👥 Autoría

Proyecto realizado en el contexto del **Bootcamp de Data Analytics**.

- Javier Carnero Frías
- Daniel Gámez Soto

## 📄 Informe final

Consulta `Informe_Ejecutivo_EDA_Mundial_Futbol_2026.pdf`, incluido en el repositorio, para ver el desarrollo completo, los gráficos y la interpretación de los resultados.
