import fingerprint_feature_extractor
import cv2

def minucje(path):
    img = cv2.imread(path, 0)
    FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=1, invertImage=False, showResult=False, saveResult=False)

    image = cv2.imread(path)
    color=(255,0,0)
    for i in FeaturesTerminations:
        center_coordinates =(i.locY,i.locX)
        image = cv2.circle(image, center_coordinates, 4, color, 2)
    return image