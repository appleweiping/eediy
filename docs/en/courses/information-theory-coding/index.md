---
title: "Information Theory and Coding"
description: "Entropy, capacity, rate-distortion, and modern error-correcting codes for both limits and constructions."
page_type: track
track_id: "track-information-theory-coding"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: e24613e670d18135 -->

# Information Theory and Coding

## Track position

Entropy, capacity, rate-distortion, and modern error-correcting codes for both limits and constructions.

## Recommended prerequisite tracks

- [Probability, Statistics, and Random Processes](../probability-statistics/index.md)
- [Communication Systems](../communications/index.md)

## EE 276 and 6.441 are proof archives at different densities

[Stanford EE 276](102-ee-276.md) is the better first complete course. Its [official page](https://web.stanford.edu/class/ee276/) connects entropy, typical sets, source coding, channel capacity, rate-distortion, and an entry to multiuser problems. The public archive contains an older 18-lecture note sequence, 8 current solved assignments, and 2 examinations, but only 1 current slide deck was verified. Read every item with its offering date rather than relabeling the old notes as the active lectures. [MIT 6.441](103-6-441.md) has an [official OCW archive](https://ocw.mit.edu/courses/6-441-information-theory-spring-2010/) with 23 denser lectures and 9 problem sets. Its proofs and multiuser treatment go further, but the sets have no public solutions. Use the EE 276 problem-solution-exam chain for the foundation and consult 6.441 for a specific converse, rate region, or multiuser question. Synchronization, detection, waveform, and modem implementation belong first to [communication systems](../communications/index.md); information theory establishes limits rather than a physical link.

## Make one problem survive definitions, proof, and boundary distributions

The useful prerequisite is the ability to argue in the language of [probability and statistics](../probability-statistics/index.md). Starting from one joint law, calculate entropy, conditional entropy, and mutual information while naming the conditioning information, logarithm base, and bit or nat units. Write the direction and assumptions of data processing for a Markov chain. For a BSC or BEC, state the input law, block length, error criterion, and quantifiers in achievability and converse claims. Uniform and degenerate distributions, together with crossover probabilities zero and one, expose hidden divisions and support assumptions. Treating capacity as the fixed bit rate printed on hardware indicates a definition problem involving alphabets, input cost, and decoding error, not an algebra problem.

For a solved EE 276 assignment, produce a closed-book draft, inspect only the earliest divergent step, and then derive the whole result again. Take the two examinations under their published time limits to separate definition gaps, proof technique, and pacing. The 9 sets in 6.441 require checks from definitions, a second derivation, extreme distributions, or line-by-line discussion because no official answers are public. Neither course includes a programming laboratory. Numerical code may test intuition, but it is neither a course assignment nor an institutional grade. The central reading habit is to identify exactly where independence, convexity, exchange of limits, or typicality licenses each equality.

## A finite-block experiment brings asymptotic theorems back to data

Choose a BSC, BEC, or a simple input-constrained channel. Write a complete source-coding argument, a channel-coding bound, and a data-processing consequence with consistent random variables, distributions, block lengths, limiting order, and error definition. Then implement a rerunnable experiment covering at least three block lengths and three channel parameters. Compare empirical error, a finite-length bound, and asymptotic capacity; include the trial count, an interval for random estimates, and one hand-enumerable small case. Visible finite-length departure from the asymptote is the phenomenon to explain.

After changing the input constraint, mutual-information values are not comparable apart from their optimizing laws, and a curve near capacity does not prove that one decoder is optimal. End on the block-length/channel-parameter case with the largest departure from the asymptote. Check its decoder, finite-length bound, confidence interval, and input constraint, then name the unmet assumption that explains the gap. The theorem's claim, the program's estimate, and unresolved finite-length behavior then occupy one figure.

## Courses

| Course | Institution | Role | Editorial evidence | Practice coverage |
|---|---|---|---|---|
| [Information Theory](102-ee-276.md) | Stanford University | Main course | Public-material guide | Public assignments or labs |
| [Information Theory](103-6-441.md) | MIT | Supplement | Public-material guide | Partial or restricted |
