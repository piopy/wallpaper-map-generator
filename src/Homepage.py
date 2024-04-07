import streamlit as st
import prettymaps
import io
import osmnx as ox
import json

# Titolo della pagina e config
st.set_page_config(
    "PosterGen",
    ":earth_africa:",
)
st.title("PosterGen")


# with open("./presets/minimal_r.json", "r") as f:
#     dizi = json.loads(f.read())
#     prettymaps.create_preset("minimal_reversed", **dizi)


theme_options = [
    p for p in prettymaps.presets().preset.tolist() if "barcelona-plotter" not in p
]
theme_options.append("B/W")
img = io.BytesIO()


with st.form("Settings"):
    # Textinput per il nome della località
    location_name = st.text_input("Inserisci il nome della località:")

    # Textinput per lo stato
    state_name = st.text_input("Inserisci lo stato:")

    # Menu a cascata per scegliere il tema

    selected_theme = st.selectbox("Seleziona un tema:", theme_options)

    # Barra di valori numerici per il raggio
    radius = st.slider(
        "Seleziona il raggio: \n\n NB: l'algoritmo B/W ha in ogni caso raggio minimo corrispondente ai confini della città.",
        500,
        10000,
        500,
    )
    quality = st.radio("Qualità", ["standard", "hq"], horizontal=True)
    quality_ = (12, 12) if quality == "standard" else (50, 50)
    circle = False  # st.checkbox("Immagine circolare", False)

    # Pulsante "Genera"
    if st.form_submit_button("Genera"):
        with st.spinner("Generando l'immagine"):
            if selected_theme != "B/W":
                # pmap
                plot = prettymaps.plot(
                    f"{location_name}, {state_name}",
                    circle=circle,
                    radius=radius,
                    credit=False,
                    preset=selected_theme,
                    constrained_layout=False,
                    dilate=0,
                    figsize=quality_,
                )
            else:
                # ox puro
                graph = ox.graph_from_place(
                    f"{location_name}, {state_name}",
                    network_type="all",
                    clean_periphery=False,
                    buffer_dist=radius,
                )
                fig, ax = ox.plot_graph(
                    ox.project_graph(graph),
                    show=False,
                    close=False,
                    edge_color="black",
                    edge_linewidth=0.5,
                    node_size=0,
                )
                fig.set_size_inches(quality_)

            st.session_state["keep_plot"] = True
            st.session_state["plot"] = plot.fig if selected_theme != "B/W" else fig
if "keep_plot" in st.session_state and st.session_state["keep_plot"]:
    plot = st.session_state["plot"]
    st.pyplot(plot)
    plot.savefig(img, format="png", dpi=300, bbox_inches="tight", pad_inches=0)
    st.session_state["access"] = True
    st.session_state["keep_plot"] = True

if "access" in st.session_state and st.session_state["access"]:
    # with open("Download.png", "rb") as img:
    # Pulsante di salvataggio del grafico
    if st.download_button(
        label="Clicca qui per scaricare l'immagine",
        data=img,  # Puoi specificare il formato desiderato
        file_name="grafico.png",  # Specifica il nome del file
        key="download_button",
    ):
        st.success("Immagine salvata con successo!")
