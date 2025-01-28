import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import os  # Para manejar rutas de archivos


# Función para cargar el CSV automáticamente desde la carpeta 'data'
def cargar_csv():
    """Carga automáticamente el archivo analisis_dolor.csv desde GitHub"""
    url = "https://raw.githubusercontent.com/diamelah/dashboard-experiencia-cliente/main/Data/analisis_dolor.csv"
    
    try:
        return pd.read_csv(url, delimiter=";", encoding="utf-8")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {e}")
        return None


def run():
    # Configuración del Dashboard
    st.write("Este análisis nos permite entender qué problemas específicos afectan más a los clientes, partiendo desde Dolor 1 como el problema principal y desglosándolo en Dolor 2 y Dolor 3 para analizar en profundidad las causas raíz.")

    # Cargar datos desde el CSV
    df = cargar_csv()

    if df is not None:
        # Verificar que las columnas necesarias existan
        required_columns = ['comentario_nps', 'dolor_1', 'dolor_2', 'dolor_3']
        if not all(col in df.columns for col in required_columns):
            st.error(f"El archivo CSV debe contener las siguientes columnas: {', '.join(required_columns)}")
        else:
            # 🎯 **Filtros de Análisis de Dolor**
            st.subheader("🎯 Filtrar por Dolor 1, Dolor 2 y Dolor 3")
            col1, col2, col3 = st.columns(3)

            with col1:
                dolor_1_options = st.multiselect(
                    "Dolor 1",
                    options=df['dolor_1'].dropna().unique().tolist(),
                    default=[]
                )

            with col2:
                dolor_2_options = st.multiselect(
                    "Dolor 2",
                    options=df['dolor_2'].dropna().unique().tolist(),
                    default=[]
                )

            with col3:
                dolor_3_options = st.multiselect(
                    "Dolor 3",
                    options=df['dolor_3'].dropna().unique().tolist(),
                    default=[]
                )

            # Aplicar los filtros seleccionados
            filtered_df = df.copy()

            if dolor_1_options:
                filtered_df = filtered_df[filtered_df["dolor_1"].isin(dolor_1_options)]
            if dolor_2_options:
                filtered_df = filtered_df[filtered_df["dolor_2"].isin(dolor_2_options)]
            if dolor_3_options:
                filtered_df = filtered_df[filtered_df["dolor_3"].isin(dolor_3_options)]

            # 📊 **Tabla Verbatims por Dolor**
            st.subheader("📊 Tabla Verbatims por Dolor")
            st.dataframe(filtered_df[['comentario_nps', 'dolor_1', 'dolor_2', 'dolor_3']])

            # 📊 **Gráfico de Distribución**
            st.subheader("📊 Gráfico de Distribución")
            col1, col2 = st.columns(2)

            # Gráfico de torta para Dolor 2
            with col1:
                if not filtered_df['dolor_2'].dropna().empty:
                    fig1, ax1 = plt.subplots(figsize=(6, 6))
                    counts_dolor2 = filtered_df['dolor_2'].value_counts()

                    cmap = cm.get_cmap('tab20')  
                    colores = cmap(np.linspace(0, 1, len(counts_dolor2)))

                    ax1.pie(counts_dolor2, labels=counts_dolor2.index, autopct='%1.1f%%', startangle=90, colors=colores)
                    ax1.axis('equal')
                    ax1.set_title("Distribución de Dolor 2")
                    st.pyplot(fig1)
                else:
                    st.warning("No hay datos para Dolor 2.")

            # Gráfico de torta para Dolor 3
            with col2:
                if not filtered_df['dolor_3'].dropna().empty:
                    fig2, ax2 = plt.subplots(figsize=(6, 6))
                    counts_dolor3 = filtered_df['dolor_3'].value_counts()
                    ax2.pie(counts_dolor3, labels=counts_dolor3.index, autopct='%1.1f%%', startangle=90)
                    ax2.axis('equal')
                    ax2.set_title("Distribución de Dolor 3")
                    st.pyplot(fig2)
                else:
                    st.warning("No hay datos para Dolor 3.")

            # 📌 **Análisis final**
            st.markdown("## 🔍 ¿Qué nos dice este análisis?")
            st.markdown("""
            💡 **Los problemas más frecuentes están agrupados en Dolor 2 y Dolor 3, reflejando la percepción de los clientes sobre distintas áreas del servicio.**

            ### 1️⃣ Dolor 2 → Problemas de segunda capa más frecuentes
            - 🔵 **Resolución (44%)** → Gran parte de los clientes menciona que sus problemas no se resuelven adecuadamente.
            - 🟠 **Ajustes (8%)** → Quejas relacionadas con cambios en la facturación o condiciones del servicio.
            - 🟢 **Pagos (8%)** → Inconvenientes con los métodos de pago o confirmación de transacciones.
            - 🟣 **Fraude, Confianza e Imputación de pago (4% cada uno)** → Casos específicos con impacto en la percepción de seguridad del servicio.

            ### 2️⃣ Dolor 3 → Causas raíz más profundas
            - 🟠 **Resolución (25%)** → Problemas sin resolver en múltiples instancias.
            - 🟢 **Mal Asesoramiento (25%)** → Errores en la información provista por los agentes de servicio.
            - 🔵 **Fraude (25%)** → Casos críticos relacionados con fraude o irregularidades.
            - 🟣 **Funcionamiento y Distribución FT (12.5% cada uno)** → Relacionados con cortes de servicio o problemas en la entrega de facturas.
            """)

            st.markdown("## 🎯 ¿Cómo usar esta información?")
            st.markdown("""
            ✅ **Priorización de recursos según la severidad de los problemas**
            - Resolución y Mal Asesoramiento deben ser tratados con urgencia para evitar pérdida de confianza.
            - Fraude y Seguridad requieren análisis detallados y medidas preventivas.

            ✅ **Optimización de procesos internos**
            - Mejorar capacitación de agentes en resolución de problemas.
            - Implementar mecanismos de detección temprana para fraudes y errores en facturación.

            ✅ **Estrategias para mejorar la experiencia del cliente**
            - Automatización de soluciones para pagos y ajustes → reducir quejas recurrentes.
            - Mayor claridad en la comunicación sobre condiciones del servicio.
            """)

            st.markdown("## 📌 Próximos pasos")
            st.markdown("""
            📅 **Comparar estos datos con períodos anteriores** para medir la evolución de los problemas.  
            📊 **Cruzarlo con información de NPS** para ver el impacto en la satisfacción del cliente.  
            📢 **Diseñar acciones correctivas** basadas en insights de Dolor 2 y Dolor 3.
            """)

            st.markdown("## 🚀 Conclusión")
            st.markdown("""
            Este análisis nos da una visión clara de **qué problemas afectan más a los clientes**, permitiendo tomar decisiones estratégicas para **mejorar el servicio y optimizar la atención al cliente**.
            """)

    else:
        st.info("Por favor, asegúrate de que el archivo CSV esté en la carpeta correcta.")
