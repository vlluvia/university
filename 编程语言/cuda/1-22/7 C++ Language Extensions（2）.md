
## 7.5. Memory Fence Functions

CUDA 编程模型假定设备具有弱有序内存模型，即 CUDA 线程将数据写入共享内存、全局内存、页面锁定主机内存或对等设备内存的顺序不一定是观察到数据由另一个 CUDA 或主机线程写入的顺序。两个线程在不同步的情况下读取或写入同一内存位置是未定义的行为。  
``` 
__device__ int X = 1, Y = 2;

__device__ void writeXY()
{
    X = 10;
    Y = 20;
}

__device__ void readXY()
{
    int B = Y;
    int A = X;
}
```

> 两个线程同时从相同的内存位置 X和Y 读取和写入。任何数据争用都是未定义的行为，并且没有定义的语义。 A 和 B 的结果值可以是任何值。    
> 内存围栏函数可用于对内存访问强制执行顺序一致的排序。内存围栏函数在强制执行排序的作用域上有所不同，但它们与访问的内存空间（共享内存、全局内存、页面锁定主机内存和对等设备的内存）无关。
``` 
void __threadfence_block();
```
> 等效于 cuda：：atomic_thread_fence（cuda：：memory_order_seq_cst， cuda：：thread_scope_block），并确保：
> 1. 调用线程块中的所有线程都会观察到调用线程在调用__threadfence_block（）之前对所有内存进行的所有写入，这些写入发生在调用线程调用__threadsfence_bock（）之后对所有内存执行的所有写入之前
> 2. 在调用__threadfence_block（）之前，调用线程从所有内存进行的所有读取都在调用__hreadfence_block（）之后，调用线程对所有内存进行所有读取之前排序。

``` 
void __threadfence();
```
> 等效于 cuda：：atomic_thread_fence（cuda：：memory_order_seq_cst， cuda：：thread_scope_device），并确保设备中的任何线程都不会观察到在调用 之前对调用线程 __threadfence() 对所有内存进行任何写入之前发生的写入 __threadfence() 。   

``` 
void __threadfence_system();
```

> 等效于 cuda：：atomic_thread_fence（cuda：：memory_order_seq_cst， cuda：：thread_scope_system），并确保设备中的所有线程、主机线程和对等设备中的所有线程都观察到调用线程在调用 之前对调用线程 __threadfence_system() 进行的所有内存写入之前发生 __threadfence_system() 。    
> __threadfence_system() 仅受计算能力为 2.x 及更高版本的设备支持。


``` 
__device__ int X = 1, Y = 2;

__device__ void writeXY()
{
    X = 10;
    __threadfence();
    Y = 20;
}

__device__ void readXY()
{
    int B = Y;
    __threadfence();
    int A = X;
}
```

> For this code, the following outcomes can be observed:
> 1. A equal to 1 and B equal to 2, 
> 2. A equal to 10 and B equal to 2, 
> 3. A equal to 10 and B equal to 20.

> 第四种结果是不可能的，因为第一次写入必须在第二次写入之前可见。  
> If thread 1 and 2 belong to the same block, it is enough to use __threadfence_block()  
> 如果线程1和2不属于同一个块，则如果它们是来自同一设备的CUDA线程，则必须使用__threadfence（）；
> 如果它们是两个不同设备的CUDA线程，则则必须使用__ threadfence_system（）。

> 一个常见的用例是线程使用其他线程生成的一些数据，如以下内核代码示例所示，该内核在一次调用中计算 N 个数字数组的总和。每个模块首先对数组的子集求和，并将结果存储在全局内存中。当所有块都完成后，最后一个完成的块会从全局内存中读取这些部分总和中的每一个，并将它们求和以获得最终结果。为了确定哪个块最后完成，每个块以原子方式递增一个计数器，以表示它已经完成了计算和存储其部分总和（请参阅关于原子函数的原子函数）。最后一个块是接收计数器值等于 gridDim.x-1 的块。如果在存储部分总和和递增计数器之间没有设置围栏，则计数器可能会在存储部分总和之前递增，因此可能会到达 gridDim.x-1 并让最后一个块在内存中实际更新之前开始读取部分总和。   
> 内存围栏函数仅影响线程对内存操作的排序;它们本身并不能确保这些内存操作对其他线程可见（就像 __syncthreads() 对块中的线程所做的那样（请参阅同步函数））。在下面的代码示例中，通过将变量声明为易失性变量来确保对 result 变量的内存操作的可见性（请参阅 Volatile 限定符）。

``` 
__device__ unsigned int count = 0;
__shared__ bool isLastBlockDone;
__global__ void sum(const float* array, unsigned int N,
                    volatile float* result)
{
    // Each block sums a subset of the input array.
    float partialSum = calculatePartialSum(array, N);

    if (threadIdx.x == 0) {

        // Thread 0 of each block stores the partial sum
        // to global memory. The compiler will use
        // a store operation that bypasses the L1 cache
        // since the "result" variable is declared as
        // volatile. This ensures that the threads of
        // the last block will read the correct partial
        // sums computed by all other blocks.
        result[blockIdx.x] = partialSum;

        // Thread 0 makes sure that the incrementation
        // of the "count" variable is only performed after
        // the partial sum has been written to global memory.
        __threadfence();

        // Thread 0 signals that it is done.
        unsigned int value = atomicInc(&count, gridDim.x);

        // Thread 0 determines if its block is the last
        // block to be done.
        isLastBlockDone = (value == (gridDim.x - 1));
    }

    // Synchronize to make sure that each thread reads
    // the correct value of isLastBlockDone.
    __syncthreads();

    if (isLastBlockDone) {

        // The last block sums the partial sums
        // stored in result[0 .. gridDim.x-1]
        float totalSum = calculateTotalSum(result);

        if (threadIdx.x == 0) {

            // Thread 0 of last block stores the total sum
            // to global memory and resets the count
            // varialble, so that the next kernel call
            // works properly.
            result[0] = totalSum;
            count = 0;
        }
    }
}
```

---
## 7.6. Synchronization Functions
> 等到线程块中的所有线程都到达这一点，并且这些线程之前 __syncthreads() 所做的所有全局和共享内存访问对块中的所有线程都是可见的。

> __syncthreads() 用于协调同一块的线程之间的通信。当块中的某些线程访问共享或全局内存中的相同地址时，其中一些内存访问可能存在先写后写、后写或后写危险。通过在这些访问之间同步线程，可以避免这些数据危害。

> __syncthreads() 在条件代码中是允许的，但前提是条件在整个线程块中的计算结果相同，否则代码执行可能会挂起或产生意外的副作用。

> 计算能力为 2.x 及更高版本的设备支持下面描述的 __syncthreads() 三种变体。

``` 
int __syncthreads_count(int predicate);
```
> 与附加功能相同 __syncthreads() ，即它为块的所有线程计算谓词，并将谓词计算的线程数返回为非零。

``` 
int __syncthreads_and(int predicate);
```
> 与附加功能相同 __syncthreads() ，即它为块的所有线程计算谓词，并返回非零，当且仅当谓词对所有线程的计算结果为非零时。

``` 
int __syncthreads_or(int predicate);
```

> 与 __syncthreads() 附加功能相同，它为块的所有线程评估谓词，并返回非零，当且仅当谓词对其中任何一个线程的计算结果为非零时。

``` 
void __syncwarp(unsigned mask=0xffffffff);
```
> 将导致执行线程等待，直到 mask 中命名的所有 warp 通道都执行了 a __syncwarp() （具有相同的掩码），然后再恢复执行。每个调用线程都必须在掩码中设置自己的位，并且掩码中命名的所有未退出的线程都必须执行具有相同掩码的对应 __syncwarp() 线程，否则结果未定义。


---
## 7.7. Mathematical Functions

> 参考手册列出了设备代码中支持的所有 C/C++ 标准库数学函数以及仅在设备代码中支持的所有内部函数。  
> https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#mathematical-functions-appendix

--- 

## 7.8. Texture Functions
> Texture objects are described in Texture Object API. https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#texture-object-api  
> Texture fetching is described in Texture Fetching.   https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#texture-fetching

### 7.8.1. Texture Object API

#### 7.8.1.1. tex1Dfetch()
``` 
template<class T>
T tex1Dfetch(cudaTextureObject_t texObj, int x);
```
> 使用整数纹理坐标x从一维纹理对象texObj指定的线性内存区域提取。tex1Dfetch（）仅适用于非标准化坐标，因此仅支持边界和箝位寻址模式。它不执行任何纹理过滤。对于整数类型，它可以选择性地将整数提升为单精度浮点。

#### 7.8.1.2. tex1D()
``` 
template<class T>
T tex1D(cudaTextureObject_t texObj, float x);
```

> 使用 texture coordinate x 从一维纹理对象 texObj 指定的 CUDA 数组中获取。

#### 7.8.1.3. tex1DLod()
``` 
template<class T>
T tex1DLod(cudaTextureObject_t texObj, float x, float level);
```
> 使用细节 level 级别的纹理坐标 x 从一维纹理对象 texObj 指定的 CUDA 数组中获取。

#### 7.8.1.4. tex1DGrad()
``` 
template<class T>
T tex1DGrad(cudaTextureObject_t texObj, float x, float dx, float dy);
```
> 使用纹理坐标x从一维纹理对象texObj指定的CUDA阵列中获取。细节级别从x梯度dx和Y梯度dy导出。


#### 7.8.1.5. tex2D()


#### 7.8.1.13. tex3D()




### 7.9. Surface Functions

> Surface 对象在 Surface Object API 中进行了描述 https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#surface-object-api-appendix

> 在以下部分中，boundaryMode指定边界模式，即如何处理超出范围的曲面坐标；它等于cudaBoundaryModeClamp，在这种情况下，超出范围的坐标被箝位到有效范围，或者等于cudaBoundaryModeZero，在这种情形下，超出区域的读取返回零并且超出范围的写入被忽略，或者等于cudaBoundaryModeTrap，在这种情况下，超过范围的访问导致内核执行失败。









