"""
This library is a collection of functions for interacting and setting up `cupy`.
It enables efficient abstractions over compute units, like CPUs and GPUs.  
"""

import cupy as cp
import logging

def set_memory_limits():
    device_count = cp.cuda.runtime.getDeviceCount()
    logging.info( f"GPU module has found {device_count} devices. Setting memory limits..." )
    
    mempool = cp.get_default_memory_pool()
    for device_id in range(device_count):
        mempool.set_limit(size=10*1024**3)  # 10 GiB
       