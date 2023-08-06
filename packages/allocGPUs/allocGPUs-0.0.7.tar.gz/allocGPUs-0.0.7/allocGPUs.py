import os
import gpustat
import random

stats = gpustat.GPUStatCollection.new_query()
ids = map(lambda gpu: int(gpu.entry['index']), stats)
ratios = map(lambda gpu: float(gpu.entry['memory.used'])/float(gpu.entry['memory.total']), stats)
pairs = list(zip(ids, ratios))
random.shuffle(pairs)

## input how many gpus you want
num_gpus = int(input("Number of GPUs: "))
## allocate gpu
try:
    gpus = sorted(pairs, key=lambda x: x[1])[0:num_gpus]
except IndexError:
    print(" Could not load {} gpus".format(num_gpus))

print("setGPU: Setting GPU to: {}".format(gpus))

os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(f'{gpu}' for gpu in gpus)
