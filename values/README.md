# Values

Human beings have **values** — ideas and practices that they cherish and propagate in their societies.

LLMs do not have values per se, but the alignment steps in their training (eg the RLHF step) likely reflect the value systems of the people and corporations that trained them.

So a question we can ask is: Is it possible to get an LLM to reveal the value system it has learned?

The World Values Survey and European Values Survey have run multiple international surveys: 200+ questions, more than 100 countries, more than 1000 respondents per country, most than 40 years of data.

Ten of the WVS/EVS questions contribute to two key indicators: 'survival vs self-expression values' and 'traditional vs secular values'. Together, these are often shown on a Inglehart–Welzel Cultural Map. A recent paper, Tao et al 2024, plots LLMs on this map.

Let's try to reproduce it!


## References 

EVS (2022). EVS Trend File 1981-2017 (ZA7503; Version 3.0.0) [Data set]. GESIS, Cologne. https://doi.org/10.4232/1.14021

Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen et al. (eds.). 2022. World Values Survey Trend File (1981-2022) Cross-National Data-Set. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. Data File Version 4.0.0, doi:10.14281/18241.27.

Tao, Y, O Viberg, RS Baker, RF Kizilcec (2024). Cultural bias and cultural alignment of large language models. PNAS Nexus 3 (9), September 2024, https://doi.org/10.1093/pnasnexus/pgae346.