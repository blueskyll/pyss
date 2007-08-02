#! /usr/bin/env python2.4

import sys
if __debug__:
    import warnings
    #warnings.warn("Running in debug mode, this will be slow... try 'python2.4 -O %s'" % sys.argv[0])

from base.workload_parser import parse_lines
from base.prototype import _job_inputs_to_jobs
from schedulers.simulator import run_simulator
import optparse

from schedulers.fcfs_scheduler import FcfsScheduler

from schedulers.conservative_scheduler import ConservativeScheduler
from schedulers.double_conservative_scheduler import DoubleConservativeScheduler

from schedulers.easy_scheduler import EasyBackfillScheduler
from schedulers.double_easy_scheduler import DoubleEasyBackfillScheduler
from schedulers.greedy_easy_scheduler import GreedyEasyBackfillScheduler
from schedulers.easy_plus_plus_scheduler import EasyPlusPlusScheduler
from schedulers.lookahead_easy_scheduler import LookAheadEasyBackFillScheduler
from schedulers.shrinking_easy_scheduler import ShrinkingEasyScheduler


def parse_options():
    parser = optparse.OptionParser()
    parser.add_option("--num-processors", type="int", \
                      help="the number of available processors in the simulated parallel machine")
    parser.add_option("--input-file", \
                      help="a file in the standard workload format: http://www.cs.huji.ac.il/labs/parallel/workload/swf.html")
    parser.add_option("--scheduler", 
                      help="1) FcfsScheduler, 2) ConservativeScheduler, 3) DoubleConservativeScheduler, 4) EasyBackfillScheduler, 5) DoubleEasyBackfillScheduler, 6) GreedyEasyBackfillScheduler, 7) EasyPlusPlusScheduler, 8) ShrinkingEasyScheduler, 9) LookAheadEasyBackFillScheduler") 
    
    options, args = parser.parse_args()

    if options.num_processors is None:
        parser.error("missing num processors")

    if options.input_file is None:
        parser.error("missing input file")

    if options.scheduler is None:
         parser.error("missing scheduler")

    if args:
        parser.error("unknown extra arguments: %s" % args)

    return options

def main():
    options = parse_options()

    input_file = open(options.input_file)

    if options.scheduler == "FcfsScheduler" or options.scheduler == "1":
        scheduler = FcfsScheduler(options.num_processors)

    elif options.scheduler == "ConservativeScheduler" or options.scheduler =="2":
        scheduler = ConservativeScheduler(options.num_processors)

    elif options.scheduler == "DoubleConservativeScheduler" or options.scheduler == "3":
        scheduler = DoubleConservativeScheduler(options.num_processors)

    elif options.scheduler == "EasyBackfillScheduler" or options.scheduler == "4":
        scheduler = EasyBackfillScheduler(options.num_processors)
        
    elif options.scheduler == "DoubleEasyBackfillScheduler" or options.scheduler == "5":
        scheduler = DoubleEasyBackfillScheduler(options.num_processors)

    elif options.scheduler == "GreedyEasyBackfillScheduler" or options.scheduler == "6":
        scheduler = GreedyEasyBackfillScheduler(options.num_processors)

    elif options.scheduler == "EasyPlusPlusScheduler" or options.scheduler == "7":
        scheduler = EasyPlusPlusScheduler(options.num_processors)
        
    elif options.scheduler == "ShrinkingEasyScheduler" or options.scheduler == "8":
        scheduler = ShrinkingEasyScheduler(options.num_processors)

    elif options.scheduler == "LookAheadEasyBackFillScheduler" or options.scheduler == "9":
        scheduler = LookAheadEasyBackFillScheduler(options.num_processors)
        
    else:
        print "No such scheduler"
        return 

    try:
        run_simulator(
                num_processors = options.num_processors, # TODO: read this from the workload input file 
                jobs = _job_inputs_to_jobs(parse_lines(input_file, options.num_processors)),
                scheduler = scheduler 
            )
        
        print "Num of Processors: ", options.num_processors
        print "Input file: ", options.input_file
        print "Scheduler:", type(scheduler)
    finally:
        input_file.close()

if __name__ == "__main__":
    main()
