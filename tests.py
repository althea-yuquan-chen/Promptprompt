import torch 
from sentence_transformers import SentenceTransformer, util

SIM_MODEL = SentenceTransformer("all-MiniLM-L6-v2") 

from bert_score import score
from rouge import Rouge

# --- Metric ---

# 1. Semantic Sim (using the global SIM_MODEL)
def get_sim_score(ref_text, gen_text):
    emb_ref = SIM_MODEL.encode(ref_text)
    emb_gen = SIM_MODEL.encode(gen_text)
    sim = util.cos_sim(torch.tensor(emb_ref), torch.tensor(emb_gen))

    return float(sim[0][0]) 

# 2. BERT F1
def bert_score_eval(before_output, after_output):
    P, R, F1 = bert_score([after_output], [before_output], lang="en", verbose=False)
    return float(F1[0])

# 3. ROUGE-L
def rouge_eval(before_output, after_output):
    rouge = Rouge()
    scores = rouge.get_scores(after_output, before_output)[0]
    return scores["rouge-l"]["f"]

# --- Execution ---
if __name__ == "__main__":

    # Example outputs — replace with real outputs later
    before_output = """AI helps with writing emails."""
    after_output = """AI systems can assist users in drafting emails effectively."""

  print("=== Running Evaluation Tests ===")

    # Inconsistent print formatting
    sem_sim = get_sim_score(ref, gen)
    print(f"Sem Sim (ST): {sem_sim:.4f}")

    bert_f1 = bert_f1_val(ref, gen)
    print("BERT F1:", bert_f1)

    rouge_l = calculate_rouge_l(ref, gen)
    print(f"ROUGE-L F1: {rouge_l:.4f}\n")
    
    print("Done.")
