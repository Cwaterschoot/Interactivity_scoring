# Interactivity/diversity scoring of (online) threads containing arguments

#### Assumptions for the calculation of interactivity/argument diversity:
* Each included message from the dataset will portray at least one argument.
* Every argument can be assigned either to the 'pro' or 'con' camp in the discussion.
* The more an argument is repeated, the smaller the contribution a new repetition will make in terms of diversity/interactivity.
* The more a single argument is repeated, the greater a new repetition will weigh towards the extremes of echo chamber/opposition flood, i.e. constant repeating of identical reasoning will result quicker in an echo chamber or opposition flooding.
* A thread score below -0.5 is constituted an echo chamber. A thread receiving a score above 0.5 equals opposition flooding.


________________________________________________________________________________________________________________________________________________



scoring.py calculates the following indicators:


#### 1) Thread Interactivity Score

The full thread receives a single score based on the interactivity detected. This indicator informs you whether the presented collection of arguments constitutes an echo chamber, opposition flood or a balanced discussion. 
To provide this, each message receives a cumulative log operator, which differs from the individual log as it increases when the argument is already present. Using this factor, repetition of a single reasoning weighs heavier towards the extreme, either echo chamber or opposition flood.
This score is the difference between the opposition score (sum of opposition shares calculated on the cumulative log operators) and the echo score (sum of echo shares calculated on the cumulative log operators).

Calculating the log operator for both the echo and opposition scores requires **the cumulative count of the argument (j)** in each message at that point in time. Simply put, this variable equals the n-th iteration of the particular argument represented in the sample at the order given in the dataframe.


#### 2) Message Interactivity Contribution

Individual messages will receive an interactivity score representing the extent that this message at the time of posting contributed to the overall thread score. Simply put, it is the difference between the thread score before the individual message was added and after. Subsequent identical arguments are downgraded by the individual log operator, which decreases the more an already presented argument is added. 

To derive this MIC indicator, the message share at that point in time  is calculated using the individual log operator, which, in contrast to the cumulative log used for TIS, decreases as argument X was already prevalent in the discussion. This share equals 1 minus the log of the cumulative count of the argument, i.e. j, divided by the number of arguments in the thread at the point in time of the message (i).

The parent message of a thread always receives MIC = 0, as it is not a reply. Similarly, the thread score starts at 0. From the first reply onwards, the score is adjusted with each new reply. The closer this score converges to zero, the smaller the interactive contribution of the message. Naturally, this contribution creeps closely in the ranges around 0 after numerous replies, as most will have been said at that point. 


##### 2.1) Contribution valuation

To determine whether a message is a valuable contribution to the thread in terms of interactivity and argument diversity, the current MIC value of the post (i) is compared to that one of the previous comment (i-1). Replies with a greater MIC value than the previous post are deemed valuable contributions. An exception exists for the first reply, where MIC is not allowed to be smaller than 0.5, which would mean the reply showcases the same argument as the parent message, which cannot be deemed a valuable contribution to interactivity and argument diversity. 


#### 3) Dynamic Thread Interactivity Score

Iteratively, each following message receives a individual dynamic TIS. This score equals the TIS at that point in time, which can be used for echo chamber prediction,...
The dynamic TIS is included as a matrix in the output file, alongside the dynamic echo/opposition scores for each post.

