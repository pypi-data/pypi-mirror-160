# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdksas.endpoint import endpoint_data

class OperationSuspEventsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Sas', '2018-12-03', 'OperationSuspEvents')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_SuspiciousEventIds(self): # String
		return self.get_query_params().get('SuspiciousEventIds')

	def set_SuspiciousEventIds(self, SuspiciousEventIds):  # String
		self.add_query_param('SuspiciousEventIds', SuspiciousEventIds)
	def get_SubOperation(self): # String
		return self.get_query_params().get('SubOperation')

	def set_SubOperation(self, SubOperation):  # String
		self.add_query_param('SubOperation', SubOperation)
	def get_SourceIp(self): # String
		return self.get_query_params().get('SourceIp')

	def set_SourceIp(self, SourceIp):  # String
		self.add_query_param('SourceIp', SourceIp)
	def get_WarnType(self): # String
		return self.get_query_params().get('WarnType')

	def set_WarnType(self, WarnType):  # String
		self.add_query_param('WarnType', WarnType)
	def get_From(self): # String
		return self.get_query_params().get('From')

	def set_From(self, _From):  # String
		self.add_query_param('From', _From)
	def get_Operation(self): # String
		return self.get_query_params().get('Operation')

	def set_Operation(self, Operation):  # String
		self.add_query_param('Operation', Operation)
