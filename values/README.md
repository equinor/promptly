# Values

**Please follow this work at https://github.com/equinor/ai-values instead of here**

Human beings have **values** — ideas and practices that they cherish and propagate in their societies.

LLMs do not have values per se, but the alignment steps in their training (eg the RLHF step) likely reflect the value systems of the people and corporations that trained them.

So a question we can ask is: Is it possible to get an LLM to reveal the value system it has learned?

The World Values Survey and European Values Survey have run multiple international surveys: 200+ questions, more than 100 countries, more than 1000 respondents per country, most than 40 years of data.

Ten of the WVS/EVS questions contribute to two key indicators: 'survival vs self-expression values' and 'traditional vs secular values'. Together, these are often shown on a Inglehart–Welzel Cultural Map. A recent paper, Tao et al 2024, plots LLMs on this map.

Let's try to reproduce it!

## Result

So far, I have tested a few chatbots and computed their centroids (see below). I don't know why mine plot in different locations to those in the paper. Next steps: use more variants to get at least 100 or so responses from the chatbots, then set up for testing over time. And maybe compare to some country trajectories.

<img width="1232" height="855" alt="image" src="https://github.com/user-attachments/assets/5ea25865-2c06-4a73-afb4-3e39edef5653" />


## References 

EVS (2022). EVS Trend File 1981-2017 (ZA7503; Version 3.0.0) [Data set]. GESIS, Cologne. https://doi.org/10.4232/1.14021

Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen et al. (eds.). 2022. World Values Survey Trend File (1981-2022) Cross-National Data-Set. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. Data File Version 4.0.0, doi:10.14281/18241.27.

Tao, Y, O Viberg, RS Baker, RF Kizilcec (2024). Cultural bias and cultural alignment of large language models. PNAS Nexus 3 (9), September 2024, https://doi.org/10.1093/pnasnexus/pgae346.


## Related work

This is just a list of things to read:

- Which humans? Atari, Xue, Park, et al, Harvard: file:///Users/MTHA/Downloads/Which%20Humans%2009222023.pdf
- [Beyond prompt brittleness: Evaluating the reliability and consistency of political worldviews in LLMs](https://arxiv.org/pdf/2402.17649v1)
- [eval-polical-worldviews](https://github.com/tceron/eval_political_worldviews)
- [WorldValuesBench](https://aclanthology.org/2024.lrec-main.1539.pdf)
- [paper](https://arxiv.org/pdf/2506.18538v1)
- Exploring Cultural Variations in Moral Judgments with Large Language Models https://arxiv.org/pdf/2506.12433
- From Surveys to Narratives: https://arxiv.org/pdf/2505.16408v1
- Cultural fidelity: https://arxiv.org/pdf/2410.10489v1
