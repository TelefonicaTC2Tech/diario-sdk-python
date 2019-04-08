name = "diario"

import os.path

from sdklib.http import HttpSdk
from sdklib.http.authorization import X11PathsAuthentication
from sdklib.http.renderers import MultiPartRenderer
from sdklib.http.response import Api11PathsResponse

from sdklib.shortcuts import disable_warnings
disable_warnings()

__all__ = ('Diario',)


class _Route():
    """This class is just a simple storage type for route constants
    """
    VERSION = "0.1"
    BASE_URL = "/api/" + VERSION + '/'

    UPLOAD = BASE_URL + 'upload'
    ANONYMOUS_UPLOAD = '/anonymous-upload'
    VALIDATE = "/validate"
    MACRO = "/macro"
    JAVASCRIPT = "/javascript"
    MODEL = "/model"
    MODEL_LAST_VERSION = MODEL + '/last-versions'
    MODEL_DEPLOYED = MODEL + '/deployed'
    MODEL_STATISTICS = MODEL + '/statistics'
    MODEL_TRAIN = MODEL + '/train'
    MODEL_DEPLOY = MODEL + '/deploy'

    BASE_URL_OPEN = "/open/api"
    CHANGE = BASE_URL_OPEN + "/change"

    PARAM_HASH = "hash"
    PARAM_FILE = "file"
    PARAM_PREDICTION = "prediction"
    PARAM_MODEL = "model"
    PARAM_VERSION = "version"
    PARAM_DOCUMENT_TYPE = "documentType"
    PARAM_EMAIL = "email"
    PARAM_DESCRIPTION = "description"


class DocumentType():
    """This class is just a simple storage type for document type constants
    """
    PDF = "pdf"
    OFFICE = "office"


class Diario(HttpSdk):

    response_class = Api11PathsResponse

    def __init__(self, app_id, secret_key, host, port):
        """Initialize the DIARIO SDK with provided user information.
        :param app_id: User appId to be used
        :param secret_key: User secretKey to be used
        :param host: IP address or domain
        :param port: TCP port
        """

        # HttpSdk.set_default_proxy("https://localhost:8080")
        HOST = "{0}:{1}".format(host, port)
        super(Diario, self).__init__(host=HOST)

        self.app_id = app_id
        self.secret_key = secret_key
        self.authentication_instances += (X11PathsAuthentication(self.app_id, self.secret_key),)

    def upload(self, file_path):
        file_content = open(file_path, 'rb').read()
        file_name = os.path.basename(file_path)
        return self.post(url_path=_Route.UPLOAD, files={_Route.PARAM_FILE: (file_name, file_content)},
                         renderers=MultiPartRenderer())

    def __get_info(self, document_type, document_hash):
        return self.get(url_path=_Route.BASE_URL + document_type, query_params={_Route.PARAM_HASH: document_hash})

    def get_pdf_info(self, document_hash):
        return self.__get_info(DocumentType.PDF, document_hash)

    def get_office_info(self, document_hash):
        return self.__get_info(DocumentType.OFFICE, document_hash)

    def get_javascript_info(self, document_hash):
        return self.get(url_path=_Route.BASE_URL + DocumentType.PDF + _Route.JAVASCRIPT,
                        query_params={_Route.PARAM_HASH: document_hash})

    def get_macro_info(self, document_hash):
        return self.get(url_path=_Route.BASE_URL + DocumentType.OFFICE + _Route.MACRO,
                        query_params={_Route.PARAM_HASH: document_hash})


    def __anonymous_upload(self, document_hash, zip_file_path, document_type):
        zip_file = open(zip_file_path, 'rb').read()
        zip_file_name = os.path.basename(zip_file_path)
        return self.post(url_path=_Route.BASE_URL + document_type + _Route.ANONYMOUS_UPLOAD,
                         body_params={_Route.PARAM_HASH: document_hash},
                         files={_Route.PARAM_FILE: (zip_file_name, zip_file)},
                         renderers=MultiPartRenderer())

    def pdf_anonymous_upload(self, document_hash, zip_file_path):
        return self.__anonymous_upload(document_hash, zip_file_path, DocumentType.PDF)

    def office_anonymous_upload(self, document_hash, zip_file_path):
        return self.__anonymous_upload(document_hash, zip_file_path, DocumentType.OFFICE)

    def change_request(self, document_hash, document_type, prediction, email, description):
        return self.post(_Route.CHANGE,
                         body_params={
                             _Route.PARAM_HASH: document_hash,
                             _Route.PARAM_DOCUMENT_TYPE: document_type,
                             _Route.PARAM_PREDICTION: prediction,
                             _Route.PARAM_EMAIL: email,
                             _Route.PARAM_DESCRIPTION: description
                         })

