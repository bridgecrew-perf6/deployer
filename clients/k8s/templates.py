from os import path

import yaml


def get_template(name: str):
    file = open(path.join(path.dirname(__file__), f"templates/{name}.yaml"))
    return yaml.safe_load(file)


namespace_template = get_template('namespace')
resource_quota_template = get_template('resource_quota')
volume_claim_template = get_template('volume_claim')
deployment_template = get_template('deployment')
service_template = get_template('service')
