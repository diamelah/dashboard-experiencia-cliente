import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

def cargar_csv():
    """Carga automáticamente el archivo verbatims_categorias.csv desde GitHub"""
    url = "https://raw.githubusercontent.com/diamelah/dashboard-experiencia-cliente/main/data/verbatims_categorias.csv"
    
    try:
        return pd.read_csv(url, delimiter=";", encoding="utf-8")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {e}")
        return None

def run():
    # Streamlit app setup
    
    st.write("Este análisis de verbatims del mes de Noviembre 2024 clasifica los comentarios de clientes según su temática principal, proporcionando insights clave sobre los temas más mencionados en la experiencia del cliente.")

    # Cargar el archivo CSV automáticamente
    verbatims_data = cargar_csv()

    if verbatims_data is None:
        st.warning("⚠️ No se encontró el archivo `verbatims.csv`. Asegurate de colocarlo en la carpeta `data/`.")
        return

    # Definir categorías y palabras clave
    categories_keywords = {
        "Atencion al Cliente": ["cliente", "atencion"],
        "Atencion en la Venta": ["venta", "comprar"],
        "Delivery": ["delivery", "envio"],
        "Distribucion Factura": ["factura", "distribucion"],
        "Facturacion": ["facturacion", "cobro"],
        "Funcionamiento del Servicio": ["servicio", "funciona", "fallo"],
        "IVR": ["ivr", "automatico"],
        "Pagos": ["pago", "abonar"],
        "Politica Comercial": ["politica", "condiciones"],
        "Precio": ["precio", "costo"],
        "Procesos": ["proceso", "tramite"],
        "Resolucion": ["resolver", "solucion"],
        "Tiempos de Atencion": ["tiempo", "espera"]
    }

    # Verificar que la columna "verbatims" existe
    if "verbatims" in verbatims_data.columns:
        grouped_data = []

        # Clasificar verbatims por categoría
        for category, keywords in categories_keywords.items():
            filtered_verbatims = verbatims_data[verbatims_data["verbatims"].str.contains('|'.join(keywords), case=False, na=False)]
            grouped_data.append({"Categoria": category, "Cantidad": len(filtered_verbatims), "Verbatims": filtered_verbatims["verbatims"].tolist()})

        # Convertir a DataFrame para mostrar
        grouped_df = pd.DataFrame(grouped_data)

        # Calcular porcentajes
        total_verbatims = grouped_df["Cantidad"].sum()
        grouped_df["Porcentaje"] = (grouped_df["Cantidad"] / total_verbatims) * 100

        # Separar categorías con menos del 1% para visualización
        main_data = grouped_df[grouped_df["Porcentaje"] >= 1]
        small_data = grouped_df[grouped_df["Porcentaje"] < 1]

        # Mostrar la tabla de verbatims
        st.subheader("📊 Tabla de Verbatims por Categoría")
        st.dataframe(grouped_df)

        # Mostrar gráfico de torta
        st.subheader("📊 Gráfico de Distribución de Verbatims")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(
            main_data["Cantidad"], 
            labels=main_data["Categoria"], 
            autopct="%1.1f%%", 
            startangle=90, 
            colors=plt.cm.tab20.colors,
            textprops=dict(color="black")
        )

        if not small_data.empty:
            bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="white")
            ax.text(
                1.3, 0.5, 
                "Categorias menores a 1%:\n" + "\n".join(f"{row['Categoria']}: {row['Porcentaje']:.1f}%" for _, row in small_data.iterrows()),
                fontsize=10, verticalalignment='center', bbox=bbox_props
            )

        ax.axis("equal")  # Asegurar que el gráfico sea circular
        st.pyplot(fig)

        # Botón de descarga de la tabla procesada
        st.download_button(
            label="⬇️ Descargar tabla agrupada en CSV",
            data=grouped_df.to_csv(index=False).encode('utf-8'),
            file_name="verbatims_categorizados.csv",
            mime="text/csv"
        )

        # --- ANÁLISIS DEL DASHBOARD ---
        st.markdown("## 🔍 ¿Qué nos dice esta tabla?")
        st.markdown("""
        1️⃣ **Las categorías con más comentarios pueden indicar problemas recurrentes**
        - 📊 **"Funcionamiento del Servicio" (736 menciones)** → Indica que los clientes tienen experiencias relacionadas con fallas o calidad del servicio.  
        - 🔎 **"Resolución" (151 menciones)** → Sugiere que muchos clientes están insatisfechos con la solución de sus problemas.

        2️⃣ **Las menciones en cada categoría reflejan percepciones positivas y negativas**
        - **Ejemplo en "Facturación"**: Algunos clientes mencionan *"Facturación"*, *"Consulta sobre facturación"*, mientras que otros reclaman errores en las facturas.
        - **Ejemplo en "Pagos"**: Se observan quejas como *"Pésimo servicio al cliente, imposible comunicarse"*.  

        3️⃣ **Las categorías con menos menciones pueden representar problemas menos frecuentes**
        - Categorías como **"IVR" (2 menciones)** o **"Política Comercial" (1 mención)** muestran menos interacción con los clientes.
        """)

        st.markdown("## 🎯 ¿Cómo se puede usar esta información?")
        st.markdown("""
        ✅ **Optimizar la atención al cliente** → Si la mayoría de los comentarios están relacionados con *"Funcionamiento del Servicio"* y *"Resolución"*, estos deberían ser **prioridades** para mejorar la experiencia.  

        ✅ **Identificar tendencias** → Se puede comparar esta data con otros períodos para ver si algunos problemas están **aumentando o disminuyendo**.  

        ✅ **Tomar decisiones basadas en datos** → Si *Facturación* y *Resolución* tienen muchas menciones negativas, hay que mejorar la comunicación y procesos internos.  
        """)

        st.markdown("## 📌 Próximos pasos")
        st.markdown("""
        📅 **Comparar esta data con períodos anteriores** para ver tendencias.  
        📢 **Cruzar información con NPS** para ver si las menciones afectan la satisfacción.  
        📊 **Hacer un análisis de sentimientos** para diferenciar comentarios positivos y negativos.  
        """)

        st.markdown("## 🚀 Conclusión")
        st.markdown("""
        Este dashboard permite visualizar **qué temas preocupan más a los clientes** y ofrece una base de datos valiosa para mejorar la toma de decisiones en la empresa.  
        """)

    else:
        st.error("❌ El archivo `verbatims.csv` no contiene una columna llamada 'verbatims'. Verifica que el formato sea correcto.")
