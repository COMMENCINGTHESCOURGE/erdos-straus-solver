# Empirical Note: A Finite Shift Classification of Exceptional Primes in the Erdős–Straus Conjecture

**Author:** DaShawn McLaughlin  
**Affiliation:** Guinea Pig Trench LLC  
**Date:** July 2026  

---

## Abstract

The Erdős–Straus conjecture asserts that the Diophantine equation
$$\frac{4}{n} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}$$
is solvable in positive integers $x, y, z$ for all integers $n \ge 2$. For prime denominators $n = p$, solutions are structurally guaranteed by residue modular classes unless $p \equiv 1 \pmod{12}$ and the value $c = (p+3)/4$ has no prime factor $q \equiv 2 \pmod{3}$. Such primes are termed **exceptional**.

Using a two-stage parallelized modular sieve (the "Omega Solver" architecture) implemented across distributed cloud nodes, we perform a complete empirical search for the minimal additive shifts $A \equiv 3 \pmod{4}$ yielding integer solutions of the **prime-square equation** $4/p^2 = 1/x + 1/y + 1/z$ (with $x = (p^2 + A)/4$) for all $289,372$ exceptional primes up to $p \le 10^8$.

> **Note on scope:** The solver operates on $n = p^2$, not $n = p$. A solution for $4/p^2$ does not automatically descend to a solution for $4/p$ without a separate descent theorem. All claims in this document refer to the prime-square case.

Our calculations reveal three key results:

1. **The 22-Portal Classification**: Every exceptional-prime-indexed prime square $p^2$ (for $p \le 10^8$) resolves using exactly one shift value from a finite set of 22 distinct integers:
   $$\mathcal{A} = \{7, 11, 15, 19, 23, 31, 39, 43, 47, 51, 59, 67, 71, 79, 83, 87, 95, 103, 107, 111, 127, 159\}$$
   with a maximum minimal shift $A = 159$ occurring at $p = 91,267,201$.
2. **Disjointness and the Squareful Barrier**: We compare our solutions against the parametric covering solutions proposed by Bradford (arXiv:2602.11774) for $n \equiv 1 \pmod{24}$. We demonstrate $0.0\%$ agreement in the $(y, z)$ denominators. Furthermore, we identify a structural "Squareful Barrier"—showing that Bradford's parametric families fail to provide valid integer solutions for all squareful denominators $n$, whereas our finite additive shift solver handles these configurations without exception.
3. **Distribution Dynamics**: We show that $A=7$ dominates the coverage at $\approx 49.5\%$, followed by $A=11$ ($22.6\%$) and $A=15$ ($9.4\%$), showing a stable probability distribution across multiple scales of magnitude.

These results provide strong empirical evidence for the **Bounded-A Conjecture**—suggesting that the prime-square exceptional case ($4/p^2$) is covered by a finite set of residue classes of bounded shift magnitude. Whether this extends to the original Erdős–Straus case ($4/p$) requires a descent theorem.

---

### Key Data Summary

| Bound ($p$) | Exceptional Primes Found | Unique $A$-Values Used | Max minimal $A$ |
| ----------- | ------------------------ | ---------------------- | --------------- |
| $10^5$      | $606$                    | $8$                    | $43$            |
| $10^6$      | $4,540$                  | $12$                   | $71$            |
| $10^7$      | $35,750$                 | $17$                   | $103$           |
| $10^8$      | $289,372$                | $22$                   | $159$           |

### Shift Distribution table (up to $10^8$)

* **$A = 7$** ($m = 1$): $143,145$ cases ($49.47\%$)
* **$A = 11$** ($m = 2$): $65,251$ cases ($22.55\%$)
* **$A = 15$** ($m = 3$): $27,112$ cases ($9.37\%$)
* **$A = 19$** ($m = 4$): $25,644$ cases ($8.86\%$)
* **$A = 23$** ($m = 5$): $13,772$ cases ($4.76\%$)
* **Other $A \ge 31$**: $14,448$ cases ($4.99\%$)
