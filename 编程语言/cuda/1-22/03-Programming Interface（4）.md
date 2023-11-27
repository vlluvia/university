
#### 3.2.8.7.4. CUDA User Objects
> CUDA 用户对象可用于帮助管理 CUDA 中异步工作使用的资源的生命周期，此功能对于 CUDA 图形和流捕获非常有用。  
> 各种资源管理方案与 CUDA graph 不兼容。例如，考虑基于事件的池或同步创建、异步销毁方案。

> 当引用关联到 CUDA 图时，CUDA 将自动管理图操作。克隆保留 cudaGraph_t 源 cudaGraph_t 所拥有的每个引用的副本，具有相同的多重性。实例化 cudaGraphExec_t 保留源 cudaGraph_t 中每个引用的副本。当 a cudaGraphExec_t 在未同步的情况下被销毁时，引用将保留，直到执行完成。

``` 
cudaGraph_t graph;  // Preexisting graph

Object *object = new Object;  // C++ object with possibly nontrivial destructor
cudaUserObject_t cuObject;
cudaUserObjectCreate(
    &cuObject,
    object,  // Here we use a CUDA-provided template wrapper for this API,
             // which supplies a callback to delete the C++ object pointer
    1,  // Initial refcount
    cudaUserObjectNoDestructorSync  // Acknowledge that the callback cannot be
                                    // waited on via CUDA
);
cudaGraphRetainUserObject(
    graph,
    cuObject,
    1,  // Number of references
    cudaGraphUserObjectMove  // Transfer a reference owned by the caller (do
                             // not modify the total reference count)
);
// No more references owned by this thread; no need to call release API
cudaGraphExec_t graphExec;
cudaGraphInstantiate(&graphExec, graph, nullptr, nullptr, 0);  // Will retain a
                                                               // new reference
cudaGraphDestroy(graph);  // graphExec still owns a reference
cudaGraphLaunch(graphExec, 0);  // Async launch has access to the user objects
cudaGraphExecDestroy(graphExec);  // Launch is not synchronized; the release
                                  // will be deferred if needed
cudaStreamSynchronize(0);  // After the launch is synchronized, the remaining
                           // reference is released and the destructor will
                           // execute. Note this happens asynchronously.
// If the destructor callback had signaled a synchronization object, it would
// be safe to wait on it at this point.
```
> 子图节点中的图所拥有的引用与子图相关联，而不是与父图相关联。如果更新或删除子图，则引用会相应更改。如果使用 cudaGraphExecUpdate 或 更新可执行图或 cudaGraphExecChildGraphNodeSetParams 子图，则会克隆新源图中的引用，并替换目标图中的引用。无论哪种情况，如果以前的启动未同步，则将保留将释放的任何引用，直到启动完成执行。  
> 目前没有通过 CUDA API 等待用户对象析构函数的机制。用户可以从析构函数代码手动向同步对象发出信号。此外，从析构函数调用 CUDA API 是不合法的，类似于对 cudaLaunchHostFunc 的限制。这是为了避免阻塞 CUDA 内部共享线程并阻止前进。如果依赖项是单向的，并且执行调用的线程无法阻止 CUDA 工作的向前进度，则向另一个线程发出信号以执行 API 调用是合法的。  


##### 3.2.8.7.5. Updating Instantiated Graphs
> 使用图形提交工作分为三个不同的阶段： definition, instantiation, and execution。在工作流没有变化的情况下，定义和实例化的开销可以在多次执行中分摊，并且图形比流具有明显的优势。  
> 图形是工作流的快照，包括内核、参数和依赖项，以便尽可能快速有效地重放它。在工作流更改的情况下，图形将过期，必须进行修改。对图形结构（如拓扑或节点类型）的重大更改将需要重新实例化源图形，因为必须重新应用各种与拓扑相关的优化技术。  
> 重复实例化的成本会降低图形执行的整体性能优势，但只有节点参数（如内核参数和 cudaMemcpy 地址）会发生变化，而图形拓扑保持不变，这是很常见的。对于这种情况，CUDA 提供了一种称为“图形更新”的轻量级机制，它允许就地修改某些节点参数，而无需重新构建整个图形。这比重新实例化要高效得多。  
> 更新将在下次启动图形时生效，因此它们不会影响以前的图形启动，即使它们在更新时正在运行。图形可以重复更新和重新启动，因此可以在流上排队进行多个更新/启动。    
> CUDA 提供了两种更新实例化图参数的机制，全图更新和单节点更新。整个图形更新允许用户提供拓扑上相同的 cudaGraph_t 对象，其节点包含更新的参数。单个节点更新允许用户显式更新单个节点的参数。当正在更新大量节点时，或者当调用方不知道图形拓扑时（即，由库调用的流捕获生成的图形），使用更新 cudaGraph_t 更方便。当更改数量较少且用户具有需要更新的节点的句柄时，首选使用单个节点更新。单个节点更新跳过了对未更改节点的拓扑检查和比较，因此在许多情况下可以更有效。


###### 3.2.8.7.5.1. Graph Update Limitations
* Kernel nodes
  * 函数的所属上下文无法更改。
  * 函数原本不使用 CUDA 动态并行的节点无法更新为使用 CUDA 动态并行的函数。

* cudaMemset and cudaMemcpy nodes
  * operand(s) 分配/映射到的 CUDA devices 无法更改。
  * 源/目标内存必须从与原始源/目标内存相同的上下文中分配。
  * 只能更改 1D cudaMemset / cudaMemcpy 节点。

* 其他 memcpy 节点限制
  * 不支持更改源或目标内存类型（即 cudaPitchedPtr 、 cudaArray_t 等）或传输类型（即 cudaMemcpyKind ）。

* 外部信号量等待节点和记录节点
  * 不支持更改信号量的数量
  
* 条件节点
  * 图形之间的句柄创建和分配顺序必须匹配
  * 不支持更改节点参数（即条件、节点上下文中的图形数量等）
  * 更改条件主体图中节点的参数受上述规则的约束

* 对主机节点、事件记录节点或事件等待节点的更新没有限制。

###### 3.2.8.7.5.2. Whole Graph Update
> cudaGraphExecUpdate() 允许使用拓扑相同图（“更新”图）中的参数更新实例化图（“原始图”）。更新图的拓扑结构必须与用于实例化 cudaGraphExec_t .此外，指定依赖项的顺序必须匹配。最后，CUDA 需要一致地对接收器节点（没有依赖关系的节点）进行排序。CUDA 依靠特定 API 调用的顺序来实现一致的 sink 节点排序。  
> 更明确地说，遵循以下规则将导致 cudaGraphExecUpdate() 确定性地将原始图和更新图中的节点配对
> 1. 对于任何捕获流，对该流执行操作的 API 调用必须按相同的顺序进行，包括事件等待和其他与节点创建不直接对应的 API 调用。
> 2. 直接操作给定图节点的传入边缘（包括捕获的流 API、节点添加 API 和边缘添加/删除 API）的 API 调用必须按相同的顺序进行。此外，当在数组中指定这些 API 的依赖项时，在这些数组中指定依赖项的顺序必须匹配。
> 3. 接收器节点的顺序必须一致。接收器节点是调用时 cudaGraphExecUpdate() 最终图形中没有依赖节点/传出边缘的节点。以下操作会影响接收器节点排序（如果存在），并且必须（作为组合集）以相同的顺序进行
>    1. Node add APIs resulting in a sink node. 
>    2. Edge removal resulting in a node becoming a sink node. 
>    3. cudaStreamUpdateCaptureDependencies(), if it removes a sink node from a capturing stream’s dependency set. 
>    4. cudaStreamEndCapture()

``` 
cudaGraphExec_t graphExec = NULL;

for (int i = 0; i < 10; i++) {
    cudaGraph_t graph;
    cudaGraphExecUpdateResult updateResult;
    cudaGraphNode_t errorNode;

    // In this example we use stream capture to create the graph.
    // You can also use the Graph API to produce a graph.
    cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);

    // Call a user-defined, stream based workload, for example
    do_cuda_work(stream);

    cudaStreamEndCapture(stream, &graph);

    // If we've already instantiated the graph, try to update it directly
    // and avoid the instantiation overhead
    if (graphExec != NULL) {
        // If the graph fails to update, errorNode will be set to the
        // node causing the failure and updateResult will be set to a
        // reason code.
        cudaGraphExecUpdate(graphExec, graph, &errorNode, &updateResult);
    }

    // Instantiate during the first iteration or whenever the update
    // fails for any reason
    if (graphExec == NULL || updateResult != cudaGraphExecUpdateSuccess) {

        // If a previous update failed, destroy the cudaGraphExec_t
        // before re-instantiating it
        if (graphExec != NULL) {
            cudaGraphExecDestroy(graphExec);
        }
        // Instantiate graphExec from graph. The error node and
        // error message parameters are unused here.
        cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);
    }

    cudaGraphDestroy(graph);
    cudaGraphLaunch(graphExec, stream);
    cudaStreamSynchronize(stream);
}
```
> 典型的工作流是使用流捕获或图形 API 创建初始 cudaGraph_t 。然后实例 cudaGraph_t 化并正常启动。初始启动后，将使用与初始图形相同的方法创建一个新 cudaGraph_t 图形，并 cudaGraphExecUpdate() 调用该图形。如果图形更新成功（由上述示例中的 updateResult 参数指示），则启动更新 cudaGraphExec_t 。如果更新因任何原因失败，则调用 cudaGraphExecDestroy() and cudaGraphInstantiate() 以销毁原始 cudaGraphExec_t 更新并实例化新更新。  
> 也可以直接更新 cudaGraph_t 节点（即 Using cudaGraphKernelNodeSetParams() ），然后更新 cudaGraphExec_t ，但是使用下一节中介绍的显式节点更新 API 会更有效。

###### 3.2.8.7.5.3. Individual node update
> 实例化的图节点参数可以直接更新。这消除了实例化的开销以及创建新的 cudaGraph_t .如果需要更新的节点数相对于图中的节点总数较小，则最好单独更新节点。以下方法可用于更新 cudaGraphExec_t 节点：
> 1. cudaGraphExecKernelNodeSetParams()
> 2. cudaGraphExecMemcpyNodeSetParams()
> 3. cudaGraphExecMemsetNodeSetParams()
> 4. cudaGraphExecHostNodeSetParams()
> 5. cudaGraphExecChildGraphNodeSetParams()
> 6. cudaGraphExecEventRecordNodeSetEvent()
> 7. cudaGraphExecEventWaitNodeSetEvent()
> 8. cudaGraphExecExternalSemaphoresSignalNodeSetParams()
> 9. cudaGraphExecExternalSemaphoresWaitNodeSetParams()


###### 3.2.8.7.5.4. Individual node enable
> 实例化图中的内核、memset 和 memcpy 节点可以使用 cudaGraphNodeSetEnabled（） API 启用或禁用。这允许创建一个图表，其中包含所需功能的超集，可以针对每次启动进行自定义。可以使用 cudaGraphNodeGetEnabled（） API 查询节点的启用状态。  
> 禁用的节点在功能上等同于空节点，直到它被重新启用。节点参数不受启用/禁用节点的影响。启用状态不受单个节点更新或使用 cudaGraphExecUpdate（） 进行整个图形更新的影响。节点被禁用时的参数更新将在节点重新启用时生效。  
> 以下方法可用于启用/禁用 cudaGraphExec_t 节点，以及查询其状态：
> 1. cudaGraphNodeSetEnabled()
> 2. cudaGraphNodeGetEnabled()

---
##### 3.2.8.7.6. Using Graph APIs
> cudaGraph_t 对象不是线程安全的。用户有责任确保多个线程不会同时访问同一个 cudaGraph_t 线程  
> A cudaGraphExec_t 不能与自身同时运行。在之前启动同一可执行图之后，将有序启动。 cudaGraphExec_t  
> 图形执行在流中完成，以便与其他异步工作一起排序。但是，该流仅用于排序;它不会约束图的内部并行度，也不会影响图节点的执行位置。

---
##### 3.2.8.7.7. Device Graph Launch
> 有许多工作流需要在运行时做出与数据相关的决策，并根据这些决策执行不同的操作。用户可能更愿意在设备上执行此决策过程，而不是将此决策过程卸载到主机，这可能需要从设备往返。为此，CUDA 提供了一种从设备启动图形的机制  
> 可以从设备启动的图形将称为device graphs（设备图形），而无法从设备启动的图形将称为host graphs（主机图形）。  
> 设备图可以从主机和设备启动，而主机图只能从主机启动。与主机启动不同，在运行上一次启动设备图时从设备启动设备图将导致错误，返回 cudaErrorInvalidValue ;因此，不能同时从设备启动两次设备图。同时从主机和设备启动设备图将导致未定义的行为。

###### 3.2.8.7.7.1. Device Graph Creation
>  为了从设备启动图形，必须显式实例化该图形以启动设备。这是通过将 cudaGraphInstantiateFlagDeviceLaunch 标志传递给呼叫来实现 cudaGraphInstantiate() 的。与主机图一样，设备图结构在实例化时是固定的，如果不重新实例化就无法更新，并且实例化只能在主机上执行。为了使图形能够实例化以进行设备启动，它必须符合各种要求。

* 3.2.8.7.7.1.1. Device Graph Requirements
> General requirements
> 1. The graph’s nodes must all reside on a single device
> 2. The graph can only contain kernel nodes, memcpy nodes, memset nodes, and child graph nodes

> Kernel nodes
> 1. Use of CUDA Dynamic Parallelism by kernels in the graph is not permitted
> 2. Cooperative launches are permitted so long as MPS is not in use.

> Memcpy nodes
> 1. 仅允许涉及设备内存和/或固定设备映射主机内存的副本
> 2. 不允许涉及 CUDA 数组的副本。
> 3. 在实例化时，这两个操作数都必须可从当前设备访问。请注意，复制操作将从图形所在的设备执行，即使它以另一台设备上的内存为目标也是如此。


* 3.2.8.7.7.1.2. Device Graph Upload
> 为了在设备上启动图形，必须首先将其上传到设备以填充必要的设备资源。这可以通过以下两种方式之一实现。 
> 1. 首先，可以通过 显式上传图形， cudaGraphUpload() 也可以通过 请求上传作为实例化的一部分 cudaGraphInstantiateWithParams() 。
> 2. 或者，可以首先从主机启动图形，主机将在启动过程中隐式执行此上传步骤。

``` 
// Explicit upload after instantiation
cudaGraphInstantiate(&deviceGraphExec1, deviceGraph1, cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphUpload(deviceGraphExec1, stream);

// Explicit upload as part of instantiation
cudaGraphInstantiateParams instantiateParams = {0};
instantiateParams.flags = cudaGraphInstantiateFlagDeviceLaunch | cudaGraphInstantiateFlagUpload;
instantiateParams.uploadStream = stream;
cudaGraphInstantiateWithParams(&deviceGraphExec2, deviceGraph2, &instantiateParams);

// Implicit upload via host launch
cudaGraphInstantiate(&deviceGraphExec3, deviceGraph3, cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphLaunch(deviceGraphExec3, stream);
```
* 3.2.8.7.7.1.3. Device Graph Update
> 设备图只能从主机更新，并且必须在可执行图更新时重新上传到设备，才能使更改生效。这可以使用上一节中概述的相同方法实现。与主机图不同，在应用更新时从设备启动设备图将导致未定义的行为。




