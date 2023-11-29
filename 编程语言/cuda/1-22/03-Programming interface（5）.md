
### 3.2.9. Multi-Device System


#### 3.2.9.1. Device Enumeration
一个主机系统可以有多个设备。以下代码示例演示如何枚举这些设备、查询其属性以及确定启用 CUDA 的设备数。

``` 
int deviceCount;
cudaGetDeviceCount(&deviceCount);
int device;
for (device = 0; device < deviceCount; ++device) {
    cudaDeviceProp deviceProp;
    cudaGetDeviceProperties(&deviceProp, device);
    printf("Device %d has compute capability %d.%d.\n",
           device, deviceProp.major, deviceProp.minor);
}
```

#### 3.2.9.2. Device Selection
主机线程可以随时通过调用 cudaSetDevice() 来设置它所操作的设备。设备内存分配和内核启动是在当前设置的设备上进行的;流和事件是与当前设置的设备关联的。如果未调用 to cudaSetDevice() ，则当前设备为设备 0。  
以下代码示例说明了设置当前设备如何影响内存分配和内核执行。
``` 
size_t size = 1024 * sizeof(float);
cudaSetDevice(0);            // Set device 0 as current
float* p0;
cudaMalloc(&p0, size);       // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0); // Launch kernel on device 0
cudaSetDevice(1);            // Set device 1 as current
float* p1;
cudaMalloc(&p1, size);       // Allocate memory on device 1
MyKernel<<<1000, 128>>>(p1); // Launch kernel on device 1
```

#### 3.2.9.3. Stream and Event Behavior
如果内核启动发送到未与当前设备关联的流，则内核启动将失败，如以下代码示例所示

``` 
cudaSetDevice(0);               // Set device 0 as current
cudaStream_t s0;
cudaStreamCreate(&s0);          // Create stream s0 on device 0
MyKernel<<<100, 64, 0, s0>>>(); // Launch kernel on device 0 in s0
cudaSetDevice(1);               // Set device 1 as current
cudaStream_t s1;
cudaStreamCreate(&s1);          // Create stream s1 on device 1
MyKernel<<<100, 64, 0, s1>>>(); // Launch kernel on device 1 in s1

// This kernel launch will fail:
MyKernel<<<100, 64, 0, s0>>>(); // Launch kernel on device 1 in s0
```
> 即使将内存复制颁发给未与当前设备关联的流，它也会成功。   
> cudaEventRecord() 如果输入事件和输入流关联到不同的设备，则将失败。  
> cudaEventElapsedTime() 如果两个输入事件关联到不同的设备，则将失败。  
> cudaEventSynchronize() 即使输入事件与与当前设备不同的设备相关联，也会 cudaEventQuery() 成功。  
> cudaStreamWaitEvent() 即使输入流和输入事件关联到不同的设备，也会成功。 cudaStreamWaitEvent() 因此，可用于将多个设备相互同步。  
> 每个设备都有自己的默认流（请参阅默认流），因此向设备的默认流发出的命令可能会无序执行，或者与向任何其他设备的默认流发出的命令同时执行。  



#### 3.2.9.4. Peer-to-Peer Memory Access

> 根据系统属性，特别是PCIe和/或NVLINK拓扑，设备能够对彼此的内存进行寻址（即，在一个设备上执行的内核可以取消引用指向另一个设备内存的指针）。如果两个设备返回 true，则 cudaDeviceCanAccessPeer() 支持此对等内存访问功能。  
> 点对点内存访问仅在 64 位应用程序中受支持，并且必须通过调用 cudaDeviceEnablePeerAccess() 在两个设备之间启用，如以下代码示例所示。在未启用 NVSwitch 的系统上，每个设备最多可以支持系统范围内的 8 个对等连接。  
> 

``` 
cudaSetDevice(0);                   // Set device 0 as current
float* p0;
size_t size = 1024 * sizeof(float);
cudaMalloc(&p0, size);              // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0);        // Launch kernel on device 0
cudaSetDevice(1);                   // Set device 1 as current
cudaDeviceEnablePeerAccess(0, 0);   // Enable peer-to-peer access
                                    // with device 0

// Launch kernel on device 1
// This kernel launch can access memory on device 0 at address p0
MyKernel<<<1000, 128>>>(p0);
```

##### 3.2.9.4.1. IOMMU on Linux
> 仅在 Linux 上，CUDA 和显示驱动程序不支持支持 IOMMU 的裸机 PCIe 对等内存复制。但是，CUDA 和显示驱动程序确实支持通过 VM 直通的 IOMMU。因此，Linux 上的用户在本机裸机系统上运行时，应禁用 IOMMU。应启用 IOMMU，并将 VFIO 驱动程序用作虚拟机的 PCIe 直通。
> 在 Windows 上，不存在上述限制。 https://download.nvidia.com/XFree86/Linux-x86_64/396.51/README/dma_issues.html




#### 3.2.9.5. Peer-to-Peer Memory Copy
> 可以在两个不同设备的内存之间执行内存复制。  
> 当两个设备都使用统一地址空间时（请参阅统一虚拟地址空间https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#unified-virtual-address-space），这是使用设备内存(https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory)中提到的常规内存复制功能完成的。

> 否则，将使用 cudaMemcpyPeer() 、 、 cudaMemcpyPeerAsync() cudaMemcpy3DPeer() 或 cudaMemcpy3DPeerAsync() 以下代码示例中所示完成此操作。

``` 
cudaSetDevice(0);                   // Set device 0 as current
float* p0;
size_t size = 1024 * sizeof(float);
cudaMalloc(&p0, size);              // Allocate memory on device 0
cudaSetDevice(1);                   // Set device 1 as current
float* p1;
cudaMalloc(&p1, size);              // Allocate memory on device 1
cudaSetDevice(0);                   // Set device 0 as current
MyKernel<<<1000, 128>>>(p0);        // Launch kernel on device 0
cudaSetDevice(1);                   // Set device 1 as current
cudaMemcpyPeer(p1, 1, p0, 0, size); // Copy p0 to p1
MyKernel<<<1000, 128>>>(p1);        // Launch kernel on device 1
```

> 两个不同设备的内存之间的副本（在隐式 NULL 流中）：   
> does not start until all commands previously issued to either device have completed  
> runs to completion before any commands (see Asynchronous Concurrent Execution) issued after the copy to either device can start.

> 请注意，如果按照 cudaDeviceEnablePeerAccess() 点对点内存访问中所述在两个设备之间启用点对点访问，则这两个设备之间的点对点内存复制不再需要通过主机暂存，因此速度更快。

---

### 3.2.10. Unified Virtual Address Space

> 当应用程序作为 64 位进程运行时，单个地址空间将用于主机和计算能力 2.0 及更高版本的所有设备。通过 CUDA API 调用进行的所有主机内存分配以及受支持设备上的所有设备内存分配都在此虚拟地址范围内。因此  
> 1. 通过 CUDA 分配的主机或使用统一地址空间的任何设备上的任何内存的位置都可以通过使用 cudaPointerGetAttributes() 的指针值来确定。  
> 2. 当复制到使用统一地址空间的任何设备的内存或从内存中复制时，可以设置 的 cudaMemcpyKind cudaMemcpy*() 参数来 cudaMemcpyDefault 确定指针的位置。这也适用于未通过 CUDA 分配的主机指针，只要当前设备使用统一寻址即可。  
> 3. 分配 via cudaHostAlloc() 在使用统一地址空间的所有设备之间自动可移植（请参阅可移植内存），并且 返回 cudaHostAlloc() 的指针可以直接从这些设备上运行的内核中使用（即，无需获取设备指针， cudaHostGetDevicePointer() 如映射内存中所述。  

> 应用程序可以通过检查设备属性（请参阅设备枚举）是否等于 1 来查询是否将统一地址空间用于特定 unifiedAddressing 设备。


---
### 3.2.11. Interprocess Communication
> 主机线程创建的任何设备内存指针或事件句柄都可以由同一进程中的任何其他线程直接引用。但是，它在此进程之外无效，因此不能由属于其他进程的线程直接引用。  
> 若要在进程之间共享设备内存指针和事件，应用程序必须使用进程间通信 API，参考手册中对此进行了详细描述。IPC API 仅支持 Linux 上的 64 位进程以及计算能力为 2.0 及更高版本的设备。请注意， cudaMallocManaged 分配不支持使用 IPC API。  
> 使用此 API，应用程序可以使用 获取 cudaIpcGetMemHandle() 给定设备内存指针的 IPC 句柄，使用标准 IPC 机制将其传递给另一个进程 （例如，进程间共享内存或文件） ，并用于 cudaIpcOpenMemHandle() 从 IPC 句柄检索设备指针，该句柄是此其他进程中的有效指针。可以使用类似的入口点共享事件句柄。  
> 请注意，出于性能原因，可能会 cudaMalloc() 从较大的内存块进行子分配。在这种情况下，CUDA IPP API 将共享整个底层内存块，这可能会导致其他子分配被共享，这可能会导致进程之间的信息泄露。为防止此行为，建议仅共享大小为 2MiB 的分配。  
> 使用 IPC API 的一个示例是，单个主进程生成一批输入数据，使数据可供多个辅助进程使用，而无需重新生成或复制。  

> 注意:  
> 从 CUDA 11.5 开始，具有 7.x 及更高版本计算能力的 L4T 和嵌入式 Linux Tegra 设备仅支持事件共享 IPC API。Tegra 平台仍不支持内存共享 IPC API。


---
### 3.2.12. Error Checking

> 所有运行时函数都返回错误代码，但对于异步函数（请参阅异步并发执行），此错误代码不可能报告设备上可能发生的任何异步错误，因为该函数在设备完成任务之前返回;错误代码仅报告在执行任务之前在主机上发生的错误，通常与参数验证有关;如果发生异步错误，则后续一些不相关的运行时函数调用会报告该错误。  
> 因此，在某个异步函数调用之后立即检查异步错误的唯一方法是在调用后立即进行同步，方法是调用 cudaDeviceSynchronize() （或使用异步并发执行中描述的任何其他同步机制）并检查 返回的 cudaDeviceSynchronize() 错误代码。    
> 运行时为每个主机线程维护一个错误变量，每次发生错误（参数验证错误或异步错误）时，该变量都会初始化为 cudaSuccess 错误代码并被错误代码覆盖。 cudaPeekAtLastError() 返回此变量。 cudaGetLastError() 返回此变量并将其重置为 cudaSuccess 。    
> 内核启动不会返回任何错误代码，因此 cudaPeekAtLastError() 必须在 cudaGetLastError() 内核启动后立即调用，以检索任何预启动错误。为了确保在内核启动之前由 cudaPeekAtLastError() 调用返回或 cudaGetLastError() 不是源自调用的任何错误，必须确保将运行时错误变量设置为 cudaSuccess 内核启动之前，例如，在内核启动之前调用 cudaGetLastError() 。内核启动是异步的，因此要检查异步错误，应用程序必须在内核启动和调用 cudaPeekAtLastError() or cudaGetLastError() 之间同步。   
> 请注意， cudaErrorNotReady 它可能由 cudaStreamQuery() 和 cudaEventQuery() 不被视为错误返回，因此不会由 cudaPeekAtLastError() 或 cudaGetLastError() 报告。  


---
### 3.2.13. Call Stack
> 在计算能力为 2.x 及更高版本的设备上，可以使用 查询 cudaDeviceGetLimit() 调用堆栈的大小，并使用 cudaDeviceSetLimit() 进行设置。

> 当调用堆栈溢出时，如果应用程序通过 CUDA 调试器（CUDA-GDB、Nsight）运行，则内核调用将失败并出现堆栈溢出错误，否则会出现未指定的启动错误。当编译器无法确定堆栈大小时，它会发出警告，指出无法静态确定堆栈大小。递归函数通常就是这种情况。发出此警告后，如果默认堆栈大小不足，用户将需要手动设置堆栈大小。


---

### 3.2.14. Texture and Surface Memory

> CUDA 支持 GPU 用于图形访问纹理和表面内存的纹理硬件子集。从纹理或表面内存（而不是全局内存）读取数据可以带来多种性能优势，如设备内存访问中所述。

#### 3.2.14.1. Texture Memory
> 纹理内存是使用纹理函数中描述的设备函数从内核中读取的。通过调用这些函数之一读取纹理的过程称为纹理提取。每个纹理提取都会为纹理对象 API 指定一个称为纹理对象的参数。  
> texture 对象指定: 
> 1. The texture,这是提取的纹理内存片段。纹理对象是在运行时创建的，纹理是在创建纹理对象时指定的
> 2. 它的维度，指定纹理是作为使用一个纹理坐标的一维数组、使用两个纹理坐标的二维数组，还是使用三个纹理坐标的三维数组进行寻址。数组的元素称为纹素，是纹理元素的缩写。纹理宽度、高度和深度是指数组在每个维度中的大小。表 18 列出了最大纹理宽度、高度和深度，具体取决于设备的计算能力。
> 3. The type of a texel, 仅限于基本整数和单精度浮点类型，以及内置向量类型中定义的任何 1、2 和 4 分量向量类型，这些类型派生自基本整数和单精度浮点类型。
> 4. 读取模式，等于 cudaReadModeNormalizedFloat 或 cudaReadModeElementType 。如果是，并且纹素的类型是 16 位或 8 位整数类型 cudaReadModeNormalizedFloat ，则纹理提取返回的值实际上作为浮点类型返回，并且整数类型的全范围映射到 [0.0， 1.0] 对于无符号整数类型，对于有符号整数类型，映射到 [-1.0， 1.0];例如，值为 0xff 的无符号 8 位纹理元素读为 1。如果是 cudaReadModeElementType ，则不执行转换。
> 5. 纹理坐标是否归一化。默认情况下，纹理（由纹理函数的函数）使用范围 [0， N-1] 中的浮点坐标进行引用，其中 N 是与坐标对应的维度中纹理的大小。例如，对于 x 和 y 维度，将分别使用 [0， 63] 和 [0， 31] 范围内的坐标引用大小为 64x32 的纹理。归一化纹理坐标会导致在 [0.0， 1.0-1/N] 范围内指定坐标，而不是在 [0， N-1] 范围内指定坐标，因此相同的 64x32 纹理将由 x 和 y 维度上 [0， 1-1/N] 范围内的归一化坐标寻址。归一化纹理坐标非常适合某些应用程序的要求，如果纹理坐标最好与纹理大小无关。 
> 6. 寻址模式。使用超出范围的坐标调用第 B.8 节的设备函数是有效的。寻址模式定义在这种情况下发生的情况。默认寻址模式是将坐标限制在有效范围内：[0， N） 表示非归一化坐标，[0.0， 1.0） 表示归一化坐标。如果指定了边框模式，则具有超出范围的纹理坐标的纹理提取将返回零。对于归一化坐标，也可以使用环绕模式和镜像模式。使用换行模式时，每个坐标 x 将转换为 frac（x）=x - floor（x），其中 floor（x） 是不大于 x 的最大整数。使用镜像模式时，如果 floor（x） 为偶数，则每个坐标 x 转换为 frac（x），如果 floor（x） 为奇数，则将转换为 1-frac（x）。寻址模式指定为大小为 3 的数组，其第一个、第二个和第三个元素分别指定第一、第二和第三个纹理坐标的寻址模式;寻址方式为 cudaAddressModeBorder 、 、 cudaAddressModeClamp cudaAddressModeWrap 和 cudaAddressModeMirror ; cudaAddressModeWrap 并且 cudaAddressModeMirror 仅支持归一化纹理坐标
> 7. 过滤模式，用于指定如何根据输入纹理坐标计算获取纹理时返回的值。线性纹理过滤只能对配置为返回浮点数据的纹理执行。它在相邻纹素之间执行低精度插值。启用后，将读取纹理提取位置周围的纹素，并根据纹理坐标落在纹素之间的位置对纹理提取的返回值进行插值。对一维纹理进行简单线性插值，对二维纹理进行双线性插值，对三维纹理进行三线性插值。纹理提取提供了有关纹理提取的更多详细信息。过滤模式等于 cudaFilterModePoint 或 cudaFilterModeLinear 。如果是，则返回值是 cudaFilterModePoint 纹理坐标最接近输入纹理坐标的纹素。如果是，则返回值是 cudaFilterModeLinear 纹理坐标最接近输入纹理坐标的两个（对于一维纹理）、四个（对于二维纹理）或八个（对于三维纹理）纹素的线性插值。 cudaFilterModeLinear 仅对浮点类型的返回值有效。
> 

##### 3.2.14.1.1. Texture Object API
> 纹理对象是使用 cudaCreateTextureObject() 类型的 struct cudaResourceDesc 资源描述创建的，该资源描述指定纹理，并且从纹理描述中定义如下
> 

``` 
struct cudaTextureDesc
{
    enum cudaTextureAddressMode addressMode[3];
    enum cudaTextureFilterMode  filterMode;
    enum cudaTextureReadMode    readMode;
    int                         sRGB;
    int                         normalizedCoords;
    unsigned int                maxAnisotropy;
    enum cudaTextureFilterMode  mipmapFilterMode;
    float                       mipmapLevelBias;
    float                       minMipmapLevelClamp;
    float                       maxMipmapLevelClamp;
};
```

> 1. addressMode specifies the addressing mode; 
> 2. filterMode specifies the filter mode; 
> 3. readMode specifies the read mode; 
> 4. normalizedCoords specifies whether texture coordinates are normalized or not; 
> 5. See reference manual for sRGB, maxAnisotropy, mipmapFilterMode, mipmapLevelBias, minMipmapLevelClamp, and maxMipmapLevelClamp.

``` 
// Simple transformation kernel
__global__ void transformKernel(float* output,
                                cudaTextureObject_t texObj,
                                int width, int height,
                                float theta)
{
    // Calculate normalized texture coordinates
    unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;

    float u = x / (float)width;
    float v = y / (float)height;

    // Transform coordinates
    u -= 0.5f;
    v -= 0.5f;
    float tu = u * cosf(theta) - v * sinf(theta) + 0.5f;
    float tv = v * cosf(theta) + u * sinf(theta) + 0.5f;

    // Read from texture and write to global memory
    output[y * width + x] = tex2D<float>(texObj, tu, tv);
}
```

``` 
// Simple transformation kernel
__global__ void transformKernel(float* output,
                                cudaTextureObject_t texObj,
                                int width, int height,
                                float theta)
{
    // Calculate normalized texture coordinates
    unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;

    float u = x / (float)width;
    float v = y / (float)height;

    // Transform coordinates
    u -= 0.5f;
    v -= 0.5f;
    float tu = u * cosf(theta) - v * sinf(theta) + 0.5f;
    float tv = v * cosf(theta) + u * sinf(theta) + 0.5f;

    // Read from texture and write to global memory
    output[y * width + x] = tex2D<float>(texObj, tu, tv);
}
```

##### 3.2.14.1.2. 16-Bit Floating-Point Textures

> CUDA 数组支持的 16 位浮点或半格式与 IEEE 754-2008 binary2 格式相同。

> CUDA C++ 不支持匹配的数据类型，但提供了内部函数，可通过 unsigned short type： __float2half_rn(float) 和 __half2float(unsigned short) .这些函数仅在设备代码中受支持。例如，可以在 OpenEXR 库中找到主机代码的等效函数。  
> 在执行任何过滤之前，在纹理提取期间，16 位浮点组件将提升为 32 位浮点。  
> 可以通过调用其中一个 cudaCreateChannelDescHalf*() 函数来创建 16 位浮点格式的通道描述。




##### 3.2.14.1.3. Layered Textures
> 一维或二维分层纹理（在 Direct3D 中也称为纹理数组，在 OpenGL 中也称为数组纹理）是由一系列层组成的纹理，所有这些层都是具有相同维度、大小和数据类型的规则纹理。   
> 使用整数索引和浮点纹理坐标对一维分层纹理进行寻址;索引表示序列中的一个图层，坐标表示该图层中的纹素。使用整数索引和两个浮点纹理坐标对二维分层纹理进行寻址;索引表示序列中的一个图层，坐标表示该图层中的纹素。   
> 分层纹理只能通过调用 cudaArrayLayered 标志（一维分层纹理的高度为零）来成为 cudaMalloc3DArray() CUDA 数组。  
> 使用 tex1DLayered（） 和 tex2DLayered（） 中描述的设备函数获取分层纹理。纹理过滤（请参阅纹理提取）仅在一个图层内完成，而不是跨图层完成。  


##### 3.2.14.1.4. Cubemap Textures


> 立方体贴图纹理是一种特殊类型的二维分层纹理，它有六个层表示立方体的面
> 1. 图层的宽度等于其高度
> 2. 立方体贴图使用三个纹理坐标 x、y 和 z 进行寻址，这些坐标被解释为从立方体中心发出并指向立方体的一个面以及与该面对应的图层内的纹素的方向向量。更具体地说，面由最大幅度为 m 的坐标选择，相应的层使用坐标 （s/m+1）/2 和 （t/m+1）/2 寻址，其中 s 和 t 在表 3 中定义

![img.png](3-2-14-1-4_1.png)


> 立方体贴图纹理只能是 CUDA 数组，方法是使用 cudaArrayCubemap 标志进行调用 cudaMalloc3DArray() 。  
> 使用 texCubemap（） 中描述的设备函数获取立方体贴图纹理。  
> 立方体贴图纹理仅在计算能力为 2.0 及更高版本的设备上受支持。


##### 3.2.14.1.5. Cubemap Layered Textures
> 立方体贴图分层纹理是一种分层纹理，其图层是相同维度的立方体贴图。  
> 使用整数索引和三个浮点纹理坐标对立方体贴图分层纹理进行寻址;索引表示序列中的立方体贴图，坐标表示该立方体贴图中的纹素。  
> 立方体贴图分层纹理只能是 CUDA 数组，方法是使用 cudaArrayLayered 和 cudaArrayCubemap 标志进行调用 cudaMalloc3DArray() 。  
> 使用 texCubemapLayered（） 中描述的设备函数获取立方体贴图分层纹理。纹理过滤（请参阅纹理提取）仅在一个图层内完成，而不是跨图层完成。  
> 立方体贴图分层纹理仅在计算能力为 2.0 及更高版本的设备上受支持。  

##### 3.2.14.1.6. Texture Gather
> 纹理收集是一种特殊的纹理提取，仅适用于二维纹理。它由函数 tex2Dgather() 执行，该函数具有与 tex2D() 相同的参数，外加一个等于 0、1、2 或 3 的附加 comp 参数（参见 tex2Dgather（））。它返回四个 32 位数字，对应于四个纹素中每个纹素的分量 comp 值，这些纹素在常规纹理提取期间将用于双线性滤波。例如，如果这些纹素的值为 （253， 20， 31， 255）、（250， 25， 29， 254）、（249， 16， 37， 253）、（251， 22， 30， 250），并且 comp 为 2，则返回 （31， 29， 37， tex2Dgather() 30）。  
> 请注意，纹理坐标的计算精度仅为 8 位。 tex2Dgather() 因此，对于将 1.0 用于其权重之一（α 或 β，请参阅线性滤波）的情况 tex2D() ，可能会返回意外结果。例如，x 纹理坐标为 2.49805：xB=x-0.5=1.99805，但 xB 的小数部分以 8 位定点格式存储。由于 0.99805 比 255.f/256.f 更接近 256.f/256.f，因此 xB 的值为 2。因此，在这种情况下，A tex2Dgather() 将返回 x 中的索引 2 和 3，而不是索引 1 和 2。  
> 只有使用 cudaArrayTextureGather flag 创建的 CUDA 数组支持纹理收集，并且宽度和高度小于表 18 中为纹理收集指定的最大值，该值小于常规纹理提取。  
> 


#### 3.2.14.2. Surface Memory
> 对于计算能力为 2.0 及更高版本的设备，可以使用 Surface Functions 中描述的函数通过 Surface 对象读取和写入使用该 cudaArraySurfaceLoadStore 标志创建的 CUDA 数组（如 Cubemap Surfaces 中所述）。
> 


##### 3.2.14.2.1. Surface Object API
> Surface 对象是使用 cudaCreateSurfaceObject() 类型的资源描述创建的 struct cudaResourceDesc 。与纹理内存不同，表面内存使用字节寻址。这意味着，用于通过纹理函数访问纹理元素的 x 坐标需要乘以元素的字节大小，才能通过曲面函数访问相同的元素。例如，绑定到纹理对象和表面对象 texObj surfObj 的一维浮点 CUDA 数组的纹理坐标 x 处的元素使用 tex1d(texObj, x) 通过 读取，但 surf1Dread(surfObj, 4*x) 通过 surfObj texObj 。类似地，绑定到纹理对象和表面对象 texObj surfObj 的二维浮点 CUDA 数组的纹理坐标 x 和 y 处的元素使用 tex2d(texObj, x, y) via texObj 访问，但 surf2Dread(surfObj, 4*x, y) 通过 surObj （y 坐标的字节偏移量是根据 CUDA 数组的基础线间距在内部计算的）。

``` 
// Simple copy kernel
__global__ void copyKernel(cudaSurfaceObject_t inputSurfObj,
                           cudaSurfaceObject_t outputSurfObj,
                           int width, int height)
{
    // Calculate surface coordinates
    unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x < width && y < height) {
        uchar4 data;
        // Read from input surface
        surf2Dread(&data,  inputSurfObj, x * 4, y);
        // Write to output surface
        surf2Dwrite(data, outputSurfObj, x * 4, y);
    }
}

// Host code
int main()
{
    const int height = 1024;
    const int width = 1024;

    // Allocate and set some host data
    unsigned char *h_data =
        (unsigned char *)std::malloc(sizeof(unsigned char) * width * height * 4);
    for (int i = 0; i < height * width * 4; ++i)
        h_data[i] = i;

    // Allocate CUDA arrays in device memory
    cudaChannelFormatDesc channelDesc =
        cudaCreateChannelDesc(8, 8, 8, 8, cudaChannelFormatKindUnsigned);
    cudaArray_t cuInputArray;
    cudaMallocArray(&cuInputArray, &channelDesc, width, height,
                    cudaArraySurfaceLoadStore);
    cudaArray_t cuOutputArray;
    cudaMallocArray(&cuOutputArray, &channelDesc, width, height,
                    cudaArraySurfaceLoadStore);

    // Set pitch of the source (the width in memory in bytes of the 2D array
    // pointed to by src, including padding), we dont have any padding
    const size_t spitch = 4 * width * sizeof(unsigned char);
    // Copy data located at address h_data in host memory to device memory
    cudaMemcpy2DToArray(cuInputArray, 0, 0, h_data, spitch,
                        4 * width * sizeof(unsigned char), height,
                        cudaMemcpyHostToDevice);

    // Specify surface
    struct cudaResourceDesc resDesc;
    memset(&resDesc, 0, sizeof(resDesc));
    resDesc.resType = cudaResourceTypeArray;

    // Create the surface objects
    resDesc.res.array.array = cuInputArray;
    cudaSurfaceObject_t inputSurfObj = 0;
    cudaCreateSurfaceObject(&inputSurfObj, &resDesc);
    resDesc.res.array.array = cuOutputArray;
    cudaSurfaceObject_t outputSurfObj = 0;
    cudaCreateSurfaceObject(&outputSurfObj, &resDesc);

    // Invoke kernel
    dim3 threadsperBlock(16, 16);
    dim3 numBlocks((width + threadsperBlock.x - 1) / threadsperBlock.x,
                    (height + threadsperBlock.y - 1) / threadsperBlock.y);
    copyKernel<<<numBlocks, threadsperBlock>>>(inputSurfObj, outputSurfObj, width,
                                                height);

    // Copy data from device back to host
    cudaMemcpy2DFromArray(h_data, spitch, cuOutputArray, 0, 0,
                            4 * width * sizeof(unsigned char), height,
                            cudaMemcpyDeviceToHost);

    // Destroy surface objects
    cudaDestroySurfaceObject(inputSurfObj);
    cudaDestroySurfaceObject(outputSurfObj);

    // Free device memory
    cudaFreeArray(cuInputArray);
    cudaFreeArray(cuOutputArray);

    // Free host memory
    free(h_data);

  return 0;
}
```


##### 3.2.14.2.2. Cubemap Surfaces
> 使用 surfCubemapread() and surfCubemapwrite() （surfCubemapread 和 surfCubemapwrite）作为二维分层曲面来访问立方体贴图面，即使用表示面的整数索引和两个浮点纹理坐标来寻址与该面对应的层中的纹素。面的顺序如表 3 所示。


##### 3.2.14.2.3. Cubemap Layered Surfaces

> 使用 surfCubemapLayeredread() and surfCubemapLayeredwrite() （surfCubemapLayeredread（） 和 surfCubemapLayeredwrite（）） 作为二维分层表面来访问立方体贴图分层曲面，即使用表示其中一个立方体贴图面的整数索引和两个浮点纹理坐标来寻址与该面对应的层内的纹素。面的排序如表 3 所示，因此索引 （（2 * 6） + 3） 例如，访问第三个立方体贴图的第四张面。



#### 3.2.14.3. CUDA Arrays

> CUDA 数组是针对纹理获取进行了优化的不透明内存布局。它们是一维、二维或三维的，由元素组成，每个元素都有 1、2 或 4 个组件，这些组件可以是有符号或无符号的 8 位、16 位或 32 位整数、16 位浮点数或 32 位浮点数。CUDA 数组只能由内核通过纹理提取（如纹理内存中所述）或表面读取和写入（如表面内存中所述）进行访问。


#### 3.2.14.4. Read/Write Coherency
> 纹理和表面内存被缓存（请参阅设备内存访问），并且在同一内核调用中，缓存在全局内存写入和表面内存写入方面不保持一致，因此任何纹理提取或表面读取到已写入的地址，通过全局写入或表面写入在同一内核调用中返回未定义的数据。换言之，仅当该内存位置已被先前的内核调用或内存副本更新时，线程才能安全地读取该纹理或表面内存位置，但如果它之前已由同一线程或来自同一内核调用的另一个线程更新，则无法读取







