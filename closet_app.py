import streamlit as st
import numpy as np
import pandas as pd
import cv2
import torch
import requests

from io import BytesIO
from PIL import Image, ImageDraw

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

from skimage.color import rgb2lab, lab2rgb

from transformers import (
    CLIPProcessor,
    CLIPModel
)

from ultralytics import YOLO


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="fitmax AI Fashion Engine",
    layout="wide"
)


# --------------------------------------------------
# PREMIUM UI STYLE
# --------------------------------------------------

st.markdown(
"""
<style>

body {
    font-family: Inter, sans-serif;
}


.stApp {

    background:
    linear-gradient(
        135deg,
        #f4f0ff,
        #ffffff
    );

}


.dashboard-card {

    background:white;

    padding:25px;

    border-radius:22px;

    box-shadow:
    0 15px 40px rgba(0,0,0,.08);

    margin-bottom:20px;

    transition:.25s;

}


.dashboard-card:hover {

    transform:
    translateY(-5px);

}


.title {

font-size:42px;
font-weight:900;

}


.subtitle {

font-size:18px;

color:#666;

}


.badge {

background:#111;

color:white;

padding:8px 15px;

border-radius:20px;

font-size:13px;

}


</style>
""",
unsafe_allow_html=True
)



# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------


@st.cache_resource
def load_clip():

    model = CLIPModel.from_pretrained(
        "openai/clip-vit-base-patch32"
    )

    processor = CLIPProcessor.from_pretrained(
        "openai/clip-vit-base-patch32"
    )

    return model, processor



@st.cache_resource
def load_detector():

    return YOLO(
        "yolov8n.pt"
    )



clip_model, clip_processor = load_clip()

detector = load_detector()



# --------------------------------------------------
# SESSION STORAGE
# --------------------------------------------------

if "wardrobe" not in st.session_state:

    st.session_state.wardrobe = []



if "embeddings" not in st.session_state:

    st.session_state.embeddings = []



# --------------------------------------------------
# IMAGE HELPERS
# --------------------------------------------------


def load_image(upload):

    return Image.open(
        upload
    ).convert(
        "RGB"
    )



def image_from_url(url):

    try:

        r=requests.get(
            url,
            timeout=10
        )

        return Image.open(
            BytesIO(r.content)
        ).convert("RGB")

    except:

        return None



# --------------------------------------------------
# COLOR AI
# --------------------------------------------------


def extract_palette(image, k=5):

    img=np.array(
        image.resize(
            (100,100)
        )
    )


    lab=rgb2lab(
        img
    )


    pixels=lab.reshape(
        -1,
        3
    )


    km=KMeans(
        n_clusters=k,
        random_state=42
    )

    km.fit(
        pixels
    )


    centers=km.cluster_centers_

    rgb=lab2rgb(
        centers.reshape(
            1,
            k,
            3
        )
    )[0]


    rgb=np.clip(
        rgb*255,
        0,
        255
    ).astype(int)


    return rgb



def rgb_hex(color):

    return "#%02x%02x%02x" % tuple(color)



# --------------------------------------------------
# CLOTHING DETECTION
# --------------------------------------------------


def detect_clothing(image):


    results=detector(
        np.array(image)
    )


    detected=[]


    for result in results:

        for box in result.boxes:


            cls=int(
                box.cls[0]
            )

            conf=float(
                box.conf[0]
            )


            detected.append(

                {
                    "object":
                    detector.names[cls],

                    "confidence":
                    round(conf,2)
                }

            )


    return detected



# --------------------------------------------------
# CLIP EMBEDDINGS
# --------------------------------------------------


def get_embedding(image):


    inputs=clip_processor(

        images=image,

        return_tensors="pt"

    )


    with torch.no_grad():

        features=clip_model.get_image_features(
            **inputs
        )


    features=features / features.norm(
        dim=-1,
        keepdim=True
    )


    return features.cpu().numpy()



# --------------------------------------------------
# STYLE AI
# --------------------------------------------------


STYLE_LIBRARY={


"Minimal Luxury":

[
"white shirt",
"black trousers",
"tailored coat",
"clean fashion"
],


"Streetwear":

[
"oversized hoodie",
"sneakers",
"baggy jeans",
"urban outfit"
],


"Formal":

[
"business suit",
"evening dress",
"formal clothing"
],


"Vacation":

[
"linen shirt",
"summer outfit",
"resort wear"
]


}



def classify_style(image):


    image_vector=get_embedding(
        image
    )


    scores={}


    for style,examples in STYLE_LIBRARY.items():


        text_inputs=clip_processor(

            text=examples,

            return_tensors="pt",

            padding=True

        )


        with torch.no_grad():

            text_features=clip_model.get_text_features(
                **text_inputs
            )


        text_features/=text_features.norm(
            dim=-1,
            keepdim=True
        )


        score=torch.mean(

            torch.tensor(

                cosine_similarity(

                    image_vector,

                    text_features.numpy()

                )

            )

        )


        scores[style]=float(score)



    return max(
        scores,
        key=scores.get
    ), scores



# --------------------------------------------------
# HEADER
# --------------------------------------------------


st.markdown(
"""
<div class="title">
fitmax AI Fashion Engine
</div>

<div class="subtitle">
Computer vision powered wardrobe intelligence
</div>

<br>
""",

unsafe_allow_html=True
)



# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

tabs=st.tabs(

[
"AI Scanner",
"Fashion Library",
"Wardrobe",
"Style Intelligence"
]

)
