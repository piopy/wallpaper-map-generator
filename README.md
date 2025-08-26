# PosterGen

PosterGen è una semplice web app che permette di generare poster di mappe personalizzate. È costruita utilizzando Streamlit e Prettymaps.

## Cosa è

Questa applicazione consente di creare mappe stilizzate di qualsiasi città o luogo del mondo. È possibile personalizzare lo stile della mappa, le dimensioni dell'immagine e altri parametri per creare un poster unico.

## Come si installa

### Usando Docker (consigliato)

Il modo più semplice per eseguire l'applicazione è utilizzare Docker.

1.  Clona il repository:
    ```bash
    git clone <repository-url>
    cd wallpaper-map-generator
    ```
2.  Esegui l'applicazione con Docker Compose:
    ```bash
    docker-compose up
    ```
    L'applicazione sarà disponibile all'indirizzo [http://localhost:8181](http://localhost:8181).

### Installazione manuale

Se non si desidera utilizzare Docker, è possibile installare le dipendenze manualmente.

1.  Clona il repository:
    ```bash
    git clone <repository-url>
    cd wallpaper-map-generator
    ```
2.  Installa le dipendenze. Puoi usare `poetry`.

    **Con Poetry:**
    ```bash
    poetry install
    ```

3.  Esegui l'applicazione Streamlit:
    ```bash
    poetry run streamlit run src/Homepage.py
    ```

## Come si usa

1.  Apri l'applicazione nel tuo browser.
2.  Inserisci il nome della località e lo stato che desideri visualizzare sulla mappa.
3.  Seleziona un tema dal menu a tendina.
4.  Regola il raggio per definire l'area della mappa da visualizzare.
5.  Scegli i DPI (dots per inch) per la risoluzione dell'immagine.
6.  Seleziona il formato della pagina.
7.  Scegli se desideri un'immagine circolare.
8.  Clicca su "Genera" per creare la mappa.
9.  Una volta generata l'immagine, puoi scaricarla cliccando sul pulsante "Clicca qui per scaricare l'immagine".

## Ringraziamenti

Questo progetto è stato reso possibile grazie alle seguenti librerie open source:

*   [Prettymaps](https://github.com/marceloprates/prettymaps)
*   [Streamlit](https://streamlit.io/)
