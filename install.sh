# where stuffs are installed
cd ..
mkdir bin

# add to path

# miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# prodigal
git clone https://github.com/hyattpd/Prodigal.git
make
# add to path

# card
conda install --channel bioconda rgi

# this need to be run under py27
conda create -n py27 python=2.7 anaconda

