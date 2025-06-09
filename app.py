import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff





st.set_page_config(page_title="Visualizador de Datos", layout="wide")

st.title("📊 Visualizador de Datos desde Excel o CSV")

# Sidebar
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <img src="https://img.freepik.com/vector-gratis/ilustracion-negocio-analisis-datos-estadisticos_24908-59546.jpg" width="150">
        <p></p>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <h1> Bienvenido a la app de Visualización de Datos </h1>
        <br/>
        Esta app permite cargar archivos con las siguientes extensiones: .xslx y .csv
        <br/><br/>
        <img src="https://dev.a1office.co/wp-content/uploads/2022/05/750-7505563_csv-or-excel-icon-png-download-excel-csv.png" width="150">
        <br/><br/>
        Proyecto creado por Salvador Joaquin Matías Ríos Sáenz
        <br/><br/>
        2025
    </div>
    """,
    unsafe_allow_html=True
)
archivo = st.file_uploader("Sube un archivo Excel o CSV", type=["csv", "xlsx"])
df = Non
if archivo is not None:
    try:
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        st.success("✅ Archivo cargado correctamente")
        st.write("Vista previa de los datos:")
        st.dataframe(df)

        columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()

        if len(columnas_numericas) == 0:
            st.warning("No se encontraron columnas numéricas para graficar.")
        else:
            st.subheader("📈 Gráficos Automáticos")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Histograma")
                eje_x_hist = st.selectbox("Selecciona el eje X para el histograma", columnas_numericas, key="hist_x")
                fig1 = px.histogram(
                    df,
                    x=eje_x_hist,
                    nbins=30,
                    color_discrete_sequence=["#7EC8E3"],
                )
                fig1.update_traces(marker_line_color='black', marker_line_width=1)
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.markdown("### Gráfico de líneas")
                eje_x_line = st.selectbox("Eje X (línea)", df.select_dtypes(include=["object", "category"]).columns,
                                          key="line_x")
                eje_y_line = st.selectbox("Eje Y (línea)", columnas_numericas, key="line_y")

                # Ordenar si el eje es 'Mes'
                if eje_x_line == "Mes" and "Mes" in df.columns:
                    orden_meses = [
                        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
                    ]
                    df["Mes"] = pd.Categorical(df["Mes"], categories=orden_meses, ordered=True)

                df_grouped = df.groupby(eje_x_line)[eje_y_line].sum().reset_index()
                fig2 = px.line(df_grouped, x=eje_x_line, y=eje_y_line)
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 📊 Gráfico de barras")
            eje_x_bar = st.selectbox("Eje X (barras)", df.select_dtypes(include=["object", "category"]).columns,
                                     key="bar_x")
            eje_y_bar = st.selectbox("Eje Y (barras)", columnas_numericas, key="bar_y")
            df_bar = df.groupby(eje_x_bar)[eje_y_bar].sum().reset_index()
            fig3 = px.bar(df_bar, x=eje_x_bar, y=eje_y_bar)
            st.plotly_chart(fig3, use_container_width=True)

            st.markdown("### 🥧 Gráfico de Pastel (Pie Chart)")
            columna_pie = st.selectbox("Selecciona columna para Pie Chart",
            df.select_dtypes(include=["object", "category"]).columns)
            conteo_pie = df[columna_pie].value_counts().reset_index()
            conteo_pie.columns = [columna_pie, 'Frecuencia']
            fig5 = px.pie(conteo_pie, values='Frecuencia', names=columna_pie)
            st.plotly_chart(fig5, use_container_width=True)


            def mostrar_indicadores_filtrados(df):
                st.markdown("## 🎛 Filtros de datos")

                # Filtro por Departamento
                if "Departamento" in df.columns:
                    regiones = sorted(df["Departamento"].dropna().unique())
                    seleccion_regiones = st.multiselect("Filtrar por Departamento", regiones, default=regiones)
                else:
                    seleccion_regiones = df["Departamento"].unique()

                # Filtro por Mes
                if "Mes" in df.columns:
                    meses = [
                        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
                    ]
                    seleccion_meses = st.multiselect("Filtrar por Mes", meses, default=meses)
                    df["Mes"] = pd.Categorical(df["Mes"], categories=meses, ordered=True)
                else:
                    seleccion_meses = df["Mes"].unique()

                # Aplicar filtros
                df_filtrado = df.copy()
                if "Departamento" in df.columns:
                    df_filtrado = df_filtrado[df_filtrado["Departamento"].isin(seleccion_regiones)]
                if "Mes" in df.columns:
                    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(seleccion_meses)]

                # Mostrar KPIs
                st.markdown("## 📌 Indicadores generales (según filtros aplicados)")
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Prom. de Ventas", f"{df_filtrado['Ventas'].mean():,.2f}")
                kpi2.metric("Prom. de Costo", f"{df_filtrado['Costo'].mean():,.2f}")
                kpi3.metric("Prom. de Ganancia", f"{df_filtrado['Ganancia'].mean():,.2f}")

                kpi4, kpi5, kpi6 = st.columns(3)
                kpi4.metric("Mayor venta", f"{df_filtrado['Ventas'].max():,.0f}")
                kpi5.metric("Menor venta", f"{df_filtrado['Ventas'].min():,.0f}")
                kpi6.metric("Costo máximo", f"{df_filtrado['Costo'].max():,.0f}")

                kpi7, _, _ = st.columns(3)
                kpi7.metric("Ganancia total", f"{df_filtrado['Ganancia'].sum():,.0f}")

                return df_filtrado


            df = mostrar_indicadores_filtrados(df)

            st.markdown("## 🗺️ MAPA DE CALOR")

            coordenadas_departamentos = {
                "Lima": {"Latitud": -12.0464, "Longitud": -77.0428},
                "Cusco": {"Latitud": -13.5319, "Longitud": -71.9675},
                "Arequipa": {"Latitud": -16.4090, "Longitud": -71.5375},
                "La Libertad": {"Latitud": -8.1150, "Longitud": -79.0290},
                "Piura": {"Latitud": -5.1945, "Longitud": -80.6328},
                "Junín": {"Latitud": -11.1582, "Longitud": -75.9920},
                "Ancash": {"Latitud": -9.5261, "Longitud": -77.5286},
                "Lambayeque": {"Latitud": -6.7041, "Longitud": -79.9061}
            }

            df["Latitud"] = df["Departamento"].map(lambda d: coordenadas_departamentos[d]["Latitud"])
            df["Longitud"] = df["Departamento"].map(lambda d: coordenadas_departamentos[d]["Longitud"])

            fig_map = px.scatter_geo(
                df,
                lat="Latitud",
                lon="Longitud",
                color="Departamento",
                size="Ventas",
                hover_name="Departamento",
                projection="natural earth"
            )
            st.plotly_chart(fig_map, use_container_width=True)


    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
