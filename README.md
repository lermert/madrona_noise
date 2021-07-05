# madrona_noise
Set of scripts to perform clustering on Seattle node data.


### installation of dependencies with conda
conda config --add channels conda-forge

conda create -n madrona python=3 scipy numpy obspy pandas scikit-learn jupyter h5py seaborn

conda activate madrona


pip install kneed

