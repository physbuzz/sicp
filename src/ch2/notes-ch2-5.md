<div class="nav">
    <span class="activenav"><a href="notes-ch2-4.html">← Previous</a></span>
    <span class="activenav"><a href="../index.html">↑ Up</a></span>
    <span class="inactivenav">Next →</span>
    <!--<span class="activenav"><a href="notes-ch2-5.html">Next →</a></span>-->
</div>


[HTML Book Chapter 2.5 Link](https://sarabander.github.io/sicp/html/2_002e5.xhtml#g_t2_002e5)

@toc

## Section 2.5

Note: At the end it looks like we talk about polynomials, it might be worth skimming over some simple algorithms from Ideals, Varieties, and Algorithms and maybe implementing a simple one. 
### Introduction

### Exercises

##### Solution

#### Exercise 2.77

Louis Reasoner tries to evaluate
the expression `(magnitude z)` where `z` is the object shown in
Figure 2.24.  To his surprise, instead of the answer 5 he gets an error
message from `apply-generic`, saying there is no method for the operation
`magnitude` on the types `(complex)`.  He shows this interaction to
Alyssa P. Hacker, who says "The problem is that the complex-number selectors
were never defined for `complex` numbers, just for `polar` and
`rectangular` numbers.  All you have to do to make this work is add the
following to the `complex` package:"

```rkt
(put 'real-part '(complex) real-part)
(put 'imag-part '(complex) imag-part)
(put 'magnitude '(complex) magnitude)
(put 'angle '(complex) angle)
```

Describe in detail why this works.  As an example, trace through all the
procedures called in evaluating the expression `(magnitude z)` where
`z` is the object shown in Figure 2.24.  In particular, how many
times is `apply-generic` invoked?  What procedure is dispatched to in each
case?

##### Solution

Okay, so we've added the `put` statements. 
Implicitly, we must mean that we have also defined:

```rkt
(define (magnitude z)
  (apply-generic 'magnitude z))
```

So then the sequence of calls looks like: 

```rkt
(magnitude z)
(apply-generic 'magnitude z)
;; This calls the following inside apply-generic:
;;   (apply (get op type-tags) (map contents args))
;; type-tags is just equal to 'complex, so we call magnitude again, 
;; this time it was the magnitude scoped inside the complex package. 
;; The argument to this function is the contents of args, so inside
;; the structure ('complex . ('rectangular . (3 . 4))) we've stripped away the 'complex.
(apply-generic 'magnitude ('rectangular . (3 . 4)))
;; Inside install-rectangular-package
(magnitude (3 . 4))
5
```

TODO: make it clearer which packages we're inside.




#### Exercise 2.78

The internal procedures in the
`scheme-number` package are essentially nothing more than calls to the
primitive procedures `+`, `-`, etc.  It was not possible to use the
primitives of the language directly because our type-tag system requires that
each data object have a type attached to it.  In fact, however, all Lisp
implementations do have a type system, which they use internally.  Primitive
predicates such as `symbol?` and `number?`  determine whether data
objects have particular types.  Modify the definitions of `type-tag`,
`contents`, and `attach-tag` from 2.4.2 so that our
generic system takes advantage of Scheme's internal type system.  That is to
say, the system should work as before except that ordinary numbers should be
represented simply as Scheme numbers rather than as pairs whose `car` is
the symbol `scheme-number`.

##### Solution

So, the point of this problem is that we can make these modifications
and that's all we need to do: we need no modifications to the 
scheme-number package.

```rkt
(define (attach-tag type-tag contents)
  (if (equal? type-tag 'scheme-number) 
      contents
      (cons type-tag contents)))
(define (type-tag datum)
  (cond ((pair? datum) (car datum))
        ((number? datum) 'scheme-number)
        (else (error "Bad tagged datum: TYPE-TAG" datum))))
(define (contents datum)
  (cond ((pair? datum) (cdr datum))
        ((number? datum) datum)
        (else (error "Bad tagged datum: CONTENTS" datum))))
```

Working example:


@src(code/ex2-78.rkt)

#### Exercise 2.79

Define a generic equality
predicate `equ?` that tests the equality of two numbers, and install it in
the generic arithmetic package.  This operation should work for ordinary
numbers, rational numbers, and complex numbers.

##### Solution

#### Exercise 2.80

Define a generic predicate
`=zero?` that tests if its argument is zero, and install it in the generic
arithmetic package.  This operation should work for ordinary numbers, rational
numbers, and complex numbers.

##### Solution

#### Exercise 2.81

Louis Reasoner has noticed that
`apply-generic` may try to coerce the arguments to each other's type even
if they already have the same type.  Therefore, he reasons, we need to put
procedures in the coercion table to coerce arguments of each type to
their own type.  For example, in addition to the
`scheme-number->complex` coercion shown above, he would do:

```rkt
(define (scheme-number->scheme-number n) n)
(define (complex->complex z) z)

(put-coercion 'scheme-number 'scheme-number
              scheme-number->scheme-number)

(put-coercion 'complex 'complex 
              complex->complex)
```

**1.** With Louis's coercion procedures installed, what happens if
`apply-generic` is called with two arguments of type `scheme-number`
or two arguments of type `complex` for an operation that is not found in
the table for those types?  For example, assume that we've defined a generic
exponentiation operation:

```rkt
(define (exp x y) 
  (apply-generic 'exp x y))
```


and have put a procedure for exponentiation in the Scheme-number
package but not in any other package:

```rkt
@r{;; following added to Scheme-number package}
(put 'exp 
     '(scheme-number scheme-number)
     (lambda (x y) 
       (tag (expt x y)))) 
       @r{; using primitive `expt`}
```


What happens if we call `exp` with two complex numbers as arguments?

**2.** Is Louis correct that something had to be done about coercion with arguments of
the same type, or does `apply-generic` work correctly as is?

**3.** Modify `apply-generic` so that it doesn't try coercion if the two
arguments have the same type.



##### Solution

#### Exercise 2.82

Show how to generalize
`apply-generic` to handle coercion in the general case of multiple
arguments.  One strategy is to attempt to coerce all the arguments to the type
of the first argument, then to the type of the second argument, and so on.
Give an example of a situation where this strategy (and likewise the
two-argument version given above) is not sufficiently general.  (Hint: Consider
the case where there are some suitable mixed-type operations present in the
table that will not be tried.)

##### Solution

#### Exercise 2.83

Suppose you are designing a
generic arithmetic system for dealing with the tower of types shown in
Figure 2.25: integer, rational, real, complex.  For each type (except
complex), design a procedure that raises objects of that type one level in the
tower.  Show how to install a generic `raise` operation that will work for
each type (except complex).

##### Solution

#### Exercise 2.84

Using the `raise` operation
of Exercise 2.83, modify the `apply-generic` procedure so that it
coerces its arguments to have the same type by the method of successive
raising, as discussed in this section.  You will need to devise a way to test
which of two types is higher in the tower.  Do this in a manner that is
``compatible'' with the rest of the system and will not lead to problems in
adding new levels to the tower.

##### Solution

#### Exercise 2.85

This section mentioned a method
for ``simplifying'' a data object by lowering it in the tower of types as far
as possible.  Design a procedure `drop` that accomplishes this for the
tower described in Exercise 2.83.  The key is to decide, in some general
way, whether an object can be lowered.  For example, the complex number 
${1.5 + 0i$} can be lowered as far as `real`, the complex number ${1 + 0i$} can
be lowered as far as `integer`, and the complex number ${2 + 3i$} cannot
be lowered at all.  Here is a plan for determining whether an object can be
lowered: Begin by defining a generic operation `project` that ``pushes''
an object down in the tower.  For example, projecting a complex number would
involve throwing away the imaginary part.  Then a number can be dropped if,
when we `project` it and `raise` the result back to the type we
started with, we end up with something equal to what we started with.  Show how
to implement this idea in detail, by writing a `drop` procedure that drops
an object as far as possible.  You will need to design the various projection
operations and
install `project` as a generic operation in the system.  You will also
need to make use of a generic equality predicate, such as described in
Exercise 2.79.  Finally, use `drop` to rewrite `apply-generic`
from Exercise 2.84 so that it ``simplifies'' its answers.

##### Solution

#### Exercise 2.86

Suppose we want to handle complex
numbers whose real parts, imaginary parts, magnitudes, and angles can be either
ordinary numbers, rational numbers, or other numbers we might wish to add to
the system.  Describe and implement the changes to the system needed to
accommodate this.  You will have to define operations such as `sine` and
`cosine` that are generic over ordinary numbers and rational numbers.

##### Solution

#### Exercise 2.87

Install `=zero?` for
polynomials in the generic arithmetic package.  This will allow
`adjoin-term` to work for polynomials with coefficients that are
themselves polynomials.

##### Solution

#### Exercise 2.88

Extend the polynomial system to
include subtraction of polynomials.  (Hint: You may find it helpful to define a
generic negation operation.)

##### Solution

#### Exercise 2.89

Define procedures that implement
the term-list representation described above as appropriate for dense
polynomials.

##### Solution

#### Exercise 2.90

Suppose we want to have a
polynomial system that is efficient for both sparse and dense polynomials.  One
way to do this is to allow both kinds of term-list representations in our
system.  The situation is analogous to the complex-number example of 
2.4, where we allowed both rectangular and polar representations.  To do
this we must distinguish different types of term lists and make the operations
on term lists generic.  Redesign the polynomial system to implement this
generalization.  This is a major effort, not a local change.

##### Solution

#### Exercise 2.91

A univariate polynomial can be
divided by another one to produce a polynomial quotient and a polynomial
remainder.  For example,

$${x^5 - 1 \over x^2 - 1} \,=\, {x^3 + x,} \text{  remainder  } {x - 1.}  $$

Division can be performed via long division.  That is, divide the highest-order
term of the dividend by the highest-order term of the divisor.  The result is
the first term of the quotient.  Next, multiply the result by the divisor,
subtract that from the dividend, and produce the rest of the answer by
recursively dividing the difference by the divisor.  Stop when the order of the
divisor exceeds the order of the dividend and declare the dividend to be the
remainder.  Also, if the dividend ever becomes zero, return zero as both
quotient and remainder.

We can design a `div-poly` procedure on the model of `add-poly` and
`mul-poly`. The procedure checks to see if the two polys have the same
variable.  If so, `div-poly` strips off the variable and passes the
problem to `div-terms`, which performs the division operation on term
lists. `Div-poly` finally reattaches the variable to the result supplied
by `div-terms`.  It is convenient to design `div-terms` to compute
both the quotient and the remainder of a division.  `Div-terms` can take
two term lists as arguments and return a list of the quotient term list and the
remainder term list.

Complete the following definition of `div-terms` by filling in the missing
expressions.  Use this to implement `div-poly`, which takes two polys as
arguments and returns a list of the quotient and remainder polys.

```rkt
(define (div-terms L1 L2)
  (if (empty-termlist? L1)
      (list (the-empty-termlist) 
            (the-empty-termlist))
      (let ((t1 (first-term L1))
            (t2 (first-term L2)))
        (if (> (order t2) (order t1))
            (list (the-empty-termlist) L1)
            (let ((new-c (div (coeff t1) 
                              (coeff t2)))
                  (new-o (- (order t1) 
                            (order t2))))
              (let ((rest-of-result
                     ⟨@var{compute rest of result 
                     recursively}⟩ ))
                ⟨@var{form complete result}⟩ ))))))
```

##### Solution

#### Exercise 2.92

By imposing an ordering on
variables, extend the polynomial package so that addition and multiplication of
polynomials works for polynomials in different variables.  (This is not easy!)

##### Solution

#### Exercise 2.93

Modify the rational-arithmetic
package to use generic operations, but change `make-rat` so that it does
not attempt to reduce fractions to lowest terms.  Test your system by calling
`make-rational` on two polynomials to produce a rational function:

```rkt
(define p1 (make-polynomial 'x '((2 1) (0 1))))
(define p2 (make-polynomial 'x '((3 1) (0 1))))
(define rf (make-rational p2 p1))
```

Now add `rf` to itself, using `add`. You will observe that this
addition procedure does not reduce fractions to lowest terms.

##### Solution

#### Exercise 2.94

Using `div-terms`, implement
the procedure `remainder-terms` and use this to define `gcd-terms` as
above.  Now write a procedure `gcd-poly` that computes the polynomial
@abbr{GCD} of two polys.  (The procedure should signal an error if the two
polys are not in the same variable.)  Install in the system a generic operation
`greatest-common-divisor` that reduces to `gcd-poly` for polynomials
and to ordinary `gcd` for ordinary numbers.  As a test, try

```rkt
(define p1 
  (make-polynomial 
   'x '((4 1) (3 -1) (2 -2) (1 2))))

(define p2 
  (make-polynomial 
   'x '((3 1) (1 -1))))

(greatest-common-divisor p1 p2)
```


and check your result by hand.

##### Solution

#### Exercise 2.95

Define $P_1$, $P_2$, and
$P_3$ to be the polynomials

$$\begin{array}{rl}
  P_1:  &   x^2 - 2x + 1, \\
  P_2:  &   11x^2 + 7,    \\
  P_3:  &   13x + 5.
\end{array}
$$

Now define $Q_1$ to be the product of $P_1$ and $P_2$, and $Q_2$ to be
the product of $P_1$ and $P_3$, and use `greatest-common-divisor`
(Exercise 2.94) to compute the @abbr{GCD} of $Q_1$ and $Q_2$.
Note that the answer is not the same as $P_1$.  This example introduces
noninteger operations into the computation, causing difficulties with the
@abbr{GCD} algorithm.  To understand what is happening, try tracing
`gcd-terms` while computing the @abbr{GCD} or try performing the
division by hand.

##### Solution

#### Exercise 2.96

**1.** Implement the procedure `pseudoremainder-terms`, which is just like
`remainder-terms` except that it multiplies the dividend by the
integerizing factor described above before calling `div-terms`.  Modify
`gcd-terms` to use `pseudoremainder-terms`, and verify that
`greatest-common-divisor` now produces an answer with integer coefficients
on the example in Exercise 2.95.

**2.** The @abbr{GCD} now has integer coefficients, but they are larger than those
of $P_1$.  Modify `gcd-terms` so that it removes common factors from the
coefficients of the answer by dividing all the coefficients by their (integer)
greatest common divisor.



##### Solution

#### Exercise 2.97

**1.** Implement this algorithm as a procedure `reduce-terms` that takes two term
lists `n` and `d` as arguments and returns a list `nn`,
`dd`, which are `n` and `d` reduced to lowest terms via the
algorithm given above.  Also write a procedure `reduce-poly`, analogous to
`add-poly`, that checks to see if the two polys have the same variable.
If so, `reduce-poly` strips off the variable and passes the problem to
`reduce-terms`, then reattaches the variable to the two term lists
supplied by `reduce-terms`.

**2.** Define a procedure analogous to `reduce-terms` that does what the original
`make-rat` did for integers:

```rkt
(define (reduce-integers n d)
  (let ((g (gcd n d)))
    (list (/ n g) (/ d g))))
```

and define `reduce` as a generic operation that calls `apply-generic`
to dispatch to either `reduce-poly` (for `polynomial` arguments) or
`reduce-integers` (for `scheme-number` arguments).  You can now
easily make the rational-arithmetic package reduce fractions to lowest terms by
having `make-rat` call `reduce` before combining the given numerator
and denominator to form a rational number.  The system now handles rational
expressions in either integers or polynomials.  To test your program, try the
example at the beginning of this extended exercise:

```rkt
(define p1 
  (make-polynomial 'x '((1 1) (0 1))))
(define p2 
  (make-polynomial 'x '((3 1) (0 -1))))
(define p3 
  (make-polynomial 'x '((1 1))))
(define p4 
  (make-polynomial 'x '((2 1) (0 -1))))
(define rf1 (make-rational p1 p2))
(define rf2 (make-rational p3 p4))
(add rf1 rf2)
```

See if you get the correct answer, correctly reduced to lowest terms.

##### Solution




