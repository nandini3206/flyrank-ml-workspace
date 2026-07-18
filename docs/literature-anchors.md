# Literature anchors for the refresh-opportunity capstone

These references were found via the **Hugging Face Papers API** (`paper_search` MCP tool and
`https://huggingface.co/api/papers/search`). Each paper is mapped to a section of this
workspace so you can cite credible prior work without inventing a literature review from scratch.

Use careful language when citing: these papers study *related* ranking problems, not FlyRank's
exact product or data.

---

## 1. Why "which page first?" is a known ranking problem

**Screening prioritisation** — ranking an unordered set so humans review the highest-value items
first — is the closest published framing to the capstone decision.

| Paper | Why it matters here | HF link |
|---|---|---|
| Wang et al., *Neural Rankers for Effective Screening Prioritisation in Medical Systematic Review Literature Search* (2022) | Defines screening prioritisation as ranking documents so assessors start downstream work earlier and can skip low-ranked items. Same decision shape as a refresh queue, different domain. | [hf.co/papers/2212.09017](https://hf.co/papers/2212.09017) |

**Where to use it:** `w01_research_question.ipynb` (section 2 — decision and cost of a wrong call),
capstone paper Introduction.

**Suggested sentence:** "Our task resembles *screening prioritisation* in information retrieval:
given many candidates and limited human attention, the goal is to rank items so reviewers act on
the most important ones first (Wang et al., 2022)."

---

## 2. Why precision@K is the right headline metric

The capstone evaluates with **precision@50** because only the top of the queue gets human action.
That matches how IR literature treats precision-oriented ranking.

| Paper | Why it matters here | HF link |
|---|---|---|
| MacAvaney et al., *Training Curricula for Open Domain Answer Re-Ranking* (2020) | States explicitly that in precision-oriented tasks, ranking many relevant items highly matters more than retrieving every relevant item. Reports P@1 and MRR gains. | [hf.co/papers/2004.14269](https://hf.co/papers/2004.14269) |
| Divekar, *Statistically Reliable LLM-Based Ranking Evaluation via Prediction-Powered Inference* (2026) | Treats **Precision@K** as a first-class evaluation metric and discusses how to estimate it reliably with limited labels. | [hf.co/papers/2606.05308](https://hf.co/papers/2606.05308) |

**Where to use it:** `w05_model.ipynb` (method choice), `w06_validation_audit.ipynb`, capstone
paper Methodology and Results.

**Suggested sentence:** "Because editors act on a short head of the queue, we report
precision@50 rather than overall recall — consistent with precision-oriented ranking work in IR
(MacAvaney et al., 2020)."

---

## 3. Why a tree-based learned ranker on tabular signals is defensible

This workspace trains **logistic regression, decision trees, and random forests** on search and
engagement features — not LLMs on page text. Recent LTR work still blends classical rankers with
hand-crafted signals.

| Paper | Why it matters here | HF link |
|---|---|---|
| Nardini et al., *Blending Learning to Rank and Dense Representations for Efficient and Effective Cascades* (2025) | Uses a **forest of decision trees** as the LTR stage over 253 lexical features, improving nDCG@10 while staying efficient. Parallel to tabular random-forest ranking here. | [hf.co/papers/2510.16393](https://hf.co/papers/2510.16393) |

**Where to use it:** `w05_model.ipynb` (section 1 — method choice), capstone paper
Methodology.

**Suggested sentence:** "Tree-based learning-to-rank on structured relevance signals remains a
practical and well-studied approach, including recent cascaded retrieval systems (Nardini et al.,
2025); we adopt the same family of models on search-console and analytics features."

---

## 4. Content drift as background (optional)

| Paper | Why it matters here | HF link |
|---|---|---|
| Baranchuk et al., *DeDrift: Robust Similarity Search under Content Drift* (2023) | Studies how content distributions shift over time — useful vocabulary for why pages "decay" without claiming you model Google's algorithm. | [hf.co/papers/2308.02752](https://hf.co/papers/2308.02752) |

**Where to use it:** capstone paper Introduction or Limitations — one sentence of context only.

---

## How this file was produced

```text
# HF MCP (authenticated as Nantt)
paper_search(query="screening prioritisation ranking documents human review precision")

# HF Papers REST API (no auth required for public search)
GET https://huggingface.co/api/papers/search?q=learning+to+rank+precision
GET https://huggingface.co/api/papers/2004.14269
```

Re-run either query when drafting ML-11 to refresh links or find newer work.
