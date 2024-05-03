FROM nvcr.io/nvidia/pytorch:24.04-py3

# General system update and upgrade
RUN apt-get update && apt-get upgrade -y

# Installing system dependencies
RUN apt install graphviz libgraphviz-dev graphviz-dev pkg-config -y

# Installing additional pip packages other than the ones provided in the base container image
RUN pip install jupyter ipywidgets widgetsnbextension pandas-profiling tqdm
RUN pip install yfinance statsmodels 
RUN pip install pygraphviz
RUN pip install networkx
RUN pip install dowhy 
RUN pip install wbdata

ENTRYPOINT ["bash"]
