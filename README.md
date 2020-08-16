# Dating-Bail-Out
Inspired by Hannah Fry's TED talk about love.

I was curious is it really the case that if it was just statistics you should dump first 37% of partners and then stick tothe first best one so far. The next question was what happens when there's an improvement (increase in attractiveness).

There are two folder for two approaches: 'single core' and 'multithreading'.
Each 'main.py' creates a .csv file in 'Results' folder. File name specifies all variables used.



Version one was with Python lists, but it's much easyier and faster sticking to Numpy.

The bigger population and the number of cycles the longerit takes.The higher the cycles the smaller the variations due to ramdomness.



I've benchmarked 'single core' and 'multithreading' after going offline and stopping most unnecessary programs, CPU IDLEup to 3%. I have 6 cores and 12 logical processors, so the script was running 12 processes at once.

The benchmark data stops in different places, because:
 - single core: decided I won't wait longer that 40 min for a next point
 - multithreading: would go further, but was running out of memory (16GB), and the scripts in Sublime Text crashed