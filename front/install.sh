#/!bin/sh

#环境按照脚本
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

pip install pandas Flask pymongo redis -i https://pypi.mirrors.ustc.edu.cn/simple

echo 'export PATH=$PATH:/home/jiawen/.local/bin' >> ~/.bashrc #加入PATH路径
source ~/.bashrc

mkdir -p ~/.pip

cat <<EOL > ~/.pip/pip.conf
[global]
index-url = https://pypi.mirrors.ustc.edu.cn/simple
EOL