
# Chapter 1.1
## Question
### Statement
What does Lisp stand for? REPL? What are prefix/postfix/infix? What is a "combination" in Lisp?

### Answer

Lisp = "List Processing". REPL = Read-Eval-Print-Loop. Prefix = `(+ a b)`. Postfix might look something like `(a b +)`. Infix would be `(a + b)`.

A combination is term in parentheses of the form `(a b c ...)` where `a` is the operator and `b c ...` are the operands.

## Question
### Statement
How do you define a named constant in Lisp? A named function?
### Answer
Named variable: `(define pi 3.14159)`

Named function: `(define (square x) (* x x))`

## Question
### Statement
Exercise 1.5: how does this procedure evaluate using normal order? Using applicative order?
```rkt
(define (p) (p))
(define (test x y) 
  (if (= x 0) 0 y))
(test 0 (p))
```
### Answer
This is a point of confusion! Using applicative order, we first evaluate the arguments of `test`. One of these is a recursive bomb, so it gets implement recursion right away. This is how Scheme evaluates things, so this program will blow up.

In normal order evaluation, we don't evaluate the arguments right away, and in fact `if` is a special form with an evaluation rule such that in applicative or normal order the unused argument is not evaluated if it doesn't need to be. So `(if (= 0 0) 0 (p))` never evaluates `(p)`. The argument isn't 100% convincing to me, but the bottom line is that Haskell uses normal order evaluation and in Haskell the analogue of `test 0 p` runs just fine, with `p` never evaluating its infinite recursive call.

## Question
### Statement
Loosely define the substitution model of evaluation of a Scheme program, and write out the evaluation of `(f 5)` in the program below using the substitution model.
```rkt
(define (square x) (* x x))
(define (sum-of-squares x y)
  (+ (square x) (square y)))
(define (f a)
  (sum-of-squares (+ a 1) (* a 2)))
(f 5)
```
### Answer
The substitution model is just obtained by evaluating function arguments and then substituting the definitions of the smallest sub-expressions that can be evaluated. 

```rkt
(f 5)
(sum-of-squares (+ 5 1) (* 5 2))
(sum-of-squares 6 10)
(+ (square 6) (square 10))
(+ (* 6 6) (* 10 10))
(+ 36 100)
136
```

## Question
### Statement
How do you write `if` and `cond` statements in Scheme? What's special about their evaluation?
### Answer
`(if bool a b)` is a *special form* which evaluates `bool` and then evaluates `a` if bool is true or `b` if bool is false. 
This breaks the strict rule of applicative order evaluation, which might lead you to believe that `bool a b` are all evaluated.

`cond` is another way to achieve conditional evaluation. Here we see how to evaluate `e1`, `e2`, or `e3` based on Boolean predicates `p1` and `p2`.
```rkt
(cond (p1 e1)
    (p2 e2)
    (else e3))
```

# Chapter 1.2

## Question
### Statement
Write out the linear recursive and linear iterative factorial functions.

### Answer

Linear recursive:
```rkt
(define (factorial n)
  (if (= n 1) 
      1 
      (* n (factorial (- n 1)))))
```
This is "linear recursive" because the size of the "call stack" grows linearly.

Linear iterative:
```rkt
(define (factorial n) 
  (fact-iter 1 1 n))

(define (fact-iter product counter max-count)
  (if (> counter max-count)
      product
      (fact-iter (* counter product)
                 (+ counter 1)
                 max-count)))
```
This is not linear recursive, but it is linear iterative, and it is an example of tail-recursion.

## Question
### Statement
Write out the tree recursive and linear iterative Fibonacci functions.
### Answer
Tree recursive:
```rkt
(define (fib n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fib (- n 1))
                 (fib (- n 2))))))
```
Linear iterative:
```rkt
(define (fib n) 
  (fib-iter 1 0 n))

(define (fib-iter a b count)
  (if (= count 0)
      b
      (fib-iter (+ a b) a (- count 1))))
```
## Question
### Statement
What are the $\Theta(n)$ time and space requirements for the linear recursive factorial algorithm? For the linear iterative factorial algorithm?
### Answer
The linear recursive version is $\Theta(n)$ time and space.

The linear iterative version is $\Theta(n)$ time and $\Theta(1)$ space.
## Question
### Statement
What are the $\Theta(n)$ time and space requirements for the linear recursive Fibonacci algorithm? For the tree recursive version?
### Answer
The linear iterative version is $\Theta(n)$ time and $\Theta(1)$ space.

The tree-recursive Fibonacci algorithm takes $\Theta(\varphi^n)$ steps and $\Theta(n)$ space.
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
## Question
### Statement
### Answer
