#lang racket
(define (symbol<? s1 s2)
  (string<? (symbol->string s1) (symbol->string s2)))
(define (symbol=? s1 s2)
  (string=? (symbol->string s1) (symbol->string s2)))

;; Verify that a monomial like '((x 1) (y 2) (z 1)) is in the correct order
;; If we had '((z 1) (y 2) (x 1)) this would be incorrect order.
(define (verify-order order)
  (or (null? order)
      (null? (cdr order))
      (let ((x (car order)) (y (cadr order)))
        (and (symbol<? (car x) (car y))
             (verify-order (cdr order))))))
;; Lexicographic ordering for terms like '(x 1) or '(y 2) or '(foobar 10).
(define (single-order<? so1 so2)
  (or (symbol<? (car so1) (car so2))
      (and (symbol=? (car so1) (car so2))
           (< (cadr so1) (cadr so2)))))
(define (single-order=? so1 so2)
  (equal? so1 so2))

;;(define (single-order=? so1 so2)
;;  (and (symbol=? (car so1) (car so2))
;;       (= (cadr so1) (cadr so2))))

;; Lexicographic ordering on monomials. If we want the highest order monomial as the first element, we 
;; could sort from least to greatest where we define '() to be the greatest element, so this definition
;; might look a bit backwards.
(define (order<? o1 o2)
  (if (null? o2)
    (not (null? o1))
    (if (null? o1)
      #f
      (or (< (length o2) (length o1))
          (single-order<? (car o2) (car o1))
          (and (single-order=? (car o2) (car o1))
               (order<? (cdr o1) (cdr o2)))))))

(define l1 '((x 2) (y 1)))
(define l2 '((x 2) (y 2)))
(define l3 (sort '((x 2) (y 2) (foobar 10) (a 4)) single-order<?))
(define l4 '())
(sort (list l1 l2 l3 l4)  order<?)
    

;;  (or (< (length o2) (length o1))
;;    (and (= (length o2) (length o1))
;;
;;      (or (null? o2)
;;          (symbol<? 

;; (define (order term) (car term))
;; (define (coeff term) (cadr term))
;; 
;; (define (verify-single-term term)
;;   (verify-order (order term)))
;;(define (verify-terms terms)
;;  (or (null? terms)
;;    (let ((x (car terms)))
;;      (and (verify-single-term (car terms)) 
;;        (or (null? (cdr terms))
;;          (let ((y (cadr terms)))
;;(sort (list l1 l2 l3 l4) (lambda (x y) (< (length x) (length y))))
;;(order<? l4 l2)


;; (sort (
;; 
;; (single-order<? (list 'x 1) (list 'x 2))
;; (single-order<? (list 'x 1) (list 'y 2))
;; (single-order<? (list 'y 1) (list 'foobar 2))
;; 
;; 
;; (symbol<? 'a 'b)
;; (symbol<? 'b 'a)
;; (verify-order (list (list 'x 2) (list 'y 1)))
;; (verify-order (list (list 'y 2) (list 'x 1)))
;; (equal? (list (list 'x 2) (list 'y 1)) (list (list 'x 2) (list 'y 1)))
;; (equal? (list (list 'x 1) (list 'y 1)) (list (list 'x 2) (list 'y 1)))
