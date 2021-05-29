class BarcodeAttr:
   def __init__(self):
        self.sample_id = ""
        self.barcode = ""

   def set_attr(self, keys, data):
        """
            data    dictionary containing one sample
                    from barcode
        """
        keys_lower = [i.lower() for i in keys]
        for i,key in enumerate(keys_lower):
            val = data[keys[i]]
            if key == "sample_id":
                 self.sample_id = val
            if key == "barcode_index":
                self.barcode = val

   def __repr__(self):
       return "Barcode {sample_id}: {barcode}".format(
               sample_id = self.sample_id,
               barcode = self.barcode)
