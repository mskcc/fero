class PatientAttr:
   def __init__(self):
        self.pool = ""
        self.sample_id = ""
        self.collab_id = ""
        self.patient_id = ""
        self.sample_class = "" # confusingly, field in sample is "sample_type"
        self.sample_type = "" # confusingly, field in sample is "preservation"
        self.input_ng = ""
        self.library_yield = ""
        self.pool_input = ""
        self.bait_version = ""
        self.sex = ""

   def set_attr(self, keys, data):
        """
            data    dictionary containing one sample
                    from patient file
        """
        keys_lower = [i.lower() for i in keys]
        for i,key in enumerate(keys_lower):
            val = data[keys[i]]
            if key == "pool":
                self.pool = val
            if key == "sample_id":
                self.sample_id = val
            if key == "collab_id":
                self.collab_id = val
            if key == "patient_id":
                self.patient_id = val
            if key == "class":
                self.sample_class = val # confusingly, field in sample is "sample_type"
            if key == "sample_type":
                self.sample_type = val # confusingly, field in sample is "preservation"
            if key == "input_ng":
                self.input_ng = val
            if key == "library_yield":
                self.library_yield = val
            if key == "pool_input":
                self.pool_input = val
            if key == "bait_version":
                self.bait_version = val
            if key == "sex":
                self.sex = val

   def __repr__(self):
       return "Patient {sample_id}: {patient_id}, {sample_class}".format(
               sample_id = self.sample_id,
               patient_id = self.patient_id,
               sample_class = self.sample_class)
