# Erdős-Straus Exceptional Primes ($10^8$ Sweep Results)

**Commit SHA:** `b9c5b5494b842363890ff5aabf2713561e90388e`
**Environment:** Python 3.11.9, Windows (Antigravity Scratch Workspace)
**Command Line:** `python sweep_100m.py 100000000`
**Execution Time:** 608.5 seconds (Rate: ~476/sec)

## Execution Summary
* **Domain:** Exceptional primes $p \le 10^8$
* **Equation:** $4/p^2 = 1/x + 1/y + 1/z$
* **Total Scanned:** 289,372
* **Total Solved:** 289,372 (100%)
* **Failures:** 0
* **Mean minimal m:** 2.25
* **Max minimal m:** 39 ($A = 159$)

## Comparison vs Biased Legacy Scan

The strict ascending search proved the legacy scan's ordering bias did indeed corrupt the minimality results at the extreme tail. One prime that the legacy scan solved using $A=103$ actually possessed a smaller valid shift at $A=95$. The corrected scan reassigned this prime to its true minimal portal.

| Metric | Biased Legacy Scan | Strict Ascending Scan | Delta |
|--------|---------------------|------------------------|-------|
| $10^5$ Max m | 12 | 10 | `-2` |
| $10^7$ Max m | 27 | 25 | `-2` |
| $A=95$ hits | 1 | 2 | `+1` |
| $A=103$ hits | 8 | 7 | `-1` |

## Corrected Complete Distribution

The exact set of 22 $A$-values remains unchanged, and the skipped shifts ($27, 35, 55, 63, 75$, etc.) are **still structurally skipped** in the unbiased scan. The Bounded-A conjecture and 22-portal classification survive the debiasing, though the tail frequencies are now mathematically exact.

```
Distribution by m (A = 4m+3):
  m=  1 (A=  7): 143145 (49.47%)
  m=  2 (A= 11):  65251 (22.55%)
  m=  3 (A= 15):  27112 (9.37%)
  m=  4 (A= 19):  25644 (8.86%)
  m=  5 (A= 23):  13772 (4.76%)
  m=  7 (A= 31):   7459 (2.58%)
  m=  9 (A= 39):   3697 (1.28%)
  m= 10 (A= 43):   1325 (0.46%)
  m= 11 (A= 47):   1080 (0.37%)
  m= 12 (A= 51):    241 (0.08%)
  m= 14 (A= 59):    331 (0.11%)
  m= 16 (A= 67):     87 (0.03%)
  m= 17 (A= 71):    119 (0.04%)
  m= 19 (A= 79):     60 (0.02%)
  m= 20 (A= 83):     16 (0.01%)
  m= 21 (A= 87):     12 (0.00%)
  m= 23 (A= 95):      2 (0.00%)
  m= 25 (A=103):      7 (0.00%)
  m= 26 (A=107):      4 (0.00%)
  m= 27 (A=111):      5 (0.00%)
  m= 31 (A=127):      2 (0.00%)
  m= 39 (A=159):      1 (0.00%)
```

## Highest minimal A values (Tail)
* `p= 91267201, A=159, m= 39`
* `p= 36851929, A=127, m= 31`
* `p= 68204761, A=127, m= 31`
* `p= 10386601, A=111, m= 27`
* `p= 47985961, A=111, m= 27`
* `p= 69869809, A=111, m= 27`
* `p= 78079369, A=111, m= 27`
* `p= 98391049, A=111, m= 27`
