import io

from datomizer import DatoMapper
from datomizer.helpers import common_helper
from datomizer.helpers.train import enhance_ml_helper, train_helper
from datomizer.utils.general import ID, MODELS, ERROR
from datomizer.utils.step_types import ML_TRAIN_AND_GENERATE, ML_SPLIT_AND_EVALUATE
from datomizer.utils.enhance_ml import Metrics, Algorithms


class DatoEnhancer(object):
    dato_mapper: DatoMapper
    train_id = 0
    models = []
    metric_list = []
    algorithm_list = []
    target_table = ""
    target_column = ""

    def __init__(self, dato_mapper: DatoMapper):
        """Create DatoTrainer object for training a generative model for the mapped input data.
        Args:
            dato_mapper: the DatoMapper object for the input data."""
        dato_mapper.next_step_validation()
        self.dato_mapper = dato_mapper

    @classmethod
    def restore(cls, dato_mapper: DatoMapper, train_id):
        dato_enhancer = cls(dato_mapper)
        dato_enhancer.train_id = train_id
        dato_enhancer.wait(ML_SPLIT_AND_EVALUATE)
        return dato_enhancer

    def enhance(self, target_table: str = "", target_column: str = "",
                metric_list: [Metrics] = [], algorithm_list: [Algorithms] = [], wait=True) -> None:
        if self.train_id > 0:
            return

        self.target_table = self.dato_mapper.schema.table(target_table).name
        self.target_column = self.dato_mapper.schema.column(target_table, target_column).name
        self.metric_list = metric_list
        self.algorithm_list = algorithm_list

        self.train_id = enhance_ml_helper.enhance_ml_evaluate(self.dato_mapper,
                                                              target_table=self.target_table,
                                                              target_column=self.target_column,
                                                              metric_list=self.metric_list,
                                                              algorithm_list=self.algorithm_list)
        if wait:
            self.wait(ML_SPLIT_AND_EVALUATE)

    def generate(self, wait=True) -> None:
        self.restore_validation()

        self.train_id = enhance_ml_helper.enhance_ml_generate(self.dato_mapper,
                                                              target_table=self.target_table,
                                                              target_column=self.target_column,
                                                              metric_list=self.metric_list,
                                                              algorithm_list=self.algorithm_list)
        if wait:
            self.wait(ML_TRAIN_AND_GENERATE)

    def wait(self, step_type) -> None:
        """Wait until the train method returns."""
        self.restore_validation()
        status = common_helper.wait_for_step_type(datomizer=self.dato_mapper.datomizer,
                                                  business_unit_id=self.dato_mapper.business_unit_id,
                                                  project_id=self.dato_mapper.project_id,
                                                  flow_id=self.dato_mapper.flow_id,
                                                  step_type=step_type,
                                                  train_id=self.train_id,
                                                  how_many=2)
        if status == ERROR:
            raise Exception("Trainer Failed")
        train = train_helper.get_train_iteration(self.dato_mapper, self.train_id)
        self.models = train[MODELS]

    def get_generated_data(self, is_full: bool = False) -> None:
        self.restore_validation()

        print(common_helper.get_generated_zip(datomizer=self.dato_mapper.datomizer,
                                              business_unit_id=self.dato_mapper.business_unit_id,
                                              project_id=self.dato_mapper.project_id,
                                              flow_id=self.dato_mapper.flow_id,
                                              model_id=self.get_model_id(is_full),
                                              train_id=self.train_id))

    def get_generated_data_csv(self, table_name: str = None, is_full: bool = False) -> io.StringIO:
        """Get the generated data in a csv format.
                Args:
                    table_name: the name of the generated data
                    is_full: the model trained on full data
                Returns:
                    StringIO object containing the generated data"""
        self.restore_validation()

        table_name = self.dato_mapper.schema.table(table_name).name

        return common_helper.get_generated_csv(datomizer=self.dato_mapper.datomizer,
                                               business_unit_id=self.dato_mapper.business_unit_id,
                                               project_id=self.dato_mapper.project_id,
                                               flow_id=self.dato_mapper.flow_id,
                                               train_id=self.train_id,
                                               model_id=self.get_model_id(is_full),
                                               table_name=table_name)

    def get_model_id(self, is_full: bool = False):
        model_index = 0
        if is_full:
            if len(self.models) > 1:
                model_index = 1
            else:
                raise Exception("there is no fully trained model")
        return self.models[model_index][ID]

    def restore_validation(self):
        if not (self.train_id > 0):
            raise Exception("train id required for this step")

    def next_step_validation(self):
        if not (self.train_id > 0):
            raise Exception("train id required for this step")
