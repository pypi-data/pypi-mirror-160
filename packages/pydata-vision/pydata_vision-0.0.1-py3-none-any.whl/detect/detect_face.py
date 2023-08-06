import cv2
import face_recognition


class Face:
    def __init__(self, img_path):
        self.img_path = img_path

    def detect(self):
        test_image = face_recognition.load_image_file(self.img_path)
        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

        face_test = face_recognition.face_locations(test_image)[0]
        encoded_test = face_recognition.face_encodings(test_image)[0]
        cv2.rectangle(test_image, (face_test[3], face_test[0]), (face_test[1], face_test[2]), (20, 214, 17), 2)

        cv2.putText(test_image, f'{"True"}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('image', test_image)
        cv2.waitKey(0)