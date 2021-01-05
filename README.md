# Interactivity_scoring
Interactivity scoring of online threads and messages


Interactivity.py calculates the following indicators:

#### 1) Message Interactivity Contribution

Individual messages will receive an interactivity score representing the extent that this message at the time of posting contributed to the overall thread score. Simply put, it is the difference between the thread score before the individual message was added and after. Subsequent identical arguments are downgraded by the individual log operator, which decreases the more an already presented argument is added. 

#### 2) Thread Interactivity Score

The full thread receives a single score based on the interactivity detected. This indicator informs you whether the presented collection of arguments constitutes an echo chamber, opposition flood or a balanced discussion. 
To provide this, each message receives a cumulative log operator, which differs from the individual log as it increases when the argument is already present. Using this factor, repetition of a single reasoning weighs heavier towards the extreme, either echo chamber or opposition flood.
This score is the difference between the opposition score (sum of opposition shares calculated on the cumulative log operators) and the echo score (sum of echo shares calculated on the cumulative log operators).


#### 3) Dynamic Thread Interactivity Score

Iteratively, each following message receives a individual dynamic TIS. This score equals the TIS at that point in time, which can be used for echo chamber prediction,...


#### How to:

The following is needed:
* dataset: Labelled message sheet
* level1: Argument dataframe with pro variable and con variable (listing the arguments)
* weight: Weight assignment for extra punishment repetition of parent argument

Defaults:
* testdf.xlsx
* arg_pro_con.xlsx
* 1.1

> python interactivity.py --dataset data/testdf.xlsx --weight 1.1 --level1 argumentation/arg_pro_con.xlsx


