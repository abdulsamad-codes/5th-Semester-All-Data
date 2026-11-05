# Comprehensive 20-Minute Pre-Exam Master Notes: Parallel & Distributed Computing (Lectures 1–5)

---

## 1. Lecture 1: Foundations of Parallel & Distributed Computing

### 1.1 Core Concepts & System Architecture
* **Computing Definition**: The process of using computer technology to complete goal-oriented tasks (including hardware/software design, structuring, and information management).
* **Serial vs. Parallel Computing**:
  * **Serial Computing**: Executes a single task sequentially on a single processor core. Instructions execute one after another.
  * **Parallel Computing**: The simultaneous execution of a single task (split into smaller independent parts via *divide-and-conquer*) across multiple physical processors or cores to produce faster results.
* **Basic Hardware Elements**:
  * **CPU Architecture**: Contains the **Control Unit (CU)** (directs instruction flow) and **Arithmetic Logic Unit (ALU)** (performs mathematical/logical calculations).
  * **Buses**: System channels connecting hardware—**Control Bus** (signals), **Data Bus** (payloads), and **Address Bus** (memory pointers). An $n$-bit address bus yields an addressable space of $2^n$ unique locations.
  * **Main Memory (RAM)** & **Cache**: Cache is small, high-speed SRAM located on or near the CPU that holds frequently accessed data/instructions to bridge the speed gap between CPU and RAM.
  * **NUMA (Non-Uniform Memory Access)**: A memory architecture where access time depends on memory location relative to the processor (local RAM access is fast; remote RAM access across interconnects introduces latency).

### 1.2 Motivations & Scope
* **Why Use Parallel Computing?**:
  1. **Real-World Modeling**: Natural phenomena (weather patterns, fluid dynamics, economic markets, gene folding) involve billions of concurrent events that serial systems cannot simulate efficiently.
  2. **Save Time & Money**: Throwing more compute resources at a problem reduces time-to-completion and increases throughput using cost-effective commodity clusters.
  3. **Solve Large/Complex Problems**: Massive datasets (e.g., global web search, transaction processing) exceed the memory and processing bounds of single-processor systems.
  4. **Hardware Reality**: Modern hardware is intrinsically parallel (multicore chips). Running serial software wastes potential hardware processing power.
* **Application Domains**:
  * *Engineering*: Internal combustion engine modeling, micro/nano-scale systems.
  * *Scientific*: Protein characterization, galaxy evolution in astrophysics, climate/flood forecasting.
  * *Commercial*: Data mining, financial risk analysis, enterprise web and mail servers.

### 1.3 System Limitations
* **Memory Access Bottlenecks**: Shared memory contention occurs when multiple cores attempt simultaneous access to RAM over a shared bus. NUMA systems introduce inconsistent access latencies.
* **Communication Overhead**: Processors spend clock cycles exchanging data and synchronizing across interconnects rather than computing, reducing overall speedup.
* **Data and Control Dependencies**:
  * *Data Dependency*: A task cannot execute until the output of a preceding task is available.
  * *Control Dependency*: Conditional branches (`if-else`) create non-deterministic execution paths, restricting parallelization.

### 1.4 Data Parallelism vs. Task Parallelism
* **Data Parallelism**: The dataset is partitioned into sub-chunks, and the **same operation** is performed on each chunk concurrently across different cores (*Same Operation, Different Data*). 
  * *Examples*: Image filtering (applying a brightness filter to different pixel blocks), vector/matrix additions.
* **Task Parallelism**: The overall algorithm is divided into distinct, independent functional tasks executed concurrently on different cores (*Different Operations, Same/Different Data*).
  * *Examples*: Game engines (Core 1: Physics, Core 2: AI, Core 3: Audio, Core 4: Graphics rendering).

| Feature | Data Parallelism | Task Parallelism |
| :--- | :--- | :--- |
| **Partitioning Focus** | Data elements (arrays, matrices, images). | Computational functions/tasks. |
| **Operation Type** | **Same** operation across multiple cores. | **Different** operations across multiple cores. |
| **Scalability** | Scales easily with dataset size. | Bounded by the number of distinct tasks available. |

### 1.5 Distributed Systems Architecture
* **Definition**: A collection of independent, autonomous computers connected via a network that coordinate their actions **only by passing explicit messages**. Each node maintains its own private address space.
* **Justification for Distributed Computing**:
  1. *Historical*: Connecting existing independent office workstations to share files/data.
  2. *Functional*: Sharing expensive specialized hardware or software services over the network without duplicating installations.
  3. *Economical*: Assembling low-cost commodity computers into a cluster provides aggregate computing power rivaling expensive mainframes at a fraction of the cost.
  4. *Scalability*: Adding additional nodes expands system capacity flexibly without taking the whole system offline.
  5. *Reliability/Fault Tolerance*: Replicating data across networked nodes ensures system availability even when individual nodes fail.

| Feature | Parallel Computing | Distributed Computing |
| :--- | :--- | :--- |
| **System Architecture** | Single physical system with multiple cores/processors. | Multiple independent networked computers (nodes). |
| **Memory Model** | Shared memory space (or high-speed local bus). | Distributed memory only (private RAM per node). |
| **Communication** | Fast hardware bus or shared RAM access. | Network message passing (TCP/IP, Ethernet, InfiniBand). |
| **Scalability** | Limited by single-system socket/bus limits. | Highly scalable (can add thousands of independent nodes). |
| **Fault Tolerance** | Low (single system hardware failure halts execution). | High (built-in redundancy; nodes fail independently). |
| **Programming Model** | OpenMP, Shared Memory Threads, CUDA. | MPI (Message Passing Interface), MapReduce, Hadoop. |

### 1.6 Scalability Dimensions & Scaling Models
* **Scalability Definition**: The property of a system to effectively handle increasing workloads by adding hardware resources.
* **5 Dimensions of Scalability**:
  1. *Physical/Load Scalability*: Ability to expand system size by adding/removing users and compute nodes.
  2. *Functional Scalability*: Ability to add new features without disrupting ongoing activities.
  3. *Geographic Scalability*: Ability to maintain performance across wide geographic distances.
  4. *Generation Scalability*: Ability to integrate newer hardware generations into existing systems seamlessly.
  5. *Heterogeneous Scalability*: Ability to integrate components from different hardware/software vendors.
* **Horizontal vs. Vertical Scaling**:
  * **Horizontal Scaling (Scale Out)**: Adding more independent physical machine nodes to a cluster network.
  * **Vertical Scaling (Scale Up)**: Adding more resources (CPUs, RAM, storage) into a single existing server node.

### 1.7 Performance Metrics, Speedup & Amdahl's Law
* **Parallel Speedup ($S$)**: Measure of performance gain from parallelization:
  $$S = \frac{T_{\text{serial}}}{T_{\text{parallel}}}$$
* **Amdahl's Law**: Calculates the theoretical speedup limit for a fixed workload given a parallelizable fraction $P$ ($0 \le P \le 1$) and $N$ processors:
  $$S = \frac{1}{(1 - P) + \frac{P}{N}}$$
* **Theoretical Maximum Speedup ($S_{\max}$)**: As the number of processors approaches infinity ($N \to \infty$), $\frac{P}{N} \to 0$:
  $$S_{\max} = \frac{1}{1 - P}$$
  *Key Exam Insight*: The inherently serial fraction $(1 - P)$ creates an unyielding performance ceiling regardless of how many cores are deployed.

#### Worked Numerical Calculations:
1. *Scenario 1*: If $80\%$ of a program is parallelizable ($P = 0.8$, $1 - P = 0.2$):
   * On 4 cores ($N = 4$): $S = \frac{1}{0.2 + \frac{0.8}{4}} = \frac{1}{0.2 + 0.2} = \frac{1}{0.4} = \mathbf{2.5\times}$
   * Maximum Speedup ($N \to \infty$): $S_{\max} = \frac{1}{1 - 0.8} = \frac{1}{0.2} = \mathbf{5\times}$
2. *Scenario 2*: If $90\%$ of a program is parallelizable ($P = 0.9$, $1 - P = 0.1$):
   * Maximum Speedup ($N \to \infty$): $S_{\max} = \frac{1}{1 - 0.9} = \frac{1}{0.1} = \mathbf{10\times}$

### 1.8 Physical Scaling Barriers
* **Power Wall**: Increasing single-core clock frequencies requires higher voltages, causing dynamic power dissipation to grow exponentially ($P \propto V^2 f$).
* **Thermal Wall**: The extreme heat generated by high-frequency single cores exceeds the physical dissipation capacity of air-cooling systems, causing structural instability.
* **Multicore Shift**: Because single-core clock speeds hit the Power/Thermal Walls, hardware vendors shifted to placing multiple energy-efficient cores on a single chip to boost performance through parallelism.

---

## 2. Lecture 2: Parallel Hardware & CPU Architectures

### 2.1 Von Neumann Architecture & The Bottleneck
* **Stored Program Concept**: Both instruction code and operational data are stored in the same physical memory space (RAM).
* **Sequential Execution**: Instructions are fetched, decoded, and executed one by one sequentially via a central processing unit.
* **Von Neumann Bottleneck**: The physical data bus shared between CPU and RAM restricts throughput because instructions and data cannot be fetched simultaneously, limiting overall system speed.

### 2.2 The 5 Primary CPU Architecture Types
Hardware designers evolved processor microarchitectures along 5 main trajectories:

1. **Scalar Architecture**:
   * Executes **one instruction per clock cycle on a single data element**.
   * Simple hardware design featuring a single processing pipeline.
   * *Example*: Early microprocessors (Intel 8086).
2. **Vector Architecture**:
   * Operates on **multiple data elements simultaneously using a single instruction**.
   * Designed specifically for data-parallel matrix/array tasks in scientific computing. Uses specialized **vector registers**.
   * *Examples*: Cray-1 supercomputer, modern GPUs (Graphics Processing Units), SIMD extensions (AVX/NEON).
3. **Pipelined Architecture**:
   * Divides instruction execution into sequential sub-stages (Fetch `IF`, Decode `ID`, Execute `EX`, Write-Back `WB`), overlapping execution like an assembly line.
   * Increases overall **instruction throughput** (does not reduce latency of a single instruction).
   * *Examples*: MIPS R2000, ARM Cortex-M.
4. **Superscalar Architecture**:
   * Executes **multiple independent instructions per clock cycle** by replicating internal execution units (multiple ALUs, load/store units).
   * Relies on **Instruction-Level Parallelism (ILP)** and **dynamic hardware scheduling at runtime**.
   * *Examples*: Intel Pentium, ARM Cortex-A series.
5. **VLIW (Very Long Instruction Word) Architecture**:
   * The compiler packs multiple independent operations into a single wide instruction word (e.g., 128-bit) that triggers multiple execution units simultaneously.
   * Simplifies hardware logic by shifting scheduling responsibility entirely to the **compiler at compile-time**.
   * *Examples*: Intel Itanium, digital signal processors (DSPs).

### 2.3 Instruction-Level Parallelism (ILP) & Scheduling
* **ILP Definition**: Hardware techniques that allow a single processor core to execute multiple instructions or functional units simultaneously.
* **Static vs. Dynamic Multiple Issue**:
  * **Static Multiple Issue**: Instruction scheduling decisions are made by the compiler at compile-time (e.g., VLIW).
  * **Dynamic Multiple Issue**: Instruction scheduling and hardware hazard detection are managed dynamically by the CPU control logic at runtime (e.g., Superscalar).

### 2.4 Speculation & Branch Recovery
* **Speculation**: To keep multiple execution pipelines full, the CPU or compiler predicts the outcome of conditional instructions (such as `if-else` branches) and speculatively executes instructions ahead of time based on that prediction.
* **Execution Flow**:
  1. *Guessing Phase*: The CPU guesses branch outcome (e.g., assuming $z > 0$ in `if (z > 0) w = x; else w = y;`) and pre-executes $w = x$.
  2. *Verification*: Once the branch condition completes calculation in the ALU, the guess is checked.
  3. *Recovery*: If the speculation was correct, performance increases. If **incorrect (mis-speculation)**, the CPU must discard all speculated results, roll back processor registers to the pre-branch state, and recalculate the correct branch path ($w = y$).

### 2.5 Flynn's Taxonomy (1966)
Michael J. Flynn classified computer architectures based on the number of concurrent **Instruction Streams** and **Data Streams**:

| Stream Classification | Single Data (SD) | Multiple Data (MD) |
| :--- | :--- | :--- |
| **Single Instruction (SI)** | **1. SISD** (Standard Uniprocessor) | **2. SIMD** (Vector / GPU / Array Processors) |
| **Multiple Instruction (MI)** | **3. MISD** (Fault-Tolerant Redundant Systems) | **4. MIMD** (Multicore CPUs / Distributed Clusters) |

1. **SISD (Single Instruction Stream, Single Data Stream)**: Classic single-core uniprocessor (Von Neumann / Scalar model).
2. **SIMD (Single Instruction Stream, Multiple Data Streams)**: A single instruction stream controls multiple execution units acting concurrently on distinct data elements (Vector processors, GPUs).
3. **MISD (Multiple Instruction Streams, Single Data Stream)**: Multiple independent instruction streams operate on a single shared data stream. Rare; used primarily in fault-tolerant redundant systems (e.g., space shuttle flight controls).
4. **MIMD (Multiple Instruction Streams, Multiple Data Streams)**: Multiple autonomous processors execute different instruction streams on different data streams concurrently (Multicore CPUs, distributed clusters).

### 2.6 Architecture Comparison Matrix

| Architecture | Parallelism Level | Who Handles Scheduling? | Hardware Complexity | Real-World Example |
| :--- | :--- | :--- | :--- | :--- |
| **Scalar** | 1 instruction / cycle | Hardware (sequential) | Low (Single pipeline) | Intel 8086 |
| **Vector** | 1 instruction = many data ops | Hardware (vector units) | Medium (Vector registers) | Cray-1, Modern GPUs |
| **Pipelined** | Overlapped stages | Hardware (stage registers) | Medium (Pipeline stages) | MIPS R2000, ARM Cortex-M |
| **Superscalar** | Multiple instructions / cycle | Hardware (**Dynamic at runtime**) | High (Multiple ALUs + schedulers) | Intel Pentium, ARM Cortex-A |
| **VLIW** | Multiple instructions / cycle | Compiler (**Static at compile-time**) | Medium (Compiler dependency) | Intel Itanium, DSPs |

---

## 3. Lecture 3: Software Architecture & Parallel Programming Models

### 3.1 Software Architecture Foundations
* **Definition**: Refers to the fundamental structures of a software system, component decomposition, interfaces, and their relationships.
* **"The Burden is on Software"**: Hardware vendors no longer boost single-core clock speeds; thus, software developers must explicitly structure code for parallelism:
  * *Shared-Memory Software*: Start a single process and **fork multiple threads** to perform tasks.
  * *Distributed-Memory Software*: Launch **multiple independent processes** that communicate across nodes.

### 3.2 Parallel Programming Models: SPMD vs. MPMD
* **SPMD (Single Program Multiple Data)**:
  * A **single compiled executable binary program** is loaded onto all processors.
  * Every processor executes the same codebase, but individual processes branch into different execution paths based on their assigned **Process Rank / ID** or local data chunk.
  * *Exam Fact*: SPMD running on MIMD hardware is the dominant paradigm for modern MPI parallel software.
* **MPMD (Multiple Program Multiple Data)**:
  * **Different, distinct executable programs** are loaded onto different processors (e.g., Process 0 runs `master.exe`, Processes 1–3 run `worker.exe`).

### 3.3 The 3 Steps for Writing Parallel Programs
1. **Work Partitioning & Load Balancing**: Divide the total problem across processes/threads such that each worker gets roughly an equal workload (load balancing) while minimizing cross-node communication.
2. **Synchronization**: Coordinate the execution order of processes/threads to prevent race conditions.
3. **Communication**: Set up explicit message transfers or shared memory channels to move data between workers.

### 3.4 Process vs. Thread
* **Process**: An active **program in execution**. Heavyweight OS entity with its own **isolated, private memory address space**.
* **Thread**: A lightweight execution unit contained **within a parent process**. Multiple threads inside the same process share the parent's memory address space, global variables, and file descriptors.

| Property | Process | Thread |
| :--- | :--- | :--- |
| **Definition** | Program in active execution. | Sub-segment / execution unit of a process. |
| **Memory Isolation** | **Private, isolated** address space. | **Shared** address space within same process. |
| **Creation/Context Cost**| High (expensive OS page table setup). | Low (lightweight stack/register switch). |
| **Communication** | Explicit Message Passing (IPC/MPI). | Direct Shared Memory read/write. |

* *Real-World Example*: A modern Word Processor runs as 1 Process containing 4 Threads: Thread 1 (Keystroke UI), Thread 2 (Spell checker), Thread 3 (Image renderer), Thread 4 (Autosave timer).

### 3.5 Shared-Memory Thread Paradigms: Dynamic vs. Static
To exploit Thread-Level Parallelism (TLP) in shared memory systems:
1. **Dynamic Threads Paradigm**:
   * A master thread waits for work, **forks new worker threads** when tasks arrive, and worker threads **terminate and join** the master upon task completion.
   * *Advantage*: Efficient memory resource utilization (allocates RAM only when active).
   * *Disadvantage*: High performance overhead from frequent thread creation and destruction calls.
2. **Static Threads Paradigm**:
   * A fixed pool of worker threads is created at startup (**Thread Pool**). Work units are dispatched to idle threads in the pool. Threads stay alive until global program cleanup.
   * *Advantage*: High performance (zero runtime creation/termination overhead).
   * *Disadvantage*: Potential waste of system memory resources if threads sit idle during light workloads.

### 3.6 Message Passing Paradigm & Basic Prototypes
* **Key Attributes**:
  1. *Partitioned Address Space*: Each process has exclusive access to its own private RAM.
  2. *Explicit Communication*: Data transfer requires explicit calling of communication routines.
* **Basic Function Prototypes**:
  * `send(void *sendbuf, int nelems, int dest)`
  * `receive(void *recvbuf, int nelems, int source)`
* **Data Integrity Semantics Rule**: If Process 0 sets `a = 100`, calls `send(&a, 1, 1)`, and immediately modifies `a = 0`, the message passing library **must deliver 100 (the original snapshot)** to Process 1, ignoring subsequent local modifications.

### 3.7 The 4 Message Passing Protocols & Idling Overhead
Message passing operations are classified by two factors: **Blocking vs. Non-blocking** and **Buffered vs. Non-buffered**:

1. **Blocking Buffered**: Sender places message into a system memory buffer and returns immediately. Sender blocks **only if the buffer is full**. Receiver blocks if the buffer is empty.
2. **Blocking Non-Buffered (Rendezvous Communication)**: No intermediate buffer exists. The sender **must wait until the receiver posts a matching `receive()`**. Both processes block and synchronize via a handshake protocol.
   * *Idling Overhead*: If sender and receiver reach the communication line at different times, the earlier process sits completely idle, wasting CPU cycles.
3. **Non-Blocking Buffered**: Sender drops data into the buffer and **returns immediately without blocking**. Receiver blocks if empty.
4. **Non-Blocking Non-Buffered**: No buffer exists and sender returns immediately. If the receiver is not ready when data arrives, **the message is lost or an error occurs** (unreliable).

| Protocol Type | Sender Blocks? | Receiver Blocks? | Buffer Exists? | Synchronization (Handshake)? |
| :--- | :--- | :--- | :--- | :--- |
| **Blocking Buffered** | Only if buffer full | If buffer empty | **Yes** | No |
| **Blocking Non-Buffered** | **Yes** (until recv ready) | **Yes** (until send ready) | **No** | **Yes (Rendezvous)** |
| **Non-Blocking Buffered** | **No** | If buffer empty | **Yes** | No |
| **Non-Blocking Non-Buffered** | **No** | **No** (may miss msg) | **No** | **No (Unreliable)** |

---

## 4. Lecture 4: Distributed Shared Memory (DSM) & Memory Hierarchy

### 4.1 Memory Hierarchy, Cache & The MMU
* **Cache Operation**: Small, high-speed memory between CPU and RAM. On data request:
  * *Cache Hit*: Requested data found in cache slot (fast access).
  * *Cache Miss*: Requested data absent; entire cache line/block fetched from RAM into cache slot.
* **MMU (Memory Management Unit)**: Hardware unit that translates instruction **Virtual Addresses** into physical RAM **Physical Addresses**.

### 4.2 Logical Cache vs. Physical Cache
* **Logical Cache (Virtual Cache)**:
  * Located **between CPU and MMU**. Stores data tagged with Virtual Addresses.
  * *Advantage*: Faster access speed because cache hits skip MMU address translation.
  * *Critical Exam Fact*: Because different applications share identical virtual address ranges, a Logical Cache **must be completely flushed on every OS context switch** to prevent Process B from accessing Process A's cached memory.
* **Physical Cache**:
  * Located **between MMU and Main Memory**. Stores data tagged with physical RAM addresses.
  * *Advantage*: No cache flushing required during context switches (physical addresses are globally unique).

### 4.3 Distributed Shared Memory (DSM) Architecture
* **Definition**: A software or hardware architecture where physically separated, distributed node memories are abstracted and presented to applications as **one single, unified shared address space**.
* **Transparency**: Hides the complex underlying network message passing from developers, allowing them to use shared-memory programming models across distributed clusters.

### 4.4 Hardware vs. Software DSM Implementation Models

#### A. Hardware-Based DSM
1. *On-Chip Memory*: Direct hardware interconnects between CPU and memory on-chip. Extremely fast, but expensive and complex.
2. *Bus-Based Multiprocessors*: Cores with local caches connect to RAM via a shared bus. Uses bus prevention algorithms to handle bus contention.
3. *Ring-Based Multiprocessors*: Nodes connect via a token-passing ring. Memory is split into a **private section** (local stack/unshared data) and a **shared section** (accessible to all nodes).

#### B. Software-Based DSM
1. *OS-Implemented DSM (Page-Based Approach)*: Integrated into the operating system virtual memory infrastructure. Intercepts memory access faults and transparently maps/swaps virtual memory **pages** across network nodes.
2. *Library / Language-Level DSM*:
   * **Shared Variable Approach**: Developers link software libraries providing specific function routines to synchronize access to shared variables.
   * **Object-Based Approach**: Shared data is encapsulated inside concurrent objects managed by object-oriented libraries.

### 4.5 Pros and Cons of Distributed Shared Memory (DSM)

| Advantages of DSM | Disadvantages of DSM |
| :--- | :--- |
| **High Scalability**: Supports large node counts without single bus bottlenecks. | **Latency Penalty**: Accessing remote node memory is slower than local RAM. |
| **Message Passing Hidden**: Hides explicit network primitives from programmers. | **Protection Complexity**: Requires complex locks/coherence mechanisms to prevent race conditions. |
| **Complex Data Structures**: Allows passing complex data structures by reference. | **Consistency Model Burden**: Programmers must understand complex memory consistency rules. |
| **Exploits Page Locality**: Fetches entire memory pages, exploiting spatial locality. | **Underlying Asynchrony**: Built over asynchronous message passing, making it inherently less efficient than tuned native message passing. |
| **Cost Effective**: Built using cheap commodity hardware components. | **Lack of Fine Control**: Programmer has little direct control over generated network messages. |

---

## 5. Lecture 5: Distributed Memory Programming with MPI

### 5.1 MPI Principles & Fundamentals
* **Message Passing Interface (MPI)**: A standardized, portable message-passing library specification for parallel computers running SPMD programs on MIMD architectures.
* **Core Principles**: Assumes partitioned address space, explicit two-way communication, and explicit parallelization.
* **Header & Syntax**:
  * Include `#include <mpi.h>` in C programs.
  * All functions, constants, and types prefix with `MPI_` (e.g., `MPI_Init`, `MPI_COMM_WORLD`). Return code for success is `MPI_SUCCESS`.

### 5.2 MPI Environment & Core Lifecycle Functions
Every MPI program relies on 6 core functions:

1. **`MPI_Init(int *argc, char ***argv)`**: Initializes the MPI execution environment. Must be called before any other MPI routine.
2. **`MPI_Finalize()`**: Cleans up MPI resources and terminates the MPI environment. Must be called at the end of execution.
3. **`MPI_Comm_size(MPI_Comm comm, int *size)`**: Queries the total number of processes $p$ participating in the communicator.
4. **`MPI_Comm_rank(MPI_Comm comm, int *rank)`**: Queries the 0-indexed rank ID ($0, 1, \dots, p-1$) of the calling process.
5. **`MPI_Send(...)`**: Sends a message to a target process.
6. **`MPI_Recv(...)`**: Receives a message from a source process.

* **Communicator (`MPI_Comm`)**: Defines a communication domain (a set of processes authorized to exchange messages). `MPI_COMM_WORLD` is the default communicator containing all processes launched at execution.

### 5.3 Compilation & Execution Workflow
* **Compilation Command**:
  ```bash
  mpicc -g -Wall -o mpi_hello mpi_hello.c
  ```
  *(Uses `mpicc` wrapper script; `-g` enables debug symbols; `-Wall` turns on all warnings; `-o` names executable)*.
* **Execution Command**:
  ```bash
  mpiexec -n 4 ./mpi_hello
  ```
  *(Launches the executable simultaneously across 4 parallel process ranks)*.

### 5.4 Standard C/MPI Boilerplate Code Structure
```c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int np, myrank;

    // Initialize MPI environment
    MPI_Init(&argc, &argv);

    // Get total number of processes
    MPI_Comm_size(MPI_COMM_WORLD, &np);

    // Get rank of current process
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    printf("Greetings from process %d of %d!\n", myrank, np);

    // Finalize MPI environment
    MPI_Finalize();
    return 0;
}
```

### 5.5 MPI Point-to-Point Communication & Message Matching
* **`MPI_Send` Prototype**:
  ```c
  int MPI_Send(void *buf, int count, MPI_Datatype datatype, int dest, int tag, MPI_Comm comm);
  ```
* **`MPI_Recv` Prototype**:
  ```c
  int MPI_Recv(void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Status *status);
  ```
* **Standard MPI Datatypes**: `MPI_INT`, `MPI_FLOAT`, `MPI_DOUBLE`, `MPI_CHAR`, `MPI_LONG`.
* **Message Matching Criteria**: A receive call matches a send call ONLY if `source`, `tag`, and `comm` match.
* **Wildcards for Receive**:
  * `MPI_ANY_SOURCE`: Accepts messages from any sender process.
  * `MPI_ANY_TAG`: Accepts messages carrying any tag integer.

### 5.6 Message Inspection (`MPI_Status` & Data Querying)
* **`MPI_Status` Structure**: Structure returned by `MPI_Recv` containing metadata about the received message:
  ```c
  typedef struct MPI_Status {
      int MPI_SOURCE;  // Rank of sender
      int MPI_TAG;     // Message tag
      int MPI_ERROR;   // Error status code
  } MPI_Status;
  ```
* **Querying Received Payload Size**:
  To determine the exact number of elements received when using buffer wildcards, use `MPI_Get_count`:
  ```c
  MPI_Status status;
  int count;
  MPI_Recv(buffer, 100, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
  MPI_Get_count(&status, MPI_INT, &count);
  printf("Received %d integers from process %d\n", count, status.MPI_SOURCE);
  ```

### 5.7 Circular Wait Deadlocks & The 3 Solutions
* **The Deadlock Problem (Circular Wait)**:
  Consider a ring pattern where Process $i$ attempts to send data to Process $i+1 \pmod p$ before receiving from Process $i-1 \pmod p$. If `MPI_Send` behaves as a blocking non-buffered operation, **all processes block forever waiting to send**, creating a system deadlock.

#### The 3 Official Exam Solutions to Break Deadlocks:

1. **Odd-Even Rank Pairing (Code Reordering)**:
   Partition processes into odd and even ranks to break the circular wait condition. Even processes send first then receive; odd processes receive first then send:
   ```c
   if (myrank % 2 == 0) {
       MPI_Send(sendbuf, count, MPI_INT, dest, tag, MPI_COMM_WORLD);
       MPI_Recv(recvbuf, count, MPI_INT, source, tag, MPI_COMM_WORLD, &status);
   } else {
       MPI_Recv(recvbuf, count, MPI_INT, source, tag, MPI_COMM_WORLD, &status);
       MPI_Send(sendbuf, count, MPI_INT, dest, tag, MPI_COMM_WORLD);
   }
   ```
2. **Simultaneous `MPI_Sendrecv`**:
   Combines sending and receiving into a single atomic hardware/library call, eliminating deadlock risks:
   ```c
   MPI_Sendrecv(sendbuf, sendcount, sendtype, dest, sendtag,
                recvbuf, recvcount, recvtype, source, recvtag,
                MPI_COMM_WORLD, &status);
   ```
3. **In-Place Buffer Swap `MPI_Sendrecv_replace`**:
   When space is limited and a single buffer is used for both outgoing and incoming data:
   ```c
   MPI_Sendrecv_replace(buf, count, datatype, dest, sendtag,
                        source, recvtag, MPI_COMM_WORLD, &status);
   ```

---

## 6. Pre-Exam Quick Reference Cheat Sheet

### Essential Formulas to Remember:
1. **Speedup**: $S = \frac{T_{\text{serial}}}{T_{\text{parallel}}}$
2. **Amdahl's Law**: $S = \frac{1}{(1 - P) + \frac{P}{N}}$
3. **Theoretical Max Speedup**: $S_{\max} = \frac{1}{1 - P}$

### Key Terms to Spot in Multiple Choice / Short Answer:
* **NUMA**: Memory access time depends on physical memory location relative to CPU.
* **SPMD**: 1 binary executable file executed across all processes branching on Rank ID.
* **Rendezvous**: Blocking Non-Buffered communication forcing direct process handshake.
* **Logical Cache Flush**: Required on OS context switch because virtual addresses overlap.
* **Flynn's SIMD**: Single instruction stream acting on multiple data elements (GPUs, Vector architectures).
* **VLIW**: Static compile-time instruction packing into long instruction words.
* **Dynamic Multiple Issue**: Runtime hardware scheduling of superscalar instructions.
* **Amdahl's Bottleneck**: Serial fraction $(1-P)$ limits maximum speedup as $N \to \infty$.
* **`MPI_COMM_WORLD`**: Default communicator containing all processes launched at execution.
