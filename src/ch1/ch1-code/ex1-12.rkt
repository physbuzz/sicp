#lang sicp

(define (choose n m)
  (if (or (< m 1) (> m (- n 1)))
    1
    (+ (choose (- n 1) m)
       (choose (- n 1) (- m 1)))))

(choose 6 0)
(choose 6 1)
(choose 6 2)
(choose 6 3)
(choose 6 4)
(choose 6 5)
(choose 6 6)

