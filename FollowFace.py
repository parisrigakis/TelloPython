from tello import Tello
import cv2
import pygame
import time

# Face recognition cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Speed of the drone
S = 30


class FrontEnd(object):

    def __init__(self):
        # Init pygame
        pygame.init()

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10
        self.faceFound = False
        self.send_rc_control = True


    def run(self):

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        frame_read = self.tello.get_frame_read()
        if self.tello.takeoff():
            print('Takeoff successfull')
        self.tello.connect()
        star = time.time()

        while True:
            # if time.time() - star > 10:
                # self.tello.connect()
                # star = time.time()
            pygame.event.pump()
            frame = frame_read.frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 10, minSize=(65, 65))
            for (x, y, w, h) in faces:
                self.faceFound = True
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cx = (2*x+w)/2
                cy = (2*y+h)/2
                faceSize = (w+h)/2
            if self.faceFound:
                yaw_dif = abs(cx - 480)
                updo_dif = abs(cy - 360)
                face_dif = abs(faceSize - 140)
                sign_yaw = (cx - 480)/yaw_dif
                sign_updo = (360 - cy)/updo_dif
                sign_face = (140 - faceSize)/face_dif
                if yaw_dif > 65:
                    self.yaw_velocity = sign_yaw*S#*(yaw_dif/65)
                else:
                    self.yaw_velocity = 0

                if updo_dif > 45:
                    self.up_down_velocity = sign_updo*S#*(updo_dif/45)
                else:
                    self.up_down_velocity = 0
                if face_dif > 35:
                    self.for_back_velocity = sign_face*S#*(face_dif/35)
                else:
                    self.for_back_velocity = 0
            else:
                self.for_back_velocity = 0
                self.yaw_velocity = 0
                self.up_down_velocity = 0
            self.update()
            cv2.imshow('img', frame)
            frame_read.out.write(frame)
            self.faceFound = False
            k = cv2.waitKey(30) & 0xff
            if k==27:
                break


        self.tello.end()
        frame_read.out.release()
        frame_read.cap.release()
        cv2.destroyAllWindows()
        return 0


    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
