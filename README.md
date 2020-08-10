# Dating-Bail-Out
Inspired by Hannah Fry's TED talk about love.

I was curious is it really the case that if it was just statistics you should dump first 37% of partners and then stick tothe first best one so far. The next question waswhathappens when there's an improvement (increase in attractiveness)

After failed attempt using Python lists (the final values were wrong) I decided to use Numpy

I've taken into account 3 options in approaching the issue:
Option 1. Average score (if there's noimprovement should stay flat

Option 2. Try to find someone better that the one you just had (if unlucky you end up eith the last one)

Option 3. Main one: Try to find someone better than you had so far (if unlucky you end up eith the last one)




Please change the main folder directories to yours (if the main folder generation is in if: ... and alse: ...)

You can use steps variable to check incrementally smaller populations down to zero.

The script gives a folder with the settings as the name with the settings. Inside there are folders and in each detailed  lists of Option 1, Option 2 and Option 3 and text file with summary  of steps, time, max values, when they happened (index) and crossing of Option 2 and Option 3. Untill some point Option 3 is better than Option 2.

The bigger population and the number of cycles the longerit takes.The higher the cycles the smaller the variations due to ramdomness.
