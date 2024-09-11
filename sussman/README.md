Gerald Sussman (MIT CSAIL) wrote [a PhD thesis (LINK)](https://www.cs.cmu.edu/~mmv/planning/readings/AITR-297.pdf) entitled, _A Computational Model of Skill Acquisition_, dated August 1973. 

Here is the abstract:

<img width="732" alt="image" src="https://github.com/kwinkunks/promptly/assets/1692372/5664fbed-bfe7-44eb-bf24-f9e300c04c7a">

The thesis contains some images describing a scene, plus some text decribing a task to be performed, eg by a robot. These examples could form a small benchmark for testing the planning capabilities of AIs

This folder contains the relevant figures, along with the actual text Sussman gave.

The so-called [Sussman anomaly](https://en.wikipedia.org/wiki/Sussman_anomaly) starts with the figure shown in `problem_1-3-a.png`, which is a solution to problem 1.3.

One potential strategy for solving tasks like this is to extract data from the image or plain English scene description, transform it to a [PDDL (a planning DSL)](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language) domain description, then have a specialized solver take on the actual task (e.g. see [Silver et al, 2024](https://openreview.net/pdf?id=1QMMUB4zfl), at NeurIPS). Also, check out [`pyperplan`](https://github.com/aibasel/pyperplan) for an interesting project with a lot of benchmarks.

---

Blocks World images &copy; Gerald Sussman 1973 and reproduced here under the fair use doctrine
