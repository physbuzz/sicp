
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
```
(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))
```
becomes
```
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
```
(define (abs x)
  (cond ((> x 0) x)
        ((= x 0) 0)
        ((< x 0) (- x))))
```
Also `else`
```
(define (abs x)
  (cond ((< x 0) (- x))
        (else x)))
```
Also
```
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

#### 1.1

@import()






