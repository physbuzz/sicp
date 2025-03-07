<div class="nav">
    <span class="inactivenav">← Previous</span>
    <span class="activenav"><a href="../index.html">↑ Up</a></span>
    <span class="activenav"><a href="notes-ch1-2.html">Next →</a></span>
</div>


[https://sarabander.github.io/sicp/html/1_002e1.xhtml](https://sarabander.github.io/sicp/html/1_002e1.xhtml)

## Section 1.1


### Introduction

- Lisp, for List Processing, was invented in the late 1950s
- Seminal paper "Recursive Functions of Symbolic Expressions and Their Computation by Machine" ([McCarthy 1960](https://dl.acm.org/doi/10.1145/367177.367199))
- There are many lisp dialects, we're using Scheme introduced in [Steele and Sussman 1975](https://dspace.mit.edu/handle/1721.1/5794)
- Common Lisp was developed in the 80's and 90's to make an industrial standard.
- Cool paper [Sussman and Wisdom 1992](https://pubmed.ncbi.nlm.nih.gov/17800710/) about solar system chaos. This would be nice to compare to my own calculations where I was able to reproduce the eccentricity of [this graph](https://en.wikipedia.org/wiki/Milankovitch_cycles#/media/File:MilankovitchCyclesOrbitandCores.png) to about 100KYRs.

### 1.1.1-1.1.3

- **Definition:** *Primitive expressions* are the simplest entities the language is concerned with.
- Prefix notation is used. The operator is the leftmost element and can take an arbitrary number of elements, for example `(+ 1 2 3 4)` evaluated to 10. 
- REPL = "read-eval-print loop"
- Pretty printing is defined such that each operator with a deeper nesting starts at a deeper level of indentation. For example
```rkt
(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))
```
becomes
```rkt
(+ (* 3
      (+ (* 2 4)
         (+ 3 5)))
   (+ (- 10 7)
      6))
```
- We can associate values with variables. `(define size 2)` defines a value in a global environment.
- Evaluation can be done recursively in this model, "tree accumulation" is one way to evaluate tree expressions.
- *Special forms* are exceptions to the general evaluation rules. "define" is one of them. We deal with a very simple language -> small number of special forms.

### 1.4 

The syntax to define a procedure is
`(define (square x) (* x x))`

### 1.5

For chapters 1 and 2 we can use the substitution model, but in chapter 3 we'll need to deal with mutable data and will need a more complicated model.

Models define the "meaning" of procedure application. They're generally ways to think about procedures, rather than being ways that the interpreter actually works.

Applicative ordering vs. normal ordering. 
*Normal-order evaluation* is when the interpreter fully expands and then reduces the expression.
*Applicative-order evaluation* is when the interpreter evaluates the arguments needed for the immediate expression and then applies them.

### 1.6
New special form `cond`:
```rkt
(define (abs x)
  (cond ((> x 0) x)
        ((= x 0) 0)
        ((< x 0) (- x))))
```
Also `else`
```rkt
(define (abs x)
  (cond ((< x 0) (- x))
        (else x)))
```
Also
```rkt
(define (abs x)
  (if (< x 0)
      (- x)
      x))
```

The format for `if` statements is 
`(if predicate consequent alternative)`

There's also `and`, `or`, `not`, 

### More Notes
Bound variable, free variable, variable scope, captured variable (changing from free to bound)

### Aside on Mathematica:

`(+ 1 2 3 4)` is represented in mathematica as `Add[1,2,3,4]`. in Mathematica, this expression gets substituted with `10` immediately, but say we have another expression `expression = add[1,2,3,4]` (lowercase "A"). Then in fact `expression[[0]]` returns `add`, `expression[[1]]` returns `1`, and so on (2,3,4). So this is identical to lisp, where the operator is called the head in Mathematica (and can be retrieved through `Head[expression]` which returns `add`).

One example is that "it is meaningless to speak of the value of `(+ x 1)`". In Mathematica `add[x,1]` is perfectly meaningful even if add and x have no definitions! It is `add[x,1]`!

To translate `(define (square x) (* x x))` to Mathematica, we'd do something like 
`Set[square,Function[x,Times[x,x]]]` which I think is a bit different because `Function[x,x*x]` can be regarded as a lambda. Functions can also be defined via replacement rules and pattern matching, but that's a whole different ball game which is a core aspect of Wolfram language but we can ignore.

### Exercises

#### Exercise 1.1

Below is a sequence of expressions. What is the result printed by the interpreter in response to each expression? Assume that the sequence is to be evaluated in the order in which it is presented.

##### Solution

@src(ch1-code/ex1-1.rkt)

#### Exercise 1.2
Translate the following expression into prefix form:
$$\frac{5+4+(2-(3-(6+\frac{4}{5})))}{3(6-2)(2-7)}$$

##### Solution

@src(ch1-code/ex1-2.rkt)

#### Exercise 1.3
Define a procedure that takes three numbers as arguments and returns the sum of the squares of the two larger numbers.
##### Solution

@src(ch1-code/ex1-3.rkt)

#### Exercise 1.4

Observe that our model of evaluation allows for combinations whose operators are compound expressions. Use this observation to describe the behavior of the following procedure:

```rkt
(define (a-plus-abs-b a b)
  ((if (> b 0) + -) a b))
```
##### Solution

@src(ch1-code/ex1-4.rkt)

#### Exercise 1.5
Ben Bitdiddle has invented a test to determine whether the interpreter he is faced with is using applicative-order evaluation or normal-order evaluation. He defines the following two procedures:

```rkt
(define (p) (p))

(define (test x y) 
  (if (= x 0) 
      0 
      y))
```
Then he evaluates the expression

`(test 0 (p))`

What behavior will Ben observe with an interpreter that uses applicative-order evaluation? What behavior will he observe with an interpreter that uses normal-order evaluation? Explain your answer. (Assume that the evaluation rule for the special form if is the same whether the interpreter is using normal or applicative order: The predicate expression is evaluated first, and the result determines whether to evaluate the consequent or the alternative expression.)

##### Solution

So, `(p)` is a bomb, and whenever we evaluate it we get stuck in an infinite loop. The question is whether we encounter this bomb or not.

Using applicative order evaluation, we first evaluate both arguments. `0` evaluates to `0`, but evaluating `(p)` triggers our bomb. So our applicative order evaluator hangs or crashes. Scheme is applicative order, so we expect it to hang or crash.

Normal ordering is different, we "fully expand then reduce" but as the problem points out, the word "fully expand" does not refer to the argument of the if-statement, and so we're saved from fully expanding `(p)` right off the bat. When we evaluate `(if (= 0 0) 0 (p))`, our reduce step is smart enough to only evaluate `0`, so the expression returns `0`. I'm told this is the semantics of Haskell, so we'd expect some Haskell program implementing the same idea to run just fine.

This is the same reasoning as given in the answers to [this stackoverflow question](https://stackoverflow.com/questions/16036139/seek-for-some-explanation-on-sicp-exercise-1-5).


#### 1.6

Alyssa P. Hacker doesn’t see why if needs to be provided as a special form. “Why can’t I just define it as an ordinary procedure in terms of cond?” she asks. Alyssa’s friend Eva Lu Ator claims this can indeed be done, and she defines a new version of if:

```rkt
(define (new-if predicate 
                then-clause 
                else-clause)
  (cond (predicate then-clause)
        (else else-clause)))
```
Eva demonstrates the program for Alyssa:

```rkt
(new-if (= 2 3) 0 5)
5

(new-if (= 1 1) 0 5)
0
```

Delighted, Alyssa uses new-if to rewrite the square-root program:

```rkt
(define (sqrt-iter guess x)
  (new-if (good-enough? guess x)
          guess
          (sqrt-iter (improve guess x) x)))
```

What happens when Alyssa attempts to use this to compute square roots? Explain.

##### Solution

The key here is not the behavior of `cond` versus `if`, but in the conditional evaluation of each of the terms following the `if` special form. 

`(if cond A B)` evaluated B only on the condition that cond is false. 

But `(new-if cond A B)` will evaluate `cond`, `A`, and `B`, regardless of how `new-if` is defined (at least given what we know at this point in the text, not sure if something arises later). Since B contains a recursive function call, we immediately get infinite recursion.

#### Exercise 1.7

The `good-enough?` test used in computing square roots will not be very effective for finding the square roots of very small numbers. Also, in real computers, arithmetic operations are almost always performed with limited precision. This makes our test inadequate for very large numbers. Explain these statements, with examples showing how the test fails for small and large numbers. An alternative strategy for implementing good-enough? is to watch how guess changes from one iteration to the next and to stop when the change is a very small fraction of the guess. Design a square-root procedure that uses this kind of end test. Does this work better for small and large numbers?

##### Solution

If $y$ is our guess for $\sqrt{x}$, we can write $y=\sqrt{x}+\delta y$ and plug this into our stopping condition $|y^2-x|\lt \varepsilon$ to get:
<p>$$
\begin{align*}
\varepsilon&\approx |y^2-x|\\
&\approx |x+2\delta y \sqrt{x} - x| \\
&\;\Downarrow\\
\varepsilon&\approx 2|\delta y|\sqrt{x}
\end{align*}
$$</p>
So that our error magnitude is $\delta y\approx \varepsilon/(2\sqrt{x})$. If $x$ is very large, this means that for fixed epsilon we get a ton of digits of accuracy in $\delta y.$ If $x$ is small, we get very few digits of accuracy in $y$. 

For large $x$, I imagine there would be problems where $|y^2-x|$ cannot be less than epsilon due to floating point precision errors, but I didn't find an example of this. 

For small $x$, the implementation of the procedure demonstrates that using the fractional change as a stop condition is better.

@src(ch1-code/ex1-7.rkt)

#### Exercise 1.8
Newton’s method for cube roots is based on the fact that if y
 is an approximation to the cube root of x
, then a better approximation is given by the value
$$\frac{x/y^2+2y}{3}.$$

Use this formula to implement a cube-root procedure analogous to the square-root procedure. (In 1.3.4 we will see how to implement Newton’s method in general as an abstraction of these square-root and cube-root procedures.)

##### Solution

@src(ch1-code/ex1-8.rkt)




