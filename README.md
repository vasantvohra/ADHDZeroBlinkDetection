# ADHDZeroBlinkDetection
Attention Span detection of ADHD patients using a non intrusive method that only uses a cheap web cam to detect blinking and predict the attention percentage of the user.

A Custom HAAR Cascade was created to detect the blinks. 

## Video Example: 
### https://youtu.be/yErXjEeZRts

## Main Dependency: 
OpenCV 2.4.7
Python



## Constraints:

However multiple constraints must be taking into consideration as the accuracy may fluctuate due to one of the following:
Distance between the patient and the camera must be as if the patient is typing on the laptop’s keyboard.
- No eye glasses should be worn by the patient. 
- The background of the patient’s room must be clear and clean to avoid false positives.
- Room’s lighting must be slightly strong to avoid shading on the patient’s face or different parts of the area in order to avoid false positives.

## Main UI window explaination: 

Focus percentage: it means the percentage of time that the patient is focused during the experiment, the percentage is calculated by knowing the standard deviation from a specific threshold based on the averages of the team, however, to be able to estimate an accurate threshold, clinical trials should be made using the manual experimentation module and neurofeedback devices to be able to estimate research backed thresholds to eventually result in a more accurate focus percentage.
Blinks Average: This is the blinking average of all the defined rate periods. Ex: if blinking defined rate is 10 seconds, and during an experiment duration of one minute of one min the user blinked 10 times, therefore the blinks average will be 10/(60/10).
Blinks count: The total number of blinks during the whole experiment duration.
Blinks max: The maximum number of blinks during the defined blinking rate duration period.
Blinks min: The minimum number of blinks during the defined blinking rate duration period.
Blinking rate standard deviation: The deviation from the mean value of the blinks number per the defined blinking detection rate. 

## Logging blinks: 

An example of the logging format of the first timestamping file: 
 
Name: Yehia/Omar/Hesham
Age: 24
Blink Detected
Blink Time:  2017-07-04 21:56:35
Blink Detected
Blink Time:  2017-07-04 21:56:36
Blink Detected
Blink Time:  2017-07-04 21:56:38
Blink Detected
Blink Time:  2017-07-04 21:56:39
Blink Detected
Blink Time:  2017-07-04 21:56:46
Blink Detected
Blink Time:  2017-07-04 21:56:47
Blink Detected
Blink Time:  2017-07-04 21:56:48
Blink Detected
Blink Time:  2017-07-04 21:56:50
Blink Detected
Blink Time:  2017-07-04 21:56:52


An example of the logging format of the second blinking states file: 


Name: Yehia/Omar/Hesham
Age: 24
1
Blinking Rate: 1 Per 5.0 Seconds.
Incrementing average: 0 per rate time.
Standard Deviation: 0.0
2
Blinking Rate: 3 Per 5.0 Seconds.
Incrementing average: 1 per rate time.
Standard Deviation: 0.05
3
Blinking Rate: 0 Per 5.0 Seconds.
Incrementing average: 1 per rate time.
Standard Deviation: 0.0816496580928
4
Blinking Rate: 3 Per 5.0 Seconds.
Incrementing average: 1 per rate time.
Standard Deviation: 0.0712390342439
5



