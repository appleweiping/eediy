---
title: Version Control and Engineering Collaboration
description: Follow one filter revision to learn how to record design reasons, review EDA changes, and rebuild any milestone.
page_type: guide
comments: true
---


# Version Control and Engineering Collaboration

Git is most useful not as a way to put files in the cloud, but as a record of
why a design became what it is. One EE change may touch a schematic, component
values, a simulation netlist, firmware, measurement data, and a report. If the
history says only `update`, the files may all survive while the reason for the
new result is lost.

A local repository is enough for the first exercise; public hosting is not
required. Git's official [user manual](https://git-scm.com/docs/user-manual)
explains objects, the index, branches, and remotes. Understanding the working
tree, staging area, and commit is more valuable than memorizing dozens of
commands first.

## Commit one decision, not one directory

Start with the repository's [offline RC low-pass
starter](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass)
as a compact version-control exercise: its parameters, calculation or
simulation inputs, result-generation scripts, and explanation are already
separated. Your first commit should contain a rebuildable baseline: \(R\),
\(C\), theoretical cutoff frequency, run command, and expected output. Keep
temporary waveforms, caches, and machine-specific paths out of it. The [`gitignore`
manual](https://git-scm.com/docs/gitignore) also makes an important
distinction: ignore rules do not make already tracked files disappear, so
inspect `git status` and the staged diff before the first commit.

Create a short branch and double the capacitor. Write the expected change in
an issue or design note before editing the parameter, then rebuild and compare
theoretical and simulated results. Whether “change parameter” and “update the
generated report” should be separate commits depends on whether each commit
leaves the repository coherent and runnable. The objective is not the fewest
changed lines; it is a complete reason that a reviewer can follow.

Inspect the diff line by line before merging. If a schematic produces only an
opaque binary change, export a reviewable netlist, BOM, ERC/DRC report, or
versioned PDF. After verification, create an annotated tag and rebuild that
tag in a different temporary directory. It is a milestone only when the tag,
parameters, generation command, and summary identify the same result. A
folder named `final-final` is not one.

## Use a branch to isolate an unproven assumption

A branch is well suited to “what happens if the model, topology, or sample
rate changes?” It is a poor place to accumulate dependent half-finished work
forever. Give each experiment a question and comparison criterion. A failed
experiment need not be merged, but retain a short conclusion so it is not
unknowingly repeated months later. When collaborating through a remote,
fetch first and understand where the remote-tracking branch points; do not
treat `pull` as a synchronization button when the divergence is unknown.

A useful self-review can answer:

- which parameter or interface actually changed;
- which test, simulation, or measurement supports the new conclusion;
- whether generated artifacts can be rebuilt from sources and inputs;
- which risks, licenses, or hardware assumptions changed with it;
- whether returning to the preceding commit really restores the behavior.

For a combined firmware and hardware change, a clean merge does not establish
safe operation. Recheck pinout, supply, current limiting, and default outputs
before flashing. Read scripts and firmware from an unfamiliar branch before
running them, especially when the target is attached to an actuator or
higher-energy load.

## Choose a separate policy for binary EDA files and experimental data

Text code, netlists, and configuration work well with ordinary Git diffs.
PCB databases, oscilloscope captures, and long time series often do not.
First ask whether a file is rebuildable. Rebuildable output usually stays out
of the repository while its command and summary remain. Irreplaceable raw
measurements need checksums, provenance, and read-only retention, but not
necessarily in the source repository.

[Git LFS](https://git-lfs.com/) stores large content outside the repository
and leaves a pointer in Git. It reduces clone size, but it does not create a
meaningful waveform or schematic diff, and it depends on the remote service's
storage, bandwidth, and retention policy. If the project uses LFS, document
the required client and retrieval path, then verify that a fresh clone
contains real objects rather than pointer text. A checksummed release archive
or institutional data repository may be a better choice when every
collaborator cannot reliably reach the same LFS service.

Even for text-based EDA formats such as KiCad's, avoid two people performing
large layout rearrangements or automatic formatting at the same time.
Generate ERC/DRC, BOM, and key screenshots for review, while keeping the
source project authoritative. A screenshot records what someone saw; it does
not replace a rerunnable design check.

## If a secret is committed, revoke it first

`.gitignore` is not a confidentiality mechanism. A committed token remains in
history and in other clones. If a credential enters the repository, revoke or
rotate it before merely deleting the newest file. GitHub's official
[sensitive-data removal
guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
describes the consequences of a history rewrite: changed commit hashes,
affected pull requests and signatures, branch-protection coordination, and
stale collaborator clones. Rewrite only with explicit coordination and a
backup.

At the end of the exercise, the repository should contain a readable
baseline, an experimental branch with a prediction, a rebuildable tag, and
one intentional verification failure. Another reader can start from a clone,
without knowing any absolute path on your computer, and obtain the same
cutoff frequency and comparison. If the final report is visible but its
inputs and generation command are not, the repository is still only a file
cabinet.

Use [Reproducible Engineering](reproducibility.md) next to place the rebuild
under an automated check, or [Technical Writing](technical-writing.md) to
turn the branch decisions into a design review. Never store access tokens,
private keys, personal identifiers, controlled device information, or
unauthorized course solutions in the repository.
