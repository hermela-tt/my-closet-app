import json
import os
from datetime import datetime


# -------------------------------------------------------
# Wardrobe Storage
# -------------------------------------------------------

DEFAULT_FILE = "wardrobe_data.json"


def create_wardrobe():

    return []


# -------------------------------------------------------
# Load / Save
# -------------------------------------------------------

def load_wardrobe(
    filename=DEFAULT_FILE
):

    if not os.path.exists(
        filename
    ):
        return []


    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return []



def save_wardrobe(
    wardrobe,
    filename=DEFAULT_FILE
):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            wardrobe,
            file,
            indent=4
        )


# -------------------------------------------------------
# Add Clothing Item
# -------------------------------------------------------

def add_item(
    wardrobe,
    name,
    category,
    style,
    analysis,
    image_path=None
):

    item = {

        "id":
        len(wardrobe) + 1,


        "name":
        name,


        "category":
        category,


        "style":
        style,


        "image":
        image_path,


        "colors":
        analysis.get(
            "palette",
            []
        ),


        "brightness":
        analysis.get(
            "brightness",
            0
        ),


        "texture":
        analysis.get(
            "texture",
            ""
        ),


        "wear_count":
        0,


        "favorite":
        False,


        "created":
        datetime.now().isoformat()

    }


    wardrobe.append(
        item
    )


    return wardrobe



# -------------------------------------------------------
# Remove Item
# -------------------------------------------------------

def remove_item(
    wardrobe,
    item_id
):

    return [

        item

        for item in wardrobe

        if item.get(
            "id"
        ) != item_id

    ]



# -------------------------------------------------------
# Find Item
# -------------------------------------------------------

def get_item(
    wardrobe,
    item_id
):

    for item in wardrobe:

        if item.get(
            "id"
        ) == item_id:

            return item


    return None



# -------------------------------------------------------
# Wear Tracking
# -------------------------------------------------------

def increase_wear(
    wardrobe,
    item_id
):

    item = get_item(
        wardrobe,
        item_id
    )


    if item:

        item["wear_count"] += 1


    return wardrobe



# -------------------------------------------------------
# Favorites
# -------------------------------------------------------

def toggle_favorite(
    wardrobe,
    item_id
):

    item = get_item(
        wardrobe,
        item_id
    )


    if item:

        item["favorite"] = not item["favorite"]


    return wardrobe



# -------------------------------------------------------
# Search
# -------------------------------------------------------

def search_items(
    wardrobe,
    query
):

    query = query.lower()


    results = []


    for item in wardrobe:

        searchable = (

            item.get(
                "name",
                ""
            )
            +
            item.get(
                "category",
                ""
            )
            +
            item.get(
                "style",
                ""
            )

        ).lower()


        if query in searchable:

            results.append(
                item
            )


    return results



# -------------------------------------------------------
# Filtering
# -------------------------------------------------------

def filter_category(
    wardrobe,
    category
):

    return [

        item

        for item in wardrobe

        if item.get(
            "category"
        ) == category

    ]



def filter_style(
    wardrobe,
    style
):

    return [

        item

        for item in wardrobe

        if item.get(
            "style"
        ) == style

    ]



# -------------------------------------------------------
# Analytics
# -------------------------------------------------------

def wardrobe_statistics(
    wardrobe
):

    if not wardrobe:

        return {

            "total":
            0,

            "favorites":
            0,

            "most_used":
            None

        }



    favorite_count = sum(

        1

        for item in wardrobe

        if item.get(
            "favorite"
        )

    )


    most_used = max(

        wardrobe,

        key=lambda x:
        x.get(
            "wear_count",
            0
        )

    )


    styles = {}


    for item in wardrobe:

        style = item.get(
            "style",
            "Unknown"
        )


        styles[style] = (
            styles.get(
                style,
                0
            )
            + 1
        )


    return {

        "total":
        len(
            wardrobe
        ),

        "favorites":
        favorite_count,

        "most_used":
        most_used.get(
            "name"
        ),

        "styles":
        styles

    }



# -------------------------------------------------------
# Color Collection
# -------------------------------------------------------

def collect_colors(
    wardrobe
):

    colors = []


    for item in wardrobe:

        colors.extend(

            item.get(
                "colors",
                []
            )

        )


    return colors