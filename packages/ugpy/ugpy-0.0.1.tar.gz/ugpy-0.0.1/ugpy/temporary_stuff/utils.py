import torch


def set_device():
    """
  Set the device. CUDA if available, CPU otherwise
    (from deeplearning.neuromatch)
  """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("GPU is NOT enabled in this notebook.")
    else:
        print("GPU is enabled in this notebook.")

    return device
