# Interactivity/diversity scoring of (online) threads containing arguments

#### Assumptions for the calculation of interactivity/argument diversity:
* Each included message from the dataset will portray at least one argument.
* Every argument can be assigned either to the 'pro' or 'con' camp in the discussion.
* The more an argument is repeated, the smaller the contribution a new repetition will make in terms of diversity/interactivity.
* The more a single argument is repeated, the greater a new repetition will weigh towards the extremes of echo chamber/opposition flood, i.e. constant repeating of identical reasoning will result quicker in an echo chamber or opposition flooding.
* A thread score below -0.5 is constituted an echo chamber. A thread receiving a score above 0.5 equals opposition flooding.


________________________________________________________________________________________________________________________________________________


Arguments:

  * dataset : labelled discussion threads 
  * weight : extra weight for repetition of argument in first post
  * level1 : dataframe consisting of two variables: pro arguments & con arguments

scoring.py calculates the following indicators:


#### 1) Thread Interactivity Score

The full thread receives a single score based on the interactivity detected. This indicator informs you whether the presented collection of arguments constitutes an echo chamber, opposition flood or a balanced discussion. 
To provide this, each message receives a cumulative log operator, which differs from the individual log as it increases when the argument is already present. Using this factor, repetition of a single reasoning weighs heavier towards the extreme, either echo chamber or opposition flood.
This score is the difference between the opposition score (sum of opposition shares calculated on the cumulative log operators) and the echo score (sum of echo shares calculated on the cumulative log operators).


#### 2) Message Interactivity Contribution

Individual messages will receive an interactivity score representing the extent that this message at the time of posting contributed to the overall thread score. Simply put, it is the difference between the thread score before the individual message was added and after. Subsequent identical arguments are downgraded by the individual log operator, which decreases the more an already presented argument is added. 


##### 2.1) Interactive contribution

To determine whether a message is an interactive contribution to the thread in terms of interactivity and argument diversity, the current MIC value of the post (i) is compared to that one of the previous comment (i-1). Replies with a greater MIC value than the previous post are deemed interactive. An exception exists for the first reply, where MIC is not allowed to be smaller than 0.5, which would mean the reply showcases the same argument as the parent message, which cannot be deemed a valuable contribution to interactivity and argument diversity. 


#### 3) Dynamic Thread Interactivity Score

Iteratively, each following message receives a individual dynamic TIS. This score equals the TIS at that point in time, which can be used for echo chamber prediction,...
The dynamic TIS is included as a matrix in the output file.

