# RDK Reinforcement Learning Mountain Car

## 节点介绍

本仓库让开发者在RDK系列开发板上使用强化学习模型DQN体验小车爬山Demo

## 节点使用

本项目包含一个mountain_car节点，该节点包括一个服务器和一个客户端。用户需要通过启动客户端的方式来触发服务器，跑起X5上的小车爬山Demo。

### 环境准备

安装ros依赖：
```
sudo apt update
sudo apt install python3-colcon-ros
```

激活ros环境（注：每次新开一个terminal（终端），都建议重新激活一下环境，即执行以下代码）
对于RDK OS V3.0版本，执行：`source /opt/tros/humble/setup.bash`
对于RDK OS V2.1版本，执行：`source /opt/tros/setup.bash`

在RDK开发板上新建一个工作空间目录，并构建src子目录：

```
mkdir -p colcon_ws/src
cd colcon_ws/src
```

使用git clone命令，将本项目克隆至src目录下。

进入项目，安装pip依赖。
```
cd rdk_rl_mountain_car
pip3 install -r requirements.txt
cd ..
```
注：该项目与RDK Model Zoo依赖保持一致，均需要bpu_infer_lib，如尚未安装bpu_infer_lib，请参考https://github.com/D-Robotics/rdk_model_zoo链接进行安装

回到工作空间目录，构建项目

```
cd ..
colcon build
```


激活项目环境（注：在完成环境构建后，每次新开一个terminal（终端），都建议重新激活一下环境，即执行以下代码）
对于RDK OS V3.0版本，执行：`source ./install/setup.sh`
对于RDK OS V2.1版本，执行：`source ./install/setup.bash`


### 使用节点

我们首先在MobaXTerm打开一个终端，启动一个服务端，注意这里需要填入bin模型的地址做为参数，模型已在github中提供，请根据实际情况填入地址：

```
ros2 run mountain_car server --ros-args -p model_path:=/root/car_dqn/car_dqn_output.bin
```

启动服务端后，我们看到DQN Server is ready的回显，但并未跳出任何界面。

我们需要使用客户端进行触发。

我们首先在MobaXTerm打开另一个终端，启动一个客户端：

```
ros2 run mountain_car client
```

此时，MobaXTerm会弹出一个窗口，并为我们显示强化学习DQN网络是如何爬山的。