class RequestAttr:
    def __init__(self):
        self.assay = ""
        self.design_file = ""
        self.request_id = ""
        self.investigator = ""
        self.investigator_name = ""
        self.pi = ""
        self.pi_name = ""
        self.project_id = ""
        self.project_desc = ""
        self.project_title = ""
        self.project_manager = ""
        self.project_manager_email = ""
        self.species = ""
        self.tumor_type = ""
        self.run_mode= "hiseq" # this is assumed for now
        self.metadata = dict()

    def set_attr(self, keys, data):
        keys_lower = [i.lower() for i in keys]
        for i,key in enumerate(keys_lower):
            val = data[keys[i]]
            if key == "assay":
                self.assay = val
            if key == "rundate":
                self.run_date = val
            if key == "requestid":
                self.request_id = val
            if key == "investigator":
                self.invesgator = val
            if key == "investigator_name":
                self.investigator_name = val
            if key == "pi":
                self.pi = val
            if key == "pi_name":
                self.pi_name = val
            if key == "projectid":
                self.project_id = val
            if key == "projectdesc":
                self.project_desc = val
            if key == "projecttitle":
                self.project_title = val
            if key == "project_manager":
                self.project_manager = val
            if key == "project_manager_email":
                self.project_manager_email = val
            if key == "species":
                self.species = val
            if key == "tumortype":
                self.tumor_type = val


    def set_metadata(self):
        self.metadata["recipe"] = self.assay
        self.metadata["runDate"] = self.run_date
        self.metadata["requestId"] = self.request_id
        self.metadata["investigator"] = self.investigator
        self.metadata["investigatorName"] = self.investigator_name
        self.metadata["pi"] = self.pi
        self.metadata["piName"] = self.pi_name
        self.metadata["projectId"] = self.project_id
        self.metadata["projectDesc"] = self.project_desc
        self.metadata["projectTitle"] = self.project_title
        self.metadata["projectManager"] = self.project_manager
        self.metadata["projectManagerEmail"] = self.project_manager_email
        self.metadata["species"] = self.species
        self.metadata["tumorType"] = self.tumor_type
        self.metadata["runMode"] = self.run_mode

    def __repr__(self):
        return "Request {request_id}: {assay}, {pi}".format(
                request_id = self.request_id,
                assay = self.assay,
                pi = self.pi)
