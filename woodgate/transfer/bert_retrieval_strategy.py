"""
bert_retrieval_strategy.py - This module contains the
BertRetrievalStrategy class definition.
"""
import os
import glob
import subprocess
from ..woodgate_logger import WoodgateLogger
from ..woodgate_settings import WoodgateSettings
from .bert_model_parameters import BertModelParameters


class BertRetrievalStrategy:
    """
    BertRetrievalStrategy - This class encapsulates logic
    related to downloading Google's BERT for transfer learning.
    """

    def __init__(
            self,
            bert_model_parameters: BertModelParameters
    ) -> None:
        #: The `bert_model_parameters` attribute represents the
        #: specific BERT model intended to be built. The three
        #: parameters required when choosing a BERT model may
        #: be set via environment variables `BERT_H_PARAM`,
        #: `BERT_L_PARAM`, and `BERT_A_PARAM`.
        #:
        #: See `https://github.com/google-research/bert` for
        #: more about these parameters.
        self.bert_model_parameters: BertModelParameters = \
            bert_model_parameters

        #: The `bert_base_url` attribute represents the base
        #: URL/endpoint where the BERT model is hosted. This
        #: attribute is set via the `BERT_BASE_URL` environment
        #: variable. If the `BERT_BASE_URL` environment variable
        #: is not set, then `bert_base_url` defaults to
        #: `https://storage.googleapis.com/`.
        #:
        #: See `https://github.com/google-research/bert` for
        #: more on where BERT is hosted.
        self.bert_base_url: str = os.getenv(
            "BERT_BASE_URL",
            'https://storage.googleapis.com'
        )

        #: The `bert_models_url_component` is the URL component
        #: directly preceded by `bert_base_url`. The
        #: `bert_models_url_component` is set via the
        #: `BERT_MODELS_URL_COMPONENT` environment variable.
        #: If the `BERT_MODELS_URL_COMPONENT` environment
        #: variable is not set, then the
        #: `bert_models_url_component` default to the string
        #: `bert_models`.
        #:
        #: See `https://github.com/google-research/bert` for more
        #: on where BERT is hosted.
        self.bert_models_url_component: str = os.getenv(
            "BERT_MODELS_URL_COMPONENT",
            "bert_models"
        )

        #: The `bert_models_url` attribute represents the URL to
        #: the bert models directory. This attribute is set via
        #: the `BERT_MODELS_URL` environment variable. If the
        #: `BERT_MODELS_URL` environment variable is not set,
        #: then the `bert_models_url` defaults to
        #: `bert_base_url/bert_models_url_component`.
        #:
        #: See `https://github.com/google-research/bert` for more
        #: on where BERT is hosted.
        self.bert_models_url: str = os.getenv(
            "BERT_MODELS_URL",
            os.path.join(
                self.bert_base_url,
                self.bert_models_url_component
            )
        )

        #: The `bert_version_url_component` is the URL component
        #: directly preceded by `bert_models_url`. The
        #: `bert_version_url_component` is set via the
        #: `BERT_MODELS_URL_COMPONENT` environment variable.
        #: If the `BERT_MODELS_URL_COMPONENT` environment
        #: variable is not set, then the
        #: `bert_version_url_component` default to the string
        #: `2020_02_20`.
        #:
        #: See `https://github.com/google-research/bert` for
        #: more on where BERT is hosted.
        self.bert_version_url_component: str = os.getenv(
            "BERT_VERSION_URL_COMPONENT",
            "2020_02_20"
        )

        #: The `bert_version_url` attribute represents the URL to
        #: the bert version directory. This attribute is set via
        #: the `BERT_VERSION_URL` environment variable. If the
        #: `BERT_VERSION_URL` environment variable is not set,
        #: then the `bert_version_url` defaults to
        #: `bert_models_url/bert_version_url_component`.
        #:
        #: See `https://github.com/google-research/bert` for more
        #: on where BERT is hosted.
        self.bert_version_url: str = os.getenv(
            "BERT_VERSION_URL",
            os.path.join(
                self.bert_models_url,
                self.bert_version_url_component
            )
        )

        #: The `bert_zip_url_component` is the URL component
        #: directly preceded by `bert_version_url`. The
        #: `bert_zip_url_component` is set via the
        #: `BERT_ZIP_URL_COMPONENT` environment variable.
        #: If the `BERT_ZIP_URL_COMPONENT` environment variable
        #: is not set, then the `bert_zip_url_component` defaults
        #: to the string `uncased_L-12_H-768_A-12.zip`
        #: (BERT base).
        #:
        #: See `https://github.com/google-research/bert` for more
        #: on
        #: where BERT is hosted.
        self.bert_zip_url_component: str = os.getenv(
            "BERT_ZIP_URL_COMPONENT",
            "uncased_"
            + f"L-{self.bert_model_parameters.bert_l_param}_"
            + f"H-{self.bert_model_parameters.bert_h_param}_"
            + f"A-{self.bert_model_parameters.bert_a_param}.zip"
        )

        #: The `bert_zip_url` attribute represents the URL to the
        #: bert zip directory. This attribute is set via
        #: the `BERT_ZIP_URL` environment variable. If the
        #: `BERT_ZIP_URL` environment variable is not set, then
        #: the `bert_zip_url` defaults to
        #: `bert_version_url/bert_zip_url_component`.
        #:
        #: See `https://github.com/google-research/bert` for more
        #: on where BERT is hosted.
        self.bert_zip_url: str = os.getenv(
            "BERT_ZIP_URL",
            os.path.join(
                self.bert_version_url,
                self.bert_zip_url_component
            )
        )

    def download_bert(self) -> None:
        """

        :return: None
        :rtype: NoneType
        """
        # downloading the models is an expensive process
        # so first make sure we actually need the files
        if not glob.glob(
                f"{WoodgateSettings.get_bert_model_path()}*"
        ) or not os.path.isfile(
            WoodgateSettings.get_bert_config_path()
        ) or not os.path.isfile(
            WoodgateSettings.get_bert_vocab_path()
        ):
            process = subprocess.Popen(
                [
                    'wget',
                    self.bert_zip_url
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            WoodgateLogger.logger.info(stdout)
            WoodgateLogger.logger.error(stderr)

            os.makedirs(
                WoodgateSettings.bert_dir,
                exist_ok=True
            )

            process = subprocess.Popen(
                [
                    'unzip',
                    self.bert_zip_url_component,
                    '-d',
                    WoodgateSettings.bert_dir
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            WoodgateLogger.logger.info(stdout)
            WoodgateLogger.logger.error(stderr)

            process = subprocess.Popen(
                [
                    'rm',
                    f'./{self.bert_zip_url_component}'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            WoodgateLogger.logger.info(stdout)
            WoodgateLogger.logger.error(stderr)

        return None
