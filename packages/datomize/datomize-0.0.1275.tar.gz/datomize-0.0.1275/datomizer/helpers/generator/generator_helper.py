import json
import requests
from datomizer import DatoTrainer
from datomizer.utils.constants import MANAGEMENT_PUT_SYNTH_FLOW
from datomizer.utils.general import ID, NEW_PRIVATE_ID, SPARK_WRITE_OPTIONS_OVERWRITE


def create_synth_request(dato_trainer: DatoTrainer,
                         datasource_id: int = NEW_PRIVATE_ID,
                         sample_output_ratio: float = 1) -> dict:
    return {
        "title": "Synth SDK",
        "datasourceId": datasource_id,
        "sizeInGB": 0,
        "sampleOutputRatio": sample_output_ratio,
        "modelId": dato_trainer.model_id,
        "synthStrategy": SPARK_WRITE_OPTIONS_OVERWRITE
    }


def generate(dato_trainer: DatoTrainer, datasource_id: int, output_ratio: float = 1) -> int:
    dato_trainer.wait()
    response_json = dato_trainer.dato_mapper.datomizer.get_response_json(
        requests.put,
        url=MANAGEMENT_PUT_SYNTH_FLOW,
        url_params=[dato_trainer.dato_mapper.business_unit_id,
                    dato_trainer.dato_mapper.project_id,
                    dato_trainer.dato_mapper.flow_id],
        headers={"Content-Type": "application/json"},
        data=json.dumps(create_synth_request(dato_trainer, datasource_id, output_ratio)))
    return response_json[ID]
