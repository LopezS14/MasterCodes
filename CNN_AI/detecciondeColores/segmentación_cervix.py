# cervix_blue_roi_cellpose_hsv.py
# pip install cellpose opencv-python numpy matplotlib

import cv2
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models


def centroid_from_mask(mask_255: np.ndarray):
    m = cv2.moments((mask_255 > 0).astype(np.uint8))
    if m["m00"] == 0:
        H, W = mask_255.shape[:2]
        return (W / 2.0, H / 2.0)
    return (m["m10"] / m["m00"], m["m01"] / m["m00"])


def largest_component_from_labels(label_img: np.ndarray) -> np.ndarray:
    labels, counts = np.unique(label_img, return_counts=True)
    labels = labels[labels != 0]
    counts = counts[labels != 0]
    if labels.size == 0:
        return np.zeros_like(label_img, dtype=np.uint8)
    largest = labels[np.argmax(counts)]
    return (label_img == largest).astype(np.uint8) * 255


def hsv_red_pink_mask(img_bgr: np.ndarray, s_min=35, v_min=40) -> np.ndarray:
    blur = cv2.GaussianBlur(img_bgr, (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)

    # rojo (dos bandas) + rosado/salmón
    red  = (H <= 15) | (H >= 165)
    pink = (H >= 5) & (H <= 35)

    sat_ok = (S >= s_min)
    val_ok = (V >= v_min)

    # quitar brillos blancos: V muy alto y S bajo
    spec = (V >= 235) & (S <= 50)

    mask = ((red | pink) & sat_ok & val_ok & (~spec)).astype(np.uint8) * 255

    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    k_open  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_close)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k_open)

    return mask


def pick_blue_roi_component(rp_in_cervix: np.ndarray, img_bgr: np.ndarray, cervix_mask: np.ndarray,
                           min_area=500, w_dist=1.0, w_red=1.5):
    """
    Elige la 'región azul' como el componente conectado dentro del cérvix que:
    - esté cerca del centro del cérvix (no del frame)
    - y sea más rojizo (score en LAB a*)
    """
    num, lab, stats, centroids = cv2.connectedComponentsWithStats(rp_in_cervix, connectivity=8)
    if num <= 1:
        return rp_in_cervix

    cx0, cy0 = centroid_from_mask(cervix_mask)

    # Prepara mapa de "rojizo" usando LAB (canal a*)
    lab_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    a = lab_img[:, :, 1].astype(np.float32)  # a* alto = más rojo/magenta

    best_i = None
    best_score = -1e18

    H, W = rp_in_cervix.shape[:2]
    diag2 = (H*H + W*W)  # para normalizar distancias

    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < min_area:
            continue

        cx, cy = centroids[i]
        # distancia normalizada al centro del cérvix
        d2 = (cx - cx0)**2 + (cy - cy0)**2
        dist_score = 1.0 - (d2 / diag2)  # más cerca => más grande

        # “rojizo” promedio dentro del componente
        comp = (lab == i)
        red_score = float(a[comp].mean())  # a* promedio

        # score combinado
        score = w_dist * dist_score + w_red * red_score

        if score > best_score:
            best_score = score
            best_i = i

    if best_i is None:
        # fallback: más grande
        best_i = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    return (lab == best_i).astype(np.uint8) * 255


def main(img_path: str, gpu: bool = False):
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise FileNotFoundError(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 1) Cellpose: máscara de cérvix (objeto principal)
    model = models.CellposeModel(gpu=gpu)
    masks, _, _ = model.eval(img_rgb, channels=[0, 0])  # estable en muchos casos
    cervix_mask = largest_component_from_labels(masks)

    # suaviza contorno del cérvix
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    cervix_mask = cv2.morphologyEx(cervix_mask, cv2.MORPH_CLOSE, k)

    # 2) HSV rojo/rosado
    rp_mask = hsv_red_pink_mask(img_bgr, s_min=35, v_min=40)

    # 3) restringir a dentro del cérvix
    rp_in_cervix = cv2.bitwise_and(rp_mask, rp_mask, mask=cervix_mask)

    # 4) elegir SOLO la región tipo "azul"
    blue_roi = pick_blue_roi_component(
        rp_in_cervix, img_bgr, cervix_mask,
        min_area=600, w_dist=1.0, w_red=0.015
    )
    # Nota: w_red parece “chico” porque a* está ~[0..255]. Ajuste rápido abajo.

    # 5) aplicar máscara final
    roi_bgr = cv2.bitwise_and(img_bgr, img_bgr, mask=blue_roi)
    roi_rgb = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2RGB)

    # contorno sobre original
    overlay = img_rgb.copy()
    cnts, _ = cv2.findContours(blue_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(overlay, cnts, -1, (0, 255, 255), 3)  # cian (RGB)

    # plots
    plt.figure(figsize=(16, 4))
    plt.subplot(1, 4, 1); plt.imshow(img_rgb); plt.title("Original"); plt.axis("off")
    plt.subplot(1, 4, 2); plt.imshow(cervix_mask, cmap="gray"); plt.title("Cérvix (Cellpose)"); plt.axis("off")
    plt.subplot(1, 4, 3); plt.imshow(rp_in_cervix, cmap="gray"); plt.title("Rojo/rosado dentro del cérvix (HSV)"); plt.axis("off")
    plt.subplot(1, 4, 4); plt.imshow(roi_rgb); plt.title("ROI final (solo región azul)"); plt.axis("off")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(7, 5))
    plt.imshow(overlay)
    plt.title("Contorno ROI (cian) sobre original")
    plt.axis("off")
    plt.show()

    cv2.imwrite("mask_cervix_cellpose.png", cervix_mask)
    cv2.imwrite("mask_roi_azul.png", blue_roi)
    cv2.imwrite("roi_azul.png", roi_bgr)


if __name__ == "__main__":
    main("Pacientes_imagenes/Paciente1/Captura_1.jpg", gpu=False)
