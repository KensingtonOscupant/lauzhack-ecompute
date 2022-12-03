% KNOWLEDGE
time(0..@horizon - 1).
job(I,L,D) :- (I,L,D) = @job.

% GENERATE
% Assign at most one assignment per time step
0 { schedule(T,I) : job(I,_,_) } 1 :- time(T).

% TEST
% Every job must be scheduled as much as its long
:- job(I,L,_), L1 = #sum { 1, T : schedule(T,I) }, L != L1.

% Every job must finish within its deadline
:- job(I,_,D), schedule(I,T), T > D.

% OPTIMIZE
% Summation and minimization of costs
cost(T,I,@costs(T)) :- schedule(T,I).
costs(CS) :- CS = #sum { C,T : cost(T,_,C) }.

#minimize { C : costs(C) }.
