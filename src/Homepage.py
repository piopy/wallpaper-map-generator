import streamlit as st
import io
import json
import prettymaps

# --- CONFIGURAZIONE INIZIALE ---
st.set_page_config("PosterGen", ":earth_africa:", layout="wide")
st.title("PosterGen")

# --- DEFINIZIONE LAYER E CARICAMENTO PRESET ---
CONFIGURABLE_LAYERS = {
    "green": {
        "label": "Aree verdi",
        "tags": {"landuse": "grass", "natural": ["island", "wood"], "leisure": "park"},
        "default_colors": ["#8BC34A"],
        "zorder": 1,
    },
    "forest": {
        "label": "Foreste",
        "tags": {"landuse": "forest"},
        "default_colors": ["#4CAF50"],
        "zorder": 1,
    },
    "park": {
        "label": "Parchi",
        "tags": {"leisure": "park"},
        "default_colors": ["#AABD8C"],
        "zorder": 1,
    },
    "garden": {
        "label": "Giardini",
        "tags": {"leisure": "garden"},
        "default_colors": ["#a9d1a9"],
        "zorder": 1,
    },
    "grass": {
        "label": "Aree erbose",
        "tags": {"landuse": "grass"},
        "default_colors": ["#72C07A"],
        "zorder": 1,
    },
    "water": {
        "label": "Acqua",
        "tags": {"natural": ["water", "bay"]},
        "default_colors": ["#2196F3"],
        "zorder": 2,
    },
    "Sea": {
        "label": "Mare",
        "default_colors": ["#005DA8", "#2F3737", "#9bc3d4"],
        "zorder": 99,
    },
    "pedestrian": {
        "label": "Aree pedonali",
        "tags": {"area:highway": "pedestrian"},
        "default_colors": ["#7BC950"],
        "zorder": 2,
    },
    "beach": {
        "label": "Spiagge",
        "tags": {"natural": "beach"},
        "default_colors": ["#FFC107"],
        "zorder": 3,
    },
    "wetland": {
        "label": "Zone umide",
        "tags": {"natural": "wetland"},
        "default_colors": ["#D2D68D"],
        "zorder": 3,
    },
    "parking": {
        "label": "Parcheggi",
        "tags": {"amenity": "parking"},
        "default_colors": ["#F2F4CB"],
        "zorder": 3,
    },
    "streets": {
        "label": "Strade",
        "default_colors": ["#795548"],
        "zorder": 4,
        "width": {
            "motorway": 5,
            "trunk": 5,
            "primary": 4.5,
            "secondary": 4,
            "tertiary": 3.5,
            "residential": 3,
            "service": 2,
            "unclassified": 2,
            "pedestrian": 2,
            "footway": 1,
        },
    },
    "building": {
        "label": "Edifici",
        "tags": {"building": True},
        "default_colors": ["#F44336"],
        "zorder": 5,
    },
}


@st.cache_data
def load_presets():
    with open("presets/PRESETS.json", "r") as f:
        return json.load(f)


PRESETS = load_presets()
theme_options = list(PRESETS.keys())


# --- GESTIONE DELLO STATO ---
def update_state_from_theme():
    theme_name = st.session_state.selected_theme
    preset_data = PRESETS.get(theme_name, {})
    preset_layers = preset_data.get("layers", {})
    preset_style = preset_data.get("style", {})

    st.session_state.bg_color = preset_style.get("background", {}).get("fc", "#FFFFFF")

    for key, info in CONFIGURABLE_LAYERS.items():
        st.session_state[f"{key}_active"] = key in preset_layers

        colors = info["default_colors"]
        is_palette = False
        palette_has_ec = False

        if key in preset_style:
            style_info = preset_style[key]
            if "palette" in style_info:
                is_palette = True
                colors = style_info["palette"].copy()
                if "ec" in style_info:
                    colors.append(style_info["ec"])
                    palette_has_ec = True
            else:
                new_colors = []
                if "fc" in style_info:
                    new_colors.append(style_info["fc"])
                if "ec" in style_info:
                    new_colors.append(style_info["ec"])
                if new_colors:
                    colors = new_colors

        st.session_state[f"{key}_colors"] = colors
        st.session_state[f"{key}_is_palette"] = is_palette
        st.session_state[f"{key}_palette_has_ec"] = palette_has_ec


# Inizializzazione dello stato se non esiste
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = theme_options[0]
    update_state_from_theme()

# --- INTERFACCIA UTENTE ---
img = io.BytesIO()

st.header("Impostazioni Principali")
col1, col2 = st.columns(2)
with col1:
    location_name = st.text_input("Località:", "Roma")
    st.selectbox(
        "Seleziona un tema:",
        theme_options,
        key="selected_theme",
        on_change=update_state_from_theme,
    )
    radius = st.slider("Raggio (m):", 500, 10000, 1000)
    circle = st.checkbox("Circolare:", False)
with col2:
    state_name = st.text_input("Stato:", "Italia")
    page_sizes = {
        "A4": (8.27, 11.69),
        "A5": (5.83, 8.27),
        "Square": (12, 12),
        "A3": (11.69, 16.54),
        "A2": (16.54, 23.39),
        "A1": (23.39, 33.11),
    }
    page_size = st.selectbox("Dimensioni:", page_sizes.keys(), index=2)
    width, height = page_sizes[page_size]
    dpi = st.number_input("DPI:", 150, 1000, 300, 50)

col3, col4 = st.columns(2)
with col3:
    st.header("Personalizzazione Layer")
    st.color_picker("Colore Sfondo", key="bg_color")

    for key, info in CONFIGURABLE_LAYERS.items():
        # cols = st.columns([1, 5])
        # with cols[0]:
        # with cols[1]:
        colors_in_state = st.session_state.get(f"{key}_colors", info["default_colors"])
        color_cols = st.columns(len(colors_in_state) + 1 or 1)
        is_palette = st.session_state.get(f"{key}_is_palette", False)
        with color_cols[0]:
            st.checkbox(f"Attiva {info['label']}", key=f"{key}_active")
        for i, color in enumerate(colors_in_state):
            with color_cols[i + 1]:
                label = f"Colore {i + 1}"
                if not is_palette and len(colors_in_state) > 1:
                    if i == 0:
                        label = "Colore Fill"
                    elif i == 1:
                        label = "Colore Bordo"
                st.color_picker(label, value=color, key=f"{key}_color_{i}")
with col4:
    if st.button(
        "Genera Mappa",
        use_container_width=True,
    ):
        with st.spinner("Generando l'immagine..."):
            final_layers = {"perimeter": {}}
            final_style = {
                "perimeter": {"fill": False, "lw": 0, "zorder": 0},
                "background": {"fc": st.session_state.bg_color, "zorder": -1},
            }

            for key, config in CONFIGURABLE_LAYERS.items():
                if st.session_state.get(f"{key}_active"):
                    if "tags" in config:
                        final_layers[key] = {"tags": config["tags"]}
                    elif "width" in config:
                        final_layers[key] = {"width": config["width"]}

                    colors = []
                    i = 0
                    while f"{key}_color_{i}" in st.session_state:
                        colors.append(st.session_state[f"{key}_color_{i}"])
                        i += 1

                    style_dict = {
                        "lw": 0.5 if key == "building" else 0,
                        "zorder": config["zorder"],
                    }

                    is_palette = st.session_state.get(f"{key}_is_palette", False)
                    palette_has_ec = st.session_state.get(
                        f"{key}_palette_has_ec", False
                    )

                    if is_palette:
                        if palette_has_ec:
                            style_dict["palette"] = colors[:-1]
                            style_dict["ec"] = colors[-1]
                        else:
                            style_dict["palette"] = colors
                            style_dict["ec"] = "#2F3737"
                    elif len(colors) == 1:
                        style_dict["fc"] = colors[0]
                        style_dict["ec"] = colors[0]
                    elif len(colors) == 2:
                        style_dict["fc"] = colors[0]
                        style_dict["ec"] = colors[1]
                    elif len(colors) > 2:  # Fallback for palettes not from presets
                        style_dict["palette"] = colors
                        style_dict["ec"] = "#2F3737"

                    if colors:
                        final_style[key] = style_dict

            if location_name.startswith("(") and location_name.endswith(")"):
                query = location_name
            else:
                query = f"{location_name}, {state_name}"
            plot = prettymaps.plot(
                location_name,
                circle=circle,
                radius=radius,
                credit=False,
                figsize=(width, height),
                layers=final_layers,
                style=final_style,
                constrained_layout=False,
            )
            st.session_state.keep_plot = True
            st.session_state.plot = plot.fig
            st.session_state.filename = f"{location_name.replace(' ', '_')}_{st.session_state.selected_theme}.png"

    # --- VISUALIZZAZIONE E DOWNLOAD ---
    if st.session_state.get("keep_plot"):
        st.pyplot(st.session_state.plot)
        st.session_state.plot.savefig(
            img,
            format="png",
            dpi=st.session_state.get("dpi", 300),
            bbox_inches="tight",
            pad_inches=0,
        )
        if st.download_button(
            "Scarica l'immagine",
            data=img,
            file_name=st.session_state.get("filename", "mappa.png"),
            use_container_width=True,
        ):
            st.success("Immagine scaricata!")
