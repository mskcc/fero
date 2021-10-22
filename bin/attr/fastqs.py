import os

class FastqsAttr:
   def __init__(self):
        self.sample_id = ""
        self.run_id = list()
        self.fcid = list()
        self.paths = list()

   def set_attr(self, sample_id, paths, run_fc_ids):
        self.sample_id = sample_id
        self.paths = paths

        for path in self.paths:
            run_id, fcid = self._get_run_fc_id(path, run_fc_ids)
            self.run_id.append(run_id)
            self.fcid.append(fcid)


   def __repr__(self):
       return "Fastqs {sample_id}, {run_ids}, {fcids}: {paths}".format(
                sample_id = self.sample_id,
                paths = self.paths,
                run_ids = self.run_id,
                fcids = self.fcid)

   def _get_run_fc_id(self, path, run_fc_ids):
       val = self._get_row(path, run_fc_ids)
       """
       run id and fcid are derived from the same
       column, but they MUST be delim by underscore

       we are assuming there are two underscores in
       the mapping file
       """
       if val.count("_") < 2:
           print("Can't get run id/fcid from {val} ({sample_id}); assigning defaults".format(val=val,sample_id=self.sample_id))
           run_id = "DEFAULT_RUNID"
           fcid ="DEFAULT_FCID"
       else:
           run_id = "_".join(val.split("_")[0:2])
           fcid = val.split("_")[2]
       return run_id, fcid


   def _get_row(self, path, run_fc_ids):
       print(self.sample_id)
       return run_fc_ids[path]
