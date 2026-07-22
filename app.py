import streamlit as st
import pandas as pd
import numpy as np
import cv2
import requests
from io import BytesIO
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb, deltaE_ciede2000
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="CAPSULE — Smart Wardrobe Engine", page_icon="👔", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f1419; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    .card { background-color: #1a1f2e; padding: 1rem; border-radius: 12px; border: 2px solid #2d3748; margin-bottom: 1rem; transition: all 0.3s ease; }
    .card:hover { border-color: #667eea; background-color: #202b3d; }
    .card-selected { background-color: #667eea; border-color: #667eea; color: #ffffff; }
    .select-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; border: none; padding: 0.6rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
    .trending-label { background-color: #f59e0b; color: #000000; padding: 0.3rem 0.8rem; border-radius: 4px; font-weight: 700; font-size: 0.75rem; }
    .celebrity-label { background-color: #ec4899; color: #ffffff; padding: 0.3rem 0.8rem; border-radius: 4px; font-weight: 700; font-size: 0.75rem; }
    code { background-color: #2d3748; color: #60d394; padding: 0.2rem 0.6rem; border-radius: 4px; }
    .section-title { color: #667eea; font-size: 1.5rem; font-weight: 700; margin-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- COMPUTER VISION CORE ---
def extract_palette_from_image(image_input, k=3):
    """
    Extracts dominant colors using CIELAB space K-Means.
    Accepts PIL Image or Uploaded File Bytes.
    """
    if isinstance(image_input, Image.Image):
        img = np.array(image_input.convert('RGB'))
    else:
        file_bytes = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.resize(img, (100, 100))
    img_lab = rgb2lab(img)
    pixels_lab = img_lab.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k, n_init=5, random_state=42)
    kmeans.fit(pixels_lab)

    centers_lab = kmeans.cluster_centers_.reshape((1, k, 3))
    centers_rgb = (lab2rgb(centers_lab)[0] * 255).astype(int)
    centers_rgb = np.clip(centers_rgb, 0, 255)
    return centers_rgb

def rgb_to_hex(rgb):
    return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"

def fetch_image_from_url(url):
    """Fetches an image securely over HTTP/HTTPS."""
    try:
        response = requests.get(url, timeout=5)
        return Image.open(BytesIO(response.content))
    except Exception:
        return None

def fetch_trending_fashion_photos():
    """Fetches trending fashion photos from Unsplash API."""
    trending_urls = [
        "https://images.unsplash.com/photo-1608844593658-88f6b01b7b39?w=400&q=80",  # Fashion
        "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=400&q=80",  # Outfit
        "https://images.unsplash.com/photo-1609932149074-d01ae72cd60f?w=400&q=80",  # Casual
        "https://images.unsplash.com/photo-1529389807024-f7b8c9f14b1f?w=400&q=80",  # Style
        "https://images.unsplash.com/photo-1595777707802-21b287e3fbf7?w=400&q=80",  # Dress
        "https://images.unsplash.com/photo-1575575865872-15f298e51d87?w=400&q=80",  # High Fashion
        "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400&q=80",  # Minimalist
        "https://images.unsplash.com/photo-1551569867-240d0d4e6b36?w=400&q=80",  # Streetwear
    ]
    return trending_urls

def fetch_celebrity_inspiration_photos():
    """Fetches celebrity fashion inspiration photos."""
    celebrity_urls = [
        "https://images.unsplash.com/photo-1539008588435-666cafc3f3b2?w=400&q=80",  # Elegant
        "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=400&q=80",  # Red Carpet
        "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&q=80",  # Glamorous
        "https://images.unsplash.com/photo-1552289550-fee674aa84d5?w=400&q=80",  # Chic
        "https://images.unsplash.com/photo-1572992122207-37eab73ab6b4?w=400&q=80",  # Luxury
        "https://images.unsplash.com/photo-1586362891335-a58bbd1c57f0?w=400&q=80",  # Sophisticated
        "https://images.unsplash.com/photo-1581570871968-c5922b5d9222?w=400&q=80",  # Evening Wear
        "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&q=80",  # Designer
    ]
    return celebrity_urls

# --- STATE INIT ---
if 'wardrobe' not in st.session_state:
    st.session_state.wardrobe = pd.DataFrame(columns=[
        "id", "name", "category", "context", "wears", "rating", "rgb"
    ])

# Default Pinterest/Inspiration Preset Image Links
if 'pinterest_queue' not in st.session_state:
    st.session_state.pinterest_queue = [
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400",
        "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=400",
        "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=400",
        "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=400"
    ]

# Trending Fashion Photos
if 'trending_queue' not in st.session_state:
    st.session_state.trending_queue = fetch_trending_fashion_photos()

# Celebrity Inspiration Photos
if 'celebrity_queue' not in st.session_state:
    st.session_state.celebrity_queue = fetch_celebrity_inspiration_photos()

if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None

if 'selected_image_source' not in st.session_state:
    st.session_state.selected_image_source = None

# --- UI APP ---
st.title("CAPSULE")
st.caption("Visual Closet Management & Pinterest Inspiration Import Engine")

tabs = st.tabs(["📌 Pinterest & Web Discovery", "⭐ Celebrity Inspired", "🔥 Trending", "🖼️ Closet Archive", "🎨 Palette Gap Analysis"])

# ---------------------------------------------------------
# TAB 1: PINTEREST & WEB IMPORT WITH ONE-CLICK SELECT
# ---------------------------------------------------------
with tabs[0]:
    st.subheader("1. Add Pinterest / Web Image Links")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        url_input = st.text_input("Paste Image URL or Pinterest Direct Image Link", placeholder="https://i.pinimg.com/originals/...")
    with col2:
        if st.button("➕ Add", use_container_width=True):
            if url_input and url_input not in st.session_state.pinterest_queue:
                st.session_state.pinterest_queue.append(url_input)
                st.success("Added image to grid!")

    st.divider()
    st.subheader("2. Click an Image to Extract & Import")
    
    # Display images in interactive visual grid
    grid_cols = st.columns(4)
    for idx, img_url in enumerate(st.session_state.pinterest_queue):
        with grid_cols[idx % 4]:
            st.image(img_url, use_container_width=True)
            if st.button(f"✓ Select", key=f"select_pinterest_{idx}", use_container_width=True):
                fetched_img = fetch_image_from_url(img_url)
                if fetched_img:
                    st.session_state.selected_image = fetched_img
                    st.session_state.selected_image_source = "Pinterest"
                    st.toast(f"Selected from Pinterest! ✓")
                else:
                    st.error("Could not load image from URL.")

    # Details Form for Selected Image
    if st.session_state.selected_image is not None:
        st.divider()
        st.subheader("3. Confirm & Archive Selected Item")
        
        
        c_prev, c_meta = st.columns([1, 2])
        with c_prev:
            st.image(st.session_state.selected_image, width=220)
        
        with c_meta:
            rgbs = extract_palette_from_image(st.session_state.selected_image, k=3)
            st.write("**Extracted Palette Signature:**")
            
            p1, p2, p3 = st.columns(3)
            for i, p_col in enumerate([p1, p2, p3]):
                with p_col:
                    st.color_picker(f"Tone {i+1}", value=rgb_to_hex(rgbs[i]), disabled=True, key=f"p_{i}")
                    
            item_name = st.text_input("Item Label", value="Pinterest Inspired Look")
            cat = st.selectbox("Category", ["Tops", "Bottoms", "Outerwear", "Footwear", "Accessories"])
            ctx = st.selectbox("Context Tag", ["Work", "Casual", "Formal", "Vacation", "Loungewear"])
            
            if st.button("Save to Wardrobe Archive"):
                new_item = {
                    "id": len(st.session_state.wardrobe) + 1,
                    "name": item_name, "category": cat, "context": ctx,
                    "wears": 0, "rating": 5, "rgb": rgbs[0].tolist()
                }
                st.session_state.wardrobe = pd.concat([st.session_state.wardrobe, pd.DataFrame([new_item])], ignore_index=True)
                st.success(f"Successfully archived '{item_name}' to your closet!")
                st.session_state.selected_image = None
                st.rerun()

# ---------------------------------------------------------
# TAB 2: CELEBRITY INSPIRATION
# ---------------------------------------------------------
with tabs[1]:
    st.markdown('<p class="section-title">👗 Celebrity Fashion Inspiration</p>', unsafe_allow_html=True)
    st.write("Discover high-fashion styles from celebrity wardrobes and red carpet events.")
    
    st.divider()
    
    # Display celebrity images in interactive visual grid
    grid_cols = st.columns(4)
    for idx, img_url in enumerate(st.session_state.celebrity_queue):
        with grid_cols[idx % 4]:
            st.image(img_url, use_container_width=True)
            st.markdown('<span class="celebrity-label">✨ CELEBRITY</span>', unsafe_allow_html=True)
            if st.button(f"✓ Select", key=f"select_celebrity_{idx}", use_container_width=True):
                fetched_img = fetch_image_from_url(img_url)
                if fetched_img:
                    st.session_state.selected_image = fetched_img
                    st.session_state.selected_image_source = "Celebrity"
                    st.toast(f"Selected from Celebrity Inspiration! ✓")
                else:
                    st.error("Could not load image from URL.")

    # Details Form for Selected Celebrity Image
    if st.session_state.selected_image is not None and st.session_state.selected_image_source == "Celebrity":
        st.divider()
        st.subheader("Add to Your Wardrobe")
        
        c_prev, c_meta = st.columns([1, 2])
        with c_prev:
            st.image(st.session_state.selected_image, width=220)
            st.markdown('<span class="celebrity-label">✨ CELEBRITY</span>', unsafe_allow_html=True)
        
        with c_meta:
            rgbs = extract_palette_from_image(st.session_state.selected_image, k=3)
            st.write("**Extracted Palette Signature:**")
            
            p1, p2, p3 = st.columns(3)
            for i, p_col in enumerate([p1, p2, p3]):
                with p_col:
                    st.color_picker(f"Tone {i+1}", value=rgb_to_hex(rgbs[i]), disabled=True, key=f"celeb_p_{i}")
                    
            item_name = st.text_input("Item Label", value="Celebrity Inspired Outfit", key="celeb_name")
            cat = st.selectbox("Category", ["Tops", "Bottoms", "Outerwear", "Footwear", "Accessories"], key="celeb_cat")
            ctx = st.selectbox("Context Tag", ["Work", "Casual", "Formal", "Vacation", "Loungewear"], key="celeb_ctx")
            
            if st.button("💾 Save to Wardrobe Archive", use_container_width=True):
                new_item = {
                    "id": len(st.session_state.wardrobe) + 1,
                    "name": item_name, "category": cat, "context": ctx,
                    "wears": 0, "rating": 5, "rgb": rgbs[0].tolist()
                }
                st.session_state.wardrobe = pd.concat([st.session_state.wardrobe, pd.DataFrame([new_item])], ignore_index=True)
                st.success(f"Successfully archived '{item_name}' to your closet!")
                st.session_state.selected_image = None
                st.rerun()

# ---------------------------------------------------------
# TAB 3: TRENDING FASHION
# ---------------------------------------------------------
with tabs[2]:
    st.markdown('<p class="section-title">🔥 Trending Fashion Now</p>', unsafe_allow_html=True)
    st.write("Stay current with the latest fashion trends and viral outfit styles.")
    
    st.divider()
    
    # Display trending images in interactive visual grid
    grid_cols = st.columns(4)
    for idx, img_url in enumerate(st.session_state.trending_queue):
        with grid_cols[idx % 4]:
            st.image(img_url, use_container_width=True)
            st.markdown('<span class="trending-label">🔥 TRENDING</span>', unsafe_allow_html=True)
            if st.button(f"✓ Select", key=f"select_trending_{idx}", use_container_width=True):
                fetched_img = fetch_image_from_url(img_url)
                if fetched_img:
                    st.session_state.selected_image = fetched_img
                    st.session_state.selected_image_source = "Trending"
                    st.toast(f"Selected from Trending! ✓")
                else:
                    st.error("Could not load image from URL.")

    # Details Form for Selected Trending Image
    if st.session_state.selected_image is not None and st.session_state.selected_image_source == "Trending":
        st.divider()
        st.subheader("Add to Your Wardrobe")
        
        c_prev, c_meta = st.columns([1, 2])
        with c_prev:
            st.image(st.session_state.selected_image, width=220)
            st.markdown('<span class="trending-label">🔥 TRENDING</span>', unsafe_allow_html=True)
        
        with c_meta:
            rgbs = extract_palette_from_image(st.session_state.selected_image, k=3)
            st.write("**Extracted Palette Signature:**")
            
            p1, p2, p3 = st.columns(3)
            for i, p_col in enumerate([p1, p2, p3]):
                with p_col:
                    st.color_picker(f"Tone {i+1}", value=rgb_to_hex(rgbs[i]), disabled=True, key=f"trend_p_{i}")
                    
            item_name = st.text_input("Item Label", value="Trending Outfit", key="trend_name")
            cat = st.selectbox("Category", ["Tops", "Bottoms", "Outerwear", "Footwear", "Accessories"], key="trend_cat")
            ctx = st.selectbox("Context Tag", ["Work", "Casual", "Formal", "Vacation", "Loungewear"], key="trend_ctx")
            
            if st.button("💾 Save to Wardrobe Archive", use_container_width=True, key="trend_save"):
                new_item = {
                    "id": len(st.session_state.wardrobe) + 1,
                    "name": item_name, "category": cat, "context": ctx,
                    "wears": 0, "rating": 5, "rgb": rgbs[0].tolist()
                }
                st.session_state.wardrobe = pd.concat([st.session_state.wardrobe, pd.DataFrame([new_item])], ignore_index=True)
                st.success(f"Successfully archived '{item_name}' to your closet!")
                st.session_state.selected_image = None
                st.rerun()

# ---------------------------------------------------------
# TAB 4: CLOSET VIEW
# ---------------------------------------------------------
with tabs[3]:
    st.markdown('<p class="section-title">🖼️ Your Wardrobe Archive</p>', unsafe_allow_html=True)
    if st.session_state.wardrobe.empty:
        st.info("✨ No items in your closet yet. Select and save images from Pinterest, Celebrity, or Trending tabs.")
    else:
        cols = st.columns(3)
        for idx, row in st.session_state.wardrobe.iterrows():
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="card">
                    <h3>{row['name']}</h3>
                    <p><b>Category:</b> {row['category']}</p>
                    <p><b>Context:</b> <code>{row['context']}</code></p>
                    <p><b>Wears:</b> {row['wears']} | <b>Rating:</b> ⭐ {row['rating']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.color_picker("Dominant Tone", value=rgb_to_hex(row['rgb']), disabled=True, key=f"w_cp_{row['id']}")

# ---------------------------------------------------------
# TAB 5: PALETTE GAP ENGINE
# ---------------------------------------------------------
with tabs[4]:
    st.markdown('<p class="section-title">🎨 Your Color Spectrum</p>', unsafe_allow_html=True)
    st.write("Visualize the color palette of your entire wardrobe at a glance.")
    st.divider()
    
    if not st.session_state.wardrobe.empty:
        st.write(f"**Total Items:** {len(st.session_state.wardrobe)}")
        
        # Create a beautiful spectrum visualization
        for idx, (_, row) in enumerate(st.session_state.wardrobe.iterrows()):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f'<div style="background-color:{rgb_to_hex(row["rgb"])}; height:40px; border-radius:6px; border: 2px solid #667eea;"></div>', unsafe_allow_html=True)
            with col2:
                st.write(f"**{row['name']}** — {row['category']} ({row['context']})")
    else:
        st.write("📊 Archive items to render your closet's color spectrum.")