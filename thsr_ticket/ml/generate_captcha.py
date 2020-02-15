import os
import random
import time
from typing import List, Union

import numpy as np  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw  # type: ignore
from sklearn.linear_model import Ridge  # type: ignore
from sklearn.preprocessing import PolynomialFeatures  # type: ignore

CHARS = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"


class GenerateCaptcha:
    def __init__(
            self,
            width: int = 145,
            height: int = 55,
            font_size: int = 50
        ) -> None:
        self._width = width
        self._height = height
        self._font_size = font_size
        self._mode = "L"  # 8-bit pixel
        #self._font = ImageFont.truetype("tahoma.ttf", size=font_size-10)
        self._font = ImageFont.truetype("calibri.ttf", size=font_size)

    def generate(self) -> Union[Image.Image, List]:
        image = Image.new(self._mode, (self._width, self._height), color=255)
        chars = [s for s in CHARS]
        c_list = np.random.choice(chars, size=4, replace=False)
        image = self.draw_characters(image, c_list)
        image = self.add_arc(image)
        image = self.add_noise(image)
        image = self.add_sp_noise(image)
        return image, c_list

    def add_noise(self, img: Image.Image, color_bound: int = 80) -> Image.Image:
        arr = np.array(img)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                cur_c = arr[i, j]
                c = random.randint(0, color_bound)
                arr[i, j] = cur_c-c if cur_c>color_bound else cur_c+c
        return Image.fromarray(arr)

    def add_sp_noise(self, img: Image.Image, prob: float = 0.03) -> Image.Image:
        arr = np.array(img)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                p = random.random()
                if p < prob:
                    arr[i, j] = 0 if arr[i, j] > 128 else 255
        return Image.fromarray(arr)
    
    def add_arc(self, img: Image.Image) -> Image.Image:
        arr = np.array(img)
        start = random.randint(20, 25)
        diff = random.randint(15, 18)
        y = [start, start-diff//2, start-diff]
        rx = np.array([0, random.randint(32, 38), arr.shape[1]])
        x = PolynomialFeatures(degree=2).fit_transform(rx[:, np.newaxis])
        model = Ridge().fit(x, y)
        xx = np.arange(arr.shape[1])
        x = PolynomialFeatures(degree=2).fit_transform(xx[:, np.newaxis])
        yy = np.round(model.predict(x)).astype('int')
        for i in range(len(xx)):
            ry = range(yy[i]-2, yy[i]+2)
            val = np.where(arr[ry, xx[i]]<128, 255, 0)
            arr[ry, xx[i]] = val
        return Image.fromarray(arr)

    def _draw_character(self, img: Image.Image, c: str) -> Image.Image:
        w, h = self._font_size-6, self._font_size-6 #Draw(img).textsize(c, font=self._font)

        dx = random.randint(0, 6)
        dy = random.randint(0, 6)
        im = Image.new(self._mode, (w + dx, h + dy), color=255)
        Draw(im).text((dx, dy), c, font=self._font, fill=0)

        # rotate
        im = im.crop(im.getbbox())
        im = im.rotate(random.uniform(-10, 5), Image.BILINEAR, expand=1, fillcolor=255)

        # warp
        ddx = w * random.uniform(0.1, 0.2)
        ddy = h * random.uniform(0.1, 0.2)
        x1 = int(random.uniform(-ddx, ddx))
        y1 = int(random.uniform(-ddy, ddy))
        x2 = int(random.uniform(-ddx, ddx))
        y2 = int(random.uniform(-ddy, ddy))
        w2 = w + abs(x1) + abs(x2)
        h2 = h + abs(y1) + abs(y2)
        data = (
            x1, y1,
            -x1, h2 - y2,
            w2 + x2, h2 + y2,
            w2 - x2, -y1,
        )
        im = im.resize((w2, h2))
        im = im.transform((w, h), Image.QUAD, data, fill=255, fillcolor=255)
        return im

    def draw_characters(self, img: Image.Image, chars: List[str]) -> Image.Image:
        images = []
        for c in chars:
            images.append(self._draw_character(img, c))

        text_width = sum([im.size[0] for im in images])

        width = max(text_width, self._width)
        #img = img.resize((width, self._height))

        average = int(text_width / len(chars))
        rand = int(0.1 * average)
        offset = int(average * 0.1)

        table = [150 for i in range(256)]
        for idx, im in enumerate(images):
            w, h = Draw(im).textsize(chars[idx], font=self._font)
            mask = im.point(table)
            img.paste(im, (offset, (self._height - h) // 2), mask)
            offset = offset + w + random.randint(-rand, 0)

        h_offset = 4
        arr = np.array(img)[h_offset:-h_offset, :offset+w//3]
        arr = np.where(arr<255, 0, 255)
        return Image.fromarray(arr)

def generate_captcha(num_caps: int, save_path: str = None) -> None:
    captcha = GenerateCaptcha()
    for i in range(num_caps):
        img, c_list = captcha.generate()
        if save_path is not None:
            path = os.path.join(save_path, "{}.png".format(i))
            img.convert("RGB").save(path)

if __name__ == "__main__":
    captcha = GenerateCaptcha()
    start_t = time.time()
    img, c_list = captcha.generate()
    diff_t = time.time() - start_t
    print("".join(c_list), diff_t)
    img.show()
    #plt.imshow(np.array(img))
    #plt.show()