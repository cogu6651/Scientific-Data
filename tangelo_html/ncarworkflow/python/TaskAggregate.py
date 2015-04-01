"""@package docstring
This script Aggregates data in from a given NetCDF file via a NCL script. The NCL script
takes in an input file, output file, the variable on which to aggregate, the method to use (mean, min, max),
the interval on which to aggregate (day, month, season, or year), and the outtime to set (the date/time of interval
to set the aggregate result). The output file is then a NetCDF with the aggregate data
"""

import subprocess
import sys
import re
import pyutilib.workflow

class taskAggregate(pyutilib.workflow.Task):
    def __init__(self, *args, **kwds):
        """Constructor."""
        pyutilib.workflow.Task.__init__(self,*args,**kwds)
        self.inputs.declare('filename')
        self.inputs.declare('variable')
        self.inputs.declare('interval')
        self.inputs.declare('method')
        self.inputs.declare('outtime')
        self.inputs.declare('cyclic')
        self.outputs.declare('result')
        self.workflowID = 1234

    def execute(self):
        sFilename = "filename=\"{0}\"".format(self.filename)
        sInterval = "interval=\"{0}\"".format(self.interval)
        if not method:
                sMethod = ""
        else:
                sMethod = "method=\"{0}\"".format(self.method)
        if not outtime:
                sOuttime = ""
        else:
                sOuttime = "outtime=\"{0}\"".format(self.outtime)
        sCyclic = "cyclic={0}".format(self.cyclic)
        sVariable = "variable=\"{0}\"".format(self.variable)
        wid = "wid={0}".format(self.workflowID)
        tid = "tid={0}".format(self.id)

        args = ['ncl', '-n', '-Q', wid, tid, sFilename, sVariable, sInterval, sMethod, sOuttime, sCyclic, 'ncl/aggregate.ncl']
        args = filter(None,args)

        sysError = False
        nclError = False
        try:
                status = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        except:
                sysError = True
                error = "System error, please contact site administrator."
    
        nclError = False
        if not sysError:
                for line in status.stdout:
                        if line.find("fatal") != -1:
                            nclError = True
                            error = re.sub('\[.*?\]:',' ',line)
                            break
                        if line.find("Invalid") != -1:
                            nclError = True
                            error = re.sub('.*?Invalid','Invalid',line)
                            break
        result = "/data/{0}/{1}_aggregate.nc".format(wid,tid)
        if nclError or sysError:
                self.result = { "error": error }
        else:
                self.result = { "result":  result }