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

The prompt benchmarking framework from Microsoft. It can handle many prompts at once, and we also need to test 30+ prompts, so it fits what we're doing really well. The structure is clear and easy to follow, so it's a strong reference for building our large-scale testing workflow.

## 3. lm-evaluation-harness
https://github.com/EleutherAI/lm-evaluation-harness/tree/main/tests

I think this basically shows us “this is what a proper evaluation system looks like.” It doesn't help us compare prompts directly，but its task folders, metric files, and evaluation flow may can give us a super clear example of how to build our own tester. We can use its structure。

# Category B: Text Evaluation Tools  
These tools directly support us comparing outputs generated before and after prompt optimization. Then compute similarity scores, measure quality differences, and run statistical tests.
