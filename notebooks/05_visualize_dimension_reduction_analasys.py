import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""# Dimension Redunction Analysis""")
    return


@app.cell
def _():
    import marimo as mo
    import json
    import polars as pl
    import altair as alt
    import os
    return alt, json, mo, os, pl


@app.cell
def _(mo):
    mo.md(r"""Well use this to decide what is the minimal number of embedding we could use and still keep the quality.""")
    return


@app.cell
def _(mo):
    mo.accordion({
        "How is this app implemented?": """
        - The articles are embedded using
        azure-openai-embedding's embedd∈g-3-lar≥text-embedding-3-large.
        - there is the main full length embedding and smaller one which can scale down
        - We then plot both using umap into a lower dimension and compare the dinamix plot to the true full scale
        - The most point where we are still having relatively high quality while having lowere number of embedding is the goal.
        - that embeddign number is the answer
        """
    })
    return


@app.cell
def _(mo):
    mo.md(r"""## load the texts for comparing""")
    return


@app.cell
def _(json, mo, os):
    data_path = str(mo.notebook_location() / "public" / "test_texts.json")
    # Load cache if it exists
    if os.path.exists(data_path):
        with open(data_path, "rb") as text_file:
            texts = json.load(text_file)
    texts
    return data_path, text_file, texts


@app.cell
def _(mo):
    import pickle 
    import pandas as pd

    mo.md(r"""## load the cashed embedding made with text-embedding-3-large""")
    return pd, pickle


@app.cell
def _(mo, os, pd, pickle, texts):
    CACHE_FILE = str(mo.notebook_location() / "public" / "embeddings_cache.pkl")

    # Load cache if it exists
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
    else:
        cache = {}


    # Retrieve final embeddings
    final_embeddings = [cache[text] for text in texts]

    # Convert to DataFrame
    embeddings_df = pd.DataFrame({
        'text': texts,
        'vector': final_embeddings,
        **{f"dim_{i}": [emb[i] for emb in final_embeddings] for i in range(len(final_embeddings[0]))}
    })

    embeddings_df = embeddings_df[:500]
    embeddings_df
    return CACHE_FILE, cache, embeddings_df, f, final_embeddings


@app.cell
def _(mo, os, pd, pickle, texts):
    CACHE_FILE2 = str(mo.notebook_location() / "public" / "embeddings_cache2.pkl")
    BATCH_SIZE = 1000  # Adjust based on OpenAI's rate limits

    # Load cache if it exists
    if os.path.exists(CACHE_FILE2):
        with open(CACHE_FILE2, "rb") as f2:
            cache2 = pickle.load(f2)
    else:
        cache2 = {}

    # Retrieve final embeddings
    final_embeddings2 = [cache2[text] for text in texts]

    # Convert to DataFrame
    custom_embeddings_df = pd.DataFrame({
        'text': texts,
        'vector': final_embeddings2,
        **{f"dim_{i}": [emb2[i] for emb2 in final_embeddings2] for i in range(len(final_embeddings2[0]))}
    })

    custom_embeddings_df = custom_embeddings_df[:500]
    custom_embeddings_df
    return (
        BATCH_SIZE,
        CACHE_FILE2,
        cache2,
        custom_embeddings_df,
        f2,
        final_embeddings2,
    )


@app.cell
def _(custom_embeddings_df, embeddings_df):
    import numpy as np

    all_embeddings = np.array([row.vector for row in embeddings_df.itertuples()])
    all_embeddings2 = np.array([row.vector for row in custom_embeddings_df.itertuples()])
    print(f"Embeddings shape: {all_embeddings.shape}")
    print(f"Embeddings shape: {all_embeddings2.shape}")
    return all_embeddings, all_embeddings2, np


@app.cell
def _(mo):
    mo.md(
        f"""
        Now to visualize the embedding we can use many thing. for example below we used UMAP
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## clustering using UMAP""")
    return


@app.cell
def _(mo):
    mo.md(r"""### Original""")
    return


@app.cell
def _(all_embeddings, embeddings_df, pd):
    from umap import UMAP
    from scipy.stats import zscore

    # UMAP Projection
    features = all_embeddings[:500]
    print(f"Features shape: {features.shape}")

    umap_2d = UMAP(n_components=20, random_state=42, init="random")
    umap_3d = UMAP(n_components=30, random_state=42, init="random")

    projection_2d = umap_2d.fit_transform(features)
    projection_3d = umap_3d.fit_transform(features)

    # Create DataFrames
    umap_embedding_plot_2d = pd.DataFrame(
        {
            "x": projection_2d[:, 0],
            "y": projection_2d[:, 1],
            "full_text": [row.text for row in embeddings_df.itertuples()]
        }
    )

    umap_embedding_plot_3d = pd.DataFrame(
        {
            "x": projection_3d[:, 0],
            "y": projection_3d[:, 1],
            "z": projection_3d[:, 2],
            "full_text": [row.text for row in embeddings_df.itertuples()]
        }
    )

    # Remove NaN values
    umap_embedding_plot_2d.dropna(inplace=True)
    umap_embedding_plot_3d.dropna(inplace=True)

    # Function to remove outliers using IQR #not used
    def remove_outliers_iqr(df, columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df


    # Limit data to 5000 points
    umap_embedding_plot_2d = umap_embedding_plot_2d.sample(n=min(100, 500), random_state=42)
    umap_embedding_plot_3d = umap_embedding_plot_3d.sample(n=min(100, 500), random_state=42)
    return (
        UMAP,
        features,
        projection_2d,
        projection_3d,
        remove_outliers_iqr,
        umap_2d,
        umap_3d,
        umap_embedding_plot_2d,
        umap_embedding_plot_3d,
        zscore,
    )


@app.cell
def _(mo, umap_embedding_plot_2d):
    import plotly.express as px

    # 2D Scatter Plot
    mo.ui.plotly(
    px.scatter(
        umap_embedding_plot_2d, x="x", y="y",
        title="UMAP Projection (2D)",
        hover_data={'x': ':.2f', 'y': ':.2f', 'full_text': True},
        facet_col_spacing=0.1
    )
    )
    return (px,)


@app.cell
def _(mo, px, umap_embedding_plot_3d):
    # 3D Scatter Plot
    mo.ui.plotly(
     px.scatter_3d(
        umap_embedding_plot_3d, x="x", y="y", z="z",
        title="UMAP Projection (3D)",
        hover_data={'x': ':.2f', 'y': ':.2f', 'z': ':.2f', 'full_text': True}
    )
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### Custom""")
    return


@app.cell
def _(UMAP, all_embeddings2, custom_embeddings_df, pd, projection_3d):
    # UMAP Projection
    features2 = all_embeddings2[:500]
    print(f"Features shape: {features2.shape}")

    umap_2d2 = UMAP(n_components=20, random_state=42, init="random")
    umap_3d2 = UMAP(n_components=30, random_state=42, init="random")

    projection_2d2 = umap_2d2.fit_transform(features2)
    projection_3d2 = umap_3d2.fit_transform(features2)
    custom_embeddings_df = custom_embeddings_df[:500]
    # Create DataFrames
    umap_embedding_plot_2d2 = pd.DataFrame(
        {
            "x": projection_2d2[:, 0],
            "y": projection_2d2[:, 1],
            "full_text": [row.text for row in custom_embeddings_df.itertuples()]
        }
    )

    umap_embedding_plot_3d2 = pd.DataFrame(
        {
            "x": projection_3d[:, 0],
            "y": projection_3d[:, 1],
            "z": projection_3d[:, 2],
            "full_text": [row.text for row in custom_embeddings_df.itertuples()]
        }
    )

    # Remove NaN values
    umap_embedding_plot_2d2.dropna(inplace=True)
    umap_embedding_plot_3d2.dropna(inplace=True)

    # Limit data to 5000 points
    umap_embedding_plot_2d2 = umap_embedding_plot_2d2.sample(n=min(100, 500), random_state=42)
    umap_embedding_plot_3d2 = umap_embedding_plot_3d2.sample(n=min(100, 500), random_state=42)
    return (
        custom_embeddings_df,
        features2,
        projection_2d2,
        projection_3d2,
        umap_2d2,
        umap_3d2,
        umap_embedding_plot_2d2,
        umap_embedding_plot_3d2,
    )


@app.cell
def _(mo, px, umap_embedding_plot_2d2):
    # 2D Scatter Plot
    mo.ui.plotly(px.scatter(
        umap_embedding_plot_2d2, x="x", y="y",
        title="UMAP Projection (2D) Custom",
        hover_data={'x': ':.2f', 'y': ':.2f', 'full_text': True},
        facet_col_spacing=0.1
    )
    )
    return


@app.cell
def _(mo, px, umap_embedding_plot_3d2):
    # 3D Scatter Plot
    mo.ui.plotly(px.scatter_3d(
        umap_embedding_plot_3d2, x="x", y="y", z="z",
        title="UMAP Projection (3D) Custom",
        hover_data={'x': ':.2f', 'y': ':.2f', 'z': ':.2f', 'full_text': True}
    )
                 )
    return


if __name__ == "__main__":
    app.run()
