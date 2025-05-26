#lang sicp


;; First note that the deque could *almost* be written without any
;; modifications to queue. The issue comes when you try to rear-delete-deque
;; and you realize you don't have a pointer to the second-to-last element
;; anywhere! So, the problem is to maintain a doubly linked list in O(1).
;;
;; I could make the deque be a pair:
;;   (front-ptr . rear-ptr)
;; pointing to doubly-linked list:
;;   '((value prev next) (value prev next) ...)
;;
;; But that's a lot of work! Instead, how about we just let the deque structure 
;; be:
;;   '(front-ptr rear-ptr 
;;      auxiliary-list-front-ptr aux-rear-ptr)
;; front-ptr and rear-ptr will have their usual stuff. 
;; The aux list will be maintained to have pointers to the list in reverse order

(define (front-ptr deque) (car deque))
(define front-deque front-ptr) ;; (smug face)
(define (rear-ptr deque) (cdr deque))
(define rear-deque rear-ptr) 
(define (set-front-ptr! deque item) (set-car! deque item))
(define (set-rear-ptr! deque item) (set-cdr! deque item))
(define (empty-deque? deque) (null? (front-ptr deque)))
(define (make-deque) (cons '() '()))

(define (front-deque deque)
  (if (empty-deque? deque)
      (error "FRONT called with an
              empty deque" deque)
      (car (front-ptr deque))))

(define (rear-insert-deque! deque item)
  (let ((new-pair (cons item '())))
    (cond ((empty-deque? deque)
           (set-front-ptr! deque new-pair)
           (set-rear-ptr! deque new-pair)
           deque)
          (else (set-cdr! (rear-ptr deque) 
                          new-pair)
                (set-rear-ptr! deque new-pair)
                deque))))

(define (front-insert-deque! deque item)
  (let ((new-pair (cons item (front-ptr deque))))
    (cond ((empty-deque? deque)
           (set-front-ptr! deque new-pair)
           (set-rear-ptr! deque new-pair)
           deque)
          (else (set-front-ptr! deque new-pair)
                deque))))

;; front-delete-deque!, rear-del

(define (front-delete-deque! deque)
  (cond ((empty-deque? deque)
         (error "DELETE! called with 
                 an empty deque" deque))
        (else (set-front-ptr! 
               deque 
               (cdr (front-ptr deque)))
              deque)))

(define (front-delete-deque! deque)
  (cond ((empty-deque? deque)
         (error "DELETE! called with 
                 an empty deque" deque))
        (else (set-front-ptr! 
               deque 
               (cdr (front-ptr deque)))
              deque)))

(define (print-deque deque)
  (display (front-ptr deque)) (newline))

(define q1 (make-deque))

(insert-deque! q1 'a)
;; ((a) a)
(print-deque q1)(newline)
;; (a)

(insert-deque! q1 'b)
;; ((a b) b)
(print-deque q1)(newline)
;; (a )

(delete-deque! q1)
;; ((b) b)
(print-deque q1)(newline)
;; (b)

(delete-deque! q1)
;; (() b)
(print-deque q1)(newline)
;; ()
