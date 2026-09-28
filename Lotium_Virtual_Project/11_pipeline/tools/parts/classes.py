"""Pixel color classes for Lotium masters (HSV rules tuned on LTM_*_MASTER_v001)."""
import cv2
import numpy as np

BG, SKIN, HAIR, CREAM, DARK, CYAN, ORANGE_DARK, EYE = range(8)
NAMES = ["bg", "skin", "hair_orange", "cream", "dark", "cyan", "orange_shadow", "eye"]
COLORS = [(255, 255, 255), (255, 200, 170), (255, 140, 30), (230, 225, 200), (30, 30, 40),
          (60, 240, 255), (180, 80, 10), (150, 60, 200)]


def classify(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV_FULL).astype(np.int32)
    h, s, v = hsv[..., 0] * 360 // 256, hsv[..., 1], hsv[..., 2]
    lab = np.zeros(rgb.shape[:2], np.uint8)
    lab[:] = CREAM
    lab[(v < 90)] = DARK
    lab[(s > 110) & (h >= 15) & (h <= 50) & (v >= 150)] = HAIR
    lab[(s > 110) & (h >= 5) & (h <= 40) & (v >= 90) & (v < 150)] = ORANGE_DARK
    lab[(s > 25) & (s <= 110) & (h >= 0) & (h <= 40) & (v >= 170)] = SKIN
    lab[(s > 90) & (h >= 165) & (h <= 200) & (v >= 120)] = CYAN
    # background: near white connected to the image border
    white = ((s < 18) & (v > 240)).astype(np.uint8)
    n, cc = cv2.connectedComponents(white)
    border = set(np.unique(np.concatenate([cc[0], cc[-1], cc[:, 0], cc[:, -1]]))) - {0}
    lab[np.isin(cc, list(border))] = BG
    return lab


def preview(lab):
    return np.array(COLORS, np.uint8)[lab]
