import random
from typing import Dict, List


# -------------------------------------------------------
# Style Libraries
# -------------------------------------------------------

STYLE_DATABASE = {

    "Minimal Luxury": {
        "tops": [
            "White button shirt",
            "Cashmere sweater",
            "Neutral blazer"
        ],
        "bottoms": [
            "Tailored trousers",
            "Straight-leg jeans",
            "Wide-leg pants"
        ],
        "shoes": [
            "Leather loafers",
            "Minimal sneakers",
            "Ankle boots"
        ],
        "accessories": [
            "Simple watch",
            "Leather belt",
            "Structured bag"
        ]
    },


    "Smart Casual": {
        "tops": [
            "Oxford shirt",
            "Knit polo",
            "Clean overshirt"
        ],
        "bottoms": [
            "Chinos",
            "Dark denim",
            "Pleated trousers"
        ],
        "shoes": [
            "White sneakers",
            "Derby shoes",
            "Chelsea boots"
        ],
        "accessories": [
            "Watch",
            "Sunglasses",
            "Simple jewelry"
        ]
    },


    "Streetwear / Layered": {
        "tops": [
            "Oversized hoodie",
            "Graphic tee",
            "Bomber jacket"
        ],
        "bottoms": [
            "Cargo pants",
            "Relaxed jeans",
            "Track pants"
        ],
        "shoes": [
            "Chunky sneakers",
            "High tops",
            "Running sneakers"
        ],
        "accessories": [
            "Cap",
            "Crossbody bag",
            "Chain"
        ]
    },


    "Dark Academia": {
        "tops": [
            "Turtleneck",
            "Wool sweater",
            "Long coat"
        ],
        "bottoms": [
            "Dark trousers",
            "Corduroy pants",
            "Pleated skirt"
        ],
        "shoes": [
            "Loafers",
            "Leather boots"
        ],
        "accessories": [
            "Glasses",
            "Leather bag",
            "Scarf"
        ]
    },


    "Bold Statement": {
        "tops": [
            "Patterned shirt",
            "Statement jacket",
            "Color block sweater"
        ],
        "bottoms": [
            "Wide pants",
            "Colored denim",
            "Statement skirt"
        ],
        "shoes": [
            "Designer sneakers",
            "Platform shoes"
        ],
        "accessories": [
            "Bold jewelry",
            "Statement bag"
        ]
    }

}


# -------------------------------------------------------
# Style Recommendation
# -------------------------------------------------------

def recommend_style(
    analysis: Dict
):

    detected_style = analysis.get(
        "style",
        "Smart Casual"
    )


    if detected_style in STYLE_DATABASE:

        return detected_style


    return "Smart Casual"



# -------------------------------------------------------
# Generate Outfit
# -------------------------------------------------------

def generate_outfit(
    style: str
):

    if style not in STYLE_DATABASE:

        style = "Smart Casual"


    collection = STYLE_DATABASE[
        style
    ]


    outfit = {

        "style":
        style,

        "top":
        random.choice(
            collection["tops"]
        ),

        "bottom":
        random.choice(
            collection["bottoms"]
        ),

        "shoes":
        random.choice(
            collection["shoes"]
        ),

        "accessories":
        random.choice(
            collection["accessories"]
        )

    }


    return outfit



# -------------------------------------------------------
# Occasion Recommendations
# -------------------------------------------------------

def occasion_style(
    occasion
):

    occasions = {

        "Work":
        "Smart Casual",

        "Formal":
        "Minimal Luxury",

        "Date":
        "Minimal Luxury",

        "Weekend":
        "Streetwear / Layered",

        "Study":
        "Dark Academia",

        "Party":
        "Bold Statement"

    }


    return occasions.get(
        occasion,
        "Smart Casual"
    )



# -------------------------------------------------------
# Full Recommendation
# -------------------------------------------------------

def fashion_recommendation(
    analysis,
    occasion="Everyday"
):

    style = recommend_style(
        analysis
    )


    if occasion != "Everyday":

        style = occasion_style(
            occasion
        )


    outfit = generate_outfit(
        style
    )


    return {

        "detected_style":
        analysis.get(
            "style"
        ),

        "recommended_style":
        style,

        "outfit":
        outfit,

        "reason":
        create_reason(
            analysis,
            style
        )

    }



# -------------------------------------------------------
# Explanation Generator
# -------------------------------------------------------

def create_reason(
    analysis,
    style
):

    reasons = []


    if analysis.get(
        "brightness",
        0
    ) > 170:

        reasons.append(
            "The light color profile works well with clean silhouettes."
        )


    if analysis.get(
        "texture"
    ):

        reasons.append(
            "The texture suggests a layered styling approach."
        )


    if not reasons:

        reasons.append(
            "The recommendation is based on your detected visual style."
        )


    return " ".join(
        reasons
    )



# -------------------------------------------------------
# Closet Outfit Builder
# -------------------------------------------------------

def build_from_closet(
    wardrobe,
    style_filter=None
):

    matches = []


    for item in wardrobe:

        if style_filter:

            if item.get(
                "style"
            ) != style_filter:

                continue


        matches.append(
            item
        )


    return matches