from numpy import ones, int32
import multiprocessing
import pycuda
import pycuda.autoinit as autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule

def doit(x):

    code = '''
    __global__ void test(double *x, int n)
    {
     int i = blockIdx.x * blockDim.x + threadIdx.x;
     if(i>=n) return;
     x[i] *= 2.0;
    }
    '''
    
    mod = SourceModule(code)
    f = mod.get_function('test')
    x = gpuarray.to_gpu(ones(100))
    f(x, int32(100), block=(100,1,1))
    print x.get()

pool = multiprocessing.Pool(1)
result = pool.map(doit, [0])
print result
