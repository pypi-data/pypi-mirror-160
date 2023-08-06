import io
import requests
import time
from os.path import getsize
from datomizer import Datomizer
from datomizer.utils.constants import (MANAGEMENT_GET_SYNTH_FLOW, MANAGEMENT_GET_GENERATIVE_FLOW,
                                       MANAGEMENT_GET_GENERATED_DATA, MANAGEMENT_GET_GENERATED_DATA_CSV)
from datomizer.utils.general import (ID, STEPS, TASKS, TASK_STATUS, STEP_TYPE, TRAIN_ITERATIONS,
                                     ERROR, INITIALIZING, IN_PROGRESS, URL)
from datomizer.utils.thresholds import MIN_ROW_COUNT, MAX_COLUMN_COUNT, MAX_FILE_SIZE_IN_MB, MB


def get_flow(datomizer: Datomizer,
             business_unit_id: str, project_id: str, flow_id: str, is_synth=False) -> dict:
    url = MANAGEMENT_GET_SYNTH_FLOW if is_synth else MANAGEMENT_GET_GENERATIVE_FLOW
    return datomizer.get_response_json(requests.get,
                                       url=url,
                                       url_params=[business_unit_id, project_id, flow_id])


def get_flow_step_status(datomizer: Datomizer,
                         business_unit_id: str, project_id: str, flow_id: str, is_synth=False,
                         step_type: str = '', train_id: int = 0, how_many: int = 1) -> str:
    response_json = get_flow(datomizer, business_unit_id, project_id, flow_id, is_synth)
    return get_relevant_steps_status(response_json, step_type, train_id, how_many)


def get_relevant_steps_status(response_json: {}, step_type: str = '', train_id: int = 0, how_many: int = 1) -> str:
    if train_id > 0:
        steps = [iteration for iteration in response_json[TRAIN_ITERATIONS]
                 if iteration[ID] == train_id][0][STEPS]
    else:
        steps = response_json[STEPS]

    return get_steps_status(steps, step_type, how_many)


def get_steps_status(steps: [], step_type, how_many: int = 1) -> str:
    counter = 0
    for step in steps:
        for task in step[TASKS]:
            if task[TASK_STATUS] == ERROR:
                return ERROR
            if step[STEP_TYPE] == step_type:
                counter += 1
                if counter == how_many:
                    return task[TASK_STATUS]

    return INITIALIZING


def wait_for_step_type(datomizer: Datomizer,
                       business_unit_id: str, project_id: str, flow_id: str, is_synth=False,
                       step_type: str = '', train_id: int = 0, how_many: int = 1) -> str:
    status = get_flow_step_status(datomizer, business_unit_id, project_id, flow_id,
                                  is_synth, step_type, train_id, how_many)
    while status in [INITIALIZING, IN_PROGRESS]:
        time.sleep(10)
        status = get_flow_step_status(datomizer, business_unit_id, project_id, flow_id,
                                      is_synth, step_type, train_id, how_many)
    return status


def get_generated_zip(datomizer: Datomizer,
                      business_unit_id: int, project_id: int, flow_id: int,
                      train_id: int = 0, model_id: int = 0) -> str:
    response_json = datomizer.get_response_json(requests.get,
                                                url=MANAGEMENT_GET_GENERATED_DATA,
                                                url_params=[business_unit_id, project_id, flow_id, train_id, model_id])
    return response_json[URL]


def get_generated_csv(datomizer: Datomizer,
                      business_unit_id: int, project_id: int, flow_id: int, train_id: int = 0, model_id: int = 0,
                      table_name: str = "") -> io.StringIO:
    response_json = datomizer.get_response_json(requests.get,
                                                url=MANAGEMENT_GET_GENERATED_DATA_CSV,
                                                url_params=[business_unit_id, project_id,
                                                            flow_id, train_id, model_id, table_name])
    response = requests.get(response_json[URL])
    Datomizer.validate_response(response, "Unable to get CSV from put_presigned url")

    return io.StringIO(response.content.decode('utf-8'))


def save_df_to_csv(df, temp_dir, name):
    if not name.endswith(".csv"):
        name = name + ".csv"
    path = f"{temp_dir}/{name}"
    df_type = f"{type(df).__module__}.{type(df).__name__}"

    if df_type == "pandas.core.frame.DataFrame":
        df.to_csv(path, index=False)
    elif df_type == "pyspark.sql.dataframe.DataFrame":
        df.write.csv(path=path, mode='overwrite', header='true')

    return path


def validate_data_size_limits(path, delimiter):
    with open(path) as csv_file:
        first_line = csv_file.readline()
        your_data = csv_file.readlines()

        assert_size(path)
        assert len(your_data) >= MIN_ROW_COUNT, \
            f"Row count is {len(your_data)} - is below the minimum limit of: {MIN_ROW_COUNT} rows"
        assert first_line.count(delimiter) + 1 <= MAX_COLUMN_COUNT, \
            f"Column count is {first_line.count(delimiter) + 1} - exceeds the limit of: {MAX_COLUMN_COUNT} columns"


def assert_size(path):
    size = round(getsize(path) / MB, 3)
    assert size <= MAX_FILE_SIZE_IN_MB, f"File size: {size}MB - exceeds the limit of: {MAX_FILE_SIZE_IN_MB}MB"
