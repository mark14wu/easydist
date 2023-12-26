# Copyright (c) 2023, Alibaba Group;
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from collections import defaultdict

class OutTensorMemInfo:
    def __init__(
        self,
        out_index,
        mem_size,
        mem_index,
        is_reference
    ):
        self.out_index = out_index
        self.mem_size = mem_size

        # when self.is_reference is True, it is the input tensor index it refer to
        # otherwise, it is the allocation index of all allocations of its owner node
        self.mem_index = mem_index

        # bool
        # True: it is a reference of an input tensor
        # False: it is new allocated memory
        self.is_reference = is_reference

    def __str__(self) -> str:
        mem_info_str = ""
        if self.is_reference:
            mem_info_str = "idx: " + str(self.out_index) + ", size: " + \
                           str(self.mem_size) + ", input idx: " + \
                           str(self.mem_index)
        else:
            mem_info_str = "idx: " + str(self.out_index) + ", size: " + \
                           str(self.mem_size) + ", alloc idx: " + \
                           str(self.mem_index)
        return mem_info_str

class NodeMemInfo:
    def __init__(self):
        self.out_tensor_infos = []

    def add_out_tensor_mem_info(self, out_index, mem_size, mem_index,
                                is_reference):
        out_tensor_mem_info = OutTensorMemInfo(
                                  out_index, mem_size, mem_index, is_reference)
        self.out_tensor_infos.append(out_tensor_mem_info)

    def __str__(self) -> str:
        mem_info_str = ""
        for tensor_mem_info in self.out_tensor_infos:
            mem_info_str += str(tensor_mem_info) + "\n"
        return mem_info_str

class GraphMemInfo:
    def __init__(self):
        self.node_mem_infos = defaultdict(lambda: NodeMemInfo())

    def get_node_mem_info(self, node_name) -> NodeMemInfo:
        return self.node_mem_infos[node_name]

    def __str__(self) -> str:
        graph_mem_info_str = ""
        for node_name, mem_info in self.node_mem_infos.items():
            graph_mem_info_str += node_name + ":\n" + str(mem_info) + "\n"

        return graph_mem_info_str
