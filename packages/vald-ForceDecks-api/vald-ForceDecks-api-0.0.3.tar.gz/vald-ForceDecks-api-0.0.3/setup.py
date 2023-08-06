import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="vald-ForceDecks-api",
    version="0.0.3",
    author="Régis Tremblay Lefrançois",
    description="Python module to interact with VALD ForceDecks API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["Vald_ForceDecks_API"],
    requires=["requests"],
    install_requires=["requests"],
)
