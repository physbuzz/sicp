#lang sicp

(define (inc x) (+ x 1))
(define (double f) (lambda (x) (f (f x))))

((double inc) 1)

(((double (double double)) inc) 5)
