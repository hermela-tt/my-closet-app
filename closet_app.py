import streamlit as st

from PIL import Image

from vision import analyze_image

from recommendations import (
    fashion_recommendation,
    generate_outfit
)

from wardrobe import (
    load_wardrobe,
    save_wardrobe,
    add_item,
    wardrobe_statistics,
    increase_wear,
    toggle_favorite
)

from gallery import (
    get_season_collection,
    random_inspiration
)

import ui



# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="FitMax Closet",
    page_icon="FitMax",
    layout="wide"
)


ui.load_theme()



# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

if "wardrobe" not in st.session_state:

    st.session_state.wardrobe = load_wardrobe()



# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

ui.header()



# -------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------

page = ui.sidebar()



# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

if page == "Dashboard":

    stats = wardrobe_statistics(
        st.session_state.wardrobe
    )

    ui.metrics(
        stats
    )


    st.divider()


    ui.card(
        "AI Fashion Assistant",
        "Upload clothing images, analyze your style, and generate outfits from your closet."
    )


    st.subheader(
        "Random Fashion Inspiration"
    )


    inspiration = random_inspiration()


    st.write(
        inspiration
    )



# -------------------------------------------------------
# IMAGE ANALYSIS
# -------------------------------------------------------

elif page == "Analyze Clothing":

    st.header(
        "Clothing AI Analysis"
    )


    uploaded = st.file_uploader(
        "Upload clothing image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    if uploaded:


        image = Image.open(
            uploaded
        )


        st.image(
            image,
            width=350
        )


        if st.button(
            "Analyze Clothing"
        ):


            result = analyze_image(
                image
            )


            st.session_state.analysis = result


            st.success(
                "Analysis complete"
            )


            st.write(
                result
            )


    if "analysis" in st.session_state:


        st.divider()


        name = st.text_input(
            "Clothing name"
        )


        category = st.selectbox(

            "Category",

            [

                "Top",

                "Bottom",

                "Outerwear",

                "Shoes",

                "Accessory",

                "Full Outfit"

            ]

        )


        style = st.text_input(
            "Style",
            value="Smart Casual"
        )


        if st.button(
            "Save To Closet"
        ):


            st.session_state.wardrobe = add_item(

                st.session_state.wardrobe,

                name,

                category,

                style,

                st.session_state.analysis

            )


            save_wardrobe(

                st.session_state.wardrobe

            )


            st.success(
                "Saved"
            )



# -------------------------------------------------------
# OUTFIT GENERATOR
# -------------------------------------------------------

elif page == "Outfit Generator":


    st.header(
        "AI Outfit Generator"
    )


    style = st.selectbox(

        "Choose style",

        [

            "Minimal Luxury",

            "Smart Casual",

            "Streetwear / Layered",

            "Dark Academia",

            "Bold Statement"

        ]

    )


    if st.button(
        "Generate Outfit"
    ):


        outfit = generate_outfit(
            style
        )


        ui.outfit_card(
            outfit
        )



# -------------------------------------------------------
# CLOSET
# -------------------------------------------------------

elif page == "My Closet":


    st.header(
        "My Digital Closet"
    )


    if not st.session_state.wardrobe:

        st.info(
            "Your closet is empty."
        )


    for item in st.session_state.wardrobe:


        ui.wardrobe_item(
            item
        )


        col1, col2 = st.columns(
            2
        )


        with col1:

            if st.button(
                "Wear +1",
                key=f"wear_{item['id']}"
            ):

                increase_wear(

                    st.session_state.wardrobe,

                    item["id"]

                )


                save_wardrobe(

                    st.session_state.wardrobe

                )


                st.rerun()


        with col2:

            if st.button(
                "Favorite",
                key=f"fav_{item['id']}"
            ):

                toggle_favorite(

                    st.session_state.wardrobe,

                    item["id"]

                )


                save_wardrobe(

                    st.session_state.wardrobe

                )


                st.rerun()



# -------------------------------------------------------
# STYLE GALLERY
# -------------------------------------------------------

elif page == "Style Gallery":


    st.header(
        "Fashion Gallery"
    )


    season = st.selectbox(

        "Season",

        [

            "Spring",

            "Summer",

            "Autumn",

            "Winter"

        ]

    )


    looks = get_season_collection(
        season
    )


    for look in looks:

        ui.card(

            look["name"],

            ", ".join(
                look["items"]
            )

        )



# -------------------------------------------------------
# SETTINGS
# -------------------------------------------------------

elif page == "Settings":


    st.header(
        "Settings"
    )


    st.write(
        "FitMax lightweight AI mode enabled."
    )


    st.write(
        "No Torch required."
    )