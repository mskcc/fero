import requests
import sys, os
import json

class AccessBeagleEndpoint:
    def __init__(self):
        username = os.environ['BEAGLE_USER']
        password = os.environ['BEAGLE_PW']
        BEAGLE_ENDPOINT = os.environ['BEAGLE_ENDPOINT']
        self.auth = requests.auth.HTTPBasiAuth(username, password)
        self.API = BEAGLE_ENDPOINT

    def run_url(self, url):
        req = requests.get(url, auth=self.auth, verify=False)
        return req.json()

    def get_cmoid(self, sample_id):
        url = "%s/v0/fs/files/?metadata=anon_id:%s" % (self.API, sample_id)
        return self.run_url(url)


if __name__ == "__main__":
    print(AccessBeagleEndpoint.get_cmoid(sys.argv[1]))
