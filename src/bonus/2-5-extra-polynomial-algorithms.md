
# More cool things that you can do with polynomials

## Polynomial Rootfinding
- Use a simple rootfinding algorithm to render algebraic number starscapes
- Include an algebraic number starscape picture
- Partial fraction decomposition is now trivial

## Fast polynomial multiplication
Implement the algorithm at:

https://www.youtube.com/watch?v=h7apO7q16V0

## Series expansion of rational functions
- Algorithm to generate the nth-term of a rational function expansion
- Berlekamp-Massey and Bostan-Mori? https://mzhang2021.github.io/cp-blog/berlekamp-massey/ https://codeforces.com/blog/entry/61306 https://codeforces.com/blog/entry/111862
- Interesting problems in the links above. At the very leasy cover the relation of a rational function to the Fibonacci sequence.

## Combinatorics results
- Algorithm to generate 

Results from ChatGPT that needs cross-referencing:

```
| label  | problem statement (length $n$)                                                                                                                                      | digraph size                               | OGF $F(x)$ (feel free to derive as exercise) | why it’s fun                                                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **R1** | binary strings with no **consecutive 1s**                                                                                                                           | 2 states                                   | $\displaystyle\frac{1}{1-x-x^{2}}$           | classic Fibonacci; good sanity test for code                                                                              |
| **R2** | words over $\{0,1\}$ avoiding the pattern **1011**                                                                                                                  | 4 states                                   | $\displaystyle\frac{1-x^{4}}{1-2x+2x^{4}}$   | order-4 recurrence—already unpleasant by hand for $n\approx 10^6$                                                         |
| **R3** | **bounded-height Motzkin** walks: steps $\{-1,0,1\}$ never dropping below 0 and never rising above height 4                                                         | 5 × 5 transfer matrix                      | $\dfrac{P(x)}{Q(x)}$ with $\deg Q=5$         | first time Dyck-like paths yield **rational** instead of Catalan-type algebraic, and coefficients explode combinatorially |
| **R4** | tilings of a $2\times n$ strip with dominoes **and** monominoes but forbidding vertical $\;\boxed{\begin{smallmatrix}\_\\\_\end{smallmatrix}}\;$ gaps of length > 2 | 7 states (encode rightmost column profile) | order-7 recurrence                           | great illustration of transfer-matrix technique + shows power of programmatic enumeration                                 |

5 Good references / problem sources
Flajolet & Sedgewick – Analytic Combinatorics, §2.3 (regular languages → rational OGFs) and §4.1 (Bostan–Mori).

R. Stanley – Enumerative Combinatorics I: Exercises 1.98, 2.36, 2.37 are perfect rationals. Solutions manual outlines transfer matrices.

Herbert Wilf – generatingfunctionology, Chs. 2–3 for gentle warm-ups; §2.6 already derives R2‐style forbidden-word examples.

M. Bóna – A Walk Through Combinatorics, Ch. 10 “The Transfer-Matrix Method” supplies lattice-strip tiling tasks much harder than R1 but still rational.

N. Bostan’s lecture notes〈free online〉 give pseudocode for the Bostan–Mori algorithm and Maple implementations.

If you want lots of exercises with automata: S. Lando – Lectures on Generating Functions has a full chapter of “counting words avoiding…”.
```

In particular I'd be interested in the connection of the transfer matrix method I know and love from the Ising and Potts models, to this phrasing and emphasis of rational functions.


## Pade approximations
 - The algorithm
 - Algebraic approximations for pi (ie expand tan(z))
 - Find the asymptotics of random walks and self-avoiding walks

n-queens should fail, but chatgpt says these might work:
 - Non-attacking rook placements → clean combinatorics, rational generating functions.
 - Domino tilings of rectangles → known recursions, matchings on graphs.
 - Catalan-type sequences → rational or algebraic generating functions.

Allegedly matrix exponentials relate to pade approximants:
https://arxiv.org/pdf/2404.12789

# The Abstract Algebra of Polynomial Division

## What properties did we see of polynomials?
- We saw how long division works for polynomials
- The example with $P_1,$ $P_2,$ $P_3$ is particularly illustrative.
- In general, a division algorithm works on something called a Euclidean Domain.

From Aluffi's "Algebra: Chapter 0", we have

**Definition 2.7.** A *Euclidean valuation* on an integral domain R is a function $v:R\setminus \{0\}\to \mathbb{Z}^{\ge 0}$ satisfying the following property: for all $a\in R$ and all nonzero $b\in R$ there exist
$q, r \in R$ such that $a = qb + r,$ with either $r = 0$ or $v(r) < v(b)$. An integral domain B is a Euclidean domain if it admits a Euclidean valuation.

So, if we have such a property, then we can always do a GCD algorithm. Each time we apply Euclidean division, we get a remainder $r$ whose valuation is one lower. 

Our Euclidean algorithm is...

```rkt
(define (gcd a b) 
  (if (apply-generic '=zero? b) a
    (gcd b (apply-generic 'remainder a b))))
```
At each step we reduce the valuation of our arguments by one. We may have a $b$ which isn't
zero but with a zero valuation, but this means that on the next step $(remainder a b)$ 
returns an element of the ring which either has lower valuation or which is equal to zero. 
Since it's not possible to have a negative valuation, this must return zero. So this
proves that the Euclidean algorithm terminates after a finite number of steps.

As we saw, things are only defined up to **units**. So we have to define units somewhere here.

Also, define coprime in this context. 

It would be nice to have a factorization algorithm, but this gets quite complicated. Kronecker's method can be mentioned.

## The Gaussian integers

### SICP-style package for the Gaussian Integers

gcd algorithm

frequency of coprime numbers



### Gaussian coprime numbers

frequency of coprime numbers

### Finding and plotting Gaussian primes

## The Eisenstein integers

gcd

coprime








https://www.semanticscholar.org/paper/A-Stroll-Through-the-Gaussian-Primes-Gethner-Wagon/7b7eb90bdbc4b37822ff92875870d0fa4d4fcc2a/figure/2
https://www.semanticscholar.org/paper/A-Stroll-Through-the-Gaussian-Primes-Gethner-Wagon/7b7eb90bdbc4b37822ff92875870d0fa4d4fcc2a/figure/4
https://www.mathpuzzle.com/Gaussians.html
http://www.asiapacific-mathnews.com/06/0602/0010_0014.pdf
