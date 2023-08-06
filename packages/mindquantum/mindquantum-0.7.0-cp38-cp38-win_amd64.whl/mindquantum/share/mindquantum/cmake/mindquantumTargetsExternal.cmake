# ==============================================================================
#
# Copyright 2022 <Huawei Technologies Co., Ltd>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==============================================================================



# projectq (local)
find_package(projectq
             0.5.1
             REQUIRED
             CONFIG
             NO_DEFAULT_PATH
             HINTS
             "${MQ_PACKAGE_PREFIX_DIR}/lib/mindquantum/third_party/projectq_0.5.1_d169a979e60d8cec32ef1233131fcaf9"
             REQUIRED)
if(TARGET projectq::projectq AND NOT TARGET mindquantum::projectq)
  add_library(mindquantum::projectq ALIAS projectq::projectq)
endif()

# pybind11 (system)
find_package(pybind11
             2.9.1
             REQUIRED)
if(TARGET pybind11::headers AND NOT TARGET mindquantum::pybind11_headers)
  add_library(mindquantum::pybind11_headers ALIAS pybind11::headers)
endif()
if(TARGET pybind11::module AND NOT TARGET mindquantum::pybind11_module)
  add_library(mindquantum::pybind11_module ALIAS pybind11::module)
endif()
if(TARGET pybind11::lto AND NOT TARGET mindquantum::pybind11_lto)
  add_library(mindquantum::pybind11_lto ALIAS pybind11::lto)
endif()
if(TARGET pybind11::windows_extras AND NOT TARGET mindquantum::windows_extra)
  add_library(mindquantum::windows_extra ALIAS pybind11::windows_extras)
endif()
