
# SICP Reading Group

## Book club Notes
- [Chapter 1-1](ch1/notes-ch1-1.html)
- [Chapter 1-2](ch1/notes-ch1-2.html)
- [Chapter 1-3](ch1/notes-ch1-3.html)
- [Chapter 2-1](ch2/notes-ch2-1.html)
- [Chapter 2-2](ch2/notes-ch2-2.html) <-- We are here
- [Chapter 2-3](ch2/notes-ch2-3.html)
- [Chapter 2-4](ch2/notes-ch2-4.html)
- [Chapter 2-5](ch2/notes-ch2-5.html)

## Meetings
- [Feb 23, 2025](ch1/notes-ch1-1.html#meeting-02-23-2025)
- [March 2, 2025](ch1/notes-ch1-1.html#meeting-03-02-2025)
- [March 9, 2025](ch1/notes-ch1-2.html#meeting-03-09-2025)
- [March 16, 2025](ch1/notes-ch1-2.html#meeting-03-16-2025)
- [March 23, 2025](ch1/notes-ch1-3.html#meeting-03-23-2025) 
- [March 30, 2025](ch2/notes-ch2-1.html#meeting-03-30-2025) 
- [April 6, 2025](ch2/notes-ch2-2.html#meeting-04-06-2025) (Placeholder)

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
- Enumerating binary trees and arithmetic expressions
- ✯ n queens and dancing links
- Story about polynomial long division + my grandpa
