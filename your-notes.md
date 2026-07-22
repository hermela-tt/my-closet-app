# Project Notes

## my-closet-app

A Streamlit-based fashion curation app that lets users explore inspiration images, save wardrobe items, and view color palettes.

### Current status
- The app entry point is [app.py](app.py).
- Dependencies are listed in [requirements.txt](requirements.txt).
- The project can be run locally with:
  - `streamlit run app.py`

### Notes
- The app includes multiple tabs for Pinterest/web discovery, celebrity inspiration, trending fashion, aesthetic palettes, wardrobe archive, and palette analysis.
- Wardrobe items are stored in Streamlit session state during the current session.
- Image URLs are fetched dynamically for preview and selection.
