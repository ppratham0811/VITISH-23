import cv2
import numpy as np
import os
import pathlib


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def automatic_brightness_and_contrast(image, clip_hist_percent=10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return auto_result, alpha, beta


def detect(img_rgb):
    img = img_rgb.copy()
    input_height = img_rgb.shape[0]
    input_width = img_rgb.shape[1]
    hsv_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

    # yellow color
    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    yellow = cv2.bitwise_and(yellow_mask, yellow_mask, mask=yellow_mask)

    cv2.imwrite("temp/steps/1_yellow_color_detection.png", yellow)
    # Close morph
    k = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(yellow, cv2.MORPH_CLOSE, k)

    cv2.imwrite("temp/steps/2_closing_morphology.png", closing)
    # Detect yellow area
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # List of final crops
    crops = []

    # Loop over contours and find license plates
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Conditions on crops dimensions and area
        if h*6 > w > 2 * h and h > 0.1 * w and w * h > input_height * input_width * 0.0001:

            # Make a crop from the RGB image, the crop is slided a bit at left to detect bleu area
            crop_img = img_rgb[y:y + h, x-round(w/10):x]
            crop_img = crop_img.astype('uint8')

            # Compute bleu color density at the left of the crop
            # Bleu color condition
            try:
                hsv_frame = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
                low_bleu = np.array([100,150,0])
                high_bleu = np.array([140,255,255])
                bleu_mask = cv2.inRange(hsv_frame, low_bleu, high_bleu)
                bleu_summation = bleu_mask.sum()

            except:
                bleu_summation = 0

            # Condition on bleu color density at the left of the crop
            if bleu_summation > 550:

                # Compute yellow color density in the crop
                # Make a crop from the RGB image
                imgray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                crop_img_yellow = img_rgb[y:y + h, x:x+w]
                crop_img_yellow = crop_img_yellow.astype('uint8')

                # Detect yellow color
                hsv_frame = cv2.cvtColor(crop_img_yellow, cv2.COLOR_BGR2HSV)
                low_yellow = np.array([20, 100, 100])
                high_yellow = np.array([30, 255, 255])
                yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)

                # Compute yellow density
                yellow_summation = yellow_mask.sum()

                # Condition on yellow color density in the crop
                if yellow_summation > 255*crop_img.shape[0]*crop_img.shape[0]*0.4:

                    # Make a crop from the gray image
                    crop_gray = imgray[y:y + h, x:x + w]
                    crop_gray = crop_gray.astype('uint8')

                    # Detect chars inside yellow crop with specefic dimension and area
                    th = cv2.adaptiveThreshold(crop_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                    contours2, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    # Init number of chars
                    chars = 0
                    for c in contours2:
                        area2 = cv2.contourArea(c)
                        x2, y2, w2, h2 = cv2.boundingRect(c)
                        if w2 * h2 > h * w * 0.01 and h2 > w2 and area2 < h * w * 0.9:
                            chars += 1

                    # Condition on the number of chars
                    if 20 > chars > 4:
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        pts = np.array(box)
                        warped = four_point_transform(img, pts)
                        crops.append(warped)

                        # Using cv2.putText() method
                        #img_rgb = cv2.putText(img_rgb, 'LP', (x, y), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
                        #print(pts)
                        cv2.drawContours(img_rgb, [box], 0, (0, 0, 255), 1)

    return img_rgb, crops, pts


def detect_belg(src):
    img, alpha, beta = automatic_brightness_and_contrast(src)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    crops = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if h * 6 > w > 2 * h and h > 0.1 * w and w * h > img.shape[0] * img.shape[1] * 0.0001:
            crop = th[y:y + h, x:x + w]
            white_summation = crop.sum()
            if white_summation > w * h * 0.4 * 255:
                crop = img[y:y + h, x:x + w]
                crop_img = crop.astype('uint8')
                hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
                lower_red = np.array([160, 100, 100])
                upper_red = np.array([179, 255, 255])
                red_mask = cv2.inRange(hsv, lower_red, upper_red)
                red_summation = red_mask.sum()

                if red_summation > 510:
                    crop_img = img[y:y + h, x - round(w / 10):x + w]
                    crop_img = crop_img.astype('uint8')
                    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
                    low_bleu = np.array([100, 150, 0])
                    high_bleu = np.array([140, 255, 255])
                    bleu_mask = cv2.inRange(hsv, low_bleu, high_bleu)
                    bleu_summation = bleu_mask.sum()

                    if bleu_summation > 255:
                        crop = gray[y:y + h, x:x + w]
                        crop_img = crop.astype('uint8')
                        th2 = cv2.adaptiveThreshold(crop_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                        contours2, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        j = 0
                        for c in contours2:
                            area2 = cv2.contourArea(c)
                            x2, y2, w2, h2 = cv2.boundingRect(c)
                            if w2 * h2 > h * w * 0.01 and h2 > w2 and area2 < h * w * 0.9:
                                j += 1
                        if 12 > j > 4:
                            rect = cv2.minAreaRect(cnt)
                            box = cv2.boxPoints(rect)
                            box = np.int0(box)
                            pts = np.array(box)
                            warped = four_point_transform(src, pts)
                            crops.append(warped)
                            cv2.drawContours(src, [box], 0, (0, 255, 0), 2)
    return src, crops


def process(src):
    cv2.imwrite("temp/steps/3_detected_plate.png", src)
    adjusted, a, b = automatic_brightness_and_contrast(src)
    cv2.imwrite("temp/steps/4_Brigthness_contrast_adjustment.png", adjusted)
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp/steps/5_gray.png", gray)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("temp/steps/6_threshold.png", th)
    return th


def post_process(input_file_path):
    f = open(input_file_path, "r")
    text = f.readline()
    puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=',
              '#', '*', '+', '\\', '•', '~', '@', '£',
              '·', '_', '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›', '♥', '←', '×', '§', '″', '′',
              'Â', '█', '½', '…',
              '“', '★', '”', '–', '●', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―',
              '¥', '▓', '—', '‹', '─',
              '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', '¯', '♦', '¤', '▲', '¸', '¾',
              'Ã', '⋅', '‘', '∞',
              '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'Ø',
              '¹', '≤', '‡', '√', '«', ' ']

    for punct in puncts:
        if punct in text:
            text = text.replace(punct, '')
    f.close()
    f = open(input_file_path, "w")
    f.write(text)
    f.close()
    return text


def recognise(src_path, out_path):
    cmd = str(pathlib.Path().absolute()) + '/extra/tesseract.exe '+ src_path + ' ' + out_path + ' -l eng --psm 6 --dpi 300 --oem 1'
    os.system(cmd)
    return 0
