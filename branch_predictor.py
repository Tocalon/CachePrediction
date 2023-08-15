from optparse import OptionParser
import gzip
from perceptron import *
from ie0521_bp import *
from bimodal import *
from gshared import *
from p_shared import *



parser = OptionParser()
parser.add_option("-n", dest="bits_to_index")
parser.add_option("--bp", dest="branch_predictor_type")
parser.add_option("-g", dest="global_history_size")
parser.add_option("--lh", dest="local_history_size") 
parser.add_option("-t", dest="TRACE_FILE", default="./branch-trace-gcc.trace.gz")

(options, args) = parser.parse_args()

if options.branch_predictor_type == "0":
    branch_predictor = perceptron(int(options.bits_to_index), int(options.global_history_size))
    branch_predictor.print_info()
if options.branch_predictor_type == "1":
    branch_predictor = ie0521_bp(int(options.bits_to_index))
    branch_predictor.print_info()
elif options.branch_predictor_type == "2":
    branch_predictor = bimodal(int(options.bits_to_index))
    branch_predictor.print_info()
elif options.branch_predictor_type == "3":
    branch_predictor = gshared(int(options.bits_to_index), int(options.global_history_size))
    branch_predictor.print_info()
elif options.branch_predictor_type== "4":
    branch_predictor = PSharePredictor(int(options.bits_to_index), int(options.local_history_size))
    branch_predictor.print_info()

#i = 0
with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        PC,result = line.split(" ")
     
        prediction = branch_predictor.predict(PC)
        branch_predictor.update(PC, result, prediction)
        #i+=1
        #if i == 25:
        #    break
branch_predictor.print_stats()
