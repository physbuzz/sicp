
Just some things I'm planning on writing. I've decided:

- Most of these things will be written as standalone articles, I'll probably upload em to my site as "SICP bonus chapters and ramblings" or something. 
- 




# David's Ramblings

 - Asymptotic approximations and some notes on $\Theta$, $\Omega$, $O$. 
 - The ill-fated Santa Barbara Monte Carlo machine
 - Improving convergence
 - Some thoughts on reversibility and quantum computing
 - Polynomial long division + my grandpa!

# 1.1 Important stuff
We introduce symbols 

```rkt
+ - * / 
display newline 
if cond
and or not
```
and the concept of applicative and normal order.

# 1.2 Important stuff

- linear recursive, linear iterative, tail recursive. 
- big theta notation

Important algorithms: 

- the Euclidean `gcd` algorithm
- fast exp, fast expmod
- fib iter vs fib recursive
- prime test and fast prime (heuristic sketch OK)
- `remainder`

## Exact runtime of count-change
The solution for the number of nodes in the count-change graph 
can be written out exactly. At the very least, we can write a big 
500x500 matrix and write the number of nodes required as a function of $M^n$ 
applied to some vector. Problems like this are kind of fun, so it would be 
nice to just do this, put it in Jordan normal form. We'll end up 
with a fifth degree polynomial, and $T(n,5)=P(n) + \cos(...)$ where the "cos" is a placeholder for a bunch of complicated but finite bounded oscillatory terms.

## RSA implementation

Would be good to cover some of this

## Extra number theory
We'll need lists for this, but there's good stuff involving:

 - The extended GCD algorithm (finding $x,y$ given $a,b$ such that $ax+by=\textrm{gcd}(a,b)$)
 - Chinese remainder theorem algorithm 
 - General linear diophantine equations

# 1.3 Important Stuff

## Extra number theory stuff:

 - Calculating the Euler totient function
 - Calculating base b expansions of fractions; this isn't really talked about very much, long division feels boring but it really isn't. We *could* avoid lists here.
 - Polynomial long division. We'd need lists for this.

## Other special numbers

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

 - Challenge: Ramanujan tau function. This is some memoized code using recursion that supposedly works: [https://claude.ai/chat/374b1219-3cd8-4a9e-87a3-dfddfc1f8896](https://claude.ai/chat/374b1219-3cd8-4a9e-87a3-dfddfc1f8896), but simple mathematica code can generate it too: `CoefficientList[Take[Expand[Product[(1 - x^k)^24, {k, 1, 30}]], 30],x]`

## Continued fraction expansion of 1/pi?
 It could be cool to plot the frequency of numbers in the continued fraction expansion of pi or 1/pi, if this is "easily" done with exact arithmetic.

## Numerical approximation formulas
I think there's a story to tell here starting with...

 - The nested function approximation for sine. (Who came up with this first? Is there an interesting functional equation from the polynomial?) 
 - The nested function approximation for the feigenbaum function ([this writing by Wolfram](https://writings.stephenwolfram.com/2019/07/mitchell-feigenbaum-1944-2019-4-66920160910299067185320382/) and the code used to generate [this image](https://content.wolfram.com/sites/43/2019/07/feigenbaum-function.png) - click on the image in the article to get the code). I think it can be casted in the same form as the polynomial version: iterated function -> scaled up. See also [Simone Conradi's work](https://mathstodon.xyz/@S_Conradi). This is the solution of the Feigenbaum-Cvitanović functional equation.
 - Other nested functions? I think Simone Conradi also posted code involving $f(f(x))=\sin(x)$. Hell, might as well email Conradi and also Cvitanovic while I'm at it.
 - LLMs recommended studying Schroder's equation and the Abel equation, but I don't quite understand this.

## Improving rates of convergence
I went on a tangent during our meeting about rates of convergence, so a few things could be:
 - How fast Newton's method converges (it's great)
 - Newton's method in multiple variables, maybe?
 - Successive averaging
 - Resummation schemes

# 2.1

## Algorithm to Draw Church Numerals
algorithm to draw church numerals in the style of the "what is PLUS times PLUS"  video.


# 2.2 

## Note on all of the useful library functions in SICP
It would be useful to collect all the functions. fold-left, fold-right, accumulate, yadda yadda. One of the best parts of Mathematica is giving these standard names.

## Enumerations
enumerating partitions, enumerating binary trees (rather than just counting), enumerating expressions?

## Crash course on symbols?
The problems here are super tedious without use of `'()` and an understanding of these things, which the book kind of glosses over.

## All about n-queens and dancing links!
TBD






