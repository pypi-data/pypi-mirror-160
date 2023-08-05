from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from pkg_resources import get_distribution
__version__ = get_distribution('gcloud-rest-bigquery').version

from gcloud.rest.bigquery.bigquery import Disposition
from gcloud.rest.bigquery.bigquery import SCOPES
from gcloud.rest.bigquery.bigquery import SchemaUpdateOption
from gcloud.rest.bigquery.bigquery import SourceFormat
from gcloud.rest.bigquery.dataset import Dataset
from gcloud.rest.bigquery.job import Job
from gcloud.rest.bigquery.table import Table
from gcloud.rest.bigquery.utils import query_response_to_dict


__all__ = [
    '__version__',
    'Dataset',
    'Disposition',
    'Job',
    'SCOPES',
    'SchemaUpdateOption',
    'SourceFormat',
    'Table',
    'query_response_to_dict',
]
