import streamlit as st

# Aplicar la fuente Poppins en todo el dashboard y forzarla
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Forzar la fuente en todo el dashboard */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label, button {
        font-family: 'Poppins', sans-serif !important;
    }
            
    h1 { font-size: 24px !important; }
    h2 { font-size: 20px !important; }
    h3 { font-size: 18px !important; }
    h4 { font-size: 16px !important; }
            
    /* Ocultar el menú de configuración en la esquina superior derecha */
    header {visibility: hidden;}
            
    </style>
    """, unsafe_allow_html=True)

# Sidebar para la navegación
st.sidebar.title("Menú")
menu_options = [
    "Dashboard",  # ✅ Se agregó la opción de InicioS    
    "Verbatims por categorías",
    "Relacionamiento 'Causa raíz'",
    "Análisis por Dolor"
]
menu_choice = st.sidebar.radio("Seleccioná:", menu_options)

# Página principal según la elección del usuario
if menu_choice == "Dashboard":
    st.title("📊 Dashboard de Experiencia del Cliente")
    st.subheader("Bienvenido al Dashboard de NPS y Análisis de Dolor")

    st.markdown("""
    Este dashboard permite analizar los principales insights de la **experiencia del cliente**, 
    basado en datos de **NPS (Net Promoter Score)** y **categorías de dolor**.
    
    ## 📌 ¿Qué encontrarás en este dashboard?
    🔹 **Verbatims por Categorías** → Analiza comentarios de clientes y los agrupa en categorías temáticas.  
    🔹 **Relacionamiento 'Causa Raíz'** → Identifica los principales motivos de satisfacción o insatisfacción dentro de cada grupo de NPS (Promotores, Pasivos y Detractores).  
    🔹 **Análisis por Dolor** → Explora las problemáticas clave mencionadas en Dolor 1, Dolor 2 y Dolor 3 para entender qué aspectos requieren mayor atención.  

    ## 🎯 ¿Cómo usar este dashboard?
    1️⃣ **Subí un archivo CSV** con datos de NPS y comentarios de clientes.  
    2️⃣ **Explorá las distintas secciones** usando el menú lateral.  
    3️⃣ **Filtrá y visualizá gráficos interactivos** para obtener insights clave.  
    4️⃣ **Descargá reportes en CSV** con los análisis procesados.  

    ## 🚀 Objetivo
    Ayudar a los equipos de atención al cliente y gestión de experiencia a **identificar áreas de mejora, optimizar procesos y tomar decisiones basadas en datos**.
    
    ---
    """, unsafe_allow_html=True)

elif menu_choice == "Dashboard":
    st.title("Dashboard Principal")
    st.write("Bienvenido al dashboard. Usa el menú para navegar entre las opciones.")

elif menu_choice == "Verbatims por categorías":
    st.title("Verbatims por Categorías")
    import verbatims_categorias as vc
    vc.run()

elif menu_choice == "Relacionamiento 'Causa raíz'":
    st.title("Relacionamiento 'Causa raíz'")
    import relacionamiento_craiz as rc
    rc.run()

elif menu_choice == "Análisis por Dolor":
    st.title("Análisis por Dolor")
    import analisis_dolor as mc
    mc.run()
