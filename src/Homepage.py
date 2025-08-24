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


with open("./presets/minimal_r.json", "r") as f:
    dizi = json.loads(f.read())
    # prettymaps.create_preset("minimal_reversed", **dizi)


theme_options = [
    p for p in prettymaps.presets().preset.tolist() if "barcelona-plotter" not in p
]
theme_options.append("minimal_reversed")
img = io.BytesIO()


with st.form("Settings"):
    # Textinput per il nome della località
    location_name = st.text_input(
        "Inserisci il nome della località (Città, Provincia):"
    )

    # Textinput per lo stato
    state_name = st.text_input("Inserisci lo stato:")

    # Menu a cascata per scegliere il tema

    selected_theme = st.selectbox("Seleziona un tema:", theme_options)

    # Barra di valori numerici per il raggio
    radius = st.slider(
        "Seleziona il raggio",
        500,
        10000,
        500,
    )
    dpi = st.number_input("DPI", min_value=150, max_value=1000, value=300, step=50)

    # quality_ = (12, 12)  Legacy
    page_sizes = {
        "A4": (8.27, 11.69),
        "A5": (5.83, 8.27),
        "Square": (12, 12),
        "A3": (11.69, 16.54),
        "A2": (16.54, 23.39),
        "A1": (23.39, 33.11),
    }
    page_size = st.selectbox(
        "Page Size",
        page_sizes.keys(),
        index=2,
    )
    width, height = page_sizes[page_size]
    circle = st.checkbox("Immagine circolare", False)

    # Pulsante "Genera"
    if st.form_submit_button("Genera"):
        with st.spinner("Generando l'immagine"):

            if selected_theme == "minimal_reversed":
                plot = prettymaps.plot(
                    f"{location_name}, {state_name}",
                    circle=circle,
                    radius=radius,
                    credit=False,
                    preset="minimal",
                    constrained_layout=False,
                    dilate=None,
                    figsize=(width, height),
                    layers=dizi["layers"],
                    style=dizi["style"],
                )
                st.write(dizi["layers"])
                st.write(dizi["style"])
            else:
                # pmap
                plot = prettymaps.plot(
                    f"{location_name}, {state_name}",
                    circle=circle,
                    radius=radius,
                    credit=False,
                    preset=selected_theme,
                    constrained_layout=False,
                    dilate=0,
                    figsize=(width, height),
                )

            st.session_state["keep_plot"] = True
            st.session_state["plot"] = plot.fig

if "keep_plot" in st.session_state and st.session_state["keep_plot"]:
    plot = st.session_state["plot"]
    st.pyplot(plot)
    plot.savefig(img, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0)
    st.session_state["access"] = True
    st.session_state["keep_plot"] = True

if "access" in st.session_state and st.session_state["access"]:
    # with open("Download.png", "rb") as img:
    # Pulsante di salvataggio del grafico
    if st.download_button(
        label="Clicca qui per scaricare l'immagine",
        data=img,  # Puoi specificare il formato desiderato
        file_name=f"{location_name}_{state_name}_{selected_theme}.png",  # Specifica il nome del file
        key="download_button",
        use_container_width=True,
    ):
        st.success("Immagine salvata con successo!")
