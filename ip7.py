import cv2
import threading
from datetime import datetime
import time

# from utils.service.TFLiteFaceAlignment import * 
# from utils.service.TFLiteFaceDetector import * 
# from utils.functions import *

# fd = UltraLightFaceDetecion("utils/service/weights/RFB-320.tflite", conf_threshold=0.98)

class VideoCaptureAsync:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # Default resolutions of the frame are obtained (system dependent)
        # scale_ratio = 0.3
        scale_ratio = 1
        self.frame_width = int(self.cap.get(3) * scale_ratio)
        self.frame_height = int(self.cap.get(4) * scale_ratio)

        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[ERROR] Asynchronous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            # frame = cv2.resize(frame, (self.frame_width, self.frame_height))

            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            grabbed = self.grabbed
            frame = self.frame
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def release(self):
        self.cap.release()





if __name__ == '__main__':

    # rtsp_stream_link = "rtsp://admin:vkist123456@192.168.1.120:1001/Streaming/Channels/101"

    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.24:554/profile2/media.smp" #Sanh tang 1 cua sau
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@123.16.55.212:61555/profile2/media.smp"
    rtsp_stream_link = "rtsp://admin:Phunggi@911@10.1.8.200:61555/profile2/media.smp"


    # Loi ko truy cap dc rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.27:554/profile2/media.smp" #Sanh tang 1 cua truoc
    
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.50:554/profile2/media.smp" #Sanh tang 3 BT
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.56:554/profile2/media.smp" #Sanh tang 4 IT/BT

    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.60:554/profile2/media.smp" #bai gui xe R2
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.63:554/profile2/media.smp" #bai gui xe R2

    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.61:554/profile2/media.smp" #bai gui xe A2
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.62:554/profile2/media.smp" #bai gui xe A2

    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.64:554/profile2/media.smp" #bai gui xe R3
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.66:554/profile2/media.smp" #Sanh tang 4 R3
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.73:554/profile2/media.smp" #Sanh tang 2 R3


    # rtsp_stream_link = "rtsp://admin:Phunggi@911@192.168.3.77:554/profile2/media.smp" #Sanh thang may tang 1 A1
    # rtsp_stream_link = "rtsp://admin:Phunggi@911@123.16.55.212:61054/profile2/media.smp"

    # rtsp_stream_link = "rtsp://admin:vkist123@192.168.2.130:554/Streaming/Channels/101?transportmode=unicast&profile=Profile_1"
    # rtsp_stream_link = "rtsp://admin:vkist123@123.16.55.212:61055/Streaming/Channels/101?transportmode=unicast&profile=Profile_1"

    cap = VideoCaptureAsync(rtsp_stream_link)
    cap.start()

    # video_dst_dir = 'videos/'
    # record_time = datetime.fromtimestamp(time.time())
    # year = '20' + record_time.strftime('%y')
    # month = record_time.strftime('%m')
    # date = record_time.strftime('%d')
    # record_time = str(record_time).replace(' ', '_').replace(':', '_')
    # size = (cap.frame_width, cap.frame_height)
    # record_screen = cv2.VideoWriter(video_dst_dir + 'record_' + record_time + '.avi', 
    #                 cv2.VideoWriter_fourcc(*'MJPG'),
    #                 10, size)

    # video_stream_widget.save_frame()
    while True:
        try:
            ret, frame = cap.read()
            # Display the frame
            # temp_resized_boxes, _ = fd.inference(frame)
            # draw_box(frame, temp_resized_boxes, color=(125, 255, 125))

            # if len(temp_resized_boxes) > 0:
            #     print('Found {} face(s)'.format(len(temp_resized_boxes)))
            #     record_screen.write(frame)
            cv2.imshow("IP Camera Stream", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except AttributeError:
            pass

    cap.stop()
    cap.release()