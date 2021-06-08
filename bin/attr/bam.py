class BamAttr:
   def __init__(self):
        self.sample_id = ""
        self.path = ""

   def set_attr(self, sample_id, path):
        self.sample_id = sample_id
        self.path = path

   def __repr__(self):
       return "Bam {sample_id}: {path}".format(
                sample_id = self.sample_id,
                path = self.path)
