import logging
from typing import Tuple,List,Dict
from datamonk.invest_tools.sreality import Sreality
from prefect import task
import json
import time

@task(nout=2)
def extract_sreality(config:str) -> Tuple[str,List[Dict]]:
    logger = logging.getLogger(__name__)
    global run_timestamp
    run_timestamp = round(time.time())
    s_instance = Sreality(filter_config=json.loads(config))
    # new_ids = [offer_id for offer_id in s_instance.extract_offer_ids if offer_id not in history_ids]
    # old_ids = [offer_id for offer_id in s_instance.extract_offer_ids if offer_id in history_ids]
    # delisted_ids = [offer_id for offer_id in history_ids if offer_id not in s_instance.extract_offer_ids]



    offer_list = []
    offer_transformed_list = []
    if s_instance.extract_offer_count > 0:
        for idx, URL in enumerate(s_instance.extract_offer_urls):
            offer = s_instance.extract_offer_data(URL)
            offer_list.append(offer)

            offer_transformed = s_instance.transform_offer_data(offer)
            offer_transformed_list.append(offer_transformed)

            if (idx+1) % 50 == 0:
                timestamp = round(time.time())
                duration = timestamp - run_timestamp
                remaining = round((s_instance.extract_offer_count - (idx+1)) * (duration / (idx+1)))
                logger.info("offers processed: {} out of {},duration: {}, remaining: {}"
                                     .format(str(idx+1),
                                             str(s_instance.extract_offer_count),
                                             str(duration),
                                             str(remaining)))

        offer_json = {"timestamp": run_timestamp, "offers": offer_list}


    return offer_json,offer_transformed_list
