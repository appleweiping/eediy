---
title: Literature Search for Engineering Decisions
description: Start from a decidable EE question, locate primary material, check versions and conditions, and know when the remaining uncertainty belongs on the bench.
page_type: guide
comments: true
---


# Literature Search for Engineering Decisions

What follows is a rerunnable search log. The example task is not “collect
papers about low-noise op amps”; it is to choose an input structure for a
small-signal front end with a 5 V single supply, 10 kΩ source impedance, and
100 kHz bandwidth. Every round records how the query changed, what it ruled
out, and which unresolved parameter moved to calculation or experiment.

| Round | Query or action | The only acceptable output from this round |
| --- | --- | --- |
| 0 | Broad terms used to build a synonym and topology vocabulary | Candidate terms, not a device conclusion |
| 1 | Add supply, source impedance, bandwidth, noise, and stability conditions | Comparable claims and their primary locations |
| 2 | Search failure, limitation, instability, and the opposite topology | Conditions that would overturn the current choice |
| Stop | New material no longer changes the next calculation or bench test | A scoped one-page judgment and an explicit open question |

The final artifact is not a folder full of PDFs. It is this log, an evidence
matrix, and a decision that states how it could be overturned.

## Round 0: write the decision before the query

Compress the question into one line: **object + operating conditions + alternatives + metric + threshold that changes the decision**. For example: “For a small-signal front end with 10 kΩ source impedance and 100 kHz bandwidth, compare the integrated input noise of two amplifier classes; reject a candidate if the compensation needed for stable operation reduces bandwidth below the target.” That wording forces searches for noise density, the 1/f corner, current noise, gain bandwidth, loading, and stability instead of only a product category.

List abbreviations, historical terms, circuit topologies, and exclusion terms for each concept, then preserve two or three rerunnable queries. The IEEE Xplore [search guide](https://ieeexplore.ieee.org/Xplorehelp/downloads/user-guides/IEEE_Xplore_Searching_and_Saving_Searches.pdf) documents uppercase `AND`, `OR`, and `NOT`, phrase quotes, wildcards, and field restrictions. It is useful for IEEE papers and standards, but it does not represent every publisher or decade. Manufacturer data sheets, standards bodies, author archives, and other indexes still need their own searches.

For every search round, retain the database, exact query, filters, sort order, date, and result count. This is not clerical decoration. When terminology changes or a result appears three weeks later, those details let you tell whether the difference came from the query, the index, or the literature.

## Round 1: use persistent identifiers to check version and provenance

Prefer a DOI, report number, standard number, or manufacturer document ID to a bare browser address. The DOI Foundation's [DOI Handbook](https://www.doi.org/doi-handbook/DOIHandbook_2025.pdf) describes a DOI as a persistent identifier that resolves to resources and metadata. Persistence preserves the identity of the referent; it does not promise correctness, free access, or an unchanging document.

For a source with a DOI, the Crossref [REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) provides a way to check title, authorship, publication data, license fields, and update relationships. Automated import reduces transcription errors but does not prove that metadata is complete. Open the publisher or standards-body record and determine whether you have a conference version, journal extension, correction, or preprint. For standards and data sheets, retain the revision and date because limits or test methods can change under an unchanged title.

A reference manager stores and retrieves material; it does not certify it. Zotero's [search documentation](https://www.zotero.org/support/searching) describes advanced conditions and saved searches that update as the library changes. Dynamic sets such as “full text unread,” “test conditions missing,” and “contradicts current choice” make useful working queues; remove a tag only after the record enters the comparison. If the PDF is not lawfully available, retain metadata, an abstract, and an access path. Do not evade access controls or commit restricted full text to a public repository.

## Round 2: search deliberately for conditions that break the preferred answer

A survey paper or textbook may supply vocabulary, but an important claim should move toward the closest available source: a standard defines the test, a data sheet states device conditions and rated limits, a primary paper describes the method and measurement, and software documentation states implementation parameters. Forums and lecture notes can suggest vocabulary; they are not final authority for mains, high voltage, medical devices, batteries, or RF compliance.

Use a small comparison matrix in which each row carries one claim:

| Claim | Location inside source | Test conditions | Value and uncertainty | Limitation or interest | Effect on decision |
| --- | --- | --- | --- | --- | --- |
| Candidate A has lower voltage noise | page, figure, or table | frequency, temperature, source impedance | value in a common unit | typical or guaranteed | supports or leaves unchanged |
| Candidate B is stable with capacitive load | data-sheet section | gain, load, supply | margin or specified waveform | vendor test circuit | supports or rejects |

Do not rank noise integrated over different bandwidths, power at different loads, or typical and worst-case values as though they were commensurate. Normalize definition and condition first; if that is impossible, keep two separate questions. Trace important claims backward to the original measurement and forward to replications, corrections, and later counterexamples. Then search explicitly for “failure,” “limitation,” and “instability,” plus the topology opposite the current favorite.

Publication status needs its own check. Crossref [Crossmark](https://www.crossref.org/services/crossmark/) can expose corrections, retractions, and other important updates registered by participating members. Its own documentation also says that the presence of Crossmark is not a guarantee, and coverage depends on publishers participating and depositing updates. Treat it as one status check, not as a trust badge.

## Stop log: another source no longer changes the next experiment

Write a one-page synthesis for this decision. Put the current choice and domain first. Make every important number point to a page, section, figure, or table. Separate directly reported facts, inferences assembled from several sources, and assumptions that remain untested. End with the observation that would overturn the choice. An effective search has no mandatory paper count; it has the conditions needed for the decision, at least one serious counterexample, and a remaining gap translated into a feasible test.

If two more search rounds add only repetitions under the same conditions while the central unknown remains “does this board oscillate with the actual source impedance?”, a limited-energy, observable experiment is more informative than another pile of papers. If sources instead use incompatible metrics or standard revisions, do not build yet. Resolve the definitions and design the test only after the mismatch is understood.

Archive the final queries, result count from each round, bibliography export,
evidence matrix, and one-page conclusion, but commit only material you may
distribute. Inspect attached code or firmware in isolation before execution;
publication is not a sandbox. The log's open-question field should translate
directly into an acceptance test in [Project Practice](projects.md), while
the choice, counterexample, and scope belong in the design note described by
[Technical Writing](technical-writing.md). If neither destination can use the
search result, the question has not yet become an engineering decision.
