import numpy as np
from PIL import Image, ImageFilter
import os
from typing import Optional
from io import BytesIO


def upscale_image(
    input_path: str,
    output_path: str,
    scale_factor: float = 2.0,
    enhance_sharpness: bool = True,
) -> bool:
    """
    Aumenta la risoluzione di un'immagine usando il metodo Lanczos.

    Args:
        input_path (str): Percorso dell'immagine di input
        output_path (str): Percorso dove salvare l'immagine upscalata
        scale_factor (float): Fattore di scala (es. 2.0 per raddoppiare la risoluzione)
        enhance_sharpness (bool): Se applicare un filtro di nitidezza dopo l'upscaling

    Returns:
        bool: True se l'operazione è riuscita, False altrimenti
    """
    try:
        with Image.open(input_path) as img:
            # Calcola le nuove dimensioni
            original_width, original_height = img.size
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            # Ridimensiona l'immagine usando Lanczos (migliore qualità)
            upscaled = img.resize((new_width, new_height), Image.LANCZOS)

            # Applica enhancement della nitidezza
            if enhance_sharpness:
                upscaled = upscaled.filter(
                    ImageFilter.UnsharpMask(radius=1.0, percent=150, threshold=3)
                )

            # Salva l'immagine
            upscaled.save(output_path, quality=95, optimize=True)

        print(f"Immagine upscalata salvata in: {output_path}")
        return True

    except Exception as e:
        print(f"Errore durante l'upscaling: {str(e)}")
        return False


def upscale_image_bytes(
    input_bytes: BytesIO,
    scale_factor: float = 2.0,
    enhance_sharpness: bool = True,
    output_format: str = "PNG",
) -> BytesIO:
    """
    Aumenta la risoluzione di un'immagine da BytesIO e restituisce un BytesIO.

    Args:
        input_bytes (BytesIO): BytesIO contenente l'immagine di input
        scale_factor (float): Fattore di scala (es. 2.0 per raddoppiare la risoluzione)
        enhance_sharpness (bool): Se applicare un filtro di nitidezza dopo l'upscaling
        output_format (str): Formato di output ("PNG", "JPEG", "WEBP", etc.)

    Returns:
        BytesIO: BytesIO contenente l'immagine upscalata
    """
    try:
        # Assicurati che il puntatore sia all'inizio
        input_bytes.seek(0)

        # Carica l'immagine dal BytesIO
        with Image.open(input_bytes) as img:
            # Calcola le nuove dimensioni
            original_width, original_height = img.size
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            # Ridimensiona l'immagine usando Lanczos
            upscaled = img.resize((new_width, new_height), Image.LANCZOS)

            # Applica enhancement della nitidezza
            if enhance_sharpness:
                upscaled = upscaled.filter(
                    ImageFilter.UnsharpMask(radius=1.0, percent=150, threshold=3)
                )

            # Crea il BytesIO di output
            output_bytes = BytesIO()

            # Determina i parametri di salvataggio in base al formato
            save_kwargs = {"format": output_format}
            if output_format.upper() == "JPEG":
                save_kwargs.update({"quality": 95, "optimize": True})
            elif output_format.upper() == "PNG":
                save_kwargs.update({"optimize": True})
            elif output_format.upper() == "WEBP":
                save_kwargs.update({"quality": 95, "method": 6})

            # Salva l'immagine nel BytesIO
            upscaled.save(output_bytes, **save_kwargs)

            # Riporta il puntatore all'inizio per la lettura
            output_bytes.seek(0)

            return output_bytes

    except Exception as e:
        print(f"Errore durante l'upscaling da BytesIO: {str(e)}")
        # Restituisce un BytesIO vuoto in caso di errore
        return BytesIO()


def batch_upscale(
    input_folder: str,
    output_folder: str,
    scale_factor: float = 2.0,
) -> int:
    """
    Elabora in batch tutte le immagini in una cartella usando Lanczos.

    Args:
        input_folder (str): Cartella con le immagini di input
        output_folder (str): Cartella di output
        scale_factor (float): Fattore di scala

    Returns:
        int: Numero di immagini elaborate con successo
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed = 0
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"upscaled_{filename}")

            if upscale_image(input_path, output_path, scale_factor):
                processed += 1

    print(f"Elaborate {processed} immagini")
    return processed


def get_image_info(image_path: str) -> Optional[dict]:
    """
    Ottiene informazioni sull'immagine.

    Args:
        image_path (str): Percorso dell'immagine

    Returns:
        dict: Informazioni sull'immagine o None se errore
    """
    try:
        with Image.open(image_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_mb": os.path.getsize(image_path) / (1024 * 1024),
            }
    except Exception as e:
        print(f"Errore nel leggere le informazioni dell'immagine: {str(e)}")
        return None


def get_image_info_bytes(image_bytes: BytesIO) -> Optional[dict]:
    """
    Ottiene informazioni sull'immagine da BytesIO.

    Args:
        image_bytes (BytesIO): BytesIO contenente l'immagine

    Returns:
        dict: Informazioni sull'immagine o None se errore
    """
    try:
        image_bytes.seek(0)
        with Image.open(image_bytes) as img:
            # Calcola la dimensione del BytesIO
            image_bytes.seek(0, 2)  # Vai alla fine
            size_bytes = image_bytes.tell()
            image_bytes.seek(0)  # Torna all'inizio

            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_mb": size_bytes / (1024 * 1024),
            }
    except Exception as e:
        print(f"Errore nel leggere le informazioni dell'immagine da BytesIO: {str(e)}")
        return None


#                 output_bytes = upscale_image_bytes(
#                     input_bytes,
#                     scale_factor=2.0,
#                     enhance_sharpness=True,
#                     output_format="PNG",
#                 )
