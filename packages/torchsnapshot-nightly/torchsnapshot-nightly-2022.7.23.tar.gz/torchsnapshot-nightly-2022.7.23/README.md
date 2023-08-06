# torchsnapshot

<p align="center">
<a href="https://github.com/facebookresearch/torchsnapshot/actions?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/facebookresearch/torchsnapshot/unit%20test/main" alt="build status"></a>
<a href="https://pypi.org/project/torchsnapshot"><img src="https://img.shields.io/pypi/v/torchsnapshot" alt="pypi version"></a>
<a href="https://pypi.org/project/torchsnapshot-nightly"><img src="https://img.shields.io/pypi/v/torchsnapshot-nightly?label=nightly" alt="pypi nightly version"></a>
<a href="https://codecov.io/gh/facebookresearch/torchsnapshot"><img src="https://codecov.io/gh/facebookresearch/torchsnapshot/branch/main/graph/badge.svg?token=DR67Q6T7YF" alt="codecov"></a>
<a href="https://github.com/facebookresearch/torchsnapshot/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/torchsnapshot" alt="bsd license"></a>
</div>

**This library is currently in Alpha and currently does not have a stable release. The API may change and may not be backward compatible. If you have suggestions for improvements, please open a GitHub issue. We'd love to hear your feedback.**

A light-weight library for adding fault tolerance to large-scale PyTorch distributed training workloads.


## Install

Requires Python >= 3.7 and PyTorch >= 1.11

From pip:

```bash
pip install --pre torchsnapshot-nightly
```

From source:

```bash
git clone https://github.com/facebookresearch/torchsnapshot
cd torchsnapshot
pip install -r requirements.txt
python setup.py install
```

## Concepts
- **Stateful object** - an object that whose state can be obtained via `.state_dict()` and restored via `.load_state_dict()`. Most PyTorch components (e.g. `Module`, `Optimizer`, `LRScheduler`) already implement this [protocol](https://github.com/facebookresearch/torchsnapshot/blob/main/torchsnapshot/stateful.py).
- **App state** - the application state described using multiple stateful objects.
- **Snapshot** - the persisted app state.


## Basic Usage

Describing the application state with multiple stateful objects:
```python
app_state = {"model": model, "optimizer": optimizer}
```


Taking a snapshot of the application state:
```python
from torchsnapshot import Snapshot

# File System
snapshot = Snapshot.take(path="/foo/bar/baz", app_state=app_state)

# S3
snapshot = Snapshot.take(path="s3://foo/bar", app_state=app_state)

# Google Cloud Storage
snapshot = Snapshot.take(path="gcs://foo/bar", app_state=app_state)
```

Referencing an existing snapshot:
```python
snapshot = Snapshot(path="foo/bar/baz")
```


Restoring the application state from a snapshot:
```python
snapshot.restore(app_state=app_state)
```

See the [example directory](https://github.com/facebookresearch/torchsnapshot/tree/main/examples) for more examples.


## License

torchsnapshot is BSD licensed, as found in the [LICENSE](LICENSE) file.
