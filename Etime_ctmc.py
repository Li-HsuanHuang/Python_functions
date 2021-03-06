# Fit continuous-Markov chains on an arbitrary time-series data
# and compute the expected time spent from any state before absorption

import numpy as np

def statetimetally(ts,times):
    if (len(np.diff(times)<= 0) >= 1):
        cumtseq = np.cumsum(times)
    else:
        cumtseq = times
    ind = np.where(np.diff(ts)!=0)[0]
    ts1 = np.append(ts[ind],ts[-1])
    tseq1 = np.append(cumtseq[ind],cumtseq[-1])
    if (np.min(ts1) == 0):
        N = np.max(ts1) + 1
    else:
        N = np.max(ts1)
    ts1 -= 1
    stally = np.zeros(N)
    diffseq = np.diff(tseq1)
    for i in range(len(ts1)-1):
        stally[ts1[i+1]] += diffseq[i]
    stally[ts1[0]] += tseq1[0]
    return stally

# This function creates a transition matrix recording state transitions.
# type: continuous- or discrete CTMC
# This takes care of 0 index state.
def counttrans(ts,type='continuous'):
    N = np.max(ts)
    if (np.min(ts) = 0):
        N += 1
    if (type=='continuous'):
        ind = np.where(np.diff(ts)!=0)[0]
        ts = np.append(ts[ind],ts[-1])
    transmat = np.zeros((N,N))
    for i in range(1,len(ts)-1):
        transmat[ts[i],ts[i+1]] += 1
    return transmat


# Function for creating a CTMC matrix given states, times, and the number of states.
def trainCTMC(ts,tseq,N):
    transmat = counttrans(ts,'continuous')
    timespent = statetimetally(ts,tseq)
    transratemat = transmat
    for i in range(transmat.shape[0]):
        transratemat[i,] = transratemat[i,]/timespent[i]
        transratemat[i,i] = - np.sum(transratemat[i,])
    return transratemat



# Function for compute expected time spent before absorption
# ds: dead-end state(s) (absorbing state(s))
# Putting the absorbing states in top rows
def expected_time(transratemat,ds):
    m = transratemat.shape[0]
    n = len(ds)
    #transratemat = trainCTMC(ts,cumtseq,m)
    A = transratemat[n:,n:]
    M = np.linalg.inv(-A)
    E = np.sum(M,axis=1)
    return E


###########################################################################
# Example 
ts = np.array([1,1,2,3,2,1,4,5,1])   # states
tseq = np.array([2,3,1,4,5,7,8,1,1]) # time spent in each associated state

# Train CTMC
N = np.max(ts)
transratemat = trainCTMC(ts,tseq,N)

# Supply absorbing states.
ds = np.array([0,1])

# Compute expected time to get from state i to any absorbing state in ds.
exp_time = expected_time(transratemat,ds)
print(exp_time)
