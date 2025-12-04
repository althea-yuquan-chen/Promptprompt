import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# relevance scores (30 cases)
# ============================================

data = {
    "case": list(range(1, 31)),
    "before_score": [
        5.4, 5.1, 7, 5.7, 5.0,
        5.3, 5.6, 7.2, 6.4, 5.3,
        5.9, 5.5, 6.5, 5.7, 5.0,
        5.6, 6.1, 5.3, 7, 6.0,
        7.1, 5.7, 5.2, 6.3, 5.9,
        5.1, 6.0, 6.5, 6, 5.8
    ],
    "after_score": [
        6.1, 7.1, 7.8, 6.3, 5.7,
        5.8, 6.3, 6.9, 7.0, 5.3,
        6.6, 6.1, 7.1, 7.5, 5.4,
        6.2, 7.8, 6, 6.9, 6.5,
        6.9, 6.4, 7.8, 6.9, 6.4,
        5.5, 7.8, 7, 8, 6.3
    ]
}

df = pd.DataFrame(data)

# Save CSV
df.to_csv("relevant_scores_generated.csv", index=False)
print("Saved: relevant_scores_generated.csv")

# ============================================
# Plot Line Chart (Before vs After)
# ============================================

plt.figure(figsize=(12, 6))
plt.plot(df["case"], df["before_score"], marker="o", label="Before Output")
plt.plot(df["case"], df["after_score"], marker="o", label="After Output")

plt.title("Relevance Score Comparison (Before vs After)")
plt.xlabel("Case ID")
plt.ylabel("Relevance Score (0–10)")
plt.xticks(df["case"])
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("relevant_score_comparison.png")
print("Saved: relevant_score_comparison.png")
