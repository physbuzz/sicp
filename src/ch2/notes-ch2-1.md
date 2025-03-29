<div class="nav">
    <span class="activenav"><a href="../ch1/notes-ch1-3.html">← Previous</a></span>
    <span class="activenav"><a href="../index.html">↑ Up</a></span>
    <span class="activenav"><a href="notes-ch2-2.html">Next →</a></span>
</div>


[HTML Book Chapter 2.1 Link](https://sarabander.github.io/sicp/html/2_002e1.xhtml#g_t2_002e1)

@toc

## Section 2.1


### Introduction

Test


### Exercises 

#### Exercise 2.1

Define a better version of
`make-rat` that handles both positive and negative arguments.
`Make-rat` should normalize the sign so that if the rational number is
positive, both the numerator and denominator are positive, and if the rational
number is negative, only the numerator is negative.

##### Solution

@src(code/ex2-1.rkt)

#### Exercise 2.2

Consider the problem of
representing line segments in a plane.  Each segment is represented as a pair
of points: a starting point and an ending point.  Define a constructor
`make-segment` and selectors `start-segment` and `end-segment`
that define the representation of segments in terms of points.  Furthermore, a
point can be represented as a pair of numbers: the $x$ coordinate and the
$y$ coordinate.  Accordingly, specify a constructor `make-point` and
selectors `x-point` and `y-point` that define this representation.
Finally, using your selectors and constructors, define a procedure
`midpoint-segment` that takes a line segment as argument and returns its
midpoint (the point whose coordinates are the average of the coordinates of the
endpoints).  To try your procedures, you'll need a way to print points:

```rkt
(define (print-point p)
  (newline)
  (display "(")
  (display (x-point p))
  (display ",")
  (display (y-point p))
  (display ")"))
```

##### Solution

@src(code/ex2-2.rkt)

#### Exercise 2.3

Implement a representation for
rectangles in a plane.  (Hint: You may want to make use of Exercise 2.2.)
In terms of your constructors and selectors, create procedures that compute the
perimeter and the area of a given rectangle.  Now implement a different
representation for rectangles.  Can you design your system with suitable
abstraction barriers, so that the same perimeter and area procedures will work
using either representation?

##### Solution

Super tedious! I guess this is the 1980's version of "implement these getter functions" -.-

I was tempted to implement a type system (integer switch to choose rect1 or rect2 based on the int) but I think this implementation captures the spirit of the problem.

@src(code/ex2-3.rkt)
#### Exercise 2.4

Here is an alternative procedural
representation of pairs.  For this representation, verify that `(car (cons
x y))` yields `x` for any objects `x` and `y`.

```rkt
(define (cons x y) 
  (lambda (m) (m x y)))

(define (car z) 
  (z (lambda (p q) p)))
```

What is the corresponding definition of `cdr`? (Hint: To verify that this
works, make use of the substitution model of 1.1.5.)

##### Solution

First, let's check how car works:
```rkt
(car (cons x y))
((lambda (m) (m x y)) (lambda (p q) p))
((lambda (p q) p) x y) 
x
```
So the corresponding definition of `cdr` will just have `(lambda (p q) q)` instead.

@src(code/ex2-4.rkt)

#### Exercise 2.5

Show that we can represent pairs of
nonnegative integers using only numbers and arithmetic operations if we
represent the pair $a$ and $b$ as the integer that is the product ${2^a 3^b}$.
Give the corresponding definitions of the procedures `cons`,
`car`, and `cdr`.

##### Solution

@src(code/ex2-5.rkt)
#### Exercise 2.6

In case representing pairs as
procedures wasn't mind-boggling enough, consider that, in a language that can
manipulate procedures, we can get by without numbers (at least insofar as
nonnegative integers are concerned) by implementing 0 and the operation of
adding 1 as

```rkt
(define zero (lambda (f) (lambda (x) x)))

(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))
```

This representation is known as Church numerals, after its inventor,
Alonzo Church, the logician who invented the λ-calculus.

Define `one` and `two` directly (not in terms of `zero` and
`add-1`).  (Hint: Use substitution to evaluate `(add-1 zero)`).  Give
a direct definition of the addition procedure `+` (not in terms of
repeated application of `add-1`).

##### Solution

How topical! The video ["What is PLUS times PLUS?"](https://www.youtube.com/watch?v=RcVA8Nj6HEo) just came out.

**1:**

```rkt
;; (define zero (lambda (f) (lambda (x) x)))
;; (define (add-1 n) (lambda (f) (lambda (x) (f ((n f) x)))))
(add-1 zero)
(lambda (f) (lambda (x) (f (((lambda (g) (lambda (y) y)) f) x))))
(lambda (f) (lambda (x) (f ((lambda (y) y) x))))
(lambda (f) (lambda (x) (f x)))
```

**2:**

```rkt
;; (define one (lambda (f) (lambda (x) (f x))))
;; (define (add-1 n) (lambda (f) (lambda (x) (f ((n f) x)))))
(add-1 one)
(lambda (f) (lambda (x) (f (((lambda (g) (lambda (y) (g y))) f) x))))
(lambda (f) (lambda (x) (f ((lambda (y) (f y)) x))))
(lambda (f) (lambda (x) (f (f x))))
```

**addition:**
```rkt
(define (church-add a b)
    (lambda (f) (lambda (x) ((a f) ((b f) x)))))
```

**Testing:** Yooo it works first try, nice.

To future-me/future-readers: the idea behind church-add is to first unwrap `a` and `b` so that they're simple functions that apply `f` some number of times, then apply both to `x`. 

@src(code/ex2-6.rkt)

#### Exercise 2.7

Alyssa's program is incomplete
because she has not specified the implementation of the interval abstraction.
Here is a definition of the interval constructor:

```rkt
(define (make-interval a b) (cons a b))
```

Define selectors `upper-bound` and `lower-bound` to complete the
implementation.

##### Solution
```rkt
(define (make-interval a b) (cons a b))
(Define (lower-bound int) (car int))
(Define (upper-bound int) (cdr int))
```

#### Exercise 2.8

Using reasoning analogous to
Alyssa's, describe how the difference of two intervals may be computed.  Define
a corresponding subtraction procedure, called `sub-interval`.

##### Solution

Write our two intervals as $A$ and $B$. The lower bound should be
$$\mathrm{inf}_{x\in A, y\in B}(x-y)=A_{\textrm{min}}-B_{\textrm{max}}$$
The upper bound should be
$$\mathrm{sup}_{x\in A, y\in B}(x-y)=A_{\textrm{max}}-B_{\textrm{min}}$$

```rkt
(define (sub-interval A B)
  (make-interval (- (lower-bound A) (upper-bound B)) 
                 (- (upper-bound A) (lower-bound B))))
```
#### Exercise 2.9

The width of an interval
is half of the difference between its upper and lower bounds.  The width is a
measure of the uncertainty of the number specified by the interval.  For some
arithmetic operations the width of the result of combining two intervals is a
function only of the widths of the argument intervals, whereas for others the
width of the combination is not a function of the widths of the argument
intervals.  Show that the width of the sum (or difference) of two intervals is
a function only of the widths of the intervals being added (or subtracted).
Give examples to show that this is not true for multiplication or division.

##### Solution

Addition:

Subtraction:
<div>$$\begin{align*}
\textrm{Width}_{A-B} &=
\mathrm{sup}_{x\in A, y\in B}(x-y)-\mathrm{inf}_{x\in A, y\in B}(x-y)\\
&=A_{\textrm{max}}-B_{\textrm{min}} - (A_{\textrm{min}}-B_{\textrm{max}})\\
&=\textrm{Width}_A+\textrm{Width}_B
\end{align*}$$</div>

#### Exercise 2.10

Ben Bitdiddle, an expert systems
programmer, looks over Alyssa's shoulder and comments that it is not clear what
it means to divide by an interval that spans zero.  Modify Alyssa's code to
check for this condition and to signal an error if it occurs.

##### Solution

#### Exercise 2.11

In passing, Ben also cryptically
comments: ``By testing the signs of the endpoints of the intervals, it is
possible to break `mul-interval` into nine cases, only one of which
requires more than two multiplications.''  Rewrite this procedure using Ben's
suggestion.

After debugging her program, Alyssa shows it to a potential user, who complains
that her program solves the wrong problem.  He wants a program that can deal
with numbers represented as a center value and an additive tolerance; for
example, he wants to work with intervals such as 3.5 $\pm$ 0.15 rather than
[3.35, 3.65].  Alyssa returns to her desk and fixes this problem by supplying
an alternate constructor and alternate selectors:

```rkt
(define (make-center-width c w)
  (make-interval (- c w) (+ c w)))

(define (center i)
  (/ (+ (lower-bound i) 
        (upper-bound i)) 
     2))

(define (width i)
  (/ (- (upper-bound i) 
        (lower-bound i)) 
     2))
```

Unfortunately, most of Alyssa's users are engineers.  Real engineering
situations usually involve measurements with only a small uncertainty, measured
as the ratio of the width of the interval to the midpoint of the interval.
Engineers usually specify percentage tolerances on the parameters of devices,
as in the resistor specifications given earlier.

##### Solution

#### Exercise 2.12

Define a constructor
`make-center-percent` that takes a center and a percentage tolerance and
produces the desired interval.  You must also define a selector `percent`
that produces the percentage tolerance for a given interval.  The `center`
selector is the same as the one shown above.

##### Solution

#### Exercise 2.13

Show that under the assumption of
small percentage tolerances there is a simple formula for the approximate
percentage tolerance of the product of two intervals in terms of the tolerances
of the factors.  You may simplify the problem by assuming that all numbers are
positive.

After considerable work, Alyssa P. Hacker delivers her finished system.
Several years later, after she has forgotten all about it, she gets a frenzied
call from an irate user, Lem E. Tweakit.  It seems that Lem has noticed that
the formula for parallel resistors can be written in two algebraically
equivalent ways:

$${R_1 R_2 \over R_1 + R_2}  $$


and

$${{1 \over 1 / R_1 + 1 / R_2}.}  $$

He has written the following two programs, each of which computes the
parallel-resistors formula differently:

```rkt
(define (par1 r1 r2)
  (div-interval 
   (mul-interval r1 r2)
   (add-interval r1 r2)))

(define (par2 r1 r2)
  (let ((one (make-interval 1 1)))
    (div-interval 
     one
     (add-interval 
      (div-interval one r1) 
      (div-interval one r2)))))
```

Lem complains that Alyssa's program gives different answers for the two ways of
computing. This is a serious complaint.

##### Solution

#### Exercise 2.14

Demonstrate that Lem is right.
Investigate the behavior of the system on a variety of arithmetic
expressions. Make some intervals $A$ and $B$, and use them in computing the
expressions ${A / A$} and ${A / B$}.  You will get the most insight by
using intervals whose width is a small percentage of the center value. Examine
the results of the computation in center-percent form (see Exercise 2.12).

##### Solution

#### Exercise 2.15

Eva Lu Ator, another user, has
also noticed the different intervals computed by different but algebraically
equivalent expressions. She says that a formula to compute with intervals using
Alyssa's system will produce tighter error bounds if it can be written in such
a form that no variable that represents an uncertain number is repeated.  Thus,
she says, `par2` is a ``better'' program for parallel resistances than
`par1`.  Is she right?  Why?

##### Solution

#### Exercise 2.16

Explain, in general, why
equivalent algebraic expressions may lead to different answers.  Can you devise
an interval-arithmetic package that does not have this shortcoming, or is this
task impossible?  (Warning: This problem is very difficult.)

##### Solution



