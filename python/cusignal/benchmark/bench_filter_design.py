# Copyright (c) 2019-2020, NVIDIA CORPORATION.
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

import cupy as cp
import cusignal
import numpy as np
import pytest

from cusignal.test.utils import array_equal
from scipy import signal

cusignal.precompile_kernels()


# Missing
# kaiser_beta
# kaiser_atten
# cmplx_sort


class BenchFilterDesign:
    @pytest.mark.benchmark(group="FirWin")
    @pytest.mark.parametrize("num_samps", [2 ** 15])
    @pytest.mark.parametrize("f1", [0.1, 0.15])
    @pytest.mark.parametrize("f2", [0.2, 0.4])
    class BenchFirWin:
        def cpu_version(self, num_samps, f1, f2):
            return signal.firwin(num_samps, [f1, f2], pass_zero=False)

        def bench_firwin_cpu(self, benchmark, num_samps, f1, f2):
            benchmark(
                self.cpu_version, num_samps, f1, f2,
            )

        def bench_firwin_gpu(self, benchmark, num_samps, f1, f2):

            output = benchmark(
                cusignal.firwin, num_samps, [f1, f2], pass_zero=False
            )

            key = self.cpu_version(num_samps, f1, f2)
            assert array_equal(cp.asnumpy(output), key)

    @pytest.mark.benchmark(group="KaiserBeta")
    class BenchKaiserBeta:
        def cpu_version(self, cpu_sig):
            return signal.kaiser_beta(cpu_sig)

        def bench_kaiser_beta_cpu(self, benchmark):
            benchmark(self.cpu_version, cpu_sig)

        def bench_kaiser_beta_gpu(self, benchmark):

            output = benchmark(cusignal.kaiser_beta, gpu_sig)

            key = self.cpu_version(cpu_sig)
            assert array_equal(cp.asnumpy(output), key)

    @pytest.mark.benchmark(group="KaiserAtten")
    class BenchKaiserAtten:
        def cpu_version(self, cpu_sig):
            return signal.kaiser_atten(cpu_sig)

        def bench_kaiser_atten_cpu(self, benchmark):
            benchmark(self.cpu_version, cpu_sig)

        def bench_kaiser_atten_gpu(self, benchmark):

            output = benchmark(cusignal.kaiser_atten, gpu_sig)

            key = self.cpu_version(cpu_sig)
            assert array_equal(cp.asnumpy(output), key)

    @pytest.mark.benchmark(group="CmplxSort")
    class BenchCmplxSort:
        def cpu_version(self, cpu_sig):
            return signal.cmplx_sort(cpu_sig)

        def bench_cmplx_sort_cpu(self, benchmark):
            benchmark(self.cpu_version, cpu_sig)

        def bench_cmplx_sort_gpu(self, benchmark):

            output = benchmark(cusignal.cmplx_sort, gpu_sig)

            key = self.cpu_version(cpu_sig)
            assert array_equal(cp.asnumpy(output), key)
