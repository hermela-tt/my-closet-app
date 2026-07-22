from io import BytesIO
import cv2
import numpy as np
import pandas as pd
import PIL.Image as Image
import requests
from skimage.color import lab2rgb, rgb2lab
from sklearn.cluster import KMeans
import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="fitmax — AI Fashion Engine", page_icon="✨", layout="wide"
)

st.markdown(
    """
    <style>
    :root {
        --primary-dark: #f4ebff;
        --card-bg: #f7f1ff;
        --border-light: #8f8dd6;
        --border-main: #8a7ec9;
        --text-primary: #111111;
        --text-dark: #111111;
        --accent-1: #c7b8ff;
        --accent-2: #a9c8ff;
        --light-purple: #d8c4ff;
        --gray-replacement: #c8bfe3;
    }
    
    * { box-sizing: border-box; }
    
    .stApp { 
        background: linear-gradient(135deg, #ece6ff 0%, #f7f9ff 100%);
        color: var(--text-primary); 
        font-family: 'Segoe UI', sans-serif; 
    }

    .banner-title {
        color: #111111;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .banner-subtitle {
        color: #111111;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .card { 
        background-color: var(--card-bg); 
        color: var(--text-primary);
        padding: 1rem; 
        border-radius: 12px; 
        border: 2px solid var(--border-main); 
        margin-bottom: 1rem; 
        transition: all 0.3s ease;
    }
    
    .card:hover { 
        border-color: var(--border-light); 
        background-color: #f1eaff; 
        box-shadow: 0 0 20px rgba(138, 126, 201, 0.25);
    }
    
    .trending-label { 
        background-color: var(--accent-1); 
        color: var(--text-dark); 
        padding: 0.4rem 0.9rem; 
        border-radius: 6px; 
        font-weight: 700; 
        font-size: 0.8rem; 
    }
    
    .celebrity-label { 
        background-color: var(--accent-2); 
        color: var(--text-dark); 
        padding: 0.4rem 0.9rem; 
        border-radius: 6px; 
        font-weight: 700; 
        font-size: 0.8rem; 
        margin-top: 0.5rem;
        display: inline-block;
    }
    
    .section-title { 
        color: #111111; 
        font-size: 1.8rem; 
        font-weight: 800; 
        margin-top: 1.5rem; 
    }

    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #111111 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- COMPUTER VISION CORE ---
def extract_palette_from_image(image_input, k=3):
  """Extracts dominant colors using CIELAB space K-Means."""
  if isinstance(image_input, Image.Image):
    img = np.array(image_input.convert("RGB"))
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
  """Fetches an image securely over HTTP/HTTPS with proper User-Agent headers."""
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))
  except Exception as e:
    st.error(f"Failed to fetch image: {e}")
    return None


def fetch_trending_fashion_photos():
  return [
      {
          "url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=600&q=80",
          "title": "Minimalist Chic",
      },
      {
          "url": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=600&q=80",
          "title": "Editorial Haute Couture",
      },
      {
          "url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=600&q=80",
          "title": "Monochrome Fashion Statement",
      },
      {
          "url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=600&q=80",
          "title": "Luxury Streetwear Look",
      },
  ]


def fetch_celebrity_inspiration_photos():
  """REAL celebrity images sourced directly from Wikimedia Commons."""
  return [
      {
          "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Zendaya_2019_by_Glenn_Francis.jpg/600px-Zendaya_2019_by_Glenn_Francis.jpg",
          "name": "Zendaya",
          "desc": "Red Carpet Elegance",
      },
      {
          "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Emma_Watson_2013.jpg/600px-Emma_Watson_2013.jpg",
          "name": "Emma Watson",
          "desc": "Tailored Suit Chic",
      },
      {
          "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Hunter_Schafer_by_Gage_Skidmore.jpg/600px-Hunter_Schafer_by_Gage_Skidmore.jpg",
          "name": "Hunter Schafer",
          "desc": "Avant-Garde Style",
      },
      {
          "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Colman_Domingo_2022.jpg/600px-Colman_Domingo_2022.jpg",
          "name": "Colman Domingo",
          "desc": "High-Fashion Tailoring",
      },
  ]


def fetch_aesthetic_palettes():
  return {
      "Soft Minimalist": ["#e8d5f2", "#c9b1d9", "#a68bc7"],
      "Warm Golden": ["#f4d9a6", "#e8c547", "#d4a574"],
      "Cool Ocean": ["#a3d8ff", "#87ceeb", "#6ba8d4"],
      "Berry Bliss": ["#c084d0", "#d67fd8", "#e8a4e0"],
      "Earthy Vibes": ["#c9a876", "#b89968", "#a0825a"],
      "Pastel Dream": ["#f0d9f7", "#e5c7f0", "#d4b5e8"],
  }


# --- STATE INIT ---
if "wardrobe" not in st.session_state:
  st.session_state.wardrobe = pd.DataFrame(
      columns=["id", "name", "category", "context", "wears", "rating", "rgb"]
  )

if "pinterest_queue" not in st.session_state:
  st.session_state.pinterest_queue = [
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=600&q=80",
      "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=600&q=80",
      "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=600&q=80",
  ]

if "aesthetic_palettes" not in st.session_state:
  st.session_state.aesthetic_palettes = fetch_aesthetic_palettes()

if "trending_queue" not in st.session_state:
  st.session_state.trending_queue = fetch_trending_fashion_photos()

if "celebrity_queue" not in st.session_state:
  st.session_state.celebrity_queue = fetch_celebrity_inspiration_photos()

if "selected_image" not in st.session_state:
  st.session_state.selected_image = None

if "selected_image_source" not in st.session_state:
  st.session_state.selected_image_source = None

# --- UI APP ---
st.markdown('<div class="banner-title">fitmax</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="banner-subtitle">AI-Powered Fashion Curation & Wardrobe'
    " Intelligence</div>",
    unsafe_allow_html=True,
)

tabs = st.tabs([
    "Pinterest & Web Discovery",
    "Recent Celebrity Looks",
    "Trending",
    "Color Aesthetics",
    "Closet Archive",
    "Palette Analysis",
])

# --- TAB 1: PINTEREST & WEB ---
with tabs[0]:
  st.markdown("## Upload Your Inspiration")
  st.markdown("Paste any direct image URL below to add it to your collection:")

  col1, col2 = st.columns([4, 1])
  with col1:
    url_input = st.text_input(
        "Image URL",
        placeholder="https://images.unsplash.com/photo-...",
        key="pin_url_input",
    )
  with col2:
    if st.button("➕ Add", use_container_width=True, key="add_pin_btn"):
      if url_input and url_input not in st.session_state.pinterest_queue:
        st.session_state.pinterest_queue.append(url_input)
        st.success("✅ Added image to grid!")

  st.divider()
  st.markdown("## Select an Image")

  grid_cols = st.columns(3)
  for idx, img_url in enumerate(st.session_state.pinterest_queue):
    with grid_cols[idx % 3]:
      st.image(img_url, use_container_width=True)
      if st.button(
          "Select", key=f"select_pinterest_{idx}", use_container_width=True
      ):
        fetched_img = fetch_image_from_url(img_url)
        if fetched_img:
          st.session_state.selected_image = fetched_img
          st.session_state.selected_image_source = "Pinterest Look"
          st.toast("Selected look from Pinterest!")

# --- TAB 2: CELEBRITY INSPIRATION ---
with tabs[1]:
  st.markdown(
      '<p class="section-title">Recent Celebrity Looks</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "**Full Outfit Visuals: High fashion runway & red carpet inspiration**"
  )
  st.divider()

  grid_cols = st.columns(4)
  for idx, celeb_item in enumerate(st.session_state.celebrity_queue):
    with grid_cols[idx % 4]:
      st.image(
          celeb_item["url"],
          use_container_width=True,
          caption=f"{celeb_item['name']} — {celeb_item['desc']}",
      )
      st.markdown(
          f'<span class="celebrity-label">{celeb_item["name"].upper()}</span>',
          unsafe_allow_html=True,
      )
      if st.button(
          "Select Look", key=f"select_celebrity_{idx}", use_container_width=True
      ):
        fetched_img = fetch_image_from_url(celeb_item["url"])
        if fetched_img:
          st.session_state.selected_image = fetched_img
          st.session_state.selected_image_source = f"{celeb_item['name']}'s Look"
          st.toast(f"Selected {celeb_item['name']}'s Outfit!")

# --- TAB 3: TRENDING FASHION ---
with tabs[2]:
  st.markdown(
      '<p class="section-title">What\'s Trending</p>', unsafe_allow_html=True
  )
  st.markdown("**Fresh styles and full outfit looks**")
  st.divider()

  grid_cols = st.columns(4)
  for idx, trend_item in enumerate(st.session_state.trending_queue):
    with grid_cols[idx % 4]:
      st.image(
          trend_item["url"],
          use_container_width=True,
          caption=trend_item["title"],
      )
      st.markdown(
          '<span class="trending-label">TRENDING</span>', unsafe_allow_html=True
      )
      if st.button(
          "Select Look", key=f"select_trending_{idx}", use_container_width=True
      ):
        fetched_img = fetch_image_from_url(trend_item["url"])
        if fetched_img:
          st.session_state.selected_image = fetched_img
          st.session_state.selected_image_source = (
              f"Trending: {trend_item['title']}"
          )
          st.toast("Selected Trending Look!")

# --- COMMON FORM FOR SAVING SELECTED LOOK ---
if st.session_state.selected_image is not None:
  st.divider()
  st.markdown(
      f"## Save Selected Look ({st.session_state.selected_image_source})"
  )

  c_prev, c_meta = st.columns([1, 2])
  with c_prev:
    st.image(st.session_state.selected_image, width=220)

  with c_meta:
    rgbs = extract_palette_from_image(st.session_state.selected_image, k=3)
    st.markdown("**Extracted Color Palette:**")

    p1, p2, p3 = st.columns(3)
    for i, p_col in enumerate([p1, p2, p3]):
      with p_col:
        st.color_picker(
            f"Color {i+1}",
            value=rgb_to_hex(rgbs[i]),
            disabled=True,
            key=f"p_save_{i}",
        )

    item_name = st.text_input(
        "Item Label",
        value=f"{st.session_state.selected_image_source}",
        key="save_item_name",
    )
    cat = st.selectbox(
        "Category",
        ["Tops", "Bottoms", "Outerwear", "Footwear", "Accessories", "Full Outfit"],
        key="save_item_cat",
    )
    ctx = st.selectbox(
        "Context Tag",
        ["Work", "Casual", "Formal", "Vacation", "Loungewear"],
        key="save_item_ctx",
    )

    if st.button(
        "Save to Wardrobe Archive",
        use_container_width=True,
        key="save_to_wardrobe_btn",
    ):
      new_item = {
          "id": len(st.session_state.wardrobe) + 1,
          "name": item_name,
          "category": cat,
          "context": ctx,
          "wears": 0,
          "rating": 5,
          "rgb": rgbs[0].tolist(),
      }
      st.session_state.wardrobe = pd.concat(
          [st.session_state.wardrobe, pd.DataFrame([new_item])],
          ignore_index=True,
      )
      st.success(f"✅ '{item_name}' saved to your wardrobe!")
      st.session_state.selected_image = None
      st.rerun()

# --- TAB 4: AESTHETIC PALETTES ---
with tabs[3]:
  st.markdown(
      '<p class="section-title">Aesthetic Palettes</p>', unsafe_allow_html=True
  )
  st.markdown("**Curated aesthetic color palettes to inspire your style**")
  st.divider()

  for palette_name, colors in st.session_state.aesthetic_palettes.items():
    st.markdown(f"### {palette_name}")
    cols = st.columns(len(colors))
    for idx, col in enumerate(cols):
      with col:
        st.markdown(
            f'<div style="background-color:{colors[idx]}; height:100px;'
            " border-radius:8px; display: flex; align-items: center;"
            " justify-content: center; color: #111;"
            f' font-weight: 700;">{colors[idx]}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("---")

# --- TAB 5: CLOSET VIEW ---
with tabs[4]:
  st.markdown(
      '<p class="section-title">Your Wardrobe</p>', unsafe_allow_html=True
  )
  if st.session_state.wardrobe.empty:
    st.info(
        "Your wardrobe is empty. Select outfit looks from the other tabs to"
        " add them!"
    )
  else:
    cols = st.columns(3)
    for idx, row in st.session_state.wardrobe.iterrows():
      with cols[idx % 3]:
        st.markdown(
            f"""
                <div class="card">
                    <h3>{row['name']}</h3>
                    <p><b>Category:</b> {row['category']}</p>
                    <p><b>Context:</b> {row['context']}</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

# --- TAB 6: PALETTE GAP ENGINE ---
with tabs[5]:
  st.markdown(
      '<p class="section-title">Color Spectrum</p>', unsafe_allow_html=True
  )
  st.divider()

  if not st.session_state.wardrobe.empty:
    st.markdown(
        f"### Total Saved Items: **{len(st.session_state.wardrobe)}**"
    )
    for idx, (_, row) in enumerate(st.session_state.wardrobe.iterrows()):
      col1, col2 = st.columns([1, 4])
      with col1:
        st.markdown(
            f'<div style="background-color:{rgb_to_hex(row["rgb"])};'
            ' height:40px; border-radius:6px;"></div>',
            unsafe_allow_html=True,
        )
      with col2:
        st.write(f"**{row['name']}** — {row['category']} ({row['context']})")
  else:
    st.info("Add items to your wardrobe to visualize your color spectrum!")