
# Building the Query System from the Ground Up

I found section 4-4 incredibly difficult to read. This section is my supplement
to 4-4. Instead of taking the approach of describing the abstract ideas up-front
and leaving the concrete code to the end of the chapter, I instead try to 
make everything concrete from the get-go and build systems from scratch.

Still a WIP. But I imagine that what I'll have to do is that some pieces of 
the system will be fully-featured or are verbatim what is in the book. 
At other times it might make sense to build systems which are less general or
fail at certain edge cases. So hopefully I can make it clear which code blocks
are flawed or not fully featured.

## Frames

A *frame* is an association list with keys `'(? variable)` and values 
representing the bound value of the variable. For example in the process
of matching the query `'(a b ?x)` to datum `'(a b c)`, 
we generate the frame `'(((? x) . c))`. Note that the symbol `?x` is expanded
into `'(? x)` by the procedures in `expand-question-mark` and `query-syntax-process` (4.4.4.7).

Running some examples (with the code in 4.4.4.8), we can get a feel for how things work. We define two frames by extending the empty frame `'()`.

```rkt
(define frame1 (extend '(? x) 'a '()))
(define frame2 (extend '(? y) 'b frame1))
```

Looking up behaves as expected:

```rkt
frame2
;; (((? y) . b) ((? x) . a))

(binding-in-frame '(? x) frame2)
;; ((? x) . a)

(binding-in-frame '(? y) frame2)
;; ((? y) . b)
```

and we note that we haven't done anything special to prevent inconsistent frame extensions! This has to be checked for elsewhere.
```rkt
(extend '(? x) 'b frame2)
;; (((? x) . b) ((? y) . b) ((? x) . a))
```

Note that extending a frame makes things *more* specific, because we specify
that the placeholder `'?x` has to be bound to a specific value. This means that
later on, the `and` operator will have a simple implementation because each
time we extend the frame in all possible ways we add more conditions on 
what matches we'll accept.

@src(code/simple-frame.rkt, collapsed)

## Simple Pattern Matching

Next we consider the simple pattern matching algorithm. 
"Simple" means that we don't handle
`and`, `or`, `not`, or `'lisp-value` yet.

Our function `pattern-match` is going to take three arguments:
`pat`, `dat` and `frame` and is going to traverse the whole datum `dat` recursively. If we can satisfy the given pattern, then we'll return the correct frame extension. For example:
```rkt
(pattern-match '((? x) (? x) (? y) (? y))
               '(foo foo bar bar)
               '(((? x) . foo)))
;; (((? y) . bar) ((? x) . foo))

(pattern-match '((? x) (? x) (? y) (? y))
               '(bar bar bar bar)
               '(((? x) . foo)))
;; 'failed
```

@src(code/simple-pattern-match.rkt, collapsed)

The implementation is fairly straightforward, albeit with a few dubious decisions!

`pattern-match` and `extend-if-consistent` are functions which call each other. 
`extend-if-consistent` is a helper function which actually does the symbol lookup and the 
extension to the frame. In order to determine if the pattern matching has failed or not, it calls 
`extend-if-consistent` with the pattern found by substitution from the database. 

To test understanding, I recommend trying to remember what the missing pattern `<...>` should be in the following code
snippet.

```rkt
(define (tagged-list? exp tag) (and (pair? exp) (eq? (car exp) tag)))
(define (var? exp) (tagged-list? exp '?))
(define (pattern-match pat dat frame)
  (cond ((eq? frame 'failed) 'failed)
        ((equal? pat dat) frame)
        ((var? pat) (extend-if-consistent pat dat frame))
        ((and (pair? pat) (pair? dat))
         (pattern-match <...>))
        (else 'failed)))
(define (extend-if-consistent var dat frame)
  (let ((binding (binding-in-frame var frame)))
    (if binding
        (pattern-match 
         (binding-value binding) dat frame)
        (extend var dat frame))))
```

**One weird thing:** I notice that in `extend-if-consistent`, we call pattern-match using a pattern which is the 
result of substituting user data. This means if our database contains malicious patterns like `'(? new-rule)` 
then we would start running checks based on user-provided rules! This is super funky, but whatever. 
It would probably make more sense, be more self-contained, and avoid this bad behavior entirely if we just directly 
checked for equality inside `extend-if-consistent`, but that's just my opinion!

# My Misconceptions

## "The output of a Query"
In 4.4.1, we give the example of the query:
```rkt
(and (job ?person (computer programmer))
     (address ?person ?where))
```

giving the output 
```rkt
(and (job (Hacker Alyssa P) 
          (computer programmer))
     (address (Hacker Alyssa P) 
              (Cambridge (Mass Ave) 78)))

(and (job (Fect Cy D) (computer programmer))
     (address (Fect Cy D) 
              (Cambridge (Ames Street) 3)))
```

The book also says "the output of the query is a stream of frames." 
You might think this means that our two `(and ...)` statements are the
two elements in the stream of frames, but this is incorrect! In my opinion
the book's phrasing is highly misleading here, the stream of frames which is
relevant to our query has two elements, which are:

```rkt
'(((? person) . (Hacker Alyssa P)) ((? where) . (Cambridge (Mass Ave) 78)))
'(((? person) . (Fect Cy D)) ((? where) . (Cambridge (Ames Street) 3)))
```

Later (in 4.4.4.1) we `instantiate` those frames using the input query expression, the 
frame, and a function to handle unbound variables:
```rkt
(define (instantiate 
         exp frame unbound-var-handler) ...)
```





