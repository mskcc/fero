class FastqsAttr:
   def __init__(self):
        self.sample_id = ""
        self.paths = list()

   def set_attr(self, sample_id, paths):
        self.sample_id = sample_id
        self.paths = paths

   def __repr__(self):
       return "Fastqs {sample_id}: {paths}".format(
                sample_id = self.sample_id,
                paths = self.paths)
