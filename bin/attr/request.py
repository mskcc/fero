import sys
import os

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

    def set_attr(self, keys, data):
        keys_lower = [i.lower() for i in keys]
        for i,key in enumerate(keys_lower):
            val = data[keys[i]]
            if key == "assay":
                self.assay = val
            if key == "designfile":
                self.design_file = val
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

    def __repr__(self):
        return "Request {request_id}: {assay}, {pi}".format(
                request_id = self.request_id,
                assay = self.assay,
                pi = self.pi)
