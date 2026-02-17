import cv2
import numpy as np

def cervix_contour_overlay(bgr: np.ndarray,
                           contour_color=(0, 255, 0),
                           thickness=4):
    """
    Retorna:
      overlay: imagen original con el contorno dibujado
      mask: máscara interna (por si quieres depurar)
    """

    h, w = bgr.shape[:2]

    # 1) Suavizado
    blur = cv2.GaussianBlur(bgr, (7, 7), 0)

    # 2) (Opcional) reducir brillos (specular highlights)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)
    glare = ((V > 220) & (S < 60)).astype(np.uint8) * 255
    glare = cv2.dilate(glare, np.ones((5, 5), np.uint8), iterations=1)
    img = cv2.inpaint(blur, glare, 3, cv2.INPAINT_TELEA)

    # 3) Máscara por color en LAB (baseline)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)

    # Umbrales iniciales (AJUSTA si tu cámara cambia mucho)
    # A alto => más rojizo/rosado. L evita sombras.
    mask = ((A > 145) & (L > 60)).astype(np.uint8) * 255

    # 4) Limpieza morfológica
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k, iterations=1)

    # 5) Elegir el mejor contorno
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = bgr.copy()

    if not cnts:
        return overlay, mask  # no encontró nada

    img_cx, img_cy = w / 2.0, h / 2.0

    def score(cnt):
        area = cv2.contourArea(cnt)
        if area < -0.01 * (h * w):
            return -1e9
        x, y, ww, hh = cv2.boundingRect(cnt)
        cx, cy = x + ww/2.0, y + hh/2.0
        dist = np.hypot(cx - img_cx, cy - img_cy)
        # grande y relativamente centrado
        return area - 3.0 * dist

    best = max(cnts, key=score)

    # 6) Dibujar contorno sobre la imagen original
    cv2.drawContours(overlay, [best], -1, contour_color, thickness)

    return overlay, mask


if __name__ == "__main__":
    img = cv2.imread("Cervix segmentacion/Pacientes_imagenes/Paciente4/Captura_2.jpg")  # tu imagen
    overlay, mask = cervix_contour_overlay(img, contour_color=(0, 255, 0), thickness=4)

    cv2.imwrite("cervix_contour.png", overlay)
    cv2.imwrite("debug_mask.png", mask)
