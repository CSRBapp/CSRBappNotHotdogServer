# CSRBappNotHotdogServer

## How to start the server

1. Ensure that *~/CSRBSTORAGE/* and *~/CSRBVFS/* directories exist.
1. Then start *CSRBvfsFUSE*:
    ```
    CSRBbin/SCRIPTS/start-CSRBvfsFUSE.sh CSRBbin/<OS-BUILD>/CSRBvfsFUSE
    ```
1. Start *CSRBappNothotdog.py*:
    ```
    python3 CSRBappNotHotdog.py
    ```
    
# QUICKSTART
## GCP Cloud Shell
### INIT
```
sudo apt install fuse3
git clone --recurse-submodules https://CSRBapp@github.com/CSRBapp/CSRBappNotHotdogServer.git
mkdir ~/CSRBSTORAGE
mkdir ~/CSRBVFS
```
The *Cloud Shell* VM image should already have TensorFlow installed, which is needed to run the Server. If it's not installed you can install it with:
```
apt -t testing install python3-pip
pip3 install tensorflow
```

### Start CSRBnode
```
cd CSRBappNotHotdogServer
CSRBbin/SCRIPTS/start-CSRBvfsFUSE.sh CSRBbin/UBUNTU-18.04/CSRBvfsFUSE
```
*Copy the NODE ID*

### Run as Server
OpenCV2 needs RAM so you need to enable Boost Mode.

*NOTE: Adding a swap file does not work in Cloud Shell:*
```
sudo dd if=/dev/zero of=/swap.img bs=1M count=8k
sudo chmod 0600 /swap.img
sudo mkswap /swap.img
sudo swapon /swap.img
swapon: /swap.img: swapon failed: Invalid argument
```

Start *CSRBappNotHotdog.py*:
```
cd CSRBappNotHotdogServer
python3 CSRBappNotHotdog.py
```

### Run as Client
```
cd CSRBappNotHotdogServer
python3 CSRBappNotHotdogClient.py <NODEID> <SERVER_NODEID> hotdog-or-not-hotdog/test/bottle.jpg
python3 CSRBappNotHotdogClient.py <NODEID> <SERVER_NODEID> hotdog-or-not-hotdog/test/hotdog.jpg
python3 CSRBappNotHotdogClient.py <NODEID> <SERVER_NODEID> hotdog-or-not-hotdog/test/wallpaper.jpg
python3 CSRBappNotHotdogClient.py <NODEID> <SERVER_NODEID> hotdog-or-not-hotdog/test/hot2.jpeg
```

# NOTES
## Increasing zram swap in GCP Cloud Shell
```
swapoff /dev/zram0
mount -o remount,rw
echo 1 > /sys/block/zram0/reset
#echo 0 > /sys/class/zram-control/hot_remove
#rmmod zram
#modprobe zram
echo $((1*1024*1024*1024)) > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon /dev/zram0
```
