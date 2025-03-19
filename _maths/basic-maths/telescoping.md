---
layout: default
title: Telescoping
parent: basic-maths
grand_parent: Maths
nav_order: 1
---



# Telescoping
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

Any series/sum/product that looks something like:

$$
\sum_{r=n_{\text{lower}}}^{n_{\text{upper}}} \left( f(r+1) - f(r) \right)
$$

That, or---


$$
\sum_{r=a}^{b} \left( f(r+3) - f(r-1) \right)
$$

This... or---

$$
\prod_{r=a}^{b} \left( \frac{f(r+3)}{f(r-1)} \right)
$$


_(You get the point)_ is called a Telescopic series.

## The Boring Method
Now typically one would solve this by **cancelling out the terms**, for example, take:

$$
\sum_{r=1}^{n} \left( \frac{1}{r+1} - \frac{1}{r} \right)
$$

You'd typically put the values, and write out a few  \\(T_n\\) terms to find out which ones get cancelled, like:

$$
\begin{aligned}
T_1 &= \frac{1}{2} - \frac{1}{1}\\
T_2 &= \frac{1}{3} - \frac{1}{2}\\
T_3 &= \frac{1}{4} - \frac{1}{3}\\
...\\
\end{aligned}
$$


It must be obvious, that the **left diagonal** or (top-left to bottom-right) are getting cancelled.

Since \\(S_n\\) (Sum of n terms) is \\(T_1+T_2+T_3+...\\),

\\(S_n\\) reduces to:

$$
S_n = \frac{1}{n+1} - \frac{1}{1}
$$

And then you put whatever values are given. But clearly this method will be **REALLY PAINFUL** when dealing with larger functions or series with a gap in them like: \\(\sum_{r=1}^{n} ((r+3)-(r-1))\\).


## The Hacks



## Bibliography
- [Telescoping - Anshul Sir (Youtube Video) [Main source]](https://www.youtube.com/live/7zmFMZmwX3U)
- [Sequence and Series Class 11 - Arvind Kalia Sir (Youtube Oneshot)](https://www.youtube.com/watch?v=ZbpePu2KDKY)
- [Sophie Germain's identity (wikipedia)](https://en.wikipedia.org/wiki/Sophie_Germain%27s_identity)
