import os
from client import *

EXAMPLE_GOOD_OUT='Test response :\n{\n  "torch": true,\n  "tensorflow": true,\n  "msg": ""\n}\n'

def test_gpu_tester():
    # positive case
    assert run(cer_path=None) == EXAMPLE_GOOD_OUT