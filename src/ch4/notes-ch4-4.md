<div class="nav">
    <span class="activenav"><a href="notes-ch4-3.html">← Previous</a></span>
    <span class="activenav"><a href="../index.html">↑ Up</a></span>
    <span class="activenav"><a href="../ch5/notes-ch5-1.html">Next →</a></span>
</div>

[HTML Book Chapter 4.4 Link](https://sarabander.github.io/sicp/html/4_002e4.xhtml#g_t4_002e4)

@toc


## Section 4.4

### Notes

#### This chapter, briefly.

The handling of simple queries is just a very straightforward depth-first traversal 
of the tree with a 
greedy algorithm that assigns values to the queries as we go. 
In this case, a greedy algorithm is enough. So this is like a chapter 2 thing.

Compound queries and `not` are just done with filtering and stream gymnastics. 
So this is like a chapter 3.5 thing. 

The database and indexing work seems like it would be a mutability exercise in chapter
3. 

And so that really just leaves the unification algorithm and how rules are handled
-- still reading about that.





### Outdated Notes

(I wrote these a while ago and have since come to understand stuff a lot better, so I'll
need to reread these)


#### Confusion on append-to-form
Definition 4.4 of append:


Is this saying that there's an implicit definition of append,
as... it's the symbol such that

```rkt
(equal? (append v y) z) 
=> 
(equal? (append (cons u v) y) (cons u z))
```

This definition is bonkers. However it makes more sense in rule notation:

```rkt
(rule (append-to-form () ?y ?y))
(rule (append-to-form (?u . ?v) ?y (?u . ?z))
      (append-to-form ?v ?y ?z))
```

It's not fair to call this a crazy implicit definition of 
append-to-form, we can see by how the dotted tail notation 
pattern is constructed, we're going to consume one element
of the list `?u` every time something is matched, thereby
iterating through the list recursively. 

TODO: This would be really fun to do in mathematica. 

#### Comment on "appendo"

The book The Reasoned Schemer goes into detail about 
relational programming, where I think 
`append-to-form` is `appendo`? (thanks happyNora!)


#### Mathematica Analogy

Basic patterns could be matched like this:
```mathematica
; (job ?x (computer programmer))
facts = {job["Hacker Alyssa P", {computer, programmer}], 
   address["Hacker Alyssa P", {"Cambridge", {"Mass Ave"}, 78}], 
   job["Fect Cy D", {computer, programmer}], 
   address["Fect Cy D", {"Cambridge", {"Ames Street"}, 3}], 
   job["Foo Bar", {waiter}]};
Cases[facts, job[p_, {computer, programmer}]]

{job["Hacker Alyssa P", {computer, programmer}], 
 job["Fect Cy D", {computer, programmer}]}
```

More complicated stuff gets more complicated, it doesn't match one-to-one.
Say we want to implement this:
```rkt
(and (job ?person (computer programmer))
     (address ?person ?where))
```

I couldn't get a solution working using `Cases` or `ReplaceAll`. But two 
tricks got it to work:

1. The `Orderless` attribute. If a function has this, then by default all
arguments are sorted into canonical order; but also the behavior of pattern
matching is changed so that all possible orderings are considered.
2. `ReplaceList` explicitly tries to list all possible matches, instead of
trying to find single matches with a list of elements.

With this, we have the working match code. No idea if the algorithmic complexity renders this feasible, sometimes Mathematica's pattern matching is magical enough to make this O(N).

```mathematica
In[]:= SetAttributes[factBase, Orderless];
facts = factBase[job["Hacker Alyssa P", {computer, programmer}], 
   address["Hacker Alyssa P", {"Cambridge", {"Mass Ave"}, 78}], 
   job["Fect Cy D", {computer, programmer}], 
   address["Fect Cy D", {"Cambridge", {"Ames Street"}, 3}], 
   job["Foo Bar", {waiter}]];
ReplaceList[facts,
 factBase[
   address[p_, where_], job[p_, {computer, programmer}], ___]
  :> {p, where}]

Out[]= {{"Fect Cy D", {"Cambridge", {"Ames Street"}, 
   3}}, {"Hacker Alyssa P", {"Cambridge", {"Mass Ave"}, 78}}}
```





### Exercises

#### Exercise 4.55

Give simple queries that retrieve
the following information from the data base:

**1.** all people supervised by Ben Bitdiddle;

**2.** the names and jobs of all people in the accounting division;

**3.** the names and addresses of all people who live in Slumerville.

##### Solution

```rkt
; 1.
(supervisor ?x (Bitdiddle Ben)) 
; 2. 
(job ?name (accounting . ?type))
; 3.
(address ?name (Slumerville . ?address))
```

#### Exercise 4.56

Formulate compound queries that
retrieve the following information:

**1.** the names of all people who are supervised by Ben Bitdiddle, together with
their addresses;

**2.** all people whose salary is less than Ben Bitdiddle's, together with their
salary and Ben Bitdiddle's salary;

**3.** all people who are supervised by someone who is not in the computer division,
together with the supervisor's name and job.

##### Solution

```rkt
; 1.
(and (supervisor ?x (Bitdiddle Ben))
     (address ?x ?address))
; 2. 
(and (salary (Bitdiddle Ben) ?benamount)
     (salary ?person ?personamount)
     (lisp-value < ?personamount ?benamount))
; 3.
(and (supervisor ?person ?super)
     (job ?super (?division . ?type))
     (not (job ?super (computer . ?type))))
```


#### Exercise 4.57

Define a rule that says that
person 1 can replace person 2 if either person 1 does the same job as person 2
or someone who does person 1's job can also do person 2's job, and if person 1
and person 2 are not the same person. Using your rule, give queries that find
the following:

**1.** all people who can replace Cy D. Fect;

**2.** all people who can replace someone who is being paid more than they are,
together with the two salaries.



##### Solution

#### Exercise 4.58

Define a rule that says that a
person is a ``big shot'' in a division if the person works in the division but
does not have a supervisor who works in the division.

##### Solution

#### Exercise 4.59

Ben Bitdiddle has missed one
meeting too many.  Fearing that his habit of forgetting meetings could cost him
his job, Ben decides to do something about it.  He adds all the weekly meetings
of the firm to the Microshaft data base by asserting the following:

```rkt
(meeting accounting (Monday 9am))
(meeting administration (Monday 10am))
(meeting computer (Wednesday 3pm))
(meeting administration (Friday 1pm))
```

Each of the above assertions is for a meeting of an entire division.  Ben also
adds an entry for the company-wide meeting that spans all the divisions.  All
of the company's employees attend this meeting.

```rkt
(meeting whole-company (Wednesday 4pm))
```

**1.** On Friday morning, Ben wants to query the data base for all the meetings that
occur that day.  What query should he use?

**2.** Alyssa P. Hacker is unimpressed.  She thinks it would be much more useful to be
able to ask for her meetings by specifying her name.  So she designs a rule
that says that a person's meetings include all `whole-company` meetings
plus all meetings of that person's division.  Fill in the body of Alyssa's
rule.

```rkt
(rule (meeting-time ?person ?day-and-time)
      ⟨@var{rule-body}⟩)
```

**3.** Alyssa arrives at work on Wednesday morning and wonders what meetings she has
to attend that day.  Having defined the above rule, what query should she make
to find this out?



##### Solution

#### Exercise 4.60

By giving the query

```rkt
(lives-near ?person (Hacker Alyssa P))
```

Alyssa P. Hacker is able to find people who live near her, with whom she can
ride to work.  On the other hand, when she tries to find all pairs of people
who live near each other by querying

```rkt
(lives-near ?person-1 ?person-2)
```


she notices that each pair of people who live near each other is listed twice;
for example,

```rkt
(lives-near (Hacker Alyssa P) (Fect Cy D))
(lives-near (Fect Cy D) (Hacker Alyssa P))
```

Why does this happen?  Is there a way to find a list of people who live near
each other, in which each pair appears only once?  Explain.

##### Solution

#### Exercise 4.61

The following rules implement a
`next-to` relation that finds adjacent elements of a list:

```rkt
(rule (?x next-to ?y in (?x ?y . ?u)))
(rule (?x next-to ?y in (?v . ?z))
      (?x next-to ?y in ?z))
```

What will the response be to the following queries?

```rkt
(?x next-to ?y in (1 (2 3) 4))
(?x next-to 1 in (2 1 3 1))
```

##### Solution

#### Exercise 4.62

Define rules to implement the
`last-pair` operation of Exercise 2.17, which returns a list
containing the last element of a nonempty list.  Check your rules on queries
such as `(last-pair (3) ?x)`, `(last-pair (1 2 3) ?x)` and
`(last-pair (2 ?x) (3))`.  Do your rules work correctly on queries such as
`(last-pair ?x (3))`?

##### Solution

#### Exercise 4.63

The following data base (see
Genesis 4) traces the genealogy of the descendants of Ada back to Adam, by way
of Cain:

```rkt
(son Adam Cain) (son Cain Enoch)
(son Enoch Irad) (son Irad Mehujael)
(son Mehujael Methushael)
(son Methushael Lamech)
(wife Lamech Ada) (son Ada Jabal)
(son Ada Jubal)
```

Formulate rules such as ``If $S$ is the son of $f$, and $f$ is the son of
$G$, then $S$ is the grandson of $G$'' and ``If $W$ is the wife of
$M$, and $S$ is the son of $W$, then $S$ is the son of $M$'' (which
was supposedly more true in biblical times than today) that will enable the
query system to find the grandson of Cain; the sons of Lamech; the grandsons of
Methushael.  (See Exercise 4.69 for some rules to deduce more complicated
relationships.)

##### Solution

#### Exercise 4.64

Louis Reasoner mistakenly deletes
the `outranked-by` rule (4.4.1) from the data base.  When he
realizes this, he quickly reinstalls it.  Unfortunately, he makes a slight
change in the rule, and types it in as

```rkt
(rule (outranked-by ?staff-person ?boss)
  (or (supervisor ?staff-person ?boss)
      (and (outranked-by ?middle-manager
                         ?boss)
           (supervisor ?staff-person 
                       ?middle-manager))))
```

Just after Louis types this information into the system, DeWitt Aull comes by
to find out who outranks Ben Bitdiddle. He issues the query

```rkt
(outranked-by (Bitdiddle Ben) ?who)
```

After answering, the system goes into an infinite loop.  Explain why.

##### Solution

#### Exercise 4.65

Cy D. Fect, looking forward to
the day when he will rise in the organization, gives a query to find all the
wheels (using the `wheel` rule of 4.4.1):

```rkt
(wheel ?who)
```

To his surprise, the system responds

```rkt
;;; Query results:
(wheel (Warbucks Oliver))
(wheel (Bitdiddle Ben))
(wheel (Warbucks Oliver))
(wheel (Warbucks Oliver))
(wheel (Warbucks Oliver))
```

Why is Oliver Warbucks listed four times?

##### Solution

#### Exercise 4.66

Ben has been generalizing the
query system to provide statistics about the company.  For example, to find the
total salaries of all the computer programmers one will be able to say

```rkt
(sum ?amount
     (and (job ?x (computer programmer))
          (salary ?x ?amount)))
```

In general, Ben's new system allows expressions of the form

```rkt
(accumulation-function ⟨@var{variable}⟩
                       ⟨@var{query pattern}⟩)
```


where `accumulation-function` can be things like `sum`,
`average`, or `maximum`.  Ben reasons that it should be a cinch to
implement this.  He will simply feed the query pattern to `qeval`.  This
will produce a stream of frames.  He will then pass this stream through a
mapping function that extracts the value of the designated variable from each
frame in the stream and feed the resulting stream of values to the accumulation
function.  Just as Ben completes the implementation and is about to try it out,
Cy walks by, still puzzling over the `wheel` query result in 
Exercise 4.65.  When Cy shows Ben the system's response, Ben groans,
``Oh, no, my simple accumulation scheme won't work!''

What has Ben just realized?  Outline a method he can use to salvage the
situation.

##### Solution

#### Exercise 4.67

Devise a way to install a loop
detector in the query system so as to avoid the kinds of simple loops
illustrated in the text and in Exercise 4.64.  The general idea is that
the system should maintain some sort of history of its current chain of
deductions and should not begin processing a query that it is already working
on.  Describe what kind of information (patterns and frames) is included in
this history, and how the check should be made.  (After you study the details
of the query-system implementation in 4.4.4, you may want to
modify the system to include your loop detector.)

##### Solution

#### Exercise 4.68

Define rules to implement the
`reverse` operation of Exercise 2.18, which returns a list
containing the same elements as a given list in reverse order.  (Hint: Use
`append-to-form`.)  Can your rules answer both `(reverse (1 2 3) ?x)`
and `(reverse ?x (1 2 3))`?

##### Solution

#### Exercise 4.69

Beginning with the data base and
the rules you formulated in Exercise 4.63, devise a rule for adding
``greats'' to a grandson relationship. This should enable the system to deduce
that Irad is the great-grandson of Adam, or that Jabal and Jubal are the
great-great-great-great-great-grandsons of Adam.  (Hint: Represent the fact
about Irad, for example, as `((great grandson) Adam Irad)`.  Write rules
that determine if a list ends in the word `grandson`.  Use this to express
a rule that allows one to derive the relationship `((great .  ?rel) ?x
?y)`, where `?rel` is a list ending in `grandson`.)  Check your rules
on queries such as `((great grandson) ?g ?ggs)` and `(?relationship
Adam Irad)`.

##### Solution

#### Exercise 4.70

What is the purpose of the
`let` bindings in the procedures `add-assertion!` and
`add-rule!`?  What would be wrong with the following implementation of
`add-assertion!`?  Hint: Recall the definition of the infinite stream of
ones in 3.5.2: `(define ones (cons-stream 1 ones))`.

```rkt
(define (add-assertion! assertion)
  (store-assertion-in-index assertion)
  (set! THE-ASSERTIONS
        (cons-stream assertion 
                     THE-ASSERTIONS))
  'ok)
```

##### Solution

#### Exercise 4.71

Louis Reasoner wonders why the
`simple-query` and `disjoin` procedures (4.4.4.2) are
implemented using explicit `delay` operations, rather than being defined
as follows:

```rkt
(define (simple-query 
         query-pattern frame-stream)
  (stream-flatmap
   (lambda (frame)
     (stream-append
      (find-assertions query-pattern frame)
      (apply-rules query-pattern frame)))
   frame-stream))

(define (disjoin disjuncts frame-stream)
  (if (empty-disjunction? disjuncts)
      the-empty-stream
      (interleave
       (qeval (first-disjunct disjuncts)
              frame-stream)
       (disjoin (rest-disjuncts disjuncts)
                frame-stream))))
```

Can you give examples of queries where these simpler definitions would lead to
undesirable behavior?

##### Solution

#### Exercise 4.72

Why do `disjoin` and
`stream-flatmap` interleave the streams rather than simply append them?
Give examples that illustrate why interleaving works better.  (Hint: Why did we
use `interleave` in 3.5.3?)

##### Solution

#### Exercise 4.73

Why does `flatten-stream`
use `delay` explicitly?  What would be wrong with defining it as follows:

```rkt
(define (flatten-stream stream)
  (if (stream-null? stream)
      the-empty-stream
      (interleave (stream-car stream)
                  (flatten-stream 
                   (stream-cdr stream)))))
```

##### Solution

#### Exercise 4.74

Alyssa P. Hacker proposes to use
a simpler version of `stream-flatmap` in `negate`, `lisp-value`,
and `find-assertions`.  She observes that the procedure that is mapped
over the frame stream in these cases always produces either the empty stream or
a singleton stream, so no interleaving is needed when combining these streams.

**1.** Fill in the missing expressions in Alyssa's program.

```rkt
(define (simple-stream-flatmap proc s)
  (simple-flatten (stream-map proc s)))

(define (simple-flatten stream)
  (stream-map ⟨??⟩
              (stream-filter ⟨??⟩ 
                             stream)))
```

**2.** Does the query system's behavior change if we change it in this way?



##### Solution

#### Exercise 4.75

Implement for the query language
a new special form called `unique`.  `Unique` should succeed if there
is precisely one item in the data base satisfying a specified query.  For
example,

```rkt
(unique (job ?x (computer wizard)))
```


should print the one-item stream

```rkt
(unique (job (Bitdiddle Ben)
             (computer wizard)))
```


since Ben is the only computer wizard, and

```rkt
(unique (job ?x (computer programmer)))
```


should print the empty stream, since there is more than one computer
programmer.  Moreover,

```rkt
(and (job ?x ?j) 
     (unique (job ?anyone ?j)))
```


should list all the jobs that are filled by only one person, and the people who
fill them.

There are two parts to implementing `unique`.  The first is to write a
procedure that handles this special form, and the second is to make
`qeval` dispatch to that procedure.  The second part is trivial, since
`qeval` does its dispatching in a data-directed way.  If your procedure is
called `uniquely-asserted`, all you need to do is

```rkt
(put 'unique 'qeval uniquely-asserted)
```


and `qeval` will dispatch to this procedure for every query whose
`type` (`car`) is the symbol `unique`.

The real problem is to write the procedure `uniquely-asserted`.  This
should take as input the `contents` (`cdr`) of the `unique`
query, together with a stream of frames.  For each frame in the stream, it
should use `qeval` to find the stream of all extensions to the frame that
satisfy the given query.  Any stream that does not have exactly one item in it
should be eliminated.  The remaining streams should be passed back to be
accumulated into one big stream that is the result of the `unique` query.
This is similar to the implementation of the `not` special form.

Test your implementation by forming a query that lists all people who supervise
precisely one person.

##### Solution

#### Exercise 4.76

Our implementation of `and`
as a series combination of queries (Figure 4.5) is elegant, but it is
inefficient because in processing the second query of the `and` we must
scan the data base for each frame produced by the first query.  If the data
base has $n$ elements, and a typical query produces a number of output frames
proportional to $n$ (say ${n \,/\, k$}), then scanning the data base for each
frame produced by the first query will require ${n^2 /\, k$} calls to the
pattern matcher.  Another approach would be to process the two clauses of the
`and` separately, then look for all pairs of output frames that are
compatible.  If each query produces ${n \,/\, k$} output frames, then this means
that we must perform ${n^2 /\, k^2$} compatibility checks---a factor of $k$
fewer than the number of matches required in our current method.

Devise an implementation of `and` that uses this strategy.  You must
implement a procedure that takes two frames as inputs, checks whether the
bindings in the frames are compatible, and, if so, produces a frame that merges
the two sets of bindings.  This operation is similar to unification.

##### Solution

#### Exercise 4.77

In 4.4.3 we saw
that `not` and `lisp-value` can cause the query language to give
``wrong'' answers if these filtering operations are applied to frames in which
variables are unbound.  Devise a way to fix this shortcoming.  One idea is to
perform the filtering in a ``delayed'' manner by appending to the frame a
``promise'' to filter that is fulfilled only when enough variables have been
bound to make the operation possible.  We could wait to perform filtering until
all other operations have been performed.  However, for efficiency's sake, we
would like to perform filtering as soon as possible so as to cut down on the
number of intermediate frames generated.

##### Solution

#### Exercise 4.78

Redesign the query language as a
nondeterministic program to be implemented using the evaluator of 
4.3, rather than as a stream process.  In this approach, each query will
produce a single answer (rather than the stream of all answers) and the user
can type `try-again` to see more answers.  You should find that much of
the mechanism we built in this section is subsumed by nondeterministic search
and backtracking.  You will probably also find, however, that your new query
language has subtle differences in behavior from the one implemented here.  Can
you find examples that illustrate this difference?

##### Solution

#### Exercise 4.79

When we implemented the Lisp
evaluator in 4.1, we saw how to use local environments to avoid
name conflicts between the parameters of procedures.  For example, in
evaluating

```rkt
(define (square x) 
  (* x x))

(define (sum-of-squares x y)
  (+ (square x) (square y)))

(sum-of-squares 3 4)
```


there is no confusion between the `x` in `square` and the `x` in
`sum-of-squares`, because we evaluate the body of each procedure in an
environment that is specially constructed to contain bindings for the local
variables.  In the query system, we used a different strategy to avoid name
conflicts in applying rules.  Each time we apply a rule we rename the variables
with new names that are guaranteed to be unique.  The analogous strategy for
the Lisp evaluator would be to do away with local environments and simply
rename the variables in the body of a procedure each time we apply the
procedure.

Implement for the query language a rule-application method that uses
environments rather than renaming.  See if you can build on your environment
structure to create constructs in the query language for dealing with large
systems, such as the rule analog of block-structured procedures.  Can you
relate any of this to the problem of making deductions in a context (e.g., ``If
I supposed that $P$ were true, then I would be able to deduce $A$ and
$B$.'') as a method of problem solving?  (This problem is open-ended.  A good
answer is probably worth a Ph.D.)

##### Solution

