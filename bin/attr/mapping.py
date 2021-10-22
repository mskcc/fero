import sys

class MappingAttr:
   def __init__(self):
        self.sample_id = ""
        self.run_id = []
        self.fcid = []

   def set_attr(self, keys, data):
        """
            data    dictionary containing one sample
                    from mapping file
        """
        keys_lower = [i.lower() for i in keys]
        for i,key in enumerate(keys_lower):
            val = data[keys[i]]
            if key == "sample_id":
                self.sample_id = val
            if key == "runid_flowcellid":
                """
                    run id and fcid are derived from the same
                    column, but they MUST be delim by underscore

                    we are assuming there are two underscores in
                    the mapping file
                """
                if val.count("_") < 2:
                    print("Can't get run id/fcid from {val} ({sample_id}); assigning defaults".format(val=val,sample_id=self.sample_id))
                    self.run_id = "DEFAULT_RUNID"
                    self.fcid = "DEFAULT_FCID"
#                    sys.exit(1)
                else:
                    self.run_id.append("_".join(val.split("_")[0:2]))
                    self.fcid.append(val.split("_")[2])

   def __repr__(self):
       return "Mapping {sample_id}: ".format(
               sample_id = self.sample_id)

