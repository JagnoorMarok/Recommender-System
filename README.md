# 🎓 CHPI: A Context-Dependent DEA Based Recommendation System for Learning Strategies

> Implementation of the research paper:  
> **“A Recommendation System for Effective Learning Strategies: An Integrated Approach Using Context-Dependent DEA”**  
> *Expert Systems With Applications, Vol. 211 (2023), 118535*  
> by **Lu-Tao Zhao**, **Dai-Song Wang**, **Feng-Yun Liang**, and **Jian Chen**  

---

## 📘 Overview

This repository implements the **Clustering Hierarchical Progressive Improvement (CHPI)** model — a personalized recommendation system that identifies and enhances **student learning efficiency**.  

The system combines **cluster analysis** and an **improved context-dependent Data Envelopment Analysis (DEA)** approach to recommend individualized learning strategies.  
By comparing inefficient learners with high-performing peers, CHPI provides a clear path for performance improvement.

---

## 🚀 Key Features

- 📊 **Student Data Clustering:**  
  Uses **k-Medoids (PAM)** clustering with **Gower distance** to group students by ontological characteristics (motivation, study habits, test-taking ability).

- ⚙️ **Learning Efficiency Estimation:**  
  Employs **context-dependent DEA** to calculate each student’s learning efficiency from multiple inputs and outputs.

- 🔁 **Hierarchical Stratification:**  
  Divides students into layered performance levels to identify peer benchmarks.

- 🧭 **Progressive Path Recommendation:**  
  Suggests a **stepwise improvement plan** using *attractiveness*, *progress*, and *proximity* metrics.

- 🧩 **Modular and Extensible:**  
  Each component — data preprocessing, clustering, DEA, and recommendation — is independent and reusable.

## 🧩 Implementation Details

| Step | Technique Used | Purpose |
|------|----------------|----------|
| Data Quantification | Cumulative percentage + dispersion analysis | Normalize questionnaire data |
| Clustering | PAM (k-Medoids) with Gower distance | Cluster similar learners |
| DEA Evaluation | Output-oriented context-dependent DEA | Compute efficiency values |
| Path Construction | Weighted path optimization | Recommend stepwise improvement plan |

---


## 🧮 Mathematical Foundation

The **CHPI model** combines **Cluster Analysis** and **Context-Dependent Data Envelopment Analysis (DEA)** to measure and enhance student learning efficiency.  
It uses quantitative optimization techniques to recommend a *step-by-step improvement path* for each learner.

---

### 1. Learning Efficiency (DEA Model)

The classical DEA model measures the **relative learning efficiency** of a student as the ratio of weighted outputs to weighted inputs:

$$
E_{j_0} = \\max \\frac{\\sum_{r=1}^{s} u_r y_{rj_0}}{\\sum_{i=1}^{m} v_i x_{ij_0}}
$$

Subject to the following constraints for each student \\( j \\):

$$
\\frac{\\sum_{r=1}^{s} u_r y_{rj}}{\\sum_{i=1}^{m} v_i x_{ij}} \\le 1, \\quad
u_r \\ge 0, \\quad v_i \\ge 0
$$

Where:  
- \\( E_{j_0} \\): efficiency score of student \\( j_0 \\)  
- \\( x_{ij} \\): input indicators (e.g., study time, motivation)  
- \\( y_{rj} \\): output indicators (e.g., grades, improvement)  
- \\( v_i, u_r \\): variable weights of inputs and outputs  

If \\( E_{j_0} = 1 \\), the student is **efficient**; if less than 1, **inefficient**.

---

### 2. Output-Oriented Context-Dependent DEA

To ensure achievable benchmarks, CHPI uses an **output-oriented** form of DEA with slack variables and an infinitesimal constant \\( \\varepsilon \\):

$$
\\text{maximize } \\theta_{j_0} + \\varepsilon \\left( \\sum_{i=1}^{m}s_i^- + \\sum_{r=1}^{s}s_r^+ \\right)
$$

Subject to:

$$
\\sum_{j=1}^{n} \\lambda_j x_{ij} + s_i^- = x_{i0}, \\quad i = 1,2,\\dots,m
$$

$$
\\sum_{j=1}^{n} \\lambda_j y_{rj} - s_r^+ = \\theta_{j_0} y_{r0}, \\quad r = 1,2,\\dots,s
$$

$$
\\lambda_j, s_i^-, s_r^+ \\ge 0, \\quad \\varepsilon > 0
$$

Here,  
- \\( \\theta_{j_0} \\): output expansion factor (efficiency gain)  
- \\( s_i^-, s_r^+ \\): slack variables for input/output adjustments  
- \\( \\lambda_j \\): peer weights forming the reference combination  

---

### 3. Context-Dependent Stratification

CHPI introduces **hierarchical stratification** by repeatedly applying DEA within clusters.  
After identifying the efficient students \\( E^{(1)} \\) (level 1), they are removed and the process repeats:

$$
S^{(1)} \\rightarrow E^{(1)}, \\quad 
S^{(2)} = S^{(1)} - E^{(1)} \\rightarrow E^{(2)}, \\dots
$$

This generates **layers of efficiency**, ensuring that inefficient students are compared only to peers with similar characteristics.

---

### 4. Obstruction-Based Path Optimization

For each inefficient student, CHPI computes a *progressive improvement path* using three measures:

- **Attractiveness (A)** — how suitable a higher-level student is as a benchmark  
- **Progress (P)** — how much improvement that benchmark represents  
- **Proximity (ω)** — similarity between students in adjacent levels  

The **proximity** between student \\( j_0 \\) and reference \\( j \\) is given by:

$$
\\omega_{j_0 j} = \\sum_{i=1}^{m} \\alpha_i |x_{i j_0} - x_{i j}| - \\sum_{r=1}^{s} \\alpha_r |y_{r j_0} - y_{r j}|
$$

The **degree of obstruction** \\( H_{j_0 j} \\) for moving from \\( j_0 \\) to \\( j \\) is then:

$$
H_{j_0 j} = \\frac{1}{\\omega_{j_0 j}} (A_j + P_j)
$$

To find the most achievable improvement route, the model minimizes total obstruction across layers:

$$
S^*_{j_0} = \\min (H_{j_1}^{(1)} + H_{j_2}^{(2)} + \\dots + H_{j_L}^{(L)})
$$

Where \\( S^*_{j_0} \\) is the **optimal reference path** leading the student from current to highest efficiency level.

---

### 5. Conceptual Flow

1. Quantify raw learning data (e.g., questionnaires → numerical form).  
2. Cluster students using **k-Medoids with Gower distance**.  
3. Perform context-dependent DEA within clusters to compute efficiency.  
4. Identify efficient and inefficient students, stratify them into levels.  
5. Use attractiveness, progress, and proximity to compute obstruction.  
6. Select the path with **minimum obstruction** as the recommended strategy.  

---

**In essence:**  
The CHPI model translates qualitative learning behavior into quantitative measures, constructs personalized benchmarking paths, and recommends strategies that maximize efficiency gains while minimizing learning obstacles.  
It bridges **data analytics**, **optimization**, and **education science** into one intelligent recommendation framework. 🚀


