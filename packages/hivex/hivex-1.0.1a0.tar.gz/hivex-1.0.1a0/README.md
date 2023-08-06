<div align="center">
  <img src="hivex/docs/images/hivex_thumbnail.jpg"
      style="border-radius:20px"
      alt="HiveX header image"/>
</div>

# HiveX

*Real-World Multi-Agent Reinforcement Learning problems, potentially yielding a high positive impact on society when solved.*

## About

The motivation of the HiveX suite is to provide advanced  reinforcement learning benchmarking environments with an emphasis on: (1) ***real-world*** scenarios, (2) ***multi-agent*** systems, (3) investigating problems and solutions with ***high impact on society***, (4) ***cooperation and communication*** mechanisms.

## Available Environments

|Thumbnail|Title|Domain|Paper|Env Name|
|-----|-----|-----|-----|-----|
|<a href="url"><img src="https://ai.philippsiedler.com/wp-content/uploads/2021/11/210527_Multi-Agent-Wind-Turbine-Farm_Thumbnail_04.jpg" height="auto" width="150" style="border-radius:10px" alt="WindFarm"></a>|Windfarm Orientation Optimisation|Distributed Energy Grids|[Link](https://arxiv.org/abs/2111.15611)<br>(Neurips'21)|<code>"WindFarm"</code>|
|<a href="url"><img src="https://ai.philippsiedler.com/wp-content/uploads/2022/02/MA_WT_thumb.png" height="auto" width="150" style="border-radius:10px" alt="Wildfire"></a>|Wildfire-Management<br>Resource Distribution|Catastrophe Management|[Link](https://arxiv.org/abs/2204.11350)<br>(ICLR'22)|<code>"Wildfire"</code>|
---

## Installation

`hivex` can be installed from PyPI using `pip`:

```shell
pip install hivex
```

### Manual install using conda virtual environment

The installation steps are
as follows:

1. Create and activate a virtual environment, e.g.:

    ```shell
    conda create -n hivex python=3.9
    conda activate hivex
    ```

2.  Install `hivex`:
    ```shell
    git clone -b main https://github.com/philippds/HiveX
    cd HiveX
    pip install .
    ```

3. Test the `hivex` installation:
    ```shell
    cd <hivex_root>/hivex/python/pytest
    pytest test.py
    ```

## Example Usage

### Training agents with [UnityEnvironment](https://github.com/Unity-Technologies/ml-agents) (Environment Interface | Learning Framework)

#### UnityEnvironment | Random

```shell
cd <hivex_root>/examples/UnityEnvironment
python UnityEnvironment_train.py
```

### Training agents with [ML-Agents](https://github.com/Unity-Technologies/ml-agents) (Environment Interface | Learning Framework)

#### UnityEnvironment | ML-Agents

```shell
cd <hivex_root>/examples/ml_agents
mlagents-learn config/WindFarm.yaml --env=<hivex_root>/hivex/environments/hivex_WindFarm_x86_64 --run-id="WindFarm_Test_01"
```

### Training agents with [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) (Environment Interface | Learning Framework)

#### Stable-Baselines3 VecEnv | Stable-Baselines3

```shell
cd <hivex_root>
pip install -e .[stable-baselines3]
```
```shell
cd <hivex_root>/examples/stable_baselines3
python VecEnv_train.py
```

#### [Gym](https://github.com/openai/gym) | Stable-Baselines3

```shell
cd <hivex_root>/examples/gym
python gym_train.py
```

#### [dm_env](https://github.com/deepmind/dm_env) | Random


```shell
cd <hivex_root>/examples/dm_env
python dm_env_train.py
```

Interface Test (Optional)
```shell
cd <hivex_root>/examples/dm_env/utilities
python dm_env_test.py
```

### Training agents with [RLLib](https://github.com/ray-project/ray) (Linux Only) (Environment Interface | Learning Framework)

```shell
cd <hivex_root>
pip install -e .[rllib]
pip install -e .[pettingzoo]
```

#### [PettingZoo ParallelEnv (AEC)](https://github.com/Farama-Foundation/PettingZoo) | RLLib

```shell
cd <hivex_root>/examples/pettingzoo_ParallelEnv
python ParallelEnv_train.py
```

[Interface Test](https://github.com/Farama-Foundation/PettingZoo/tree/master/pettingzoo/test) (Optional)
```shell
cd <hivex_root>/examples/pettingzoo_ParallelEnv/utilities
python api_test.py
python parallel_api_test.py
```

## Documentation

Full documentation is available
[here](hivex/docs/html/wrappers/index.html)

## Citing HiveX

If you use HiveX in your work, please cite:

```bibtex
@inproceedings{siedler2022hivex,
    title={},
    author={Philipp D. Siedler},
    year={2022},
    journal={},
    organization={}
}
```