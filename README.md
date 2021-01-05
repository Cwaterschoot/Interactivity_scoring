# Interactivity scoring of (online) messages containing arguments

Interactivity.py calculates the following indicators:

#### 1) Message Interactivity Contribution

Individual messages will receive an interactivity score representing the extent that this message at the time of posting contributed to the overall thread score. Simply put, it is the difference between the thread score before the individual message was added and after. Subsequent identical arguments are downgraded by the individual log operator, which decreases the more an already presented argument is added. 

> MIC(X) = (1-log(j)) / n        with n = number of replies at the time of post X, j = cumulative count of argumentclass(X)

#### 2) Thread Interactivity Score

The full thread receives a single score based on the interactivity detected. This indicator informs you whether the presented collection of arguments constitutes an echo chamber, opposition flood or a balanced discussion. 
To provide this, each message receives a cumulative log operator, which differs from the individual log as it increases when the argument is already present. Using this factor, repetition of a single reasoning weighs heavier towards the extreme, either echo chamber or opposition flood.
This score is the difference between the opposition score (sum of opposition shares calculated on the cumulative log operators) and the echo score (sum of echo shares calculated on the cumulative log operators).

> Echo score = ∀ X with L1(X) = L1(X0):  Σ (j(X)-log(j(X)) / N

A high echo score means large presence of argumentation that stems out of the same camp as the parent message. 

> Opposition score = ∀ Y with L1(Y) != L1(X0):  Σ (j(Y)-log(j(Y)) / N


> TIS = Opposition score - Echo score



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
* Scatterplots (Plot1 & Plot2) to visualize TIS and MIS (Plot 1) and dynamic echo/opposition scores (Plot 2)
