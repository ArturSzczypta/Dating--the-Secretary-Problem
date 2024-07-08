# Dating - the Secretary Problem
Inspired by Hannah Fry's TED talk about love.

Statistically, to choose the best option, one schould reject about 37% of the given options, and then choose first option better than any so far. With this approach, the chance of picking the best option about 37%. Asumption is that there is only one chance to accept or reject. Worst case scenario is rejecting everyone and then taking the last option, hoping it is acceptable.

Wiki: https://en.wikipedia.org/wiki/Secretary_problem

## Answers I seaked
1. When schould a person stop looking if they aim for the best option in set, what is the propability
2. When schould a person stop looking if they want to choose statistically best option, what is the propability
3. How the results above change, if we are comfortable of choosing any option from top 80%, 90% or 95%
4. How the results change, if there is a marginall improvement with time in the quality of options, 2%, 5% or 10%
5. What are the speed differences when using single- and multiprocessing

## Usage
There are two folder for two approaches: 'single core' and 'multithreading'.
Each 'main.py' creates a .csv file in 'Results' folder. File name specifies all variables used.

Version one was with Python lists, but it's much easyier and faster sticking to Numpy.

## Observations
Increase in population causes super-linear scalability.
Increase in the number of cycles (repeats) causes liear scalability. Additionaly it reduces ramdomness in results.

I've benchmarked 'single core' and 'multithreading' after going offline and stopping most unnecessary programs, CPU IDLE was up to 3%. I have 6 cores and 12 logical subprocessors, so the script was running 12 processes at once.

The benchmark data stops in different places, because:
- single core: Arbitrary run time cutoff at 40 min.
- multiprocessing: When script crasched when it runned out of RAM
