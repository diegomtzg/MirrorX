import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import os

# necessary for API to work
KEY = '81ded80172f64edeaa94d3057a25892c'
CF.Key.set(KEY)
BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)


# our defined constants
PERSON_GROUP_ID = 'mirror-pg'


#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


def createPerson(personName, imagePaths):
    res = CF.person.create(PG_ID, person_name)
    PERSON_ID = res['personId']
    for imagePath in imagePaths:
        print("Adding %s's face at %s" % (personName, imagePath))
        CF.person.add_face(imagePath, PERSON_GROUP_ID, PERSON_ID)

# identify the faces in the image at imgPath and return the personIds
# if return_names is true, return names of the people instead.
def identifyPersonInImage(imgPath, return_names=False):
    faces = CF.face.detect(imgPath)
    faceIds = list(map(lambda face: face['faceId'], faces))
    if faceIds == []:    return []
    # print(faceIds)
    identifiedFaces = CF.face.identify(faceIds, PERSON_GROUP_ID, max_candidates_return=1)
    # print(identifiedFaces)
    candidateIds = list(map(lambda candidate:  
                            candidate['candidates'][0]['personId']
                            if len(candidate['candidates']) > 0 else 
                            None
                        , identifiedFaces))
    candidateIds = list(filter(lambda id: id != None, candidateIds))
    # print(candidateIds)
    if return_names:
        candidateNames = list(map(lambda id: 
                                  CF.person.get(PERSON_GROUP_ID, id)['name']
                                  , candidateIds))
        # print(candidateNames)
        return candidateNames
    return candidateIds

def getPerson(id):
    return CF.person.get(PERSON_GROUP_ID, id)

def trainPerson(id):
    import cv2
    cam = cv2.VideoCapture(0)
    imgPath = 'data/tmpface.jpg'
    
    # adds the picture of the camera
    def addInstantPicture():
        _, im = cam.read()
        cv2.imwrite(imgPath, im)
        CF.person.add_face(imgPath, PERSON_GROUP_ID, id)

    for i in range(10):
        print("Adding pictures.... %d" % i)
        addInstantPicture()
        
    cv2.destroyAllWindows()
    CF.person_group.train(PERSON_GROUP_ID)

# if __name__ == '__main__':
    

    # identifyPersonInImage('Data/detection1.jpg')
    # for i in range(3,4):
    #     identify_test_path = ('Data/identification%d.jpg' % i)
    #     faces = CF.face.detect(identify_test_path)

    #     img = Image.open(identify_test_path)
    #     draw = ImageDraw.Draw(img)
    #     for face in faces:
    #         draw.rectangle(getRectangle(face), outline='red')
    #         identified = CF.face.identify([face['faceId']], PG_ID, max_candidates_return=1)
    #         print("identified %s as %s" % (face['faceId'], identified))

    #         draw.text(getRectangle(face)[0], CF.person.get(PG_ID, identified[0]['candidates'][0]['personId'])['name'])
            
    #     img.show()
