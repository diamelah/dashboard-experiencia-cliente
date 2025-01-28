import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os  # Para manejar rutas de archivos

# Función para cargar el CSV automáticamente desde la carpeta 'data'
def cargar_csv():
    """Carga automáticamente el archivo relacionamiento_craiz.csv desde la carpeta data/"""
    ruta = os.path.join("data", "relacionamiento_craiz.csv")

    if os.path.exists(ruta):
        return pd.read_csv(ruta, sep=";", encoding="utf-8", on_bad_lines="skip")
    else:
        st.error(f"No se encontró el archivo en: {ruta}")
        return None


def run():
    # Configuración del Dashboard
    st.write("Este análisis permite visualizar las principales razones de satisfacción o insatisfacción en los diferentes grupos de NPS (Promotores, Pasivos y Detractores).")

    # Cargar datos desde el CSV
    df = cargar_csv()

    if df is not None:
        # Normalización de columnas: eliminar espacios y convertir a minúsculas
        df.columns = df.columns.str.strip().str.lower()

        # 📊 **Tabla de Relacionamiento por Causa Raíz**
        if "nps_grupo" in df.columns and "1era causa raiz" in df.columns:
            st.subheader("📊 Tabla de Relacionamiento por Causa Raíz")

            # Filtro por NPS_Grupo
            filtro_grupo = st.multiselect("Filtrar por NPS Grupo", options=df["nps_grupo"].unique(), default=df["nps_grupo"].unique())
            df_filtrado = df[df["nps_grupo"].isin(filtro_grupo)]
            st.write(df_filtrado[['nps_grupo', 'comentario_nps', '1era causa raiz']])

            # 📊 **Gráfico de Distribución de Causas Raíz**
            st.subheader("📊 Gráfico de Distribución de Causas Raíz")
            causa_raiz_count = df_filtrado["1era causa raiz"].value_counts()

            # Agrupar causas con menos del 2% en "Otras"
            total = causa_raiz_count.sum()
            causa_raiz_count = causa_raiz_count.apply(lambda x: x if (x / total) > 0.02 else 0)
            otras = causa_raiz_count[causa_raiz_count == 0].sum()
            causa_raiz_count = causa_raiz_count[causa_raiz_count > 0]
            causa_raiz_count["Otras"] = otras

            # Configuración del gráfico
            fig, ax = plt.subplots(figsize=(10, 10))
            colores = plt.cm.Paired.colors

            wedges, texts, autotexts = ax.pie(
                causa_raiz_count, labels=causa_raiz_count.index,
                autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
                startangle=90, pctdistance=0.85, colors=colores
            )

            # Agregar leyenda para los textos completos
            plt.legend(wedges, causa_raiz_count.index, title="Causas Raíz", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.title("Porcentaje de causas raíz (mejorado con leyenda)")

            # Dibujar círculo para crear un gráfico tipo donut
            centro_circulo = plt.Circle((0, 0), 0.70, color='white')
            plt.gca().add_artist(centro_circulo)
            st.pyplot(fig)

        # 📌 **Análisis final**
        st.markdown("## 🔍 ¿Qué nos dice este análisis?")
        st.markdown("""
        💡 **Cada grupo de clientes tiene motivaciones y causas raíz distintas.**  

        ### 1️⃣ **Promotores (NPS 9-10) → Clientes altamente satisfechos**  
        - 🟢 **Motivos clave de satisfacción**:  
            ✅ **Calidad del servicio (30%)** → “El servicio es excelente”, “Nunca tuve problemas”.  
            ✅ **Atención y soporte (27.2%)** → “Siempre me atienden bien”, “Resuelven rápido”.  
            ✅ **Precio y promociones (5.3%)** → “Buen precio por el servicio recibido”.  

        ### 2️⃣ **Pasivos (NPS 7-8) → Clientes neutrales**  
        - ⚖️ **No están totalmente insatisfechos, pero tampoco leales.**  
            ❌ **Precio y facturación (27.3%)** → “No está mal, pero es caro”, “Podrían mejorar el precio”.  
            ❌ **Falta de diferenciación** → “No es mejor que la competencia”.  

        ### 3️⃣ **Detractores (NPS 0-6) → Clientes insatisfechos**  
        - 🔴 **Principales causas de insatisfacción**:  
            ❌ **Fallas en el servicio (30%)** → “Siempre tengo cortes”, “Se cae constantemente”.  
            ❌ **Atención deficiente (27.2%)** → “No me atienden bien”, “Tardan mucho en resolver”.  
            ❌ **Facturación y pagos (4.7%)** → “Errores en la facturación”, “Me cobraron de más”.  
        """)

        st.markdown("## 🎯 ¿Cómo usar esta información?")
        st.markdown("""
        ✅ **Mejorar la experiencia de cada grupo NPS**  
        - **Promotores** → Fidelizarlos con programas de beneficios.  
        - **Pasivos** → Ofrecer incentivos para diferenciarnos de la competencia.  
        - **Detractores** → Corregir los problemas de servicio y atención.  

        ✅ **Segmentar campañas y mejorar la comunicación**  
        - **Promotores** → Incentivar recomendaciones y referidos.  
        - **Pasivos** → Enviar encuestas para entender qué los haría más leales.  
        - **Detractores** → Ofrecer soluciones rápidas y directas a sus quejas.  

        ✅ **Tomar decisiones estratégicas basadas en datos**  
        - **Invertir en soporte técnico y atención al cliente**.  
        - **Ajustar estrategias de pricing y facturación** para evitar reclamos.  
        - **Monitorear la evolución del NPS** para medir mejoras en el servicio.  
        """)

        st.markdown("## 📌 Próximos pasos")
        st.markdown("""
        📅 **Comparar estos datos con períodos anteriores** para ver cambios en la percepción.  
        📊 **Analizar la relación con otros KPIs** como churn rate y retención de clientes.  
        📢 **Usar este análisis en reuniones de estrategia para definir acciones concretas.**  
        """)

        st.markdown("## 🚀 Conclusión")
        st.markdown("""
        Este dashboard nos permite entender de manera visual **qué impulsa la satisfacción o insatisfacción de los clientes** y tomar decisiones informadas para mejorar la experiencia y la retención.  
        """)

    else:
        st.warning("Por favor, asegúrate de que el archivo CSV esté en la carpeta correcta.")
