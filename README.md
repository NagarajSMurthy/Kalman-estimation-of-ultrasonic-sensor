# Kalman-estimation-of-ultrasonic-sensor
This repository explains the design and implementation of kalman filters for distance estimation of ultrasonic sensor. The implementation follows the paper 'Kalman Filter Algorithm Design for HC-SR04 Ultrasonic Sensor Data Acquisition System'. 

The sensor used is HC-SR04 ultrasonic distance sensor. To know more about the working and usage of this sensor, check out: https://www.youtube.com/watch?v=Z-j08CbcHPA 


# Setup the software on a Raspberry Pi
```
python3 -m pip -r requirements.txt
sudo apt-get -y install libatlas-base-dev libopenjp2-7-dev libopenjp2-7

```

#The setup 
![](Kalman_filter_setup.jpg)

#Implementation

![](kalman_estimation_gif.gif)


