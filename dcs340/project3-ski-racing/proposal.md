# DCS 340 Project III Proposal: Ski Racing-Line Optimizer

**Status: in progress**

Kyle Robin and Liam Baron

Repo: [github.com/krobin2005/ski-racing-line-optimizer](https://github.com/krobin2005/ski-racing-line-optimizer)

## 1) Question

Can evolution find a faster line down a real World Cup Giant Slalom course than the world's best skiers? And can it beat gradient descent on the same problem?

## 2) Why evolutionary computing

In GS, a direct line is shorter but forces tight, slow turns, while a rounder line keeps your speed but covers more ground. You also can't miss a gate or crash. That makes for a bumpy problem with lots of rules and lots of local optima, which is where gradient descent tends to get stuck and evolution can do well.

## 3) Approach

We built a skier simulator in Python and ran it on the real 3D terrain of the Gran Risa in Alta Badia, Italy, using the same course as the December 2025 men's World Cup GS. Each line is scored like a real race run, including the chance of crashing out. Then we had several algorithms try to find the fastest line with the same amount of computing time. This project isn't part of a thesis or another class.

## 4) Evolutionary techniques

We used CMA-ES, a genetic algorithm we wrote ourselves, and a hybrid that starts with CMA-ES and finishes with gradient descent. We compared them against plain gradient descent and a grid search. We also tried two different ways of describing a line to see how much that choice matters.

## 5) Status

The project is basically done. CMA-ES found a line about a second and a half faster than the real winning run. We also made a race video where every algorithm's best line races head to head, and a walkthrough notebook for people who haven't taken this class.

## 6) What's left

We still need to write our reflections with the GenAI disclosure, then do the show and tell and our interviews in December.

## 7) Team roles

We did the whole project together, every session and every prompt. We switched between our two laptops because of Claude usage limits, so the commit history doesn't show who did what. We both worked on and can explain every part of it.

## 8) Audience

Anyone who has taken DCS 211 or 229 but not this class.

## 9) GenAI use

We used Claude Code to help with the code, tests and race video, and we'll lay that out in our GenAI disclosure. The README and our reflections will be in our own words.
