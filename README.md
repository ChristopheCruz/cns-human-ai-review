# Cognitive Network Science for Human-AI Systems: A Systematic Review

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PRISMA 2020](https://img.shields.io/badge/Method-PRISMA%202020-green.svg)](https://www.prisma-statement.org/)

This repository contains all materials associated with the systematic review:

> **Cognitive Network Science for Human-AI Systems: A Systematic Review**  
> March 26, 2026  
> Following PRISMA 2020 guidelines

---

## 📁 Repository Structure

```
cns-human-ai-review/
├── paper/
│   ├── main_review.md              # Full paper text (Markdown)
│   └── references.bib              # BibTeX references (corrected)
├── code/
│   ├── build_networks.py           # Co-citation & co-authorship network analysis
│   └── export_figures.py           # SVG → PNG figure export
├── figures/
│   ├── figure1_thematic_clusters.png
│   ├── figure2_prisma_flow.png
│   ├── figure3_cocitation_network.png
│   └── figure4_coauthor_network.png
├── data/
│   └── papers_metadata.json        # Structured metadata for all 47 included papers
├── docs/
│   └── CONTRIBUTING.md
├── requirements.txt
└── README.md
```

---

## 📄 Abstract

Cognitive Network Science (CNS) applies graph-theoretic and complexity science methods to model human cognitive structures, including semantic memory, emotional associations, and conceptual knowledge. As artificial intelligence (AI) systems become deeply embedded in human cognitive environments, a systematic understanding of the intersection between CNS and Human-AI systems is urgently needed.

Following PRISMA 2020 guidelines, we conducted a systematic search across eight major academic databases. After deduplication (~2,800 unique records) and two-stage screening, **47 papers** were included in the final synthesis. Five thematic clusters were identified:

| Cluster | Theme | Key Methods |
|---------|-------|-------------|
| A | Theoretical Foundations of CNS | Graph theory, multiplex networks |
| B | CNS-based probing and auditing of AI/LLM systems | Forma mentis networks, bias detection |
| C | Human-AI collective intelligence | Social network analysis, experiments |
| D | CNS for social and emotional AI | NLP, affective computing, mental health |
| E | CNS in education, creativity, and cognitive augmentation | Semantic networks, ML |

---

## 🔬 Bibliometric Analysis

In addition to the qualitative synthesis, this repository includes a **bibliometric network analysis** of the 47 included papers:

### Co-citation Network
- 34 nodes, 187 edges, density = 0.333
- Louvain community detection → **3 empirical communities**
- Top anchor papers: Abramski et al. (2023), Bullmore & Sporns (2012), Siew et al. (2019)

### Co-authorship Network
- 62 author nodes, 115 edges, density = 0.061
- Top bridge authors by betweenness centrality:

| Author | Papers | Betweenness (β) |
|--------|--------|-----------------|
| Stella | 15 | 0.084 |
| Vitevitch | 4 | 0.020 |
| Kenett | 6 | 0.018 |
| De Deyne | 2 | 0.014 |
| Rossetti | 4 | 0.004 |

---

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.9
```

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/cns-human-ai-review.git
cd cns-human-ai-review
pip install -r requirements.txt
```

### Run the network analysis

```bash
python code/build_networks.py
```

Output figures will be saved to `figures/`.

### Export paper figures

```bash
python code/export_figures.py
```

---

## 📊 Figures

| Figure | Description |
|--------|-------------|
| Figure 1 | Thematic cluster map of CNS and Human-AI research |
| Figure 2 | PRISMA 2020 flow diagram of study selection |
| Figure 3 | Co-citation network of 47 included papers (manual clusters vs Louvain communities) |
| Figure 4 | Co-authorship network with betweenness centrality |

---

## ⚠️ Corrected References

The following references contained errors in the original manuscript and have been corrected in `paper/references.bib`:

| Original citation | Error | Corrected |
|---|---|---|
| Stella et al. (2024) | Wrong journal (*Psychological Review*) | *Psychonomic Bulletin & Review*, 31(5), 1981–2004 |
| Haim et al. (2026) | Wrong journal, DOI and co-authors | *Journal of Computational Social Science*, DOI: 10.1007/s42001-025-00446-z |
| De Duro et al. (2025) | Wrong journal, DOI and incomplete authors | *EPJ Data Science*, 15, 7, DOI: 10.1140/epjds/s13688-025-00600-7 |
| Abramski et al. (2025) | Wrong first author | Haim et al. (2025), arXiv:2502.19529 |

---

## 📝 Citation

If you use this work, please cite:

```bibtex
@article{cns_human_ai_review_2026,
  title   = {Cognitive Network Science for Human-AI Systems: A Systematic Review},
  year    = {2026},
  note    = {Preprint. Following PRISMA 2020 guidelines.}
}
```

---

## 📜 License

- **Paper and figures**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code**: [MIT License](LICENSE)
