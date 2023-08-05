from setuptools import setup, find_packages
from pathlib import Path

reqs_dir = Path("./requirements")

requirements_base = (reqs_dir / "base.txt").read_text().splitlines()
requirements_stable_baselines3 = (
    (reqs_dir / "stable_baselines3.txt").read_text().splitlines()
)
# TODO: rllib
# requirements_rllib = (reqs_dir / "rllib.txt").read_text().splitlines()
requirements_pettingzoo = (reqs_dir / "pettingzoo.txt").read_text().splitlines()
requirements_supersuit = (reqs_dir / "supersuit.txt").read_text().splitlines()
requirements_dm_env = (reqs_dir / "dm_env.txt").read_text().splitlines()

setup(
    name="hivex",
    version="1.0.1",
    license="Apache 2.0",
    license_files=["LICENSE"],
    url="https://github.com/philippds/HiveX",
    download_url="https://github.com/philippds/HiveX",
    author="Philipp D Siedler",
    author_email="p.d.siedler@gmail.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    description=(
        "Real-World Multi-Agent Reinforcement Learning problems, potentially yielding a high positive impact on society when solved."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="multi-agent reinforcement-learning python machine-learning",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_data={
        "hivex": [],
    },
    python_requires=">=3.10",
    install_requires=requirements_base,
    extras_require={
        "stable_baselines3": requirements_stable_baselines3,
        "pettingzoo": requirements_pettingzoo,
        "requirements_supersuit": requirements_supersuit,
        "dm_env": requirements_dm_env,
    },
)

# TODO: rllib
# "rllib": requirements_rllib,
