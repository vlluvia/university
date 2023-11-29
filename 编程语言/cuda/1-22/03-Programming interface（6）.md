
### 3.2.15. Graphics Interoperability

> OpenGL 和 Direct3D 中的某些资源可能会映射到 CUDA 的地址空间中，以使 CUDA 能够读取 OpenGL 或 Direct3D 写入的数据，或者使 CUDA 能够写入数据以供 OpenGL 或 Direct3D 使用。  
> 必须先将资源注册到 CUDA，然后才能使用 OpenGL 互操作性和 Direct3D 互操作性中提到的函数进行映射。这些函数返回指向 类型的 struct cudaGraphicsResource CUDA 图形资源的指针。注册资源可能会产生高开销，因此通常每个资源只调用一次。使用 cudaGraphicsUnregisterResource() 注销 CUDA 图形资源。每个打算使用该资源的 CUDA 上下文都需要单独注册它。  
> 将资源注册到 CUDA 后，可以使用 cudaGraphicsMapResources() 和 cudaGraphicsUnmapResources() 根据需要多次映射和取消映射。 cudaGraphicsResourceSetMapFlags() 可以调用以指定 CUDA 驱动程序可用于优化资源管理的使用提示（只写、只读）。  
> 内核可以使用缓冲区和 cudaGraphicsSubResourceGetMappedArray() CUDA 数组返回 cudaGraphicsResourceGetMappedPointer() 的设备内存地址读取或写入映射的资源。    
> 在映射资源时通过 OpenGL、Direct3D 或其他 CUDA 上下文访问资源会产生未定义的结果。OpenGL 互操作性和 Direct3D 互操作性提供了每个图形 API 和一些代码示例的详细信息。SLI 互操作性提供了系统处于 SLI 模式时的细节。



#### 3.2.15.1. OpenGL Interoperability


#### 3.2.15.2. Direct3D Interoperability


#### 3.2.15.3. SLI Interoperability


---
### 3.2.16. External Resource Interoperability
> 外部资源互操作性允许 CUDA 导入由其他 API 显式导出的某些资源。这些对象通常由其他 API 使用操作系统本机句柄（如 Linux 上的文件描述符或 Windows 上的 NT 句柄）导出。它们也可以使用其他统一接口（例如NVIDIA软件通信接口）导出。可以导入的资源有两种类型：内存对象和同步对象。
#### 3.2.16.1. Vulkan Interoperability


#### 3.2.16.2. OpenGL Interoperability

#### 3.2.16.3. Direct3D 12 Interoperability

#### 3.2.16.4. Direct3D 11 Interoperability

#### 3.2.16.5. NVIDIA Software Communication Interface Interoperability (NVSCI)


----

## 3.3. Versioning and Compatibility
> 开发人员在开发 CUDA 应用程序时应关注两个版本号：描述计算设备的一般规格和功能的计算能力（请参阅计算能力）和描述驱动程序 API 和运行时支持的功能的 CUDA 驱动程序 API 版本。   
> 驱动程序 API 的版本在驱动程序头文件中定义为 CUDA_VERSION 。它允许开发人员检查他们的应用程序是否需要比当前安装的设备驱动程序更新的设备驱动程序。这一点很重要，因为驱动程序 API 是向后兼容的，这意味着针对特定版本的驱动程序 API 编译的应用程序、插件和库（包括 CUDA 运行时）将继续在后续设备驱动程序版本上运行，如图 12 所示。驱动程序 API 不向前兼容，这意味着针对特定版本的驱动程序 API 编译的应用程序、插件和库（包括 CUDA 运行时）将无法在以前版本的设备驱动程序上运行。   
> 需要注意的是，支持的版本的混合和匹配存在一些限制:
> 1. 由于一个系统上一次只能安装一个版本的 CUDA 驱动程序，因此安装的驱动程序必须与构建必须在该系统上运行的任何应用程序、插件或库所依据的最高驱动程序 API 版本相同或更高。
> 2. 应用程序使用的所有插件和库都必须使用相同版本的 CUDA 运行时，除非它们静态链接到运行时，在这种情况下，运行时的多个版本可以在同一进程空间中共存。请注意，如果 nvcc 用于链接应用程序，则默认使用 CUDA Runtime 库的静态版本，并且所有 CUDA Toolkit 库都静态链接到 CUDA Runtime。
> 3. 应用程序使用的所有插件和库必须使用使用运行时的任何库（例如 cuFFT、cuBLAS 等）的相同版本，除非静态链接到这些库
> 

![img.png](3-3_1.png)


---

## 3.4. Compute Modes
> 在运行 Windows Server 2008 及更高版本或 Linux 的 Tesla 解决方案上，可以使用 NVIDIA 的系统管理接口 （nvidia-smi） 将系统中的任何设备设置为以下三种模式之一，该接口是作为驱动程序的一部分分发的工具：
> 1. 默认计算模式：多个主机线程可以同时使用设备（在使用运行时 API 时通过调用 cudaSetDevice() 此设备，或者在使用驱动程序 API 时使当前上下文与设备关联）。
> 2. 独占进程计算模式：系统中所有进程只能在设备上创建一个 CUDA 上下文。在创建该上下文的进程中，上下文可以是任意数量的线程的当前线程。
> 3. 禁止的计算模式：无法在设备上创建 CUDA 上下文。

> 这尤其意味着，如果设备 0 处于禁止模式或独占进程模式并由另一个进程使用，则使用运行时 API 而不显式调用 cudaSetDevice() 的主机线程可能与设备 0 以外的设备相关联。 cudaSetValidDevices() 可用于从设备优先级列表中设置设备。   
> 另请注意，对于采用 Pascal 架构的设备（主要修订号为 6 和更高版本的计算能力），存在对计算抢占的支持。这允许计算任务在指令级粒度上被抢占，而不是像以前的 Maxwell 和 Kepler GPU 架构那样以线程块粒度为先行，这样做的好处是可以防止具有长时间运行内核的应用程序独占系统或超时。但是，将产生与计算抢占相关的上下文切换开销，计算抢占会在支持计算抢占的设备上自动启用。具有该属性的单个属性 cudaDevAttrComputePreemptionSupported 查询函数 cudaDeviceGetAttribute() 可用于确定正在使用的设备是否支持计算抢占。希望避免与不同进程相关的上下文切换开销的用户可以通过选择独占进程模式来确保 GPU 上只有一个进程处于活动状态。


## 3.5. Mode Switches
> 具有显示输出的 GPU 将一些 DRAM 内存专用于所谓的主表面，用于刷新用户查看其输出的显示设备。当用户通过更改显示器的分辨率或位深度（使用 NVIDIA 控制面板或 Windows 上的显示控制面板）来启动显示器的模式切换时，主表面所需的内存量会发生变化。例如，如果用户将显示分辨率从 1280x1024x32 位更改为 1600x1200x32 位，则系统必须将 7.68 MB 专用于主图面，而不是 5.24 MB。（在启用抗锯齿的情况下运行的全屏图形应用程序可能需要为主图面提供更多的显示内存。在 Windows 上，可能启动显示模式切换的其他事件包括启动全屏 DirectX 应用程序、按 Alt+Tab 以从全屏 DirectX 应用程序切换任务，或按 Ctrl+Alt+Del 锁定计算机。  
> 如果模式开关增加了主表面所需的内存量，则系统可能不得不蚕食专用于 CUDA 应用程序的内存分配。因此，模式切换会导致对 CUDA 运行时的任何调用失败并返回无效上下文错误。


---
## 3.6. Tesla Compute Cluster Mode for Windows
> 使用 NVIDIA 的系统管理接口 （nvidia-smi），可以将 Tesla 和 Quadro 系列设备的 Windows 设备驱动程序置于 TCC（Tesla 计算集群）模式  
> TCC 模式删除了对任何图形功能的支持。




