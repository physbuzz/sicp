#lang sicp

(define (displayln x) (display x) (display "\n"))
; 10
displayln 10
; (display "\n")
displayln (+ 5 3 4)
displayln (- 9 1)
displayln (/ 6 2)
displayln (+ (* 2 4) (- 4 6))
displayln (define a 3)
displayln (define b (+ a 1))
displayln (+ a b (* a b))
displayln (= a b)
displayln (if (and (> b a) (< b (* a b)))
    b
    a)
displayln (cond ((= a 4) 6)
      ((= b 4) (+ 6 7 a))
      (else 25))
displayln (+ 2 (if (> b a) b a))
displayln (* (cond ((> a b) a)
         ((< a b) b)
         (else -1))
   (+ a 1))

