# Dating 
Inspired by Hannah Fry's TED talk about love.

I was curious is it really the case that if it was just statistics you should reject first 37% of partners and then stick to the first best one so far. The next question was what happens when there's an improvement (increase in attractiveness).

There are two folder for two approaches: 'single core' and 'multithreading'.
Each 'main.py' creates a .csv file in 'Results' folder. File name specifies all variables used.

Version one was with Python lists, but it's much easyier and faster sticking to Numpy.

Increase in population causes super-linear scalability.
Increase in the number of cycles (repeats) causes liear scalability. Additionaly it reduces ramdomness in results.

I've benchmarked 'single core' and 'multithreading' after going offline and stopping most unnecessary programs, CPU IDLE was up to 3%. I have 6 cores and 12 logical subprocessors, so the script was running 12 processes at once.

The benchmark data stops in different places, because:
 - single core: Arbitrary run time cutoff at 40 min.
 - multithreading: When script crasched because of running out of RAM
