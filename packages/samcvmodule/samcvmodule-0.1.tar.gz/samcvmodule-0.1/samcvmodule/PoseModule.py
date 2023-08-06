import cv2
import mediapipe as mp
import time
import math

class PoseDetector():

    def __init__(self, mode = False, modelC = 1, smoothLm = True, enableSeg = False,
                 smoothSeg = True, minDetcon = 0.5, minTrackcon = 0.5):
        self.mode = mode
        self.modelC = modelC
        self.smoothLm = smoothLm
        self.enableSeg = enableSeg
        self.smoothSeg = smoothSeg,
        self.minDetcon = minDetcon
        self.minTrackcon = minTrackcon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.modelC, self.smoothLm, self.enableSeg,
                                     self.smoothSeg, self.minDetcon, self.minTrackcon)

    def findPose(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)


        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm) # here we are getting the value in ratio format
                # Inorder to get the values in pixel format see the below code
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw = True):

        # Get the landmars for angle
        x1, y1 = self.lmList[p1][1:] # [3, 486, 284] - this is from print(lmList) from AI Trainer project p1 = 3.
        # Alternate way for above line
        # _, x1, y1 = self.lmList[p1]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1- y2, x1 - x2))
        # print(angle)

        if angle < 0:
            angle += 360
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0), 3)
            cv2.circle(img, (x1, y1), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 17, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 17, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 17, (0, 0, 255), 2)
            # cv2.putText(img, str(int(angle)), (x2-50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        return angle

# def main():
#     cap = cv2.VideoCapture(0)
#     detector = PoseDetector()
#     pTime = 0
#     while True:
#         success, img = cap.read()
#         img = detector.findPose(img)
#         lmList = detector.findPosition(img, draw=False)
#
#         if len(lmList) != 0:
#             print(lmList[14])
#             cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
#
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#
#         cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
#         cv2.imshow("Image", img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# if __name__ == "__main__":
#     main()