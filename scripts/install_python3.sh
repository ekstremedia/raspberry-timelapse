sudo apt-get install -y build-essential tk-dev libncurses5-dev \
	libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev \
	libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev

version=3.9.0

wget https://www.python.org/ftp/python/$version/Python-$version.tgz

tar zxf Python-$version.tgz
cd Python-$version
./configure --enable-optimizations
make -j4
sudo make altinstall
