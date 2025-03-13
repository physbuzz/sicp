#lang sicp

(define (square n) (* n n))
(define (smallest-divisor n)
  (find-divisor n 2))

(define (find-divisor n test-divisor)
  (cond ((> (* test-divisor test-divisor) n) 
         n)
        ((divides? test-divisor n) 
         test-divisor)
        (else (find-divisor 
               n 
               (nextdiv test-divisor)))))

(define (divides? a b)
  (= (remainder b a) 0))

(define (prime? n)
  (= n (smallest-divisor n)))

(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder
          (square (expmod base (/ exp 2) m))
          m))
        (else
         (remainder
          (* base (expmod base (- exp 1) m))
          m))))
(define (fermat-test n)
  (define (try-it a)
    (= (expmod a n n) a))
  (try-it (+ 1 (random (- n 1)))))

(define (fast-prime? n times)
  (cond ((= times 0) true)
        ((fermat-test n)
         (fast-prime? n (- times 1)))
        (else false)))


(define (nextdiv test-divisor)
  (if (= test-divisor 2) 
    3 
    (+ test-divisor 2)))

(define (timed-prime-test n start-time)
  (if (fast-prime? n 10)
    (begin 
      (display n)
      (display " : ")
      (display (- (runtime) start-time))
      (display "ms")
      (newline)
      #t)
    #f))

(define (primes-larger-than n k-primes)
  (if (not (= k-primes 0))
    (if (timed-prime-test n (runtime)) 
      (primes-larger-than (+ n 1) (- k-primes 1))
      (primes-larger-than (+ n 1) k-primes))))

(primes-larger-than 100000000 3)
(primes-larger-than 1000000000 3)
; (primes-larger-than 10000000000 3)
