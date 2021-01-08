# Interactivity/diversity scoring of (online) threads containing arguments

#### Assumptions for the calculation of interactivity/argument diversity:
* Each included message from the dataset will portray at least one argument.
* Every argument can be assigned either to the 'pro' or 'con' camp in the discussion.
* The more an argument is repeated, the smaller the contribution a new repetition will make in terms of diversity/interactivity.
* The more a single argument is repeated, the greater a new repetition will weigh towards the extremes of echo chamber/opposition flood, i.e. constant repeating of identical reasoning will result quicker in an echo chamber or opposition flooding.
* A thread score below -0.5 is constituted an echo chamber. A thread receiving a score above 0.5 equals opposition flooding.

![alt text](https://github.com/Cwaterschoot/Interactivity_scoring/blob/main/Plots/auxiliary.png)

________________________________________________________________________________________________________________________________________________



Interactivity.py calculates the following indicators:


#### 1) Thread Interactivity Score

The full thread receives a single score based on the interactivity detected. This indicator informs you whether the presented collection of arguments constitutes an echo chamber, opposition flood or a balanced discussion. 
To provide this, each message receives a cumulative log operator, which differs from the individual log as it increases when the argument is already present. Using this factor, repetition of a single reasoning weighs heavier towards the extreme, either echo chamber or opposition flood.
This score is the difference between the opposition score (sum of opposition shares calculated on the cumulative log operators) and the echo score (sum of echo shares calculated on the cumulative log operators).

Calculating the log operator for both the echo and opposition scores requires **the cumulative count of the argument (j)** in each message at that point in time. Simply put, this variable equals the n-th iteration of the particular argument represented in the sample at the order given in the dataframe.

> <img src="https://latex.codecogs.com/gif.latex?Share_{i}\begin{cases}&space;\frac{j(x_{i})-1&space;-&space;log(j(x_{i})-1)}{N}&space;*&space;(-w)&space;&plus;&space;\frac{1}{N}&space;&&space;\text{&space;if&space;}&space;argument(x_{i})=argument(x_{0})&space;\\&space;\frac{j(x_{i})-log(j(x_{i})}{N}&space;&&space;\text{&space;if&space;}&space;argument(x_{i})&space;\ne&space;argument(x_{0})&space;\wedge&space;level1(x_{i})&space;\ne&space;level1(x_{0})\\&space;\frac{j(x_{i})-log(j(x_{i})}{N}&space;*(-1)&space;&&space;\text{&space;if&space;}&space;argument(x_{i})&space;\ne&space;argument(x_{0})&space;\wedge&space;level1(x_{i})&space;=level1(x_{0})&space;\\0&space;&\text{&space;if&space;}&space;i=0\end{cases}" />

> <img src="https://latex.codecogs.com/gif.latex?TIS_{T}&space;=\sum_{i=1}^{N}&space;share_i" />


#### 2) Message Interactivity Contribution

Individual messages will receive an interactivity score representing the extent that this message at the time of posting contributed to the overall thread score. Simply put, it is the difference between the thread score before the individual message was added and after. Subsequent identical arguments are downgraded by the individual log operator, which decreases the more an already presented argument is added. 

To derive this MIC indicator, the message share at that point in time  is calculated using the individual log operator, which, in contrast to the cumulative log used for TIS, decreases as argument X was already prevalent in the discussion. This share equals 1 minus the log of the cumulative count of the argument, i.e. j, divided by the number of arguments in the thread at the point in time of the message (i).

> <img src="https://latex.codecogs.com/gif.latex?MIC_{i}&space;\begin{cases}&space;\frac{(1-log(j(x_{i}))}{i}&space;*&space;(2-w)&&space;\text{&space;if&space;}&space;argument(x_{i})=argument(x_{0})&space;\\&space;\frac{(1-log(j(x_{i}))}{i}&space;&&space;\text{&space;if&space;}&space;argument(x_{i})&space;\ne&space;argument(x_{0})&space;\\&space;0&space;&&space;\text{&space;if&space;}&space;i=0&space;\end{cases}" />

The parent message of a thread always receives MIC = 0, as it is not a reply. Similarly, the thread score starts at 0. From the first reply onwards, the score is adjusted with each new reply. Following the TIS formula, opposition arguments will have their message share added to the overall score, the share from echo messages is substracted from the score. The actual message contribution from message (i) is the result from substracting the score at message (i) from the previous comment at time (i-1). The closer this score converges to 0, the smaller the interactive contribution of the message. Naturally, this contribution creeps closely in the ranges around 0 after numerous replies, as most will have been said at that point. 

##### 2.1) Contribution valuation

To determine whether a message is a valuable contribution to the thread in terms of interactivity and argument diversity, the distance between point 0 and the MIC is derived. Message (i) is deemed valuable if distance(MIC(i), 0) > distance(MIC(i-1), 0). An exception exists for the first reply, where the distance is not allowed to be smaller than 0.5, which would mean the reply showcases the same argument as the parent message, which cannot be deemed a valuable contribution to interactivity and argument diversity. 


#### 3) Dynamic Thread Interactivity Score

Iteratively, each following message receives a individual dynamic TIS. This score equals the TIS at that point in time, which can be used for echo chamber prediction,...
The dynamic TIS is included as a matrix in the output file, alongside the dynamic echo/opposition scores for each post.

![alt text](https://github.com/Cwaterschoot/Interactivity_scoring/blob/main/Plots/plot1.png)

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

#### Output:
* Output.xlsx: a file containing all the created variables and outcomes
* Written output containing the valuable replies and their argument categories, the final TIS and individual message contributions.
* Scatterplots (Plot1 & Plot2) to visualize dynamic TIS and MIS (Plot 1) and dynamic echo/opposition scores (Plot 2)


###### Example output:
<blockquote>

Echo score = 1.0954316545944391
  
Opposite score = 0.8290717052989449

Full thread interactivity score = -0.2663599492954942 

This thread is fairly balanced.
****************************************************************************************************
The closer the individual score to 0, the smaller the interactive contribution that the message makes. 

Individual interactivity contributions:

 [0, 0.5, 0.33333333333333326, -0.25, -0.13979400086720378, -0.16666666666666669, -0.14285714285714285, -0.08737125054200236, 0.11111111111111112, -0.06989700043360189, -0.047534431389121605, -0.08333333333333333, -0.030610769897849048, 0.0499264288811442, 0.034858583018689174, 0.024871250542002357, -0.03700429434720099, -0.02614393726401688, -0.01884978988446494, 0.034948500216800946, 0.024898987870492266, 0.01808818221236535]
****************************************************************************************************
Messages receiving an individual score with a greater distance from 0 compared to the previous reply are deemed valuable interaction. 

The following replies are valuable (parent message has label 0): [1, 5, 8, 11, 13, 16, 19] 

The corresponding arguments to these replies are: ['racist_contemp', 'POC', 'innocent', 'christian', 'racist_hist', 'def_nat', 'racist_contemp'] 
 keeping in mind that the parent reply has the label def_nat
 </blockquote>



### To do list:
* Allowance for multiple argument labels per message sample 
