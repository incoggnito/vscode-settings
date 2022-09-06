# atoolbox

![](https://gitlab.com/amitronics/atoolbox/badges/master/pipeline.svg)
![](https://gitlab.com/amitronics/atoolbox/badges/master/coverage.svg)
![](https://gitlab.com/amitronics/atoolbox/workflows/build/badge.svg)
![](https://img.shields.io/pypi/pyversions/atoolbox.svg)
![](https://img.shields.io/badge/code%20style-black-000000.svg)
![](https://img.shields.io/gitlab/repo-size/amitronics/atoolbox)
![](https://img.shields.io/gitlab/license/amitronics/atoolbox)
![](https://img.shields.io/pypi/v/atoolbox)
---


---

## Getting Started

### Installation
#### Requirements:

- libsndfile (AudioFile): you have to manually install following packages on your linux machine:
    ```bash
    apt-get update && apt-get install libsndfile1 libsndfile1-dev
    ```
[Source: libsndfile projectpage](https://github.com/libsndfile/libsndfile)

The atoolbox can be installed for internal Python 3.7+ projects with

```console
poetry add git+https://git.amitronics.net/amitronics/tools/atoolbox.git
```

Currently, there is no deployment to the `pypi` server planned.


## License

atoolbox is proprietary software and prohibited from
unauthorized redistribution. See the [license](LICENSE.md) for more
information.
