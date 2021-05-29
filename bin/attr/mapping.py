class MappingAttr:
   def __init__(self):
        self.sample_id = ""

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

   def __repr__(self):
       return "Mapping {sample_id}: ".format(
               sample_id = self.sample_id)

