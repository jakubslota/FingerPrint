import cv2
import numpy as np


def finger(f1,f2,typ):
    best_score = counter = 0
    image = kp1 = kp2 = mp = None
    sift = cv2.SIFT_create()
    finger = cv2.imread(f1)
    finger2 = cv2.imread(f2)
    keypoints_1, des1 = sift.detectAndCompute(finger, None)
    keypoints_2, des2 = sift.detectAndCompute(finger2, None)
    matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(des1, des2, k = 2)
    color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    match_points = []
    result = None
    for p, q in matches:
        if p.distance < 0.1 * q.distance:
            match_points.append(p)

        keypoints = 0
        if len(keypoints_1) <= len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)
        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            image = finger2
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points
    if typ == 1:
        if len(match_points) > 0:
            napis = cv2.imread('assets/frame0/napis.PNG')
            result = cv2.drawMatches(finger, kp1, image, kp2, mp, None)
            res= result.shape
            dim=(res[1],50)
            text = "Dopasowanie " + str(round(best_score))
            napis = cv2.resize(napis, dim, interpolation = cv2.INTER_AREA)
            org = (170, 25)
            napis = cv2.putText(napis, text, org, font, 1, color, 1, cv2.LINE_AA, False)
            result = np.concatenate((result, napis), axis=0)
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            brak = cv2.imread('assets/frame0/brak.PNG')
            cv2.imshow("Result", brak)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    elif typ == 2:
        return best_score