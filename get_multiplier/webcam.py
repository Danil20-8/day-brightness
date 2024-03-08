import os
import cv2
import numpy
import time;

webcam_config_path = os.path.join("config", "webcam")
webcam_config_last_path = os.path.join("config", "webcam", "last")

if not os.path.exists(webcam_config_path):
    os.makedirs(webcam_config_path)

def get_webcam_multiplier():
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    
    shouldSleep = 0

    def get_frame_value(x):
        nonlocal shouldSleep
        if(shouldSleep == 1):
            time.sleep(.1)
        else:
            shouldSleep = 1
            
        check, frame = webcam.read()

        key = cv2.waitKey(1)

        avg_color_per_row = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # avg_color_per_row = numpy.linalg.norm(frame, axis=2)

        z = numpy.zeros((avg_color_per_row.shape[1],avg_color_per_row.shape[0]))     

        # specify circle parameters: centre ij and radius
        ci,cj=z.shape[0] / 2,z.shape[1] / 2

        # Create index arrays to z
        I,J=numpy.meshgrid(numpy.arange(z.shape[0]),numpy.arange(z.shape[1]))


        # calculate distance of all points to centre
        dist=numpy.sqrt((I-ci)**2+(J-cj)**2)
        # print(dist)

        # print(avg_color_per_row.shape, dist.shape)

        avg_color = numpy.average(avg_color_per_row, axis=0,weights=dist)

        dot_color =  numpy.average(avg_color).item()

        return dot_color

    result = numpy.average(numpy.array(list(map(get_frame_value, range(0, 3)))))

    if os.path.exists(webcam_config_last_path):
        with open(webcam_config_last_path, "r+") as lastFile:
            lastFileValue = lastFile.readline()
            if(len(lastFileValue) > 0):
                last_color = float(lastFileValue)
                lastFile.seek(0)
                lastFile.write(str(result))
                lastFile.truncate()

                return result / last_color
            else:
                lastFile.write(str(result))
                return 1.0
    else:
        with open(webcam_config_last_path, "w+") as lastFile:
            lastFile.write(str(result))

            return 1.0