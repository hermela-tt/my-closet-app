from io import BytesIO
from typing import Dict, List, Tuple

import cv2
import numpy as np
import requests
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb


# -------------------------------------------------------
# Image Loading
# -------------------------------------------------------

def load_image(source):
    """
    Load an image from:
    - Uploaded Streamlit file
    - URL
    - PIL Image

    Returns:
        PIL.Image
    """

    if isinstance(source, Image.Image):
        return source.convert("RGB")

    if hasattr(source, "read"):
        return Image.open(source).convert("RGB")

    if isinstance(source, str):

        response = requests.get(
            source,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        return Image.open(
            BytesIO(response.content)
        ).convert("RGB")

    raise ValueError("Unsupported image source")


# -------------------------------------------------------
# PIL -> OpenCV
# -------------------------------------------------------

def pil_to_cv(image):

    rgb = np.array(image)

    return cv2.cvtColor(
        rgb,
        cv2.COLOR_RGB2BGR
    )


def cv_to_pil(image):

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return Image.fromarray(rgb)


# -------------------------------------------------------
# Resize
# -------------------------------------------------------

def resize_image(
    image,
    size=(256, 256)
):

    return image.resize(size)


# -------------------------------------------------------
# Color Extraction
# -------------------------------------------------------

def extract_palette(
    image,
    clusters=5
):

    image = resize_image(image)

    pixels = np.array(image)

    pixels = pixels.reshape(
        -1,
        3
    )

    lab = rgb2lab(
        pixels.reshape(-1, 1, 3)
    ).reshape(-1, 3)

    model = KMeans(
        n_clusters=clusters,
        random_state=42,
        n_init=10
    )

    model.fit(lab)

    colors = model.cluster_centers_

    rgb = lab2rgb(
        colors.reshape(
            1,
            clusters,
            3
        )
    )[0]

    rgb = (
        rgb * 255
    ).astype(int)

    rgb = np.clip(
        rgb,
        0,
        255
    )

    return rgb


# -------------------------------------------------------
# RGB Helpers
# -------------------------------------------------------

def rgb_to_hex(color):

    return "#{:02x}{:02x}{:02x}".format(
        int(color[0]),
        int(color[1]),
        int(color[2])
    )


def average_color(image):

    img = np.array(
        resize_image(image)
    )

    return img.mean(
        axis=(0, 1)
    )


# -------------------------------------------------------
# Brightness
# -------------------------------------------------------

def brightness(image):

    hsv = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2HSV
    )

    return float(
        hsv[:, :, 2].mean()
    )


# -------------------------------------------------------
# Saturation
# -------------------------------------------------------

def saturation(image):

    hsv = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2HSV
    )

    return float(
        hsv[:, :, 1].mean()
    )


# -------------------------------------------------------
# Contrast
# -------------------------------------------------------

def contrast(image):

    gray = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2GRAY
    )

    return float(
        gray.std()
    )


# -------------------------------------------------------
# Sharpness
# -------------------------------------------------------

def sharpness(image):

    gray = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2GRAY
    )

    lap = cv2.Laplacian(
        gray,
        cv2.CV_64F
    )

    return float(
        lap.var()
    )


# -------------------------------------------------------
# Edge Density
# -------------------------------------------------------

def edge_density(image):

    gray = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2GRAY
    )

    edges = cv2.Canny(
        gray,
        80,
        180
    )

    return float(
        edges.mean()
    )


# -------------------------------------------------------
# Lightweight Image Embeddings
# -------------------------------------------------------

def create_image_embedding(image) -> np.ndarray:
    """
    Creates a lightweight visual representation.

    This replaces heavy AI embeddings like CLIP.
    Uses:
    - color
    - brightness
    - saturation
    - contrast
    - edges
    """

    palette = extract_palette(
        image,
        clusters=5
    )

    colors = palette.flatten() / 255.0

    features = np.array(
        [
            brightness(image) / 255.0,
            saturation(image) / 255.0,
            contrast(image) / 100.0,
            sharpness(image) / 1000.0,
            edge_density(image) / 255.0
        ]
    )

    embedding = np.concatenate(
        [
            colors,
            features
        ]
    )

    return embedding.astype(
        np.float32
    )


# -------------------------------------------------------
# Similarity Engine
# -------------------------------------------------------

def cosine_similarity(
    vector_a,
    vector_b
):

    denominator = (
        np.linalg.norm(vector_a)
        *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0

    score = np.dot(
        vector_a,
        vector_b
    ) / denominator

    return float(
        score
    )


def compare_outfits(
    image_one,
    image_two
):

    embedding_one = create_image_embedding(
        image_one
    )

    embedding_two = create_image_embedding(
        image_two
    )

    similarity = cosine_similarity(
        embedding_one,
        embedding_two
    )

    return round(
        similarity * 100,
        2
    )


# -------------------------------------------------------
# Clothing Region Detection
# -------------------------------------------------------

def detect_clothing_area(image):
    """
    Lightweight clothing area estimation.

    Uses image segmentation instead of
    heavy object detection models.
    """

    img = np.array(
        image
    )

    height, width = img.shape[:2]


    # Approximate outfit region:
    # middle/lower body area

    clothing_region = img[
        int(height * 0.25):
        int(height * 0.95),

        int(width * 0.15):
        int(width * 0.85)
    ]


    return Image.fromarray(
        clothing_region
    )


# -------------------------------------------------------
# Texture Analysis
# -------------------------------------------------------

def analyze_texture(image):

    gray = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2GRAY
    )

    variance = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()


    if variance < 40:

        return "Smooth / Minimal"


    elif variance < 150:

        return "Structured"


    else:

        return "Textured / Detailed"


# -------------------------------------------------------
# Fashion Style Classification
# -------------------------------------------------------

def classify_style(image):

    bright = brightness(
        image
    )

    color_strength = saturation(
        image
    )

    texture = analyze_texture(
        image
    )


    if bright > 180 and color_strength < 70:

        return "Minimal Luxury"


    if color_strength > 140:

        return "Bold Statement"


    if texture == "Textured / Detailed":

        return "Streetwear / Layered"


    if bright < 100:

        return "Dark Academia"


    return "Smart Casual"


# -------------------------------------------------------
# Clothing Attributes
# -------------------------------------------------------

def analyze_clothing(image):

    palette = extract_palette(
        image,
        clusters=3
    )


    return {

        "style":
        classify_style(image),

        "brightness":
        round(
            brightness(image),
            2
        ),

        "saturation":
        round(
            saturation(image),
            2
        ),

        "texture":
        analyze_texture(image),

        "palette":
        [
            rgb_to_hex(color)
            for color in palette
        ],

        "embedding":
        create_image_embedding(
            image
        ).tolist()

    }


    # -------------------------------------------------------
# Color Distance
# -------------------------------------------------------

def color_distance(
    color_one,
    color_two
):
    """
    Calculates RGB distance between colors.
    Lower = more similar.
    """

    a = np.array(
        color_one
    )

    b = np.array(
        color_two
    )

    return float(
        np.linalg.norm(
            a - b
        )
    )


# -------------------------------------------------------
# Palette Similarity
# -------------------------------------------------------

def compare_palettes(
    palette_one,
    palette_two
):
    """
    Compare two extracted color palettes.
    """

    scores = []

    for color_a in palette_one:

        best = min(
            [
                color_distance(
                    color_a,
                    color_b
                )
                for color_b in palette_two
            ]
        )

        scores.append(
            best
        )

    average = np.mean(
        scores
    )

    return round(
        max(
            0,
            100 - average / 3
        ),
        2
    )


# -------------------------------------------------------
# Closet Matching
# -------------------------------------------------------

def find_similar_clothing(
    target_image,
    wardrobe_items,
    limit=5
):
    """
    Finds closest wardrobe items.

    wardrobe_items format:

    [
        {
            "name": "...",
            "image": PIL.Image
        }
    ]

    """

    results = []

    target_embedding = create_image_embedding(
        target_image
    )


    for item in wardrobe_items:

        if "image" not in item:
            continue


        item_embedding = create_image_embedding(
            item["image"]
        )


        score = cosine_similarity(
            target_embedding,
            item_embedding
        )


        results.append(
            {
                "name":
                item.get(
                    "name",
                    "Unknown"
                ),

                "similarity":
                round(
                    score * 100,
                    2
                )
            }
        )


    results.sort(
        key=lambda x:
        x["similarity"],
        reverse=True
    )


    return results[:limit]


# -------------------------------------------------------
# Season Detection
# -------------------------------------------------------

def detect_season(image):

    avg = average_color(
        image
    )

    r, g, b = avg


    if r > g and r > b:

        return "Warm / Autumn"


    if b > r and b > g:

        return "Cool / Winter"


    if g > r and g > b:

        return "Spring"


    return "Summer"


# -------------------------------------------------------
# Outfit Color Compatibility
# -------------------------------------------------------

def color_harmony_score(
    image_one,
    image_two
):

    palette_one = extract_palette(
        image_one,
        clusters=3
    )

    palette_two = extract_palette(
        image_two,
        clusters=3
    )


    return compare_palettes(
        palette_one,
        palette_two
    )


# -------------------------------------------------------
# Full Clothing Report
# -------------------------------------------------------

def generate_fashion_report(
    image
):

    analysis = analyze_clothing(
        image
    )


    analysis["season"] = detect_season(
        image
    )


    analysis["clothing_region"] = detect_clothing_area(
        image
    )


    return analysis

def analyze_image(image):
    """
    Basic clothing analysis placeholder.
    Replace later with a real clothing ML model.
    """
    return {
        "category": "Unknown",
        "colors": [],
        "style": "Detected fashion item",
        "confidence": 0.0
    }