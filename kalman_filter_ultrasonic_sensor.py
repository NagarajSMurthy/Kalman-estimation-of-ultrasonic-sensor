import RPi.GPIO as GPIO
import time
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

trig = 13
echo = 15

print('setting up the pins')
#GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

xs = []
sensor_reading = []
k_estimated = []
k_uncertainity = []

file_name = 'ultrasonic_kalman_data.csv'

with open(file_name, 'a') as header:
    csvwriter = csv.writer(header)
    csvwriter.writerow(['Ultrasonic sensor data','Kalman filter estimation','Uncertainity'])
        
# initialization for kalman filters
x = np.matrix([[0.]])      # initial distance estimate
p = np.matrix([[1000.]])   # initial uncertainity

u = np.matrix([[0.]])
w = np.matrix([[0.]])
A = np.matrix([[1.]])
B = np.matrix([[0.]])
H = np.matrix([[1.]])
Q = np.matrix([[0.00001]])
R = np.matrix([[0.10071589]])


# True distance if distance is fixed
true_distance = []

def kalman(x_,p_,x_measured):
    # prediction
    x_predicted = A*x_ + B*u + w
    p_predicted = A*p_*np.transpose(A) + Q

    # measurement update
    y = x_measured - (H*x_predicted)

    # kalman estimation   
    s = H*p_predicted*np.transpose(H) + R
    K = p_predicted*np.transpose(H)*np.linalg.inv(s)

    x_estimated = x_predicted + (K*y)
    p_estimated = (1 - (K*H))*p_predicted

    return x_estimated, p_estimated

def measure(k, xs, sensor_reading, k_estimated, true_distance):
    global x, p
    GPIO.output(trig,False)
    #print('Waiting for the sensors to settle')
    time.sleep(1)

    GPIO.output(trig,True)
    time.sleep(0.00001)
    GPIO.output(trig,False)

    while(GPIO.input(echo)==0):
        pulse_start = time.time()

    while(GPIO.input(echo)==1):
        pulse_end = time.time()

    pulse = pulse_end - pulse_start
    distance = round(pulse * 17150,5)

    xs.append(k)    
    sensor_reading.append(distance)
    '''
    if k <= 15:
        true_distance.append(10)
    if k>15 and k<=30:
        true_distance.append(12)
    if k>30:
        true_distance.append(20)
    '''
    true_distance.append(10)
    
    x, p = kalman(x,p,distance)

    k_estimated.append(x.item(0))
    k_uncertainity.append(p)
    
    with open(file_name, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([distance,x.item(0),p.item(0)])

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    sensor_reading = sensor_reading[-20:]
    true_distance = true_distance[-20:]
    k_estimated = k_estimated[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, sensor_reading, label='Sensor data')
    ax.plot(xs, k_estimated, 'tab:red', label='kalman estimation')
    ax.plot(xs, true_distance, 'tab:orange', label='True distance')

    #legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    ax.legend()

    '''if k == 14 or k == 29:
        print('Distance changed')
    '''    
    # Format plot
    #plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Kalman filter data estimation of HCSR04')
    plt.ylabel('Distance (cms)')
    print('Distance from sensor: ',distance,' cms')
    print('kalman estimated distance: ',x.item(0),' cms')
    

try:
    ani = animation.FuncAnimation(fig, measure, fargs=(xs, sensor_reading, k_estimated, true_distance), interval=2000)
    plt.show()
    
except KeyboardInterrupt:
    print('Cleaning up')
    GPIO.cleanup()
