import prefect
from datamonk.utils import functions as utils, monitoring

import datamonk.scriptorium.apps.dataform as dataform
import os

@prefect.task
def dataform_transform(project_id=os.environ.get("DATAFORM_PROJECT_ID"),
                       token=os.environ.get("DATAFORM_API_KEY"),
                       schedule=os.environ.get("DATAFORM_SCHEDULE_NAME")
                       ):
       df_inst=dataform.instance(project_id=project_id,
                                 token=token)
       return df_inst.run(schedule=schedule)


@prefect.task
def data_monitoring(config_json_path):
    config=functions.local.read_configJSON(path=config_json_path)
    return monitoring.run(rules_list=config["rules"])

def prefect_parameter_read_json(path,param_name):
        return prefect.Parameter(param_name,
                                 default=utils.functions.local(path,"string")
                                 )