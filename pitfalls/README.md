# Pitfalls in the use of generative AI


## Evaluating chatbots

The table below summarizes results from the notebooks in this folder:

- [LLM_Pitfalls_GPT35.ipynb](LLM_Pitfalls_GPT35.ipynb)
- [LLM_Pitfalls_GPT4.ipynb](LLM_Pitfalls_GPT4.ipynb)
- [LLM_Pitfalls_Claude.ipynb](./LLM_Pitfalls_Claude.ipynb)

**Note:** the queries shown in these notebooks were written for ChatGPT 3.5 Turbo, with the express intention of making them fail. They are then repeated, with some tweaking and augmentation, in order to try to get them to fail for ChatGPT 4 and Claude as well. I did not pursue this failure relentlessly, and of course it would be entirely possible to write a suite of tests that will all fail for any given model, or a suite which would all pass. But I think I am comfortable saying that Claude and ChatGPT 4 perform better than ChatGPT 3.5 on the specific tasks I have outlined here, with a roughly 30% reduction in error.

<img width="1178" alt="image" src="https://github.com/user-attachments/assets/695c202a-d9d1-4d0b-9ffb-deb5407a81d9">

See the full version of this table in [the PDF file](./Generative_AI_pitfalls_v2__Matt_Hall__CC-BY.pdf) here in this folder.


## See also

See also my [`ml-pitfalls`](https://github.com/Equinor/ml-pitfalls) repository.
