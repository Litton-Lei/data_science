
import cv2



def get_video_pic(input,output):
    cap = cv2.VideoCapture(input)
    cap.set(1, int(cap.get(7)/2)) # 取它的中间帧
    rval, frame = cap.read() # 如果rval为False表示这个视频有问题，为True则正常
    if rval:
        cv2.imwrite(output, frame)  # 存储为图像
    cap.release()

get_video_pic("1.mp4",'2.jpg')
