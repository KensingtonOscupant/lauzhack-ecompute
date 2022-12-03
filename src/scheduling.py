import pandas as pd


def solve(jobs, time_tags):
    jobs = jobs.sort_values(by=['priority', 'deadline'], ascending=[False, True])

    schedule = pd.Series(index=time_tags.index)
    time_costs = time_tags.replace({'excess': 0, 'renewable': 1, 'grey': 2})
    for job_id in jobs['id']:
        prio_sorted_indices = time_costs[:jobs.loc[job_id,'deadline']]
        schedule[prio_sorted_indices[:jobs.loc[job_id,'length']]] = job_id
        time_costs.drop(prio_sorted_indices)

    if len(models) == 0:
        raise RuntimeError('No valid schedule was found.')

    schedule = [None] * len(time_tags)
    for s in models[-1]:
        if s.match('schedule', 2):
            schedule[s.arguments[0].number] = s.arguments[1].number
    return schedule
