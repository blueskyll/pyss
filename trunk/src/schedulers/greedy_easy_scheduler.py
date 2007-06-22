from common import CpuSnapshot
from base.prototype import JobStartEvent

from easy_scheduler import EasyBackfillScheduler

default_sort_key_functions = (
    lambda job : -job.submit_time, # sort by reverse submission time
    lambda job : job.submit_time,
    lambda job : job.num_processors,
    lambda job : job.estimated_run_time,
    # TODO: why don't we use this one?
    #lambda job : job.num_processors * job.estimated_run_time,
)

def basic_score_function(list_of_jobs):
    return sum(job.num_processors * job.estimated_run_time for job in list_of_jobs)

class  GreedyEasyBackFillScheduler(EasyBackfillScheduler):
    def __init__(self, num_processors, sort_key_functions=None, score_function=None):
        super(GreedyEasyBackFillScheduler, self).__init__(num_processors)

        if sort_key_functions is None:
            self.sort_key_functions = default_sort_key_functions
        else:
            self.sort_key_functions = sort_key_functions

        if score_function is None:
            self.score_function = basic_score_function
        else:
            self.score_function = score_function

    def _schedule_jobs(self, current_time):
        self.unscheduled_jobs.sort(key = self._submit_job_sort_key)

        result = super(GreedyEasyBackFillScheduler, self)._schedule_jobs(current_time)

        self.unscheduled_jobs.sort(key = self._submit_job_sort_key)

        return result

    def _backfill_jobs(self, current_time):
        "Overriding parent method"
        self._reorder_jobs_in_approximate_best_order(current_time)
        return super(GreedyEasyBackFillScheduler, self)._backfill_jobs(current_time)

    def canBeBackfilled(self, job, current_time):
        "Overriding parent method"
        return self.cpu_snapshot.canJobStartNow(job, current_time)

    def _scored_tail(self, cpu_snapshot, sort_key_func):
        tmp_cpu_snapshot = cpu_snapshot.copy()
        tentative_list_of_jobs = []
        tail = self.unscheduled_jobs[1:]
        for job in sorted(tail, key=sort_key_func):
            if tmp_cpu_snapshot.canJobStartNow(job, current_time):
                tmp_cpu_snapshot.assignJob(job, current_time)
                tentative_list_of_jobs.append(job)

        return self.score_function(tentative_list_of_jobs), tentative_list_of_jobs

    def _reorder_jobs_in_approximate_best_order(self, current_time):
        if len(self.unscheduled_jobs) == 0:
            return

        cpu_snapshot_with_job = self.cpu_snapshot.copy()
        cpu_snapshot_with_job.assignJobEarliest(first_job, current_time)

        # get tail from best (score, tail) tuple
        best_tail = max(
            self._scored_tail(cpu_snapshot_with_job, sort_key_func)
            for sort_key_func in self.sort_key_functions
        )[1]

        first_job = self.unscheduled_jobs[0]
        self.unscheduled_jobs = best_tail + [first_job]

    def _submit_job_sort_key(self, job):
        return job.submit_time

    def print_waiting_list(self):
        for job in self.unscheduled_jobs:
            print job
        print
