import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.colors as mcolors
import igraph as ig
import numpy as np
from collections import defaultdict
import leidenalg as la  # Assicurati che `leidenalg` sia installato

# Funzione per rilevare le comunità utilizzando Leiden
def detect_communities_leiden(g):
    partition = la.find_partition(g, la.RBConfigurationVertexPartition, weights=g.es["weight"])
    return partition

# Funzione per creare il grafico interattivo con i colori dei cluster e il numero del cluster
def create_interactive_graph(mini_array, post_username, use_leiden=False):
    df = pd.DataFrame(mini_array, columns=['comment_id', 'parent_id', 'username', 'body'])
    edge_weights = defaultdict(int)

    for _, row in df.iterrows():
        if pd.notna(row['parent_id']):
            parent_user = df[df['comment_id'] == row['parent_id']]['username']
            if not parent_user.empty:
                edge = (row['username'], parent_user.values[0])
                edge_weights[edge] += 1

    nodes = list(set(df['username']))
    edges = [(k[0], k[1], v) for k, v in edge_weights.items()]

    g = ig.Graph(directed=True)
    g.add_vertices(nodes)
    for edge in edges:
        g.add_edge(edge[0], edge[1], weight=edge[2])

    layout = np.array(g.layout_fruchterman_reingold(weights='weight'))

    post_vertex_index = g.vs.find(name=post_username).index
    post_layout = layout[post_vertex_index]

    layout -= post_layout
    layout[:, 0] = (layout[:, 0] - layout[:, 0].min()) / (layout[:, 0].max() - layout[:, 0].min()) * 2 - 1
    layout[:, 1] = (layout[:, 1] - layout[:, 1].min()) / (layout[:, 1].max() - layout[:, 1].min()) * 2 - 1

    if use_leiden:
        communities = detect_communities_leiden(g)
        cluster_dict = {g.vs[node]['name']: cluster for node, cluster in enumerate(communities.membership)}
    else:
        cluster_dict = None

    fig = go.Figure()

    for edge in g.es:
        source = edge.source
        target = edge.target

        original_post_id = df.iloc[0]['comment_id']
        if target == post_vertex_index:
            comments = df[df['parent_id'] == original_post_id]['body'].values.tolist()
        else:
            comments = df[(df['username'] == g.vs[target]['name']) & (df['parent_id'] == g.vs[source]['name'])]['body'].values.tolist()

        hovertext = "<br>".join(comments) if comments else "Nessun commento"
        line_color = 'Orange' if source == post_vertex_index or target == post_vertex_index else 'Gray'

        fig.add_trace(go.Scatter(
            x=[layout[source][0], layout[target][0]],
            y=[layout[source][1], layout[target][1]],
            mode='lines',
            line=dict(width=edge['weight'] / 2, color=line_color),
            hoverinfo='none',
            customdata=[[g.vs[source]['name'], g.vs[target]['name'], comments]],
            hoverlabel=dict(namelength=0)
        ))

    for vertex, vertex_layout in zip(g.vs, layout):
        if cluster_dict is not None:
            cluster_id = cluster_dict.get(vertex['name'], None)
            color = diz_colori.get(cluster_id, 'CornflowerBlue') if cluster_id is not None else 'CornflowerBlue'
            hover_text = f"Utente: {vertex['name']}<br>Cluster: {cluster_id}" if cluster_id is not None else f"Utente: {vertex['name']}"
        else:
            color = 'CornflowerBlue'
            hover_text = f"Utente: {vertex['name']}"

        fig.add_trace(go.Scatter(
            x=[vertex_layout[0]],
            y=[vertex_layout[1]],
            mode='markers+text',
            marker=dict(
                size=12,
                color=color,
                symbol='circle'
            ),
            text=cluster_id if cluster_dict is not None else "",
            textposition='top center',
            hoverinfo='text',
            hovertext=hover_text
        ))

    fig.update_layout(
        title='Grafo dei Commenti Interattivo',
        showlegend=False,
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig

# Funzione per creare il grafico a barre per l'analisi del sentiment
def create_graph(selected_keywords, title):
    filtered_data = data[data['sentiment_label'].isin(['positive', 'negative']) & data[selected_keywords].any(axis=1)]
    counts = filtered_data.groupby('sentiment_label')[selected_keywords].sum().reset_index()
    counts_long = counts.melt(id_vars='sentiment_label', var_name='keyword', value_name='count')
    counts_long_sorted = counts_long.sort_values(by='count', ascending=False)

    fig = go.Figure()
    for sentiment in ['positive', 'negative']:
        fig.add_trace(go.Bar(
            x=counts_long_sorted[counts_long_sorted['sentiment_label'] == sentiment]['keyword'],
            y=counts_long_sorted[counts_long_sorted['sentiment_label'] == sentiment]['count'],
            name=sentiment,
            marker_color=custom_palette[sentiment] if sentiment in custom_palette else 'grey'
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Keyword',
        yaxis_title='Count',
        yaxis_type='log',
        barmode='group',
        height=600  # Aumenta l'altezza del grafico
    )
    return fig

# Carica il DataFrame per l'analisi del sentiment
data = pd.read_csv('data_sentiment.csv')

# Trasforma la colonna 'body' in minuscolo
data['body'] = data['body'].str.lower()

# Parole chiave da cercare
keywords = [
    'rockstar', 'bioware', 'capcom', 'treyarch', 'microsoft', 'zenimax', 'psyonix', 'rare', 'riot', 'sega', 'nintendo', 'atari',
    'team', 'ubisoft', 'activision', 'steam', 'epic', 'fromsoftware', 'bungie', 'gears', 'ubisoft', 'valve', 'zynga',
    'ea', 'sony', 'tencent', 'namco', 'bethesda', 'naughty dog', 'rockstar', 'blizzard', 'cd projekt', 'namco'
]

# Crea nuove colonne per le parole chiave
for keyword in keywords:
    data[keyword] = data['body'].str.contains(keyword, case=False, na=False)

# Conversione dei colori RGB in formato esadecimale
custom_palette = {
    'positive': mcolors.to_hex(sns.color_palette('coolwarm', 3)[0]),  # Blu per 'positive' (cool)
    'negative': mcolors.to_hex(sns.color_palette('coolwarm', 3)[2])   # Arancione per 'negative' (warm)
}

gaming_titles = [
    "wow", "persona", "dragon age origins", "burning crusade", "advanced warfare", "far cry", "dead space 3", "apex", "re4",
    "fifa ultimate team", "dota 2", "mechassault", "fifa", "star wars galaxies", "halo",
    "crimson skies", "gta online", "path of exile", "farmville", "gog", "everquest", "team fortress 2", "silksong", "deus ex",
    "among us", "tw3", "dmc", "palworld", "minecraft", "tf2", "osrs", "gtav", "anthem", "alien isolation", "ultimate online",
    "maplestory", "terraria", "pubg", "ruined king", "sc2", "bg3", "warzone", "dq", "everquest", "gta", "botw",
    "factorio", "fortnite", "lol", "fire emblem"
]

# Aggiorna le colonne del DataFrame per includere le nuove parole chiave
for title in gaming_titles:
    data[title] = data['body'].str.contains(title, case=False, na=False)

# Carica i dati per i grafici interattivi
df1 = data[:101]
mini_array1 = df1[['comment_id', 'parent_id', 'username', 'body']].values

df2 = data[3038:3179]
df2 = df2.drop([3158, 3157])
mini_array2 = df2[['comment_id', 'parent_id', 'username', 'body']].values

# Dizionario dei colori per i cluster
diz_colori = {0: 'DarkOrchid', 1: 'Aquamarine', 2: 'IndianRed', 3: 'CornflowerBlue', 4: 'Pink',
              5: 'DarkSlateGrey', 6: 'Khaki', 7: 'Gainsboro', 8: 'Olive', 9: 'Orange', 10: 'salmon'}

# Titolo dell'applicazione
st.title('Dashboard di Sentiment Analysis e Grafici Interattivi')

# Sezione per la prima checklist
st.sidebar.header('Select Companies')
select_all_companies = st.sidebar.button('Select All Companies')
clear_all_companies = st.sidebar.button('Clear All Companies')
selected_companies = st.sidebar.multiselect('Companies', keywords, default=keywords if select_all_companies else [])

# Sezione per la seconda checklist
st.sidebar.header('Select Gaming Titles')
select_all_titles = st.sidebar.button('Select All Titles')
clear_all_titles = st.sidebar.button('Clear All Titles')
selected_titles = st.sidebar.multiselect('Gaming Titles', gaming_titles, default=gaming_titles if select_all_titles else [])

# Mostra i grafici in contenitori verticali
st.write('**Primo post:**')
st.plotly_chart(create_interactive_graph(mini_array1, df1.iloc[0]['username']))

st.write('**Secondo post:**')
st.plotly_chart(create_interactive_graph(mini_array2, df2.iloc[0]['username'], use_leiden=True))

if selected_companies:
    st.write('**Grafico di Sentiment per Aziende:**')
    st.plotly_chart(create_graph(selected_companies, 'Distribuzione delle Aziende per valori di sentiment positivi e negativi'))

if selected_titles:
    st.write('**Grafico di Sentiment per Titoli di Giochi:**')
    st.plotly_chart(create_graph(selected_titles, 'Distribuzione dei titoli dei giochi per valori di sentiment positivi e negativi'))
