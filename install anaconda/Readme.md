To install Anaconda with Jupyter Notebook inside Docker on Ubuntu, follow these steps:

## 1. Pull the Anaconda Docker Image

Open a terminal on your Ubuntu system and pull the official Miniconda or Anaconda image from Docker Hub:

```bash
docker pull continuumio/miniconda3
```

or for the full Anaconda image:

```bash
docker pull continuumio/anaconda3
```

This provides a base container with conda already installed[2][5][8].

## 2. Run the Container and Install Jupyter Notebook

Run the container with port 8888 exposed, and install Jupyter Notebook inside it. Use this command from your host terminal:

```bash
docker run -it -p 8888:8888 continuumio/miniconda3 /bin/bash -c "\
/opt/conda/bin/conda install jupyter -y --quiet && \
mkdir /opt/notebooks && \
/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser --allow-root"
```

- This command installs Jupyter in the container.
- Creates a directory for notebooks.
- Starts the Jupyter server accessible on all IPs at port 8888.
- Runs without opening a browser and allows root usage (common in containers)[2][5][7][8].

## 3. Access Jupyter Notebook

Once the container is running, the terminal will output a URL with a token, something like:

```
http://localhost:8888/?token=...
```

Open this URL in your Ubuntu host browser to access Jupyter Notebook.

## Optional: Persist Data and Customization

- To save notebooks outside the container, mount a host directory:

```bash
docker run -it -p 8888:8888 -v /path/on/host:/opt/notebooks continuumio/miniconda3 /bin/bash -c "..."
```

- Replace `/path/on/host` with your local directory path.

