import os
import sys
import time

print("Python version:", sys.version)
print("Testing torch import...")
start = time.time()
try:
    import torch
    print("Torch imported successfully in {:.2f} seconds".format(time.time() - start))
    print("CUDA available:", torch.cuda.is_available())
except Exception as e:
    print("Error importing torch:", e)
    import traceback
    traceback.print_exc()
except KeyboardInterrupt:
    print("\nImport interrupted by user.")
