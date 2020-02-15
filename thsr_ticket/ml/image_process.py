import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures


def show(data):
    plt.imshow(data)
    plt.show()

def blur(img, size=3):
    return cv2.medianBlur(img, size)

def find_start_end(img):
    s_bar = np.average(img[:, :3], axis=2)
    ws, _ = np.where(s_bar<100)
    start_y = ws[-1]

    e_bar = np.average(img[:,-3:], axis=2)
    es, _ = np.where(e_bar<100)
    end_y = es[-1]
    return start_y, end_y

def linear_func(sy, ey, length=122):
    delta = (ey-sy)/length
    func = lambda x: delta*x + sy
    return [np.round(func(i)).astype('int') for i in range(length)]

def _find_bound(img, sy, ey, up_b=3):
    y = linear_func(sy, ey, img.shape[1])
    low_b = -2
    impt = 0.9
    for i in range(1, img.shape[1]):
        y_center = np.round(impt*y[i-1] + (1-impt)*y[i]).astype('int')
        rr = range(y_center+low_b, y_center+up_b)
        chunk = np.average(img[rr, i], axis=1)
        diff = [abs(chunk[i]-chunk[i-1]) for i in range(1, len(chunk))]
        max_diff = max(diff)
        max_idx = diff.index(max_diff) if max_diff>50 else -low_b
        yi = max_idx + rr[0]
        y[i] = min(y[i], yi)
    return y

def find_bound(img, sy, ey):
    result = []
    for up_b in range(1, 4):
        result.append(_find_bound(img, sy, ey, up_b=up_b))

    end_ys = [abs(y[-1]-ey) for y in result]
    #end_ys.reverse()
    #min_diff = len(result)-end_ys.index(min(end_ys))-1
    min_diff = end_ys.index(min(end_ys))-1
    return result[min_diff]

def adjust_line(img, y):
    yy = y.copy()
    toler = 2
    th = 150
    for i in range(len(y)):
        for ii in range(1, toler+1):
            last_v = np.average(img[yy[i], i])
            cur_v = np.average(img[yy[i]+ii, i])
            if abs(cur_v-last_v) > th:
                yy[i] = yy[i]+ii
                break
    return yy

def find_line(img, y):
    rx = np.arange(len(y))
    x = PolynomialFeatures(degree=2).fit_transform(rx[:, np.newaxis])
    model = Ridge().fit(x, y)
    yy = np.round(model.predict(x)).astype('int')
    return adjust_line(img, yy)

def eliminate_line(image):
    dst = cv2.fastNlMeansDenoisingColored(image, None, 30, 30 , 7 , 21)
    sy, ey = find_start_end(dst)
    fdst = np.where(dst<150, 0, dst)
    y = find_bound(fdst, sy, ey)
    x = np.arange(fdst.shape[1])
    dy = find_line(fdst, y)

    img = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    yy = adjust_line(img, np.array(dy)-4)
    for i in range(len(dy)):
        img[yy[i]:dy[i], i] = 255 - img[yy[i]:dy[i], i]
    return img

def clean_img(img):
    img = eliminate_line(img.copy())
    dst = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)
    blur_img = blur(dst, 3)
    _, thresh = cv2.threshold(blur_img, 127, 255, 0)
    return thresh

def draw_contour(cnt, img_shape):
    img = np.zeros(img_shape)
    x = cnt[:,:,0]
    y = cnt[:,:,1]
    img[y, x] = 255
    return img

def extract(img):
    ''' 
    Original from: https://github.com/uranus4ever/Captcha-Crack/blob/master/captcha_generator.py#L56
    extract the 4 codes from img
    :param img: cv2 imread BGR Image
    :return: regions contains (x, y, w, h)
    '''
    clean = clean_img(img)

    # find the contours (continuous blobs of pixels) the image
    contours, _ = cv2.findContours(clean.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    letter_image_regions = []
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        if (w < 10) or (h < 10):
            continue

        if (x == 0) and (y == 0):
            remove = np.where(contour[:,0,0]==0)[0]
            contour = np.delete(contour, remove, axis=0)
            remove = np.where(contour[:,0,0]==clean.shape[1]-1)
            contour = np.delete(contour, remove, axis=0)
            (x, y, w, h) = cv2.boundingRect(contour)

        letter_image_regions.append((x, y, w, h))

    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[2]*x[3], reverse=True)[:4]

    letters = []
    for region in letter_image_regions:
        x, y, w, h = region
        image = clean[y:y+h, x:x+w]
        letters.append(image)

    return letter_image_regions, letters

if __name__ == "__main__":
    image = cv2.imread("captcha8.png")
    regions, letters = extract(image)
    img = clean_img(image)
    show(image)
    show(img)
    for l in letters:
        show(l)
