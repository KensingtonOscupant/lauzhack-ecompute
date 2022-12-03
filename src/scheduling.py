import pandas as pd


def solve(jobs, time_tags):
    jobs = jobs.sort_values(by=['priority', 'deadline'], ascending=[False, True])

    schedule = pd.Series(index=time_tags.index)
    time_costs = time_tags.replace({'excess': 0, 'renewable': 1, 'grey': 2})
    for job_idx in jobs.index:
        valid_indices = time_costs[time_costs.index <= jobs.loc[job_idx,'deadline']]
        if jobs.loc[job_idx,'length'] > valid_indices.size:
            raise RuntimeError('No valid schedule possible')
        index_prio = valid_indices.argsort(kind='stable')

        schedule_index = index_prio[:jobs.loc[job_idx, 'length']]
        schedule[schedule_index] = jobs.loc[job_idx, 'id']
        time_costs = time_costs.drop(time_costs.index[schedule_index])

    return schedule


if __name__ == '__main__':
    import dataloader
    from random import choice

    data = dataloader.load_data()
    ass = pd.Series([choice(['renewable', 'excess', 'grey']) for _ in range(4*24*30)])
    ass.index = data.index[:len(ass)]
    print('Finished sampling.')

    schedule = solve(
        pd.DataFrame([
            {'id': 0, 'deadline': pd.to_datetime('20231225', format='%Y%m%d', utc='CET'), 'length': 24*30, 'priority': 10},
            {'id': 1, 'deadline': pd.to_datetime('20231226', format='%Y%m%d', utc='CET'), 'length': 200, 'priority': 5},
            {'id': 2, 'deadline': pd.to_datetime('20231227', format='%Y%m%d', utc='CET'), 'length': 35, 'priority': 5},
            ]),
        ass,
    )
    print(pd.concat((schedule, ass), ignore_index=True, axis=1))

