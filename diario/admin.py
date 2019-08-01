import os
import uuid

from sdklib.http.renderers import MultiPartRenderer

import diario
from diario import _Route
from diario import DocumentType


class UnknownPredictionType(Exception):
    def __init__(self, message):
        super(UnknownPredictionType, self).__init__(message)


class Prediction():
    """Simple class to hold prediction types"""
    MALWARE = "M"
    GOODWARE = "G"


class DiarioAdmin(diario.Diario):
    """This class extends DIARIO user SDK with admin superpowers
    """

    def __init__(self, app_id, secret_key, host=None, port=None):
        if host and port:
            super(DiarioAdmin, self).__init__(app_id=app_id, secret_key=secret_key, host=host, port=port)
        elif host and not port:
            super(DiarioAdmin, self).__init__(app_id=app_id, secret_key=secret_key, host=host)
        elif port and not host:
            super(DiarioAdmin, self).__init__(app_id=app_id, secret_key=secret_key, port=port)
        else:
            super(DiarioAdmin, self).__init__(app_id=app_id, secret_key=secret_key)

    def __validate_document(self, document_type, document_hash, prediction):
        """
        :param document_hash: hash of the document
        :param prediction: prediction could be a string: 'G' or 'M'
        :return:
        """
        # TODO: Check values are compliant with every API revision
        if not prediction in ["M", "G"]:
            raise UnknownPredictionType(
                "Prediction parameter must be a member of Prediction class")
        return self.post(url_path=_Route.BASE_URL + document_type + _Route.VALIDATE,
                         body_params={_Route.PARAM_HASH: document_hash, _Route.PARAM_PREDICTION: prediction})

    # Validated document
    def validate_pdf(self, document_hash, prediction):
        return self.__validate_document(DocumentType.PDF, document_hash, prediction)

    def validate_office(self, document_hash, prediction):
        return self.__validate_document(DocumentType.OFFICE, document_hash, prediction)

    # Get model last version
    def get_last_versions_model_pdf(self):
        return self.get(url_path=_Route.BASE_URL + DocumentType.PDF + _Route.MODEL_LAST_VERSION)

    def get_last_versions_model_office(self):
        return self.get(url_path=_Route.BASE_URL + DocumentType.OFFICE + _Route.MODEL_LAST_VERSION)

    # Get deployed model
    def get_deployed_model_pdf(self):
        return self.get(url_path=_Route.BASE_URL + DocumentType.PDF + _Route.MODEL_DEPLOYED)

    def get_deployed_model_office(self):
        return self.get(url_path=_Route.BASE_URL + DocumentType.OFFICE + _Route.MODEL_DEPLOYED)

    # Model statistics
    def __get_model_statistics(self, document_type, model, version):
        return self.get(url_path=_Route.BASE_URL + document_type + _Route.MODEL_STATISTICS,
                        query_params={_Route.PARAM_MODEL: model, _Route.PARAM_VERSION: version})

    def get_model_statistics_pdf(self, model, version):
        return self.__get_model_statistics(DocumentType.PDF, model, version)

    def get_model_statistics_office(self, model, version):
        return self.__get_model_statistics(DocumentType.OFFICE, model, version)

    # Model training
    def __train_model(self, document_type, model):
        return self.post(_Route.BASE_URL + document_type + _Route.MODEL_TRAIN,
                         body_params={_Route.PARAM_MODEL: model})

    def train_pdf_model(self, model):
        return self.__train_model(DocumentType.PDF, model)

    def train_office_model(self, model):
        return self.__train_model(DocumentType.OFFICE, model)

    # Model deployment
    def __deploy_model(self, document_type, model, version):
        return self.post(_Route.BASE_URL + document_type + _Route.MODEL_DEPLOY,
                         body_params={_Route.PARAM_MODEL: model, _Route.PARAM_VERSION: version})

    def deploy_pdf_model(self, model, version):
        return self.__deploy_model(DocumentType.PDF, model, version)

    def deploy_office_model(self, model, version):
        return self.__deploy_model(DocumentType.OFFICE, model, version)

    def upload(self, file_path, prediction=None):
        file_content = open(file_path, 'rb').read()
        file_name = uuid.uuid4().hex
        body_params = {}
        if prediction:
            body_params[_Route.PARAM_PREDICTION] = prediction
        return self.post(url_path=_Route.UPLOAD, files={_Route.PARAM_FILE: (file_name, file_content)},
                         renderers=MultiPartRenderer(), body_params=body_params)
