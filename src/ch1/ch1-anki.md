

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
## Question
### Statement
### Answer
