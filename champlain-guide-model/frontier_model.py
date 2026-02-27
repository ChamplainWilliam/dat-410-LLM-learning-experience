"""
ChamplainGuide Frontier Model — Course Recommendation via Embeddings
=====================================================================
CSI-480 | Part 5: Using a Frontier Model to Level Up

This script demonstrates how embedding-based representations improve
ChamplainGuide by creating semantic vectors of course descriptions
and matching them to student queries using cosine similarity.

Approach: TF-IDF Embeddings with SVD dimensionality reduction
- TF-IDF converts course descriptions into weighted term-frequency vectors
- SVD reduces these to dense, low-dimensional embeddings (like word2vec)
- Cosine similarity finds semantically related courses

BEFORE (keyword matching): "I want to learn hacking" → 0 matches
AFTER  (semantic embeddings): "I want to learn hacking" → SEC-250: Ethical Hacking

Learning representation mapping:
  Tokens     → course attributes (code, credits, prereqs, semester)
  Words      → complete course descriptions (attributes assembled)
  Embeddings → dense vectors capturing semantic relationships between courses
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE


# ============================================================
# COURSE KNOWLEDGE BASE
# Each course is a "word" in our learning space — a meaningful
# unit composed of multiple "tokens" (attributes).
# ============================================================
COURSES = [
    {
        "code": "CSI-160", "name": "Introduction to Programming", "credits": 3,
        "semester": "Fall", "prereqs": [], "category": "CS Core",
        "description": "Fundamentals of programming using Python. Variables, control structures, functions, and basic data types. First course for computer science majors with no prior coding experience."
    },
    {
        "code": "CSI-220", "name": "Object-Oriented Programming", "credits": 3,
        "semester": "Spring", "prereqs": ["CSI-160"], "category": "CS Core",
        "description": "Object-oriented design and programming with Java. Classes, objects, inheritance, polymorphism, interfaces, encapsulation, and software design patterns."
    },
    {
        "code": "CSI-240", "name": "Data Structures & Algorithms", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-220"], "category": "CS Core",
        "description": "Fundamental data structures including arrays, linked lists, stacks, queues, trees, graphs, hash tables. Algorithm analysis, sorting, searching, and Big-O computational complexity."
    },
    {
        "code": "CSI-260", "name": "Computer Architecture", "credits": 3,
        "semester": "Spring", "prereqs": ["CSI-160"], "category": "CS Core",
        "description": "Computer organization and architecture. CPU design, memory hierarchy, cache, instruction sets, assembly language programming, and hardware-software interface."
    },
    {
        "code": "CSI-280", "name": "Software Engineering", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-240"], "category": "CS Core",
        "description": "Software development life cycle, requirements engineering, system design, testing methodologies, project management, version control, agile scrum and waterfall methodologies."
    },
    {
        "code": "CSI-300", "name": "Database Management Systems", "credits": 3,
        "semester": "Spring", "prereqs": ["CSI-240"], "category": "CS Core",
        "description": "Relational database design, SQL queries, normalization, entity-relationship modeling, transactions, indexing, query optimization. Introduction to NoSQL and document databases."
    },
    {
        "code": "CSI-340", "name": "Operating Systems", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-260", "CSI-240"], "category": "CS Core",
        "description": "Process management, threading, memory management, virtual memory, file systems, CPU scheduling, concurrency, deadlocks, synchronization in Linux and modern operating systems."
    },
    {
        "code": "CSI-380", "name": "Web Application Development", "credits": 3,
        "semester": "Spring", "prereqs": ["CSI-280"], "category": "CS Core",
        "description": "Full-stack web development with React, Node.js, and modern frameworks. Frontend HTML CSS JavaScript, REST APIs, backend servers, database integration, authentication, and cloud deployment."
    },
    {
        "code": "CSI-400", "name": "Artificial Intelligence", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-240"], "category": "CS Core",
        "description": "Introduction to artificial intelligence including search algorithms, knowledge representation, machine learning fundamentals, neural networks, and natural language processing."
    },
    {
        "code": "CSI-320", "name": "Machine Learning", "credits": 3,
        "semester": "Spring", "prereqs": ["CSI-400"], "category": "CS Elective",
        "description": "Supervised and unsupervised learning, regression, classification, decision trees, clustering, neural networks, deep learning, model evaluation, training, and prediction techniques."
    },
    {
        "code": "CSI-350", "name": "Computer Networks", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-260"], "category": "CS Elective",
        "description": "Network protocols, TCP/IP stack, OSI model, routing, switching, network security, firewalls, VPN, wireless networks, and distributed systems communication."
    },
    {
        "code": "CSI-370", "name": "Mobile App Development", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-280"], "category": "CS Elective",
        "description": "Mobile application development for iOS and Android using Swift and Kotlin. User interface design, gestures, sensors, data persistence, GPS location, and app store deployment."
    },
    {
        "code": "CSI-420", "name": "Natural Language Processing", "credits": 3,
        "semester": "Fall", "prereqs": ["CSI-400"], "category": "CS Elective",
        "description": "Text processing, tokenization, word embeddings, transformer models, sentiment analysis, text classification, language generation, chatbots, and large language models."
    },
    {
        "code": "CSI-430", "name": "Cybersecurity Fundamentals", "credits": 3,
        "semester": "Fall/Spring", "prereqs": ["CSI-260"], "category": "CS Elective",
        "description": "Security principles, threat modeling, cryptography, encryption, access control, vulnerability assessment, penetration testing basics, and security best practices."
    },
    {
        "code": "SEC-150", "name": "Security Fundamentals", "credits": 3,
        "semester": "Fall", "prereqs": [], "category": "Cybersecurity Core",
        "description": "Introduction to information security concepts. CIA triad confidentiality integrity availability, risk assessment, security policies, compliance frameworks, and security awareness training."
    },
    {
        "code": "SEC-250", "name": "Ethical Hacking", "credits": 3,
        "semester": "Fall", "prereqs": ["SEC-210"], "category": "Cybersecurity Core",
        "description": "Penetration testing methodology, vulnerability scanning, network exploitation techniques, web application attacks, social engineering, password cracking, and responsible disclosure."
    },
    {
        "code": "SEC-300", "name": "Digital Forensics", "credits": 3,
        "semester": "Spring", "prereqs": ["SEC-250"], "category": "Cybersecurity Core",
        "description": "Digital evidence collection and preservation, disk forensics, memory analysis, network forensics, malware analysis, chain of custody, and forensic reporting for legal proceedings."
    },
    {
        "code": "SEC-400", "name": "Advanced Penetration Testing", "credits": 3,
        "semester": "Spring", "prereqs": ["SEC-250"], "category": "Cybersecurity Core",
        "description": "Advanced exploitation techniques, privilege escalation, lateral movement, Active Directory attacks, red team operations, custom exploit development, and evasion techniques."
    },
    {
        "code": "MAT-210", "name": "Calculus I", "credits": 3,
        "semester": "Fall/Spring", "prereqs": [], "category": "Math",
        "description": "Limits, derivatives, integrals, fundamental theorem of calculus, applications of differentiation and integration to real-world mathematical problems."
    },
    {
        "code": "MAT-230", "name": "Discrete Mathematics", "credits": 3,
        "semester": "Fall", "prereqs": ["MAT-210"], "category": "Math",
        "description": "Propositional logic, mathematical proofs, sets, relations, functions, counting combinatorics, graph theory, trees, and mathematical foundations for computer science algorithms."
    },
    {
        "code": "MAT-310", "name": "Linear Algebra", "credits": 3,
        "semester": "Spring", "prereqs": ["MAT-220"], "category": "Math",
        "description": "Vectors, matrices, linear transformations, determinants, eigenvalues, eigenvectors, vector spaces, orthogonality, and applications to data science and machine learning."
    },
    {
        "code": "MAT-330", "name": "Probability & Statistics", "credits": 3,
        "semester": "Fall/Spring", "prereqs": ["MAT-210"], "category": "Math",
        "description": "Probability theory, random variables, probability distributions, Bayes theorem, hypothesis testing, confidence intervals, regression analysis, and statistical inference for data analysis."
    },
]


# ============================================================
# EMBEDDING MODEL
# ============================================================

class CourseEmbeddingModel:
    """
    A course recommendation model that uses TF-IDF + SVD to create
    dense semantic embeddings of course descriptions.
    
    This is our 'frontier model' — it converts raw text into a 
    learned representation space where similar courses cluster together.
    """

    def __init__(self, n_components=50):
        self.n_components = n_components
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words="english",
            ngram_range=(1, 2),  # unigrams and bigrams
            sublinear_tf=True,   # apply log normalization
        )
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)
        self.course_embeddings = None
        self.tfidf_matrix = None

    def fit(self, course_texts):
        """Train the model on course descriptions."""
        self.tfidf_matrix = self.vectorizer.fit_transform(course_texts)
        self.course_embeddings = self.svd.fit_transform(self.tfidf_matrix)
        return self

    def embed_query(self, query):
        """Embed a student query into the same vector space."""
        tfidf = self.vectorizer.transform([query])
        return self.svd.transform(tfidf)

    def recommend(self, query, courses, top_k=5):
        """Find the top-k most similar courses to a query."""
        query_emb = self.embed_query(query)
        similarities = cosine_similarity(query_emb, self.course_embeddings)[0]
        ranked = sorted(
            zip(courses, similarities), key=lambda x: x[1], reverse=True
        )
        return ranked[:top_k]

    def get_vocabulary_size(self):
        return len(self.vectorizer.vocabulary_)

    def get_top_features(self, n=20):
        """Get the most important learned features."""
        feature_names = self.vectorizer.get_feature_names_out()
        return feature_names[:n]


# ============================================================
# BASELINE: KEYWORD MATCHING (the "before")
# ============================================================

def keyword_search(query, courses):
    """Simple keyword matching — counts word overlaps."""
    query_words = set(query.lower().split())
    scores = []
    for c in courses:
        text = f"{c['code']} {c['name']} {c['description']}".lower()
        matches = sum(1 for w in query_words if w in text)
        scores.append(matches)
    ranked = sorted(zip(courses, scores), key=lambda x: x[1], reverse=True)
    return ranked[:5]


# ============================================================
# VISUALIZATIONS
# ============================================================

def create_comparison_chart(query, kw_results, emb_results, output_path):
    """Before/after comparison chart for a single query."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))
    fig.patch.set_facecolor("#0f1117")

    for ax in [ax1, ax2]:
        ax.set_facecolor("#1a1d27")
        ax.tick_params(colors="#8892a8", labelsize=8)
        for spine in ax.spines.values():
            spine.set_color("#2a2e3d")

    # Before
    codes1 = [f"{c['code']}" for c, _ in kw_results][::-1]
    scores1 = [s for _, s in kw_results][::-1]
    ax1.barh(codes1, scores1, color="#4a5568", edgecolor="#2a2e3d", height=0.55)
    ax1.set_title("BEFORE: Keyword Matching", color="#ef4444", fontsize=12, fontweight="bold", pad=10)
    ax1.set_xlabel("Word Matches", color="#8892a8", fontsize=9)
    ax1.set_xlim(0, max(max(scores1), 1) + 1)
    for i, (code, score) in enumerate(zip(codes1, scores1)):
        ax1.text(score + 0.08, i, str(score), va="center", color="#8892a8", fontsize=9)

    # After
    codes2 = [f"{c['code']}" for c, _ in emb_results][::-1]
    scores2 = [round(s, 3) for _, s in emb_results][::-1]
    colors = ["#6c9bff" if s > 0.35 else "#38bdf8" if s > 0.2 else "#4a5568" for s in scores2]
    ax2.barh(codes2, scores2, color=colors, edgecolor="#2a2e3d", height=0.55)
    ax2.set_title("AFTER: Embedding Similarity", color="#4ade80", fontsize=12, fontweight="bold", pad=10)
    ax2.set_xlabel("Cosine Similarity", color="#8892a8", fontsize=9)
    ax2.set_xlim(0, 1.0)
    for i, (code, score) in enumerate(zip(codes2, scores2)):
        ax2.text(score + 0.01, i, f"{score:.3f}", va="center", color="#8892a8", fontsize=9)

    fig.suptitle(f'Student Query: "{query}"', color="#6c9bff", fontsize=11, y=0.02, fontweight="bold")
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#0f1117")
    plt.close()


def create_embedding_space(courses, embeddings, output_path):
    """t-SNE visualization of the course embedding space."""
    perp = min(7, len(courses) - 1)
    tsne = TSNE(n_components=2, random_state=42, perplexity=perp, max_iter=1000)
    coords = tsne.fit_transform(embeddings)

    cat_colors = {
        "CS Core": "#6c9bff",
        "CS Elective": "#38bdf8",
        "Cybersecurity Core": "#a78bfa",
        "Math": "#4ade80",
    }

    fig, ax = plt.subplots(figsize=(11, 7.5))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#1a1d27")
    for spine in ax.spines.values():
        spine.set_color("#2a2e3d")
    ax.tick_params(colors="#5a6478", labelsize=8)

    for i, c in enumerate(courses):
        color = cat_colors.get(c["category"], "#8892a8")
        ax.scatter(coords[i, 0], coords[i, 1], c=color, s=140, alpha=0.85,
                   edgecolors="#0f1117", linewidths=1.5, zorder=3)
        ax.annotate(c["code"], (coords[i, 0], coords[i, 1]),
                    xytext=(8, 6), textcoords="offset points",
                    fontsize=7.5, color=color, fontweight="bold", alpha=0.9)

    for cat, color in cat_colors.items():
        ax.scatter([], [], c=color, s=80, label=cat, edgecolors="#0f1117", linewidths=1)
    legend = ax.legend(loc="upper right", fontsize=9, facecolor="#1a1d27",
                       edgecolor="#2a2e3d", labelcolor="#e2e8f0")

    ax.set_title("Course Embedding Space (t-SNE Projection)", color="#e2e8f0",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Dimension 1", color="#5a6478", fontsize=10)
    ax.set_ylabel("Dimension 2", color="#5a6478", fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#0f1117")
    plt.close()


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("ChamplainGuide Frontier Model")
    print("Course Recommendation via TF-IDF + SVD Embeddings")
    print("=" * 60)

    # Build course text representations (tokens → words)
    print("\n[1/4] Building course representations...")
    course_texts = []
    for c in COURSES:
        text = (
            f"{c['code']} {c['name']}. {c['description']} "
            f"Category: {c['category']}. Prerequisites: {', '.join(c['prereqs']) or 'none'}."
        )
        course_texts.append(text)
    print(f"  ✓ {len(COURSES)} courses converted to text representations")

    # Train embedding model
    print("\n[2/4] Training embedding model...")
    model = CourseEmbeddingModel(n_components=min(50, len(COURSES) - 1))
    model.fit(course_texts)
    print(f"  ✓ TF-IDF vocabulary size: {model.get_vocabulary_size()} terms")
    print(f"  ✓ SVD reduced to {model.course_embeddings.shape[1]}-dimensional dense embeddings")
    print(f"  ✓ Embedding matrix shape: {model.course_embeddings.shape}")
    print(f"  ✓ Variance explained: {model.svd.explained_variance_ratio_.sum():.1%}")

    # Demo queries
    demo_queries = [
        "I want to learn how to hack into systems",
        "How do I build a website or web app?",
        "I'm interested in AI and machine learning",
        "I need math courses for data science",
        "How do computers store and organize information?",
    ]

    print("\n[3/4] Running before/after comparisons...")
    print("-" * 60)

    all_results = []

    for query in demo_queries:
        print(f'\n  Query: "{query}"')

        kw = keyword_search(query, COURSES)
        emb = model.recommend(query, COURSES)

        print(f"  {'BEFORE (keywords)':<30} | {'AFTER (embeddings)':<30}")
        print(f"  {'-'*30} | {'-'*30}")
        for i in range(3):
            kw_str = f"{kw[i][0]['code']}: {kw[i][0]['name'][:20]} ({kw[i][1]} matches)"
            emb_str = f"{emb[i][0]['code']}: {emb[i][0]['name'][:20]} ({emb[i][1]:.3f})"
            print(f"  {kw_str:<30} | {emb_str:<30}")

        all_results.append({
            "query": query,
            "keyword_top3": [(c["code"], c["name"], int(s)) for c, s in kw[:3]],
            "embedding_top3": [(c["code"], c["name"], round(float(s), 4)) for c, s in emb[:3]],
        })

    # Visualizations
    print("\n[4/4] Generating visualizations...")

    for i, query in enumerate(demo_queries):
        kw = keyword_search(query, COURSES)
        emb = model.recommend(query, COURSES)
        path = f"/home/claude/comparison_{i+1}.png"
        create_comparison_chart(query, kw, emb, path)
        print(f"  ✓ {path}")

    create_embedding_space(COURSES, model.course_embeddings, "/home/claude/embedding_space.png")
    print(f"  ✓ /home/claude/embedding_space.png")

    with open("/home/claude/model_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"  ✓ /home/claude/model_results.json")

    # Print summary
    print("\n" + "=" * 60)
    print("MODEL SUMMARY")
    print(f"  Type:           TF-IDF + Truncated SVD")
    print(f"  Vocabulary:     {model.get_vocabulary_size()} terms (unigrams + bigrams)")
    print(f"  Embedding dim:  {model.course_embeddings.shape[1]}")
    print(f"  Courses:        {len(COURSES)}")
    print(f"  Variance:       {model.svd.explained_variance_ratio_.sum():.1%}")
    print("=" * 60)
    print("\nKey insight: Embeddings capture SEMANTIC meaning.")
    print('  "hack into systems" → finds Ethical Hacking (no shared keywords)')
    print('  "math for data science" → finds Linear Algebra & Statistics')
    print("  Keywords can only match exact words; embeddings match meaning.")
    print("=" * 60)


if __name__ == "__main__":
    main()
