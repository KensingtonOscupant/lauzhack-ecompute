import os
import clingo
from clingo import Function, Number

class Job:
    def __init__(self, id, length, deadline):
        self.id = id
        self.length = length
        self.deadline = deadline
    
    def to_symbol(self):
        return Function('', [Number(self.id), Number(self.length), Number(self.deadline)])

class SchedulingContext:
    def __init__(self, jobs, time_tags):
        self._jobs = jobs
        self._costs = [0] * len(time_tags)
        current_costs = 0
        for current_tag in 'excess', 'renewable', 'grey':
            for i, tag in enumerate(time_tags):
                if tag == current_tag:
                    self._costs[i] = current_costs
                    current_costs += 1

    def job(self):
        return [job.to_symbol() for job in self._jobs]

    def horizon(self):
        return Number(len(self._costs))

    def costs(self, t):
        return Number(self._costs[t.number])


def solve(jobs, time_tags):
    ctl = clingo.Control(arguments=['--models=0'])
    ctl.load(os.path.join('encodings', 'scheduling.lp'))
    ctl.ground([('base', [])], context=SchedulingContext(jobs, time_tags))

    models = []
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            models.append(model.symbols(atoms=True))

    if len(models) == 0:
        raise RuntimeError('No valid schedule was found.')

    schedule = [None] * len(time_tags)
    for s in models[-1]:
        if s.match('schedule', 2):
            schedule[s.arguments[0].number] = s.arguments[1].number
    return schedule
