'''
Notes:

The main problem for STDP does indeed appear to be the running of the STDP code
and not the get_past_values_seq method of RecentStateMonitor. So, code generation
and optimisation efforts should be focussed on the code in stdp.py.

Here is the code currently generated by stdp.py

------ no delays ---------

****** PRE **********
for _i in spikes:
    A_pre[_i]+=dA_pre
    w[_i,:]+=A_post
    w[_i,:]=clip(w[_i,:],0.000000,0.010000)
****** POST *********
for _i in spikes:
    A_post[_i]+=dA_post
    w[:,_i]+=A_pre
    w[:,_i]=clip(w[:,_i],0.000000,0.010000)
    
    
------- heterogeneous delays ------

****** PRE_IMMEDIATE **********
for _i in spikes:
    A_pre[_i]+=dA_pre

****** PRE_DELAYED **********
for _j, _i in enumerate(spikes):
    A_post__delayed = A_post__delayed_values_seq[_j]
    w[_i,:]+=A_post__delayed

    w[_i,:] = clip(w[_i,:], 0.000000, 0.010000)
****** POST *********
for _i in spikes:
    A_post[_i]+=dA_post
for _j, _i in enumerate(spikes):
    A_pre__delayed = A_pre__delayed_values_seq[_j]
    w[:,_i]+=A_pre__delayed

    w[:,_i] = clip(w[:,_i], 0.000000, 0.010000)


with some obvious speedups this should become (in Python):

------ no delays ---------

****** PRE **********
A_pre[spikes] += dA_pre
for _i in spikes:
    w[_i,:]+=A_post
    w[_i,:]=clip(w[_i,:],0.000000,0.010000)
****** POST *********
A_post[spikes] += dA_post
for _i in spikes:
    w[:,_i]+=A_pre
    w[:,_i]=clip(w[:,_i],0.000000,0.010000)

For the general case, we can't do much better than that because:

* w[i,:]+=A_post has to wokr for dense, sparse and dynamic matrices
  - for dense it would be better to replace with
       w[spikes,:]+=A_post (you probably need to reshape though)
  - for sparse but not dynamic it could be done inline maybe
       asarray(w[i,:])+=A_post
  - but this only works for row access, not for column access!
  - for dynamic, there's no getting around it
* w[i,:]=clip(...) can be made inline for dense matrices, or for sparse
  but not dynamic, but w[:,i] only for dense.

A weave based clip(matrix, spikes, low, high) could significantly improve speed,
as the profiler suggests a decent amount of time is spent on clipping.

For a C++ based optimisation, can we avoid the for loop? In Connection.propagate
we don't have to worry about data references because we only have read access to
w, but we can't avoid it here. One option is the same as the Connection.propagate
solution: we have Python code that generates a list of rows/cols and then the
output of the STDP code would act on a second list, and then these values would
then be put back into the original data structure. But it's not clear that this
would be a huge speedup as it involves several stages.

Another option would be to paste pieces of C code together that correctly
preserve the references for the different data structures. Each piece of C code
would do its iteration, and produce a variable as a C++ reference for the
next piece of code. This requires a bit more thought to implement, but has
potentially high payoffs. It may also have high payoffs for ordinary
Connection.propagate as then the entire routine would be in C++ and you could
avoid the Python list comprehension and creation of data structures that we
have at the moment.

'''

from brian import *
from scipy import weave
from brian.experimental.new_c_propagate import *

def make_update_on_pre(G_pre, G_post, dA_pre, synapses, gmax):
    code = iterate_over_spikes('_j', '_spikes',
                (load_required_variables('_j', {'A_pre':G_pre.A_pre}),
                 transform_code('A_pre += dA_pre', vars={'dA_pre':float(dA_pre)}),
                 iterate_over_row('_k', 'w', synapses.W, '_j',
                    (load_required_variables('_k', {'A_post':G_post.A_post}),
                     transform_code('w += A_post'),
                     ConnectionCode('''
                         if(w<0) w=0;
                         if(w>gmax) w=gmax;
                         ''', vars={'gmax':gmax})))))
    code, vars = code.codestr, code.vars
    vars['_spikes'] = None
    vars['_spikes_len'] = None
    vars_list = vars.keys()
    print code
    def f(_spikes):
        if len(_spikes):
            if not isinstance(_spikes, ndarray):
                _spikes = array(_spikes, dtype=int)
            vars['_spikes'] = _spikes
            vars['_spikes_len'] = len(_spikes)
            weave.inline(code, vars_list,
                         local_dict=vars,
                         compiler='gcc',
                         extra_compile_args=['-O3'])
    return f

def make_update_on_post(G_pre, G_post, dA_post, synapses, gmax):
    code = iterate_over_spikes('_j', '_spikes',
                (load_required_variables('_j', {'A_post':G_post.A_post}),
                 transform_code('A_post += dA_post', vars={'dA_post':float(dA_post)}),
                 iterate_over_col('_i', 'w', synapses.W, '_j',
                    (load_required_variables('_i', {'A_pre':G_pre.A_pre}),
                     transform_code('w += A_pre'),
                     ConnectionCode('''
                         if(w<0) w=0;
                         if(w>gmax) w=gmax;
                         ''', vars={'gmax':gmax})))))
    code, vars = code.codestr, code.vars
    vars['_spikes'] = None
    vars['_spikes_len'] = None
    vars_list = vars.keys()
    print code
    def f(_spikes):
        if len(_spikes):
            if not isinstance(_spikes, ndarray):
                _spikes = array(_spikes, dtype=int)
            vars['_spikes'] = _spikes
            vars['_spikes_len'] = len(_spikes)
            weave.inline(code, vars_list,
                         local_dict=vars,
                         compiler='gcc',
                         extra_compile_args=['-O3'])
    return f

if __name__=='__main__':
    from time import time
    
    structure = 'sparse'
    
    N=1000
    taum=10*ms
    tau_pre=20*ms
    tau_post=tau_pre
    Ee=0*mV
    vt=-54*mV
    vr=-60*mV
    El=-74*mV
    taue=5*ms
    F=15*Hz
    gmax=.01
    dA_pre=.01
    dA_post=-dA_pre*tau_pre/tau_post*1.05
    
    eqs_neurons='''
    dv/dt=(ge*(Ee-vr)+El-v)/taum : volt   # the synaptic current is linearized
    dge/dt=-ge/taue : 1
    '''
    
    input=PoissonGroup(N,rates=F)
    neurons=NeuronGroup(1,model=eqs_neurons,threshold=vt,reset=vr)
    synapses=Connection(input,neurons,'ge',weight=rand(len(input),len(neurons))*gmax, structure=structure)
    neurons.v=vr
    
    #stdp=ExponentialSTDP(synapses,tau_pre,tau_post,dA_pre,dA_post,wmax=gmax)
    ## Explicit STDP rule
    eqs_stdp='''
    dA_pre/dt=-A_pre/tau_pre : 1
    dA_post/dt=-A_post/tau_post : 1
    '''
    dA_post*=gmax
    dA_pre*=gmax
#    stdp=STDP(synapses,eqs=eqs_stdp,pre='A_pre+=dA_pre;w+=A_post',
#              post='A_post+=dA_post;w+=A_pre',wmax=gmax)
    G_pre = NeuronGroup(N, 'dA_pre/dt=-A_pre/tau_pre:1')
    G_post = NeuronGroup(1, 'dA_post/dt=-A_post/tau_post:1')
    
    synapses.compress()
    
    update_on_pre_spikes = make_update_on_pre(G_pre, G_post, dA_pre, synapses, gmax)
    update_on_post_spikes = make_update_on_post(G_pre, G_post, dA_post, synapses, gmax)
    
    M_pre = SpikeMonitor(input, function=update_on_pre_spikes)
    M_post = SpikeMonitor(neurons, function=update_on_post_spikes)
    
    rate=PopulationRateMonitor(neurons)
    
    start_time=time()
    run(100*second,report='text')
    print "Simulation time:",time()-start_time
    
    subplot(311)
    plot(rate.times/second,rate.smooth_rate(100*ms))
    subplot(312)
    plot(synapses.W.todense()/gmax,'.')
    subplot(313)
    hist(synapses.W.todense()/gmax,20)
    show()
