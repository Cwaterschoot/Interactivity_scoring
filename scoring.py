import pandas as pd
import math
import matplotlib.pyplot as plt
import argparse 
import numpy as np
plt.style.use('seaborn-whitegrid')

# arguments on level 1
# now called by args


parser = argparse.ArgumentParser()
parser.add_argument("--dataset", default="testdf.xlsx", help = "labelled messages")
parser.add_argument('--weight', type=float, default=1.1, help='extra weight repetitive parent argument')
parser.add_argument("--level1", default="arg_pro_con.xlsx", help = "argument dataframe, variable for pro and con needed")
args = parser.parse_args()

df = pd.read_excel(args.dataset)
weight = args.weight
level1 = pd.read_excel(args.level1)

# Assign pro and con lists without missing values if they have different sizes
con_temp = list(level1.con)
con = [x for x in con_temp if str(x) != 'nan']
pro_temp = list(level1.pro)
pro = [x for x in pro_temp if str(x) != 'nan']

# assign necessary variables for computation from input dataframe
l3 = df.argument
arg_num = len(df.index)


#################################################################
#################################################################
# Prereq assignments:
#################################################################
#################################################################

# Assign each message to either pro or con (level 1)
l1 = []

for i in l3:
    if i in pro:
        level1 = "pro"
        l1.append(level1)
    else:
        level1 = "con"
        l1.append(level1)

df["level1"] = l1

# cumulative count of argumentation for log operator
cumsum_arg = df.groupby('argument').cumcount() + 1
df["cumsum_l3"] = cumsum_arg


# creating log operator for each message (repetition of argument will weigh less for interactive contribution)
log_op = []

for j in cumsum_arg:
    operator = (1 - math.log(j, 10))
    log_op.append(operator)

df["log_operator_ind"] = log_op


# create cum log operator for thread interactivity (repetition of argument will weigh more towards extremes)
log_op_cumul = []

for j in cumsum_arg:
    operator = (j - math.log(j, 10)) 
    log_op_cumul.append(operator)

df["log_operator_cumul"] = log_op_cumul



# creating equalizers to level 1 and level 3 of parent message
parent_arg = df.argument[0]
parent_l1 = df.level1[0]
l1_equal = []
l3_equal = []

for k in l3:
    if k == parent_arg:
        l3_equal.append(True)
    else:
        l3_equal.append(False)

for k in l1:
    if k == parent_l1:
        l1_equal.append(True)
    else:
        l1_equal.append(False)

df["l1_equal"] = l1_equal
df["l3_equal"] = l3_equal


#################################################################
#################################################################
# SCORING:
#################################################################
#################################################################

def MIC(df): 
    reply_counter = 0
    message_score = []

    for row in df.itertuples():
        if reply_counter == 0: # Parent message receives score
            m_interact = 0
            message_score.append(m_interact)
            score_after = 0
            reply_counter = reply_counter +2
        else:
                score_before = score_after # basic scoring for each further reply
                if row.l3_equal ==False:
                    m_interact = row.log_operator_ind / reply_counter 
                else:
                    m_interact = row.log_operator_ind / reply_counter * (2-weight)
                reply_counter = reply_counter +1

                message_score.append(m_interact)
            

    df["message_interactivity_value"] = message_score
    return(df)

####################################################################

def TIS(df):
    d = {}
    rows = len(df)

    for x in range(0, len(df)):
        args = x + 1
        d["string{0}".format(x)] = []
        for row in df.head(args).itertuples():
            if args == 1:
                interact_share=0
                d["string{0}".format(x)].append(interact_share)
            else:
                if row.l3_equal == False:
                    interact_share = row.log_operator_cumul / args            
                else:
                
                    if row.cumsum_l3 == args:
                        interact_share = row.cumsum_l3 / args
                    else:
                        if row.log_operator_cumul == 1:
                            interact_share = 1 / args
                        else: 
                            interact_share = (((row.cumsum_l3-1) - math.log(row.cumsum_l3-1, 10)) / args * weight) + (1/args)
                d["string{0}".format(x)].append(interact_share)
        d["string{0}".format(x)].extend([0 for i in range(rows-args)])
                        
    dynamics = list(d.values())
    dyna_df = df

    for x in range(0, len(df)):
        dyna_df[str(x)] = dynamics[x]

    # Creating list with all echo and opposition scores by summing through the df
    echo_dyna = []
    oppo_dyna = []

    for x in range(0, len(df)):
        echo2 = df.loc[dyna_df['l1_equal'] == True, str(x)].sum()
        echo_dyna.append(echo2)
        oppo2 = df.loc[dyna_df['l1_equal'] == False, str(x)].sum()
        oppo_dyna.append(oppo2)
    

    dyna_df["echo"] = echo_dyna
    dyna_df["opposite"] = oppo_dyna

    # Calculating the thread score at post X by following the formula opposition - echo 
    dynamic_score = []

    for x in range(0, len(df)):
        score = oppo_dyna[x] - echo_dyna[x]
        dynamic_score.append(score)


    df["dynamic_score"] = dynamic_score
    return(df)

#####################################################################

def valuable(df):
    message_score = df.message_interactivity_value
    length = len(message_score)
    valuable = []
    var_val = []
    for i in range(length):
        if i==0:
            var_val.append(False)
        else:
            cur = message_score[i]
            prev = message_score[i-1]
            if (i == 1 and cur < 0.5):
                var_val.append(False)         # exception if first reply is same L3 than parent (this is no valuable interaction!)
            else:
                if cur > prev: # valuable interaction if distance is greater than previous comment
                    valuable.append(i)
                    var_val.append(True)
                else:
                    var_val.append(False)
    df["Valuable"] = var_val
    return(df)



def val_index(df):
    valuable = []
    length = len(df.message_interactivity_value)
    for i in range(length):
        if df.Valuable[i] == True:
            valuable.append(i)
        else:
            pass
    return(valuable)
            


#################################################################
#################################################################
# CALCULATING
#################################################################
#################################################################

# scoring:
df = MIC(df)
df = TIS(df)
df = valuable(df)

# getting relevant variables out of df for easy printing:
message_score = df.message_interactivity_value
valuable = val_index(df)
echo_dyna = df.echo
oppo_dyna = df.opposite
dynamic_score = df.dynamic_score

#################################################################
#################################################################
# OUTPUT 
#################################################################
#################################################################

df.to_excel("output.xlsx")

print("This thread contains", arg_num, "messages, with the parent message stating the argument of", l3[0], "which belongs to the", l1[0], "camp.", "\n")
print("The thread contains", l1_equal.count(True), l1[0], "messages and", l1_equal.count(False), "comments of the opposition camp.")
print('*'*100)
print("echo score =", echo_dyna[arg_num-1])
print("opposite score =", oppo_dyna[arg_num-1])
print("full thread interactivity score =",dynamic_score[arg_num-1], "\n")

if dynamic_score[arg_num-1] > 0.5:
    print("This thread experiences a flood of opposition messaging drowning out the messages of standpoint",l1[0], ". \n")
else:
    if dynamic_score[arg_num-1] < -0.5:
        print("This thread is an echo chamber in terms of", l1[0], "messaging.", "\n")
    else:
        print("This thread is fairly balanced.")
        
        
print('*'*100)
print("The closer the individual score to 0, the smaller the interactive contribution that the message makes.", "\n")
print("individual interactivity contributions", "\n",message_score.to_string())
print('*'*100)
print("Messages receiving an individual score with a greater distance from 0 compared to the previous reply are deemed valuable interaction.", "\n")
print("The following replies are valuable (parent message has label 0):", valuable, "\n")
print("The corresponding arguments to these replies are:", list(l3[valuable]), "\n", "keeping in mind that the parent reply has the label", l3[0])
print('*'*100)





#################################################################
#################################################################
# PLOTS
#################################################################
#################################################################

#1
x = list(range(0, arg_num))
y =  df.message_interactivity_value
f = plt.figure()
z = df.dynamic_score

plt.plot(x, z, '-ok', color='blue', label="TIS score")
plt.axhspan(-2, -0.5, facecolor='r', alpha=0.05)
plt.axhspan(0.5, 2, facecolor='r', alpha=0.05)
plt.axhspan(-0.5, 0.5, facecolor='g', alpha=0.05)
plt.ylim(-2, 2);
plt.xlabel("Message index (i)")
plt.ylabel("TIS score")
plt.legend();
f.savefig("plot-dTIS.png", bbox_inches='tight')


#2
k = plt.figure()

plt.plot(x,y, '-ok', color='black', label='MIC score')

plt.ylim(0, 1);
plt.xlabel("Message index (i)")
plt.ylabel("MIC score")
plt.legend();
k.savefig("plot-MIC.png", bbox_inches='tight')


#3
x = list(range(0, arg_num))
y =  df.opposite
g = plt.figure()
plt.plot(x, y, '-ok', color='black', label="Opposite score at post X")
z = df.echo
plt.plot(x, z, '-ok', color='blue', label="Echo score at post X")
plt.ylim(-1, 2);
plt.legend();
g.savefig("plot-echo-oppo.png", bbox_inches='tight')
