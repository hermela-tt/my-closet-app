# -------------------------------------------------------
# Fashion Gallery Database
# -------------------------------------------------------

SEASON_COLLECTIONS = {

    "Spring": [

        {
            "name":
            "Soft Neutral Layers",

            "category":
            "Minimal",

            "items":
            [
                "Cream cardigan",
                "White trousers",
                "Beige sneakers"
            ]
        },


        {
            "name":
            "Fresh Street Style",

            "category":
            "Streetwear",

            "items":
            [
                "Light bomber jacket",
                "Relaxed jeans",
                "Canvas sneakers"
            ]
        }

    ],


    "Summer": [

        {
            "name":
            "Clean Resort",

            "category":
            "Vacation",

            "items":
            [
                "Linen shirt",
                "Relaxed shorts",
                "Leather sandals"
            ]
        },


        {
            "name":
            "Modern Coastal",

            "category":
            "Casual",

            "items":
            [
                "Striped shirt",
                "Light denim",
                "Minimal shoes"
            ]
        }

    ],


    "Autumn": [

        {
            "name":
            "Dark Academia",

            "category":
            "Classic",

            "items":
            [
                "Wool coat",
                "Turtleneck",
                "Leather boots"
            ]
        },


        {
            "name":
            "Luxury Layers",

            "category":
            "Luxury",

            "items":
            [
                "Cashmere sweater",
                "Tailored pants",
                "Loafers"
            ]
        }

    ],


    "Winter": [

        {
            "name":
            "Cold Weather Minimal",

            "category":
            "Minimal",

            "items":
            [
                "Long coat",
                "Heavy knit sweater",
                "Chelsea boots"
            ]
        },


        {
            "name":
            "Urban Winter",

            "category":
            "Streetwear",

            "items":
            [
                "Puffer jacket",
                "Cargo pants",
                "Chunky sneakers"
            ]
        }

    ]

}



# -------------------------------------------------------
# Inspiration Gallery
# -------------------------------------------------------

FASHION_CATEGORIES = {

    "Minimal Luxury":
    [
        "neutral colors",
        "tailored clothing",
        "clean silhouettes",
        "premium basics"
    ],


    "Streetwear":
    [
        "oversized fits",
        "sneakers",
        "layering",
        "graphic pieces"
    ],


    "Old Money":
    [
        "linen shirts",
        "knit sweaters",
        "loafers",
        "classic colors"
    ],


    "Avant Garde":
    [
        "unusual shapes",
        "experimental cuts",
        "artistic clothing"
    ],


    "Casual Everyday":
    [
        "denim",
        "comfortable basics",
        "simple layers"
    ]

}



# -------------------------------------------------------
# Get Seasonal Looks
# -------------------------------------------------------

def get_season_collection(
    season
):

    return SEASON_COLLECTIONS.get(
        season,
        []
    )



# -------------------------------------------------------
# Get Category Inspiration
# -------------------------------------------------------

def get_category(
    category
):

    return FASHION_CATEGORIES.get(
        category,
        []
    )



# -------------------------------------------------------
# Search Gallery
# -------------------------------------------------------

def search_gallery(
    keyword
):

    keyword = keyword.lower()

    results = []


    for season, looks in SEASON_COLLECTIONS.items():

        for look in looks:

            text = (

                look["name"]
                +
                look["category"]
                +
                " ".join(
                    look["items"]
                )

            ).lower()


            if keyword in text:

                results.append(
                    look
                )


    return results



# -------------------------------------------------------
# Random Outfit Inspiration
# -------------------------------------------------------

def random_inspiration():

    import random


    season = random.choice(

        list(
            SEASON_COLLECTIONS.keys()
        )

    )


    look = random.choice(

        SEASON_COLLECTIONS[
            season
        ]

    )


    return {

        "season":
        season,

        "look":
        look

    }



# -------------------------------------------------------
# Build Mood Board
# -------------------------------------------------------

def create_mood_board(
    style
):

    style = style.lower()


    boards = {


        "minimal":
        [
            "white",
            "cream",
            "black",
            "structured shapes"
        ],


        "street":
        [
            "oversized",
            "layers",
            "sneakers",
            "bold graphics"
        ],


        "luxury":
        [
            "quality fabrics",
            "neutral tones",
            "tailoring"
        ],


        "classic":
        [
            "navy",
            "brown",
            "wool",
            "leather"
        ]

    }


    for key in boards:

        if key in style:

            return boards[key]


    return [

        "balanced colors",
        "comfortable fit",
        "personal style"

    ]