

@toc 


# Symbols and SICP Library Functions
## Symbols and Special Forms
**Chapter 1.1:**
```rkt
+ - * / 
display newline 
if cond
and or not
```

**Chapter 1.2:** 
```rkt
remainder
display
(runtime)
```

**Chapter 1.3:** 
```rkt
lambda
let
error
```

**Chapter 2.1:** 
```rkt
cons
car, cdr
pair?
```
**Chapter 2.2:** 
```rkt
nil ; More commonly '() or (list)
list
list-ref, length
cadr, caddr
append
map
```

# Asymptotic approximations and some notes on $\Theta$, $\Omega$, $O$. 

As we're reading [SICP](), the book covers the notation $\Theta(f(n))$ and makes use of it, but I think
it deserves a bit more context and grounding in mathematical methods! Comp sci books don't (in my opinion)
do a good job of selling asymptotic methods, but in fact they're powerful applied mathematical methods.
So I wanted to write this to provide some cool examples from physics as well as list some bonus resources. 

## Useful definitions

To start out, assuming you've read section 1.2 in SICP, you know the definition of $\Theta(f(n))$. To 
write it more succinctly using quantifiers $\exists$ and $\forall$:

**Definition.** For positive functions $f(n)$ and $R(n)$, we write that $R(n)$ is $\Theta(f(n))$ as $n\to\infty$ if:
$$\exists_{c_1,c_2,N}:\forall_{n\gt N}\;\; 0 \leq c_1 f(n) \leq R(n)\leq c_2 f(n)$$

That's fine and all, but a more typical approach is found in *The Algorithm Design Manual* by Skiena. We first define $O(n)$ and $\Omega(n),$ and define $\Theta(n)$ in terms of them.

**Definition.** We write that $R(n)$ is $O(f(n))$ as $n\to \infty$ if
$$\exists_{c,N}:\forall_{n\gt N}\;\; R(n)\leq c \cdot f(n)$$
$R(n)=O(f(n))$ is a statement that the growth rate of $R(n)$ is bounded above by $f(n)$ times a constant, for sufficiently large $n.$
 
**Definition.** We write that $R(n)$ is $\Omega(f(n))$ as $n\to\infty$ if
$$\exists_{c,N}:\forall_{n\gt N}\;\; 0 \leq c \cdot f(n) \leq R(n)$$
$R(n)=\Omega(f(n))$ is a statement that the growth rate of $R(n)$ is bounded below by $f(n)$ times a constant, for sufficiently large $n.$

These two statements can also be written $R(n)=O(f(n))$ and $R(n)=\Omega(f(n)).$ With those two definitions, we then say that $R(n)=\Theta(f(n))$ if $R(n)=\Omega(f(n))$ and $R(n)=O(f(n)).$ 

This is great, and now there's another super useful notation. This is introduced in *Concrete Mathematics* by Graham, Knuth, and Patashnik as $f(n)\succ g(n),$ but I know it with the notation used in Skiena, $f(n)\gg g(n).$ This is read out loud as "$f(n)$ dominates $g(n)$." The symbol used in Concrete Mathematics is $\succ$ or `\succ`, so I suppose you could also read this as 
"$f(n)$ succeeds $g(n)$" as a mnemonic for the LaTeX, if you prefer that symbol. Anyways, its definition...

**Definition.** We write $f(n)\gg g(n)$ as $n\to a$ if $\lim_{n\to a} \frac{g(n)}{f(n)}=0.$ This definition gives:
$$n!\gg 2^n \gg n^3\gg n^2\gg n\log n\gg n\gg \log n \gg 1$$

Finally, the most useful tool of all is $\sim,$ which is used when the ratio of two functions doesn't approach zero or infinity, but approaches $1$ instead. "$\sim$" is read as "is asymptotic to."

**Definition.** $f(n)\sim g(n)$ as $n\to a$ if $\lim_{n\to a} \frac{g(n)}{f(n)}=1.$

Before we get too far afield, let's use this to solve a problem from SICP.

## Using asymptotics to solve recurrence relations.

I found that for exercise **1.14** we end up really wishing we had a bigger asymptotics toolbelt!

For my solution of the exercise, I dealt with a function $T(a,n)$ representing the 
number of nodes needed to evaluate the relevant function. We end up with a series of recurrence relations:

<div>$$\begin{align*}
T(a,1)&=T(a-1,1)+2\\
T(a,2)&=T(a,1)+T(a-5,2)+1\\
T(a,3)&=T(a,2)+T(a-10,3)+1\\
T(a,4)&=T(a,3)+T(a-25,4)+1\\
T(a,5)&=T(a,4)+T(a-50,5)+1
\end{align*}$$</div>

Okay, let's start by solving this exactly. I'll admit my recurrence relation solving skills aren't great, but $T(a,1)$ is easy,
we have $T(a,1)=2a+C^{(1)}$ where $C^{(1)}=T(1,0)$. We note that $T(a,1)=\Theta(a)$, and that $T(a,1)\sim 2a$ as $a\to\infty.$ Theta gives
us the order, and $\sim$ gives us the constant out front.

Next, $T(a,2)=T(a-5,2)+2a+C^{(1)}+1.$ This is tougher, but it has general solution:


<div>$$T(a,2)=\frac{a^2+(6+C^{(1)})a}{5}+C^{(2)}_{a\textrm{ mod }5}$$ </div>
where the $C^{(2)}_{a\textrm{ mod }5}$ are determined by the base cases, just like $C^{(1)}$ was determined by the initial conditions,
of which we need five.  

The big takeaways are $T(a,2)=\Theta(a^2)$ and $T(a,2)\sim a^2/5.$

Okay, we can guess that we should really just look at the leading / dominant terms. Then we need to solve the equation:
$$T(a,3)=T(a-10,3)+T(a,2)+1$$ 

Every time $a$ increases by $10,$ we add a term of magnitude asymptotic to $a^2/5.$ So performing the same trick more explicitly...

<div>$$\begin{align*}
T(a,3)=(T(a,2)+1)+(T(a-10,2)+1)+\ldots +T(a\textrm{ mod } 5,3)
\end{align*}$$</div>

How about $T(a,3)$ and $T(a,4)$? Well, at this point it's 
good to take a step back. We really don't need the exact solutions. Instead, we see that $T(a,1)=\Theta(a)$, 
$T(a,2)=\Theta(a^2)$, and so we would like to justify $T(a,3)=\Theta(a^3)$ all the way up to 
$T(a,5)=\Theta(a^5).$ 

## An aside on asymptotic series and Stirling's approximation

The notion of the Stirling approximation also came up in conversation, and that's a good thing because the asymptotics
learned so far allow us to tackle some weird aspects of it. Stirling's approximation can be written as:

$$\log(n!)=n\log(n)-n+\frac{1}{2}\log(2\pi n) + \sum_{k=2}^M \frac{(-1)^k B_k}{k(k-1)n^{k-1}} + O\left(\frac{1}{n^M}\right)$$

This formula has two awkward aspects compared to the power series and Taylor expansions we're usually familiar with:
1. In a Taylor series we have good reason to choose $x^k$ as our basis functions
and we're guaranteed that a Taylor series of an analytic function is unique. But how do we justify expanding $\log(n!)$
in terms of $n\log(n)$? How unique is this series?
2. If we look at the coefficients $B_k,$ the Bernoulli numbers, we find that they grow very quickly. If we try to take
$M\to\infty$ then this sum doesn't converge for any finite $n$! What gives?

An asymptotic series is defined as follows. Note that writing the upper limit of the sum as infinity is an abuse of notation---*we never actually carry out the infinite sum*.

**Definition.** We write $\sum_{i=1}^\infty f_i(n) \sim g(n)$ as $n\to a$ if:

 - $f_1(n)\sim g(n)$ as $n\to a$
 - The remainder is asymptotic to $f_2$: $g(n)-f_1(n)\sim f_2(n)$ as $n\to a$
 - That remainder is asymptotic to $f_3$: $g(n)-f_1(n)-f_2(n)\sim f_3(n)$, and so on $(\textrm{as }n\to a).$ 

With these definitions, we can get a whole theory of asymptotic series along with uniqueness guarantees, such as those in 
Bender and Orszag's *Advanced Mathematical Methods for Scientists and Engineers*.

## Another application of asymptotic series

Stirling's approximation is kind of bougie as the kids say. Too rich for my blood. 
There's another simpler example of asymptotic series that I really like. 

Say that you're stuck on a desert island with only sand and the integral

$$f(a)=\int_0^\infty \frac{e^{-a x}}{1+x} \mathrm{d}x.$$

You have to compute $f(0.1),$ how do you do it?
Well, let's use a series expansion and totally ignore issues of convergence and real analysis:
<div>$$\begin{align*}
\int_0^\infty \frac{e^{-a x}}{1+x} \mathrm{d}x &= \int_0^\infty e^{-x/a}\sum_{n=0}^\infty (-1)^n x^n \mathrm{d}x \\
&= \sum_{n=0}^\infty \int_0^\infty (-1)^n e^{-x/a} x^n \mathrm{d}x \\
&= \sum_{n=0}^\infty (-1)^n n!a^{n+1} \tag{integrate by parts}\\
\end{align*}$$</div>
This infinite sum has a radius of convergence of zero! However if we plug in $a=0.1$ and keep the first few terms, we get
$$f(0.1)\approx 0.1 - 0.01 + 0.002 - 0.0006 + 0.00024=0.09164$$
compare this to the true value of $f(0.1)=0.0915633\ldots,$ it's a pretty good approximation!

Really what we've shown is that as an asymptotic series,
$$\int_0^\infty \frac{e^{-a x}}{1+x} \mathrm{d}x \sim \sum_{n=0}^\infty (-1)^n n!a^{n+1} \tag{as $a\to 0$}$$

Another interesting tidbit: We shouldn't have expected any analytic behavior as $a\to 0,$ because if we take $a$ negative the integral diverge.

I learned this from Bender and Orszag's "Advanced Mathematical Methods for Scientists and Engineers: Asymptotic Methods and Perturbation Theory". The title is a mouthful, and it comes across a lot better in video format. Carl Bender writes a lot of these equations with a smile on his face, because $\sum_{n-1}^\infty (-1)^n n!$ is an absurd sum and is kind of a joke! To a physicist or applied mathematician, what we mean by the infinite sum is really $f(1)$ where $f$ is the perfectly well-defined transcendental function given as an integral above.

<iframe width="560" height="315" src="https://www.youtube.com/embed/LYNOGk3ZjFM?si=ulaELbRC-a_tg0VM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Other Resources and Summary

Okay, so followup books are:

 - *The Algorithm Design Manual* by Skiena
 - *Concrete Mathematics* by Graham, Knuth, and Patashnik

And then into the stuff that's more for the combinatorics and theoretical physicist peeps:

 - *Generatingfunctionology* by Wilf
 - *Advanced Mathematical Methods for Scientists and Engineers* by Bender and Orszag
 - *Analytic Combinatorics* by Sedgewick and Flajolet

I know a lot of this stuff from statistical mechanics, statistical field theory, and quantum field theory. So you can imagine the reference list and topic list could explode to infinite length here. Important integrals are...

- The formula that forms the basics of Feynman diagrams, which are terms in an asymptotic series. The fast growth rate of these
coefficients means that the series doesn't typically converge, and so we're dealing with asymptotics.
$$\int_{-\infty}^\infty x^{2n}e^{-x^2/2}/\sqrt{2\pi} \mathrm{d}x = (2n-1)!!$$ 

- The [Sommerfeld expansion](https://en.wikipedia.org/wiki/Sommerfeld_expansion) of Fermi-Dirac statistics (for example, the electrons in a metal at room temperature are well-described by a degenerate Fermi-Dirac gas). Note that for large $\beta$ (=low temperature), the function $\frac{1}{e^{\beta x}+1}$ looks like a step function. So we get the answer for the step function, plus a correction term when $\beta$ is less-than-infinite. A step function isn't very analytic, and so this also explains why we have an asymptotic series instead of a convergent power series.
<div>$${\displaystyle \int _{-\infty }^{\infty }{\frac {H(\varepsilon )}{e^{\beta (\varepsilon -\mu )}+1}}\,\mathrm {d} \varepsilon =\int _{-\infty }^{\mu }H(\varepsilon )\,\mathrm {d} \varepsilon +{\frac {\pi ^{2}}{6}}\left({\frac {1}{\beta }}\right)^{2}H^{\prime }(\mu )+O\left({\frac {1}{\beta \mu }}\right)^{4}}$$</div>


# The ill-fated Santa Barbara Monte Carlo machine

# Exact runtime of count-change
The solution for the number of nodes in the count-change graph 
can be written out exactly. At the very least, we can write a big 
500x500 matrix and write the number of nodes required as a function of $M^n$ 
applied to some vector. Problems like this are kind of fun, so it would be 
nice to just do this, put it in Jordan normal form. We'll end up 
with a fifth degree polynomial, and $T(n,5)=P(n) + \cos(...)$ where the "cos" is a placeholder for a bunch of complicated but finite bounded oscillatory terms.
# RSA implementation
# Linear diophantine equations 
 - The extended GCD algorithm (finding $x,y$ given $a,b$ such that $ax+by=\textrm{gcd}(a,b)$)
 - Chinese remainder theorem algorithm 
 - General linear diophantine equations
# Bonus number theory (Euler totient, base b expansions of fractions)

 - We emphasized the Fibonacci numbers, what about algos for the Lucas numbers?
 - Partition function algorithm
 - Do any cool algorithms arise from the generating functions?
 - Pretty sure there's a catalan number algorithm in plain sight here. 
 - Negative binomial numbers. Maybe do this after the matrix stuff? There's a cool way that the square of an alternating pascal number matrix gives you the identity matrix
```mathematica
alternatingpascal[n_] := 
  Table[Table[If[i <= j, (-1)^i Binomial[j, i], 0], {i, 0, n}], {j, 
    0, n}];
alternatingpascal[10] . alternatingpascal[10] // MatrixForm
```
# Bonus special numbers (Lucas, Catalan, partition numbers, "negative binomial")
# Numerical approximation formulas 
(iterated polynomial gives sine, other iterated special polynomials give special things too)
I think there's a story to tell here starting with...

 - The nested function approximation for sine. (Who came up with this first? Is there an interesting functional equation from the polynomial?) 
 - The nested function approximation for the feigenbaum function ([this writing by Wolfram](https://writings.stephenwolfram.com/2019/07/mitchell-feigenbaum-1944-2019-4-66920160910299067185320382/) and the code used to generate [this image](https://content.wolfram.com/sites/43/2019/07/feigenbaum-function.png) - click on the image in the article to get the code). I think it can be casted in the same form as the polynomial version: iterated function -> scaled up. See also [Simone Conradi's work](https://mathstodon.xyz/@S_Conradi). This is the solution of the Feigenbaum-Cvitanović functional equation.
 - Other nested functions? I think Simone Conradi also posted code involving $f(f(x))=\sin(x)$. Hell, might as well email Conradi and also Cvitanovic while I'm at it.
 - LLMs recommended studying Schroder's equation and the Abel equation, but I don't quite understand this.
# Improving rates of convergence
I went on a tangent during our meeting about rates of convergence, so a few things could be:
 - How fast Newton's method converges (it's great). Accelerated newton
 - Newton's method in multiple variables, maybe?
 - Successive averaging
 - Resummation schemes

# Ramanujan tau function

✯ Challenge 1: try to compute the Ramanujan tau function. This is some memoized code using recursion that supposedly works: [https://claude.ai/chat/374b1219-3cd8-4a9e-87a3-dfddfc1f8896](https://claude.ai/chat/374b1219-3cd8-4a9e-87a3-dfddfc1f8896), but simple mathematica code can generate it too: `CoefficientList[Take[Expand[Product[(1 - x^k)^24, {k, 1, 30}]], 30],x]`

# Continued fraction expansion of pi
 Challenge 2: Continued fraction expansion of pi or 1/pi using exact arithmetic.

# Reversibility and Quantum Computing

# Drawing Church numerals
algorithm to draw church numerals in the style of the "what is PLUS times PLUS"  video.
# Enumerating binary trees and arithmetic expressions
enumerating partitions, enumerating binary trees (rather than just counting), enumerating expressions?
# n queens and dancing links
# Story about polynomial long division + my grandpa

<div>$$\begin{align*}
\end{align*}$$</div>
<div>$$\begin{align*}
\end{align*}$$</div>
<div>$$\begin{align*}
\end{align*}$$</div>
Well, I mentioned something about measuring asymptotics in a lab. The most famous example of this is the 
polymer statistics of the self-avoiding walk: A long polymer in a solution tends to scrunch up, but it is not a 
random walk because the links of a polymer are physical object and can't overlap with each other. Instead it's a self-avoiding
walk. If the self-avoiding walk has $N$ links, then the expected end-to-end distance is $R(N)\sim N^\nu$. For the random walk
$\nu=1/2.$ For the self-avoiding walk, $\nu$ is known as a critical exponent and 
