<div class="nav">
    <span class="inactivenav">← Previous</span>
    <span class="activenav"><a href="../index.html">↑ Up</a></span>
    <span class="inactivenav">Next →</span>
</div>

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
@src(ch1-code/ex1-6.rkt)


