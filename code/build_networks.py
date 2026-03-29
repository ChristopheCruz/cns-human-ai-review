import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import community as community_louvain
import numpy as np
from collections import defaultdict
from itertools import combinations

# ─────────────────────────────────────────────
# 1.  BIBLIOGRAPHIC DATA
# ─────────────────────────────────────────────

# Short citation keys  →  (First Author Last, Year, Cluster label A–E)
papers = {
    "Bullmore2012":   ("Bullmore",   2012, "A"),
    "Cole2015":       ("Cole",       2015, "A"),
    "Siew2019":       ("Siew",       2019, "A"),
    "Beckage2020":    ("Beckage",    2020, "A"),
    "Stella2026":     ("Stella",     2026, "A"),
    "StellaVitevitch2019":  ("Stella",     2019, "A"),
    "Stella2024":     ("Stella",     2024, "A"),
    "Citraro2023":    ("Citraro",    2023, "A"),
    "Vitevitch2023":  ("Vitevitch",  2023, "A"),
    "Vitevitch2024":  ("Vitevitch",  2024, "A"),
    "Abramski2023":   ("Abramski",   2023, "B"),
    "DeDuro2025":     ("De Duro",    2025, "B"),
    "Haim2026":       ("Haim",       2026, "B"),
    "Abramski2025":   ("Abramski",   2025, "B"),
    "Semeraro2021":   ("Semeraro",   2021, "B"),
    "Kenett2023":     ("Kenett",     2023, "B"),
    "Almaatouq2022":  ("Almaatouq", 2022, "C"),
    "Rahwan2019":     ("Rahwan",     2019, "C"),
    "Colleoni2024":   ("Colleoni",   2024, "C"),
    "Stella2020":     ("Stella",     2020, "D"),
    "Fatima2021":     ("Fatima",     2021, "D"),
    "Teixeira2021":   ("Teixeira",   2021, "D"),
    "Abramski2022":   ("Abramski",   2022, "D"),
    "Stella2022":     ("Stella",     2022, "D"),
    "Semeraro2025":   ("Semeraro",   2025, "D"),
    "Dyer2020":       ("Dyer",       2020, "D"),
    "BorgeHolthoefer2010":     ("Borge-H.",   2010, "D"),
    "Liu2024":        ("Liu",        2024, "D"),
    "Giabbanelli2024":  ("Giabbanelli",2024, "D"),
    "Denervaud2021":  ("Denervaud",  2021, "E"),
    "Luchini2024":    ("Luchini",    2024, "E"),
    "Kenett2024":    ("Kenett",     2024, "E"),
    "Chen2023":       ("Chen",       2023, "E"),
    "StellaFerrara2022":    ("Stella",     2022, "A"),
    "Page2021":       ("Page",       2021, "A"),
    "Siew2019b":      ("Siew",       2019, "A"),
}

# ─────────────────────────────────────────────
# 2.  CO-CITATION EDGES
#     Papers cited together inside the SAME section of the review
# ─────────────────────────────────────────────

sections = {
    "Background_CNS":    ["Siew2019","Siew2019b","Beckage2020","Vitevitch2023","Vitevitch2024",
                          "Citraro2023","Stella2026","StellaVitevitch2019","Stella2024",
                          "Bullmore2012","Cole2015","Semeraro2021","Abramski2023",
                          "StellaFerrara2022"],
    "Methods":           ["Page2021","Siew2019","Stella2026"],
    "Background_AI":     ["Rahwan2019","Almaatouq2022","Abramski2023"],
    "Cluster_A":         ["Bullmore2012","Cole2015","Siew2019","Siew2019b","Beckage2020",
                          "Stella2026","StellaVitevitch2019","Stella2024","Citraro2023",
                          "Vitevitch2023","Vitevitch2024","Page2021"],
    "Cluster_B":         ["Abramski2023","DeDuro2025","Haim2026","Abramski2025",
                          "Semeraro2021","Kenett2023"],
    "Cluster_C":         ["Almaatouq2022","Rahwan2019","Colleoni2024"],
    "Cluster_D":         ["Stella2020","Fatima2021","Teixeira2021","Abramski2022",
                          "Stella2022","Semeraro2025","Dyer2020","BorgeHolthoefer2010",
                          "Liu2024","Giabbanelli2024"],
    "Cluster_E":         ["Denervaud2021","Luchini2024","Kenett2024","Chen2023",
                          "Semeraro2021"],
    "Discussion":        ["Abramski2023","DeDuro2025","Rahwan2019","Colleoni2024",
                          "Fatima2021","Teixeira2021","Stella2020","Semeraro2025",
                          "Denervaud2021","Kenett2024"],
}

co_cite_weight = defaultdict(int)
for sec, plist in sections.items():
    for a, b in combinations(plist, 2):
        key = tuple(sorted([a, b]))
        co_cite_weight[key] += 1

# ─────────────────────────────────────────────
# 3.  BUILD CO-CITATION GRAPH
# ─────────────────────────────────────────────

G_cc = nx.Graph()
for pid, (author, year, cluster) in papers.items():
    G_cc.add_node(pid, author=author, year=year, cluster=cluster,
                  label=f"{author}\n{year}")

for (a, b), w in co_cite_weight.items():
    if a in G_cc and b in G_cc:
        G_cc.add_edge(a, b, weight=w)

# Louvain community detection
partition = community_louvain.best_partition(G_cc, weight='weight', random_state=42)

# ─────────────────────────────────────────────
# 4.  COLOUR MAPS
# ─────────────────────────────────────────────

manual_cluster_colors = {
    "A": "#1D9E75",   # teal
    "B": "#D85A30",   # coral
    "C": "#BA7517",   # amber
    "D": "#D4537E",   # pink
    "E": "#378ADD",   # blue
}

louvain_palette = ["#534AB7","#0F6E56","#993C1D","#854F0B","#993556",
                   "#185FA5","#639922","#A32D2D","#5F5E5A"]

# ─────────────────────────────────────────────
# 5.  PLOT CO-CITATION NETWORK
# ─────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor="none")
fig.suptitle("Co-citation Network of 36 Included Papers",
             fontsize=16, fontweight="bold", y=1.01)

pos = nx.spring_layout(G_cc, weight='weight', seed=42, k=2.2)

node_colors_manual = [manual_cluster_colors[papers[n][2]] for n in G_cc.nodes()]
node_colors_louvain = [louvain_palette[partition[n] % len(louvain_palette)]
                       for n in G_cc.nodes()]

edge_widths = [G_cc[u][v]['weight'] * 0.8 for u, v in G_cc.edges()]
node_sizes  = [300 + G_cc.degree(n, weight='weight') * 30 for n in G_cc.nodes()]
labels      = {n: papers[n][0]+"\n"+str(papers[n][1]) for n in G_cc.nodes()}

for ax, title, colors, legend_info in [
    (axes[0], "Coloured by manual thematic cluster",
     node_colors_manual,
     [("A — Theoretical foundations", "#1D9E75"),
      ("B — LLM / AI auditing",        "#D85A30"),
      ("C — Collective intelligence",  "#BA7517"),
      ("D — Social & emotional AI",    "#D4537E"),
      ("E — Education & creativity",   "#378ADD")]),
    (axes[1], "Coloured by Louvain community",
     node_colors_louvain, None),
]:
    nx.draw_networkx_edges(G_cc, pos, ax=ax, alpha=0.25, width=edge_widths,
                           edge_color="#888780")
    nx.draw_networkx_nodes(G_cc, pos, ax=ax, node_color=colors,
                           node_size=node_sizes, alpha=0.92)
    nx.draw_networkx_labels(G_cc, pos, labels=labels, ax=ax,
                            font_size=6.5, font_color="white", font_weight="bold")
    ax.set_title(title, fontsize=12, pad=10)
    ax.axis("off")
    ax.set_facecolor("none")

    if legend_info:
        patches = [mpatches.Patch(color=c, label=l) for l, c in legend_info]
        ax.legend(handles=patches, loc="lower left", fontsize=8.5,
                  framealpha=0.9, edgecolor="#D3D1C7")
    else:
        n_comm = max(partition.values()) + 1
        patches = [mpatches.Patch(color=louvain_palette[i % len(louvain_palette)],
                                  label=f"Community {i+1}")
                   for i in range(n_comm)]
        ax.legend(handles=patches, loc="lower left", fontsize=8.5,
                  framealpha=0.9, edgecolor="#D3D1C7")

plt.tight_layout()
plt.savefig("figures/figure3_cocitation_network.png",
            dpi=200, bbox_inches="tight", facecolor="none", transparent=True)
plt.close()
print("Co-citation network saved.")

# ─────────────────────────────────────────────
# 6.  CO-AUTHOR DATA
# ─────────────────────────────────────────────

authorship = {
    "Abramski2023":  ["Abramski","Citraro","Lombardi","Rossetti","Stella"],
    "Abramski2022":  ["Abramski","Citraro","Lombardi","Rossetti","Stella"],
    "Abramski2025":  ["Abramski","Citraro","Stella"],
    "Almaatouq2022": ["Almaatouq","Alsobay","Yin","Watts"],
    "Beckage2020":   ["Beckage","Siew"],
    "BorgeHolthoefer2010":    ["Borge-Holthoefer","Arenas"],
    "Bullmore2012":  ["Bullmore","Sporns"],
    "Chen2023":      ["Chen"],
    "Citraro2023":   ["Citraro","De Deyne","Rossetti","Stella"],
    "Cole2015":      ["Cole","Bassett"],
    "Colleoni2024":  ["Colleoni","Arvidsson","Strati"],
    "DeDuro2025":    ["De Duro","Franchino","Improta","Veltri","Stella"],
    "Denervaud2021": ["Denervaud","Christensen","Kenett","Beaty"],
    "Dyer2020":      ["Dyer","Kolic"],
    "Fatima2021":    ["Fatima","Li","Hills","Stella"],
    "Giabbanelli2024": ["Giabbanelli","Knox","Gray"],
    "Haim2026":      ["Haim","Natan","Kenett"],
    "Kenett2024":   ["Kenett","Beaty"],
    "Kenett2023":    ["Kenett"],
    "Liu2024":       ["Liu","Zhang","Chen"],
    "Luchini2024":   ["Luchini","Wang","Kenett","Beaty"],
    "Rahwan2019":    ["Rahwan","Cebrian","Obradovich","Bongard","Bonnefon",
                      "Breazeal","Christakis","Lazer","Pentland"],
    "Semeraro2021":  ["Semeraro","Vilella","Stella"],
    "Semeraro2025":  ["Semeraro","Vilella","Stella"],
    "Siew2019":      ["Siew","Wulff","Beckage","Kenett"],
    "Stella2020":    ["Stella"],
    "Stella2022":    ["Stella"],
    "StellaFerrara2022":   ["Stella","Ferrara","De Domenico"],
    "Stella2024":    ["Stella","Citraro","Rossetti","Marinazzo","Kenett","Vitevitch"],
    "Stella2026":    ["Stella"],
    "StellaVitevitch2019": ["Stella","Vitevitch"],
    "Teixeira2021":  ["Teixeira","Talaga","Swanson","Stella"],
    "Vitevitch2023": ["Vitevitch"],
    "Vitevitch2024": ["Vitevitch","Martinez","England"],
    "Haim2026":      ["Haim","Passaro","Stella"],
    "Page2021":      ["Page","McKenzie","Bossuyt"],
    "Siew2019b":     ["Siew"],
}

# ─────────────────────────────────────────────
# 7.  BUILD CO-AUTHOR GRAPH
# ─────────────────────────────────────────────

G_ca = nx.Graph()
for paper, authors in authorship.items():
    cluster = papers.get(paper, (None, None, "A"))[2]
    for a in authors:
        if not G_ca.has_node(a):
            G_ca.add_node(a, papers=[], clusters=set())
        G_ca.nodes[a]['papers'].append(paper)
        G_ca.nodes[a]['clusters'].add(cluster)
    for a1, a2 in combinations(authors, 2):
        if G_ca.has_edge(a1, a2):
            G_ca[a1][a2]['weight'] += 1
        else:
            G_ca.add_edge(a1, a2, weight=1)

# Node size = number of papers
paper_counts = {n: len(G_ca.nodes[n]['papers']) for n in G_ca.nodes()}

# Main cluster per author (most frequent)
def main_cluster(node):
    clusters = G_ca.nodes[node]['clusters']
    freq = defaultdict(int)
    for p in G_ca.nodes[node]['papers']:
        c = papers.get(p, (None,None,"A"))[2]
        freq[c] += 1
    return max(freq, key=freq.get)

node_colors_ca = [manual_cluster_colors[main_cluster(n)] for n in G_ca.nodes()]

# Betweenness centrality for bridge detection
betweenness = nx.betweenness_centrality(G_ca, weight='weight', normalized=True)

# ─────────────────────────────────────────────
# 8.  PLOT CO-AUTHOR NETWORK
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 11), facecolor="none")
ax.set_facecolor("none")
ax.set_title("Co-authorship Network\nNode size = paper count  |  "
             "Border thickness = betweenness centrality  |  Colour = main cluster",
             fontsize=12, pad=12)

pos_ca = nx.spring_layout(G_ca, weight='weight', seed=7, k=2.8)

edge_w_ca = [G_ca[u][v]['weight'] * 1.2 for u, v in G_ca.edges()]
node_sz_ca = [400 + paper_counts[n] * 280 for n in G_ca.nodes()]
linewidths  = [1 + betweenness[n] * 60 for n in G_ca.nodes()]

nx.draw_networkx_edges(G_ca, pos_ca, ax=ax, alpha=0.2, width=edge_w_ca,
                       edge_color="#888780")
nx.draw_networkx_nodes(G_ca, pos_ca, ax=ax,
                       node_color=node_colors_ca,
                       node_size=node_sz_ca,
                       linewidths=linewidths,
                       edgecolors="#2C2C2A",
                       alpha=0.90)
nx.draw_networkx_labels(G_ca, pos_ca, ax=ax,
                        font_size=7, font_color="white", font_weight="bold")

# Annotate top-5 by betweenness
top5 = sorted(betweenness, key=betweenness.get, reverse=True)[:5]
for n in top5:
    x, y = pos_ca[n]
    ax.annotate(f"β={betweenness[n]:.2f}",
                xy=(x, y), xytext=(x + 0.07, y + 0.07),
                fontsize=6.5, color="#3C3489",
                arrowprops=dict(arrowstyle="-", color="#534AB7", lw=0.6))

# Legend: clusters
patches = [mpatches.Patch(color=c, label=l) for l, c in [
    ("A — Theoretical foundations", "#1D9E75"),
    ("B — LLM / AI auditing",        "#D85A30"),
    ("C — Collective intelligence",  "#BA7517"),
    ("D — Social & emotional AI",    "#D4537E"),
    ("E — Education & creativity",   "#378ADD"),
]]
ax.legend(handles=patches, loc="lower left", fontsize=9,
          framealpha=0.9, edgecolor="#D3D1C7", title="Main cluster", title_fontsize=9)

ax.axis("off")
plt.tight_layout()
plt.savefig("figures/figure4_coauthor_network.png",
            dpi=200, bbox_inches="tight", facecolor="none", transparent=True)
plt.close()
print("Co-author network saved.")

# ─────────────────────────────────────────────
# 9.  PRINT KEY STATS
# ─────────────────────────────────────────────

print("\n── CO-CITATION NETWORK ──")
print(f"  Nodes : {G_cc.number_of_nodes()}")
print(f"  Edges : {G_cc.number_of_edges()}")
print(f"  Density : {nx.density(G_cc):.3f}")
top_cc = sorted(G_cc.degree(weight='weight'), key=lambda x: x[1], reverse=True)[:5]
print("  Top-5 by weighted degree:")
for n, d in top_cc:
    print(f"    {papers[n][0]} {papers[n][1]} (cluster {papers[n][2]}) — degree {d}")
n_louvain = max(partition.values()) + 1
print(f"  Louvain communities detected: {n_louvain}")

print("\n── CO-AUTHORSHIP NETWORK ──")
print(f"  Nodes (authors) : {G_ca.number_of_nodes()}")
print(f"  Edges           : {G_ca.number_of_edges()}")
print(f"  Density         : {nx.density(G_ca):.3f}")
top_ca = sorted(paper_counts.items(), key=lambda x: x[1], reverse=True)[:5]
print("  Top-5 authors by paper count:")
for a, c in top_ca:
    print(f"    {a} — {c} papers  (β={betweenness[a]:.3f})")
top_bridge = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
print("  Top-5 bridge authors (betweenness centrality):")
for a, b in top_bridge:
    print(f"    {a} — β={b:.3f}")
