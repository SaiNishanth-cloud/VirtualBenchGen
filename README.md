# VirtualBenchGen
"VirtualBenchGen: Workload generation and benchmarking for virtual computation instances."

This repository contains code for a pedestrian tracking application. The application functions as follows: 
when a user attempts to access the application, they are prompted to upload a video in any format. The uploaded video is then processed, 
and the resulting output is streamed back to the user, who also has the option to download it. The application is deployed using Docker, 
and to minimize latency, a microservices architecture is employed. This involves utilizing Kubernetes for container orchestration. 
The deployment incorporates a horizontal pod autoscaler, which dynamically adjusts the number of pods based on specified metrics. 
This ensures efficient resource utilization while maintaining responsiveness. In this manner, the goal is to achieve latency reduction 
and optimal resource utilization.
