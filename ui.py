import streamlit as st


# -------------------------------------------------------
# Page Styling
# -------------------------------------------------------

def load_theme():

    st.markdown(
        """
        <style>

        .main {
            background:
            linear-gradient(
                135deg,
                #f8f5ff,
                #eef4ff
            );
        }


        .fashion-card {

            background:
            rgba(255,255,255,0.75);

            border-radius:
            18px;

            padding:
            20px;

            margin:
            10px 0;

            border:
            1px solid rgba(120,100,200,0.25);

            box-shadow:
            0 8px 30px rgba(0,0,0,0.08);

        }


        .fashion-title {

            font-size:
            32px;

            font-weight:
            800;

            color:
            #161616;

        }


        .fashion-subtitle {

            font-size:
            16px;

            color:
            #555;

        }


        .tag {

            display:
            inline-block;

            padding:
            5px 12px;

            border-radius:
            20px;

            background:
            #ddd2ff;

            margin:
            3px;

            font-size:
            12px;

        }


        .recommend-box {

            background:
            linear-gradient(
                120deg,
                #ffffff,
                #f2edff
            );

            border-radius:
            20px;

            padding:
            25px;

            border:
            2px solid #d5c8ff;

        }


        </style>

        """,

        unsafe_allow_html=True
    )



# -------------------------------------------------------
# Header
# -------------------------------------------------------

def header():

    st.markdown(

        """
        <div class="fashion-title">
        FitMax AI Closet
        </div>

        <div class="fashion-subtitle">
        Intelligent wardrobe analysis,
        outfit generation and personal style discovery
        </div>

        """,

        unsafe_allow_html=True

    )



# -------------------------------------------------------
# Card Component
# -------------------------------------------------------

def card(
    title,
    content
):

    st.markdown(

        f"""

        <div class="fashion-card">

        <h3>
        {title}
        </h3>

        <p>
        {content}
        </p>

        </div>

        """,

        unsafe_allow_html=True

    )



# -------------------------------------------------------
# Tags
# -------------------------------------------------------

def tags(
    items
):

    html = ""


    for item in items:

        html += (

            f'<span class="tag">'
            f'{item}'
            f'</span>'

        )


    st.markdown(

        html,

        unsafe_allow_html=True

    )



# -------------------------------------------------------
# Outfit Display
# -------------------------------------------------------

def outfit_card(
    outfit
):

    st.markdown(

        """

        <div class="recommend-box">

        </div>

        """,

        unsafe_allow_html=True

    )


    st.subheader(
        "Recommended Outfit"
    )


    col1, col2 = st.columns(
        2
    )


    with col1:

        st.write(
            "Style"
        )

        st.success(

            outfit.get(
                "style",
                "Unknown"
            )

        )


        st.write(
            "Top"
        )

        st.write(

            outfit.get(
                "top"
            )

        )


        st.write(
            "Bottom"
        )

        st.write(

            outfit.get(
                "bottom"
            )

        )


    with col2:

        st.write(
            "Shoes"
        )

        st.write(

            outfit.get(
                "shoes"
            )

        )


        st.write(
            "Accessories"
        )

        st.write(

            outfit.get(
                "accessories"
            )

        )



# -------------------------------------------------------
# Wardrobe Item Card
# -------------------------------------------------------

def wardrobe_item(
    item
):

    st.markdown(

        f"""

        <div class="fashion-card">

        <h3>
        {item.get("name")}
        </h3>

        <p>
        Category:
        {item.get("category")}
        </p>

        <p>
        Style:
        {item.get("style")}
        </p>

        <p>
        Worn:
        {item.get("wear_count",0)}
        times
        </p>


        </div>

        """,

        unsafe_allow_html=True

    )



# -------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------

def sidebar():

    st.sidebar.title(
        "FitMax"
    )


    return st.sidebar.radio(

        "Navigation",

        [

            "Dashboard",

            "Analyze Clothing",

            "Outfit Generator",

            "My Closet",

            "Style Gallery",

            "Settings"

        ]

    )



# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

def metrics(
    stats
):

    c1, c2, c3 = st.columns(
        3
    )


    with c1:

        st.metric(

            "Items",

            stats.get(
                "total",
                0
            )

        )


    with c2:

        st.metric(

            "Favorites",

            stats.get(
                "favorites",
                0
            )

        )


    with c3:

        st.metric(

            "Most Used",

            stats.get(
                "most_used",
                "-"
            )

        )