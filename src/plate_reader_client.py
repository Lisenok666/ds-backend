import requests
import base64
import io
import json 


class PlateReaderClient:
    def __init__(self, host: str, image_url: str):
        self.host = host
        self.image_url = image_url
        self.images_for_numbers = list()


    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return res.json()


    def greeting(self, user: str):
        res = requests.post(
            f'{self.host}/greeting',
            headers={'Content-Type': 'application/json'},
            json={
                'user':  "me",
            },
        )

        return res.json()

    def load_image(self, imageID: int):
        res = requests.post(
            f'{self.host}/loadImage',
            headers={'Content-Type': 'application/json'},
            json={
                'imageID': self.image_url + str(imageID),
            },
        )
        res = res.json()
        return res


    def load_images(self, imagesID: list):
        json_imagesID = [self.image_url + str(imageID) for imageID in imagesID]
        res = requests.post(
            f'{self.host}/loadImages',
            headers={'Content-Type': 'application/json'},
            json={
                'imagesID': json_imagesID,
            },
        )
        res = res.json()
        return res






if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080', image_url = 'http://51.250.83.169:7878/images/')
    print('TEST1')
    res = client.load_image(9965)
    print(res)
    print('TEST2')
    res = client.load_images([9967, 10022])
    print(res)


