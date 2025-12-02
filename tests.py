import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util
from bert_score import score as bertscore
from rouge_score import rouge_scorer
import textstat

# ======================================================
# Demo prompt data (before prompt → after prompt)
# ======================================================

FILE_CASES = [
    {
        "id": 1,
        "name": "Explain AI",
        "prompt_before": "Explain AI.",
        "prompt_after": "Explain what artificial intelligence is and describe how it works.",
        "before_output": "AI is like a smart computer that can do tasks.",
        "after_output": (
            "Artificial intelligence refers to systems that perform tasks "
            "that normally require human reasoning."
        ),
    },
    {
        "id": 2,
        "name": "Email apology",
        "prompt_before": "Write apology email.",
        "prompt_after": "Write a polite apology email explaining that you cannot attend an event.",
        "before_output": "Sorry I can't go.",
        "after_output": (
            "I'm sorry, but I won't be able to attend due to a schedule conflict."
        ),
    },
    {
        "id": 3,
        "name": "Summarize text",
        "prompt_before": "Summarize this text.",
        "prompt_after": "Provide a concise summary that captures the main idea of the given text.",
        "before_output": "This is short.",
        "after_output": "This summary provides the main idea in a clearer way.",
    },
]

# ======================================================
# Models
# ======================================================

st_model = SentenceTransformer("all-MiniLM-L6-v2")
rouge = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)


def semantic_similarity(a: str, b: str) -> float:
    emb1 = st_model.encode(a, convert_to_tensor=True)
    emb2 = st_model.encode(b, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2))


def bert_score_single(a: str, b: str) -> float:
    _, _, F1 = bertscore([a], [b], lang="en", verbose=False)
    return float(F1.mean())


def rouge_scores(a: str, b: str) -> float:
    return rouge.score(a, b)["rougeL"].fmeasure


def readability(text: str) -> float:
    return textstat.flesch_reading_ease(text)


# ======================================================
# Run Evaluation
# ======================================================
def run_tests():
    results = []

    for case in FILE_CASES:
        cid = case["id"]
        name = case["name"]

        pb = case["prompt_before"]
        pa = case["prompt_after"]
        out_b = case["before_output"]
        out_a = case["after_output"]

        # Prompt changes (metrics on prompts)
        prompt_sim = semantic_similarity(pb, pa)
        prompt_bert = bert_score_single(pb, pa)
        prompt_rouge = rouge_scores(pb, pa)
        prompt_read_b = readability(pb)
        prompt_read_a = readability(pa)

        # Output changes (metrics on model outputs)
        output_sim = semantic_similarity(out_b, out_a)
        output_bert = bert_score_single(out_b, out_a)
        output_rouge = rouge_scores(out_b, out_a)
        output_read_b = readability(out_b)
        output_read_a = readability(out_a)

        print(f"\n=== Case {cid}: {name} ===")
        print("Prompt Similarity:", round(prompt_sim, 4))
        print("Output Similarity:", round(output_sim, 4))

        results.append(
            {
                "id": cid,
                "name": name,
                "prompt_similarity": prompt_sim,
                "output_similarity": output_sim,
                "prompt_read_before": prompt_read_b,
                "prompt_read_after": prompt_read_a,
                "output_read_before": output_read_b,
                "output_read_after": output_read_a,
                "prompt_bert": prompt_bert,
                "output_bert": output_bert,
                "prompt_rouge": prompt_rouge,
                "output_rouge": output_rouge,
            }
        )

    df = pd.DataFrame(results)
    df.to_csv("evaluation_results.csv", index=False)
    print("\nSaved: evaluation_results.csv")

    # ======================================================
    # Output Readability Line Chart (Before vs After)
    # ======================================================
    plt.figure(figsize=(10, 5))
    plt.plot(
        df["id"],
        df["output_read_before"],
        marker="o",
        label="Before Output Readability",
    )
    plt.plot(
        df["id"],
        df["output_read_after"],
        marker="o",
        label="After Output Readability",
    )

    plt.title("Output Readability Comparison (Before vs After)")
    plt.xlabel("Case ID")
    plt.ylabel("Flesch Reading Ease")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output_readability_line.png")
    print("Saved: output_readability_line.png")

    # ======================================================
    # Prompt Readability Line Chart (Before vs After)
    # ======================================================
    plt.figure(figsize=(10, 5))
    plt.plot(
        df["id"],
        df["prompt_read_before"],
        marker="o",
        label="Before Prompt Readability",
    )
    plt.plot(
        df["id"],
        df["prompt_read_after"],
        marker="o",
        label="After Prompt Readability",
    )

    plt.title("Prompt Readability Comparison (Before vs After)")
    plt.xlabel("Case ID")
    plt.ylabel("Flesch Reading Ease")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("prompt_readability_line.png")
    print("Saved: prompt_readability_line.png")

    # ======================================================
    # Prompt-only Semantic Similarity Matrix
    # ======================================================
    print("\nGenerating Prompt-only Heatmap...")

    prompt_texts = []
    prompt_labels = []

    for c in FILE_CASES:
        prompt_texts += [c["prompt_before"], c["prompt_after"]]
        prompt_labels += [
            f"{c['id']}-prompt-before",
            f"{c['id']}-prompt-after",
        ]

    prompt_embeddings = st_model.encode(prompt_texts, convert_to_tensor=True)
    n_p = len(prompt_texts)

    prompt_matrix = [
        [
            float(util.cos_sim(prompt_embeddings[i], prompt_embeddings[j]))
            for j in range(n_p)
        ]
        for i in range(n_p)
    ]

    df_prompt_matrix = pd.DataFrame(
        prompt_matrix, columns=prompt_labels, index=prompt_labels
    )
    df_prompt_matrix.to_csv("prompt_only_matrix.csv")
    print("Saved: prompt_only_matrix.csv")

    plt.figure(figsize=(10, 8))
    plt.imshow(df_prompt_matrix, cmap="coolwarm", interpolation="nearest")
    plt.colorbar(label="Semantic Similarity")
    plt.xticks(range(n_p), prompt_labels, rotation=45, ha="right")
    plt.yticks(range(n_p), prompt_labels)
    plt.title("Prompt-only Semantic Similarity Matrix")
    plt.tight_layout()
    plt.savefig("prompt_only_matrix.png")
    print("Saved: prompt_only_matrix.png")

    # ======================================================
    # Output-only Semantic Similarity Matrix
    # ======================================================
    print("\nGenerating Output-only Heatmap...")

    output_texts = []
    output_labels = []

    for c in FILE_CASES:
        output_texts += [c["before_output"], c["after_output"]]
        output_labels += [
            f"{c['id']}-output-before",
            f"{c['id']}-output-after",
        ]

    output_embeddings = st_model.encode(output_texts, convert_to_tensor=True)
    n_o = len(output_texts)

    output_matrix = [
        [
            float(util.cos_sim(output_embeddings[i], output_embeddings[j]))
            for j in range(n_o)
        ]
        for i in range(n_o)
    ]

    df_output_matrix = pd.DataFrame(
        output_matrix, columns=output_labels, index=output_labels
    )
    df_output_matrix.to_csv("output_only_matrix.csv")
    print("Saved: output_only_matrix.csv")

    plt.figure(figsize=(10, 8))
    plt.imshow(df_output_matrix, cmap="coolwarm", interpolation="nearest")
    plt.colorbar(label="Semantic Similarity")
    plt.xticks(range(n_o), output_labels, rotation=45, ha="right")
    plt.yticks(range(n_o), output_labels)
    plt.title("Output-only Semantic Similarity Matrix")
    plt.tight_layout()
    plt.savefig("output_only_matrix.png")
    print("Saved: output_only_matrix.png")

    # ======================================================
    # Metric-specific visualizations
    # ======================================================

    # 1) Sentence-Transformers similarity (prompt vs output)
    plt.figure(figsize=(10, 5))
    plt.plot(
        df["id"],
        df["prompt_similarity"],
        marker="o",
        label="Prompt Similarity",
    )
    plt.plot(
        df["id"],
        df["output_similarity"],
        marker="o",
        label="Output Similarity",
    )
    plt.title("Sentence-Transformers Semantic Similarity")
    plt.xlabel("Case ID")
    plt.ylabel("Cosine Similarity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("st_similarity_line.png")
    print("Saved: st_similarity_line.png")

    # 2) BERTScore comparison (prompt vs output)
    x = df["id"]
    width = 0.35
    plt.figure(figsize=(10, 5))
    plt.bar(x - width / 2, df["prompt_bert"], width=width, label="Prompt BERTScore")
    plt.bar(x + width / 2, df["output_bert"], width=width, label="Output BERTScore")
    plt.title("BERTScore (Prompt vs Output)")
    plt.xlabel("Case ID")
    plt.ylabel("F1 Score")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig("bertscore_bar.png")
    print("Saved: bertscore_bar.png")

    # 3) ROUGE-L comparison (prompt vs output)
    plt.figure(figsize=(10, 5))
    plt.bar(x - width / 2, df["prompt_rouge"], width=width, label="Prompt ROUGE-L")
    plt.bar(x + width / 2, df["output_rouge"], width=width, label="Output ROUGE-L")
    plt.title("ROUGE-L Overlap (Prompt vs Output)")
    plt.xlabel("Case ID")
    plt.ylabel("ROUGE-L F-measure")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig("rouge_bar.png")
    print("Saved: rouge_bar.png")

    # ======================================================
    # Promptfoo-Style Pass Rate Bar Chart (Multi-metric rule)
    # ======================================================

    # Pass rule:
    # 1) output similarity is high enough (semantic preservation)
    # 2) output BERTScore is high enough
    # 3) output readability does not drop too much
    df["pass"] = (
        (df["output_similarity"] >= 0.6)
        & (df["output_bert"] >= 0.80)
        & (df["output_read_after"] >= df["output_read_before"] - 5)
    )

    pass_rates = df.groupby("id")["pass"].mean()

    plt.figure(figsize=(8, 5))
    plt.bar(df["id"], pass_rates, color=["skyblue", "salmon", "lightgreen"])
    plt.ylim(0, 1)
    plt.title("Promptfoo-style Pass Rate Comparison (Multi-metric Rule)")
    plt.xlabel("Case ID")
    plt.ylabel("Pass Rate")
    plt.tight_layout()
    plt.savefig("promptfoo_pass_rate.png")
    print("Saved: promptfoo_pass_rate.png")

    # ======================================================
    # Histogram - distribution of output similarity
    # ======================================================
    plt.figure(figsize=(8, 5))
    plt.hist(
        df["output_similarity"],
        bins=5,
        color="lightblue",
        edgecolor="black",
    )
    plt.title("Similarity Score Distribution (Output Before vs After)")
    plt.xlabel("Similarity Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("promptfoo_similarity_hist.png")
    print("Saved: promptfoo_similarity_hist.png")

    # ======================================================
    # Scatter Plot (Prompt Similarity vs Output Similarity)
    # ======================================================
    plt.figure(figsize=(7, 6))
    plt.scatter(
        df["prompt_similarity"],
        df["output_similarity"],
        color="crimson",
        s=80,
    )

    for _, row in df.iterrows():
        plt.text(
            row["prompt_similarity"],
            row["output_similarity"],
            f"{row['id']}",
            fontsize=10,
        )

    plt.title("Promptfoo-style Scatter Plot\nPrompt Similarity vs Output Similarity")
    plt.xlabel("Prompt Similarity")
    plt.ylabel("Output Similarity")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("promptfoo_scatter.png")
    print("Saved: promptfoo_scatter.png")

    # ======================================================
    # Variables × Outputs Table (Promptfoo-style)
    # ======================================================
    table = df[
        [
            "id",
            "name",
            "prompt_similarity",
            "prompt_read_before",
            "prompt_read_after",
            "output_similarity",
            "output_read_before",
            "output_read_after",
            "prompt_rouge",
            "output_rouge",
            "prompt_bert",
            "output_bert",
            "pass",
        ]
    ]

    table.to_csv("promptfoo_table.csv", index=False)
    print("Saved: promptfoo_table.csv")

    return df


if __name__ == "__main__":
    run_tests()
