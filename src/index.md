
# SICP Reading Group

## Book club Notes
- [Chapter 1-1](ch1/notes-ch1-1.html) (8/8 problems, total 8/8)
- [Chapter 1-2](ch1/notes-ch1-2.html) (20/20 problems, total 28/28)
- [Chapter 1-3](ch1/notes-ch1-3.html) (18/18 problems, total 46/46)
- [Chapter 2-1](ch2/notes-ch2-1.html) (16/16 problems, total 62/62)
- [Chapter 2-2](ch2/notes-ch2-2.html) (27/36 problems, total 89/98)
- [Chapter 2-3](ch2/notes-ch2-3.html) (20/20 problems, total 109/118)
- [Chapter 2-4](ch2/notes-ch2-4.html) (4/4 problems, total 113/122)
- [Chapter 2-5](ch2/notes-ch2-5.html) (21/21 problems, total 134/143)
- [Chapter 3-1](ch3/notes-ch3-1.html) (8/8 problems, total 142/151)
- [Chapter 3-2](ch3/notes-ch3-2.html) (1/3 problems, total 143/154)
- [Chapter 3-3](ch3/notes-ch3-3.html) (0/26 problems, total /180)
- [Chapter 3-4](ch3/notes-ch3-4.html) (0/12 problems, total /192)
- [Chapter 3-5](ch3/notes-ch3-5.html) (0/33 problems, total /225)
- [Chapter 4-1](ch4/notes-ch4-1.html) (0/24 problems, total /249)
- [Chapter 4-2](ch4/notes-ch4-2.html) (0/10 problems, total /259)
- [Chapter 4-3](ch4/notes-ch4-3.html) (0/20 problems, total /279)
- [Chapter 4-4](ch4/notes-ch4-4.html) (0/25 problems, total /304)
- [Chapter 5-1](ch5/notes-ch5-1.html) (0/6 problems, total /310)
- [Chapter 5-2](ch5/notes-ch5-2.html) (0/13 problems, total /323)
- [Chapter 5-3](ch5/notes-ch5-3.html) (0/3 problems, total /326)
- [Chapter 5-4](ch5/notes-ch5-4.html) (0/8 problems, total /334)
- [Chapter 5-5](ch5/notes-ch5-5.html) (0/22 problems, total /356)

## Meetings
- [Feb 23, 2025](ch1/notes-ch1-1.html#meeting-02-23-2025)
- [March 2, 2025](ch1/notes-ch1-1.html#meeting-03-02-2025)
- [March 9, 2025](ch1/notes-ch1-2.html#meeting-03-09-2025)
- [March 16, 2025](ch1/notes-ch1-2.html#meeting-03-16-2025)
- [March 23, 2025](ch1/notes-ch1-3.html#meeting-03-23-2025) 
- [March 30, 2025](ch2/notes-ch2-1.html#meeting-03-30-2025) 
- [April 6, 2025](ch2/notes-ch2-2.html#meeting-04-06-2025)
- [April 20, 2025](ch2/notes-ch2-3.html#meeting-04-20-2025)
- [April 27, 2025](ch2/notes-ch2-4.html#meeting-04-27-2025)
- [May 4, 2025](ch2/notes-ch2-5.html#meeting-05-04-2025)
- [May 11, 2025](ch3/notes-ch3-1.html#meeting-04-27-2025)

## Nice Links
- [SICP html edition](https://sarabander.github.io/sicp/)
- [Lectures from 1986](https://www.youtube.com/playlist?list=PLE18841CABEA24090)
- Meetup link: [https://www.meetup.com/code-and-coffee-long-beach](https://www.meetup.com/code-and-coffee-long-beach)
- Twitch: [https://www.twitch.tv/codeandcoffeelb](https://www.twitch.tv/codeandcoffeelb)
- Discord: [https://www.codeandcoffee.dev/](https://www.codeandcoffee.dev/)
- [Racket IDE](https://www.racket-lang.org/)

## Extras

Filling in stuff from [bonus-notes.md](bonus-notes.html) as time goes on. A lot of this is a big TODO. Anything with a ✯ next to it means it takes significant work.

**General stuff:**

- [Anki flashcards](anki.html)
- ✯ Racket crash course
- SICP Library Functions

**Ch1 Bonuses**

- Asymptotic approximations and some notes on $\Theta$, $\Omega$, $O$. 
- The ill-fated Santa Barbara Monte Carlo machine
- Exact runtime of count-change
- RSA implementation
- Linear diophantine equations 
- Bonus number theory (Euler totient, base b expansions of fractions)
- Bonus special numbers (Lucas, Catalan, partition numbers, "negative binomial")
- Numerical approximation formulas (iterated polynomial gives sine, other iterated special polynomials give special things too)
- Improving rates of convergence (newton, accelerated newton, successive averaging, resummation)
- ✯ Challenge 1: try to compute the Ramanujan tau function. This is some memoized code using recursion that supposedly works: [https://claude.ai/chat/374b1219-3cd8-4a9e-87a3-dfddfc1f8896](https://claude.ai/chat/374b1219-3cd8-4a9e-87a3-dfddfc1f8896), but simple mathematica code can generate it too: `CoefficientList[Take[Expand[Product[(1 - x^k)^24, {k, 1, 30}]], 30],x]`
- ✯ Challenge 2: Continued fraction expansion of pi or 1/pi using exact arithmetic.
- ✯ Challenge 3: Thoughts on reversibility and quantum computing

**Ch2 Bonuses**

- ✯ Drawing Church numerals
- Enumerating binary trees and arithmetic expressions (builds on top of enumerating permutations)
- ✯ n queens and dancing links
- Story about polynomial long division + my grandpa

Chapter 2 stuff:

1. It would be useful to review all the different functions: accumulate, map, map-indexed, fold-left, fold-right. Not just how they're implemented, but also 
the generic functions you'd actually use when programming Racket or Guile or whatever. Same with `set`s.
2. For data abstraction, it might be nice to write a library containing many of 
the features from all of the practice problems for section 2.4-2.5. 
3. I'd like to write an article about polynomial stuff. Including why things 
like the gcd are only well-defined up to units, and what that means. So,
we could do a proper implementation of rational functions and polynomials. 
**A program that finds all roots**.
There's plenty of other stuff we could do here: Euclidean domains, Z[i],
Z[(-1)^(1/3)]. This is all about abstract algebra of one variable.
4. Abstract algebra with multiple variables: Groebner bases, various algos.
5. It would be really cool to implement some of Katherine Stange's [Visualizing imaginary quadratic fields](https://math.colorado.edu/~kstange/papers/Stange-short-exp.pdf)

















