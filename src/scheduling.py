import pandas as pd


def solve(jobs, time_tags):
    # Jobs are scheduled after one another, sorted by priority and deadline.
    # By scheduling jobs with a short deadline first, we ensure that they run.
    jobs = jobs.sort_values(by=['priority', 'deadline'], ascending=[False, True])

    schedule = pd.Series(index=time_tags.index)
    time_costs = time_tags.replace({'excess': 0, 'renewable': 1, 'grey': 2})
    for job_idx in jobs.index:
        # We sort the indices by their energy costs, and then choose the first ones
        # Select indices that are within the deadline
        valid_indices = time_costs[time_costs.index <= jobs.loc[job_idx,'deadline']]
        if jobs.loc[job_idx,'length'] > valid_indices.size:
            raise RuntimeError('No valid schedule possible')

        # Sort the indices by energy costs
        index_prio = valid_indices.argsort(kind='stable')

        # Schedule at as many indices as we need (as the job is long), and drop them
        # so none is selected twice
        schedule_index = index_prio[:jobs.loc[job_idx, 'length']]
        schedule[schedule_index] = jobs.loc[job_idx, 'id']
        time_costs = time_costs.drop(time_costs.index[schedule_index])

    return schedule
