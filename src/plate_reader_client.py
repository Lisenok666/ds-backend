import requests
import base64
import io
import json 


class PlateReaderClient:
    def __init__(self, host: str, image_url: str):
        self.host = host
        self.image_url = image_url
        self.images_for_numbers = list()

    def load(self, imageID, res):
        try:
            res['result'] = res['result'].encode('ISO-8859-1')  
            out = open(str(imageID) + '.jpg', "wb")
            out.write(res['result'])
            out.close()
            self.images_for_numbers.append(str(imageID) + '.jpg')
        except:
            pass

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
        self.load(imageID, res)
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
        for i, key in enumerate(res.keys()):
            self.load(key.split('/')[-1], res[key])
        return res


    def script(self , images):
        if isinstance(images, int):
            res = self.load_image(images)
            print(res)
            if len(self.images_for_numbers):
                image = self.images_for_numbers.pop()
                with open('./' + image, 'rb') as im:
                    res = self.read_plate_number(im)
                    print(res)
        elif isinstance(images, list):
            res = self.load_images(images)
            print(res)
            if len(self.images_for_numbers):
                image = self.images_for_numbers.pop()
                with open('./' + image, 'rb') as im:
                    res = self.read_plate_number(im)
                    print(res)




if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080', image_url = 'http://51.250.83.169:7878/images/')
    print('TEST1')
    client.script(9965)
    print('TEST2')
    client.script([9967, 10022])
    # res = client.load_images([9967, 10022])
    # print(res)


