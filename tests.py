import pandas as pd
import matplotlib.pyplot as plt

from sentence_transformers import SentenceTransformer, util
from bert_score import score as bertscore
from rouge_score import rouge_scorer
import textstat


# =====================================
# 1. text -- will change later
# =====================================
TEST_CASES = [
    {
        "id": 1,
        "prompt": "Explain AI",
        "before_output": "AI is like a smart computer.",
        "after_output": "Artificial intelligence refers to systems that perform tasks requiring human reasoning."
    },
    {
        "id": 2,
        "prompt": "Email apology",
        "before_output": "Sorry I can't go.",
        "after_output": "I'm sorry, but I will not be able to attend due to a schedule conflict."
    },
    {
        "id": 3,
        "prompt": "Summarize text",
        "before_output": "This is short.",
        "after_output": "This summary captures the main idea and provides a clearer explanation."
    }
]

st_model = SentenceTransformer("all-MiniLM-L6-v2")
rouge = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)

def semantic_similarity(before: str, after: str) -> float:
    emb1 = st_model.encode(before, convert_to_tensor=True)
    emb2 = st_model.encode(after, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2))


def bert_score_single(before: str, after: str) -> float:
    P, R, F1 = bertscore([after], [before], lang="en", verbose=False)
    return float(F1.mean())


def rouge_scores(before: str, after: str) -> float:
    return rouge.score(before, after)["rougeL"].fmeasure


def readability(text: str) -> float:
    return textstat.flesch_reading_ease(text)


def run_tests():
    results = []

    print("\n=== Running Evaluation on Multiple Cases ===\n")

    for case in TEST_CASES:
        pid = case["id"]
        before = case["before_output"]
        after = case["after_output"]

        sim = semantic_similarity(before, after)
        rougel = rouge_scores(before, after)
        read_after = readability(after)
        bert_f1 = bert_score_single(before, after)

        print(f"[Case {pid}] sim={sim:.4f}, rougeL={rougel:.4f}, readability={read_after:.2f}, bert_f1={bert_f1:.4f}")

        results.append({
            "id": pid,
            "semantic_similarity": sim,
            "rougeL_overlap": rougel,
            "readability_after": read_after,
            "bert_f1": bert_f1
        })

    df = pd.DataFrame(results)
    df.to_csv("eval_results.csv", index=False)
    print("\nSaved: eval_results.csv")

    plt.figure(figsize=(10,5))
    plt.bar(df["id"], df["semantic_similarity"], color='skyblue')
    plt.title("Semantic Similarity (Sentence-Transformers)")
    plt.xlabel("Case ID")
    plt.ylabel("Cosine Similarity")
    plt.tight_layout()
    plt.savefig("semantic_similarity_plot.png")
    print("Saved: semantic_similarity_plot.png")

    plt.figure(figsize=(10,5))
    plt.bar(df["id"], df["readability_after"], color='lightgreen')
    plt.title("Readability (textstat)")
    plt.xlabel("Case ID")
    plt.ylabel("Flesch Reading Ease")
    plt.tight_layout()
    plt.savefig("readability_plot.png")
    print("Saved: readability_plot.png")

    plt.figure(figsize=(10,5))
    plt.bar(df["id"], df["bert_f1"], color='salmon')
    plt.title("BERTScore (F1)")
    plt.xlabel("Case ID")
    plt.ylabel("F1 Score")
    plt.ylim(0,1)
    plt.tight_layout()
    plt.savefig("bertscore_plot.png")
    print("Saved: bertscore_plot.png")

    return df


if __name__ == "__main__":
    run_tests()

