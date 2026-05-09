import time
def test_import(module_name):
    print(f"Importing {module_name}...", end="", flush=True)
    start = time.time()
    try:
        exec(f"import {module_name}")
        print(f" OK ({time.time() - start:.2f}s)")
    except Exception as e:
        print(f" FAIL: {e}")

test_import("os")
test_import("sys")
test_import("numpy")
test_import("pathlib")
test_import("datetime")
test_import("torch")
test_import("torch.nn")
test_import("torch.nn.functional")
test_import("torch.optim")
test_import("torch.utils.data")
test_import("torchvision.transforms")
test_import("matplotlib")
test_import("matplotlib.pyplot")
test_import("seaborn")
test_import("sklearn.model_selection")
test_import("sklearn.metrics")
print("All imports tested.")
