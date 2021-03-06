class RequestAttr:
    def __init__(self):
        self.assay = ""
        self.design_file = ""
        self.request_id = ""
        self.investigator = ""
        self.investigator_name = ""
        self.pi = ""
        self.pi_name = ""
        self.pi_email = ""
        self.project_id = ""
        self.project_desc = ""
        self.project_name = ""
        self.project_title = ""
        self.project_manager = ""
        self.project_manager_email = ""
        self.species = ""
        self.specimen_type = ""
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
            if key == "pi_email":
                self.pi_email = val
            if key == "projectid":
                self.project_id = val
            if key == "projectname":
                self.project_name = val
            if key == "projectdesc":
                self.project_desc = val
            if key == "projecttitle":
                self.project_title = val
            if key == "project_manager":
                self.project_manager = val
            if key == "project_manager_email":
                self.project_manager_email = val
            if key == "species": # specimen type and species derived from request "species" field
                self.species = self.get_species(val)
                self.specimen_type = self.get_specimen_type(val)
            if key == "tumortype":
                self.tumor_type = val

    def set_metadata(self):
        self.metadata["genePanel"] = self.assay
        self.metadata["runDate"] = self.run_date
        self.metadata["igoRequestId"] = self.request_id
        self.metadata["investigator"] = self.investigator
        self.metadata["investigatorName"] = self.investigator_name
        self.metadata["pi"] = self.pi
        self.metadata["piName"] = self.pi_name
        self.metadata["projectName"] = self.project_name
        self.metadata["igoProjectId"] = self.project_id
        self.metadata["projectDesc"] = self.project_desc
        self.metadata["projectTitle"] = self.project_title
        self.metadata["projectManager"] = self.project_manager
        self.metadata["projectManagerEmail"] = self.project_manager_email
        self.metadata["species"] = self.species
        self.metadata["tumorType"] = self.tumor_type
        self.metadata["runMode"] = self.run_mode
        # not explicitly defined in request file
        self.metadata["specimenType"] = self.specimen_type
        self.metadata["labHeadName"] = self.pi_name
        self.metadata["piEmail"] = self.pi_email
        self.metadata["labHeadEmail"] = self.pi_email
        self.metadata["otherContactEmails"] = self.get_other_emails()

    def get_other_emails(self):
        # I'm assuming someday there will be more
        emails = [self.project_manager_email]
        return ",".join(set(emails))

    def get_species(self, val):
        """
        For now, only return Human
        """
        return "Human"

    def get_specimen_type(self, val):
        if "xenograft" in val.lower():
            return "PDX"
        else:
            return ""

    def __repr__(self):
        return "Request {request_id}: {assay}, {pi}".format(
                request_id = self.request_id,
                assay = self.assay,
                pi = self.pi)
