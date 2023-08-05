# coding: utf-8

"""
    Deci Platform API

    Train, deploy, optimize and serve your models using Deci's platform, In your cloud or on premise.  # noqa: E501

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from deci_lab_client.configuration import Configuration


class OptimizationRequestForm(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'target_hardware': 'HardwareType',
        'target_batch_size': 'int',
        'target_metric': 'Metric',
        'optimize_model_size': 'bool',
        'quantization_level': 'QuantizationLevel',
        'optimize_autonac': 'bool',
        'name': 'str',
        'raw_format': 'bool'
    }

    attribute_map = {
        'target_hardware': 'targetHardware',
        'target_batch_size': 'targetBatchSize',
        'target_metric': 'targetMetric',
        'optimize_model_size': 'optimizeModelSize',
        'quantization_level': 'quantizationLevel',
        'optimize_autonac': 'optimizeAutonac',
        'name': 'name',
        'raw_format': 'rawFormat'
    }

    def __init__(self, target_hardware=None, target_batch_size=None, target_metric=None, optimize_model_size=None, quantization_level=None, optimize_autonac=None, name=None, raw_format=False, local_vars_configuration=None):  # noqa: E501
        """OptimizationRequestForm - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._target_hardware = None
        self._target_batch_size = None
        self._target_metric = None
        self._optimize_model_size = None
        self._quantization_level = None
        self._optimize_autonac = None
        self._name = None
        self._raw_format = None
        self.discriminator = None

        self.target_hardware = target_hardware
        self.target_batch_size = target_batch_size
        if target_metric is not None:
            self.target_metric = target_metric
        self.optimize_model_size = optimize_model_size
        self.quantization_level = quantization_level
        self.optimize_autonac = optimize_autonac
        if name is not None:
            self.name = name
        if raw_format is not None:
            self.raw_format = raw_format

    @property
    def target_hardware(self):
        """Gets the target_hardware of this OptimizationRequestForm.  # noqa: E501


        :return: The target_hardware of this OptimizationRequestForm.  # noqa: E501
        :rtype: HardwareType
        """
        return self._target_hardware

    @target_hardware.setter
    def target_hardware(self, target_hardware):
        """Sets the target_hardware of this OptimizationRequestForm.


        :param target_hardware: The target_hardware of this OptimizationRequestForm.  # noqa: E501
        :type: HardwareType
        """
        if self.local_vars_configuration.client_side_validation and target_hardware is None:  # noqa: E501
            raise ValueError("Invalid value for `target_hardware`, must not be `None`")  # noqa: E501

        self._target_hardware = target_hardware

    @property
    def target_batch_size(self):
        """Gets the target_batch_size of this OptimizationRequestForm.  # noqa: E501


        :return: The target_batch_size of this OptimizationRequestForm.  # noqa: E501
        :rtype: int
        """
        return self._target_batch_size

    @target_batch_size.setter
    def target_batch_size(self, target_batch_size):
        """Sets the target_batch_size of this OptimizationRequestForm.


        :param target_batch_size: The target_batch_size of this OptimizationRequestForm.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and target_batch_size is None:  # noqa: E501
            raise ValueError("Invalid value for `target_batch_size`, must not be `None`")  # noqa: E501

        self._target_batch_size = target_batch_size

    @property
    def target_metric(self):
        """Gets the target_metric of this OptimizationRequestForm.  # noqa: E501


        :return: The target_metric of this OptimizationRequestForm.  # noqa: E501
        :rtype: Metric
        """
        return self._target_metric

    @target_metric.setter
    def target_metric(self, target_metric):
        """Sets the target_metric of this OptimizationRequestForm.


        :param target_metric: The target_metric of this OptimizationRequestForm.  # noqa: E501
        :type: Metric
        """

        self._target_metric = target_metric

    @property
    def optimize_model_size(self):
        """Gets the optimize_model_size of this OptimizationRequestForm.  # noqa: E501


        :return: The optimize_model_size of this OptimizationRequestForm.  # noqa: E501
        :rtype: bool
        """
        return self._optimize_model_size

    @optimize_model_size.setter
    def optimize_model_size(self, optimize_model_size):
        """Sets the optimize_model_size of this OptimizationRequestForm.


        :param optimize_model_size: The optimize_model_size of this OptimizationRequestForm.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and optimize_model_size is None:  # noqa: E501
            raise ValueError("Invalid value for `optimize_model_size`, must not be `None`")  # noqa: E501

        self._optimize_model_size = optimize_model_size

    @property
    def quantization_level(self):
        """Gets the quantization_level of this OptimizationRequestForm.  # noqa: E501


        :return: The quantization_level of this OptimizationRequestForm.  # noqa: E501
        :rtype: QuantizationLevel
        """
        return self._quantization_level

    @quantization_level.setter
    def quantization_level(self, quantization_level):
        """Sets the quantization_level of this OptimizationRequestForm.


        :param quantization_level: The quantization_level of this OptimizationRequestForm.  # noqa: E501
        :type: QuantizationLevel
        """
        if self.local_vars_configuration.client_side_validation and quantization_level is None:  # noqa: E501
            raise ValueError("Invalid value for `quantization_level`, must not be `None`")  # noqa: E501

        self._quantization_level = quantization_level

    @property
    def optimize_autonac(self):
        """Gets the optimize_autonac of this OptimizationRequestForm.  # noqa: E501


        :return: The optimize_autonac of this OptimizationRequestForm.  # noqa: E501
        :rtype: bool
        """
        return self._optimize_autonac

    @optimize_autonac.setter
    def optimize_autonac(self, optimize_autonac):
        """Sets the optimize_autonac of this OptimizationRequestForm.


        :param optimize_autonac: The optimize_autonac of this OptimizationRequestForm.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and optimize_autonac is None:  # noqa: E501
            raise ValueError("Invalid value for `optimize_autonac`, must not be `None`")  # noqa: E501

        self._optimize_autonac = optimize_autonac

    @property
    def name(self):
        """Gets the name of this OptimizationRequestForm.  # noqa: E501


        :return: The name of this OptimizationRequestForm.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OptimizationRequestForm.


        :param name: The name of this OptimizationRequestForm.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def raw_format(self):
        """Gets the raw_format of this OptimizationRequestForm.  # noqa: E501


        :return: The raw_format of this OptimizationRequestForm.  # noqa: E501
        :rtype: bool
        """
        return self._raw_format

    @raw_format.setter
    def raw_format(self, raw_format):
        """Sets the raw_format of this OptimizationRequestForm.


        :param raw_format: The raw_format of this OptimizationRequestForm.  # noqa: E501
        :type: bool
        """

        self._raw_format = raw_format

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OptimizationRequestForm):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OptimizationRequestForm):
            return True

        return self.to_dict() != other.to_dict()
