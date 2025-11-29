This document summarizes open source tools that can support the evaluation of PromptPrompt. Now, there are two categories of tools:

1. **Prompt Testing** for building the 30 prompt testing suite  
2. **Text Evaluation Tools** for comparing model outputs before and after optimization

If you find any problem， please contact me， I will update ：）

# Category A: Prompt Testing
## 1.  Promptfoo
https://github.com/promptfoo/promptfoo

This framework for testing and comparing prompts across LLMs supports batch execution, prompt diffing, scoring functions, and regression tests.
Provides ideas for batch testing, scoring, and comparison logic. Very relevant to run many prompts to collect outputs and evaluate. 

## 2. Microsoft PromptBench  
https://github.com/microsoft/promptbench

The prompt benchmarking framework from Microsoft. It can handle many prompts at once, and we also need to test 30+ prompts, so it may fits what we're doing really well.

## 3. lm-evaluation-harness
https://github.com/EleutherAI/lm-evaluation-harness/tree/main/tests

I think this basically shows us “this is what a proper evaluation system looks like.” It doesn't help us compare prompts directly，but its task folders, metric files, and evaluation flow may can give us a super clear example of how to build our own tester. We can use its structure。

# Category B: Text Evaluation Tools  
These tools directly support us comparing outputs generated before and after prompt optimization. Then compute similarity scores, measure quality differences, and run statistical tests.

## 1. sentence-transformers
https://github.com/huggingface/sentence-transformers/tree/main

Converts text into embeddings and computes cosine similarity between outputs. Measures semantic closeness between “before” and “after” responses.
Perfect for evaluating how much the optimized prompt improves or changes the meaning.  

## 2. bert_score
https://github.com/Tiiiger/bert_score

Computes similarity using contextual embeddings， produces precision/recall/F1 scores for text comparison. Use comparing optimized outputs with original outputs.

## 3.rouge ---- (Information Overlap Metric)
https://github.com/pltrdy/rouge

Measure how much information overlaps between two texts. Evaluates how much key content appears in both outputs. Maybe helps us check whether the optimized prompt produces more complete or more informative outputs

## 4.textstat  ---- (Readability Metrics)
https://github.com/textstat/textstat

Evaluates how easy a text is to understand based on vocabulary and sentence complexity. May help quantify whether optimized prompts produce more structured and easier-to-read outputs.
