import cv2
import numpy as np

class VectorOfMats:
    def __init__(self):
        self.images = []

    def add_image(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            self.images.append(image)
            return True
        else:
            return False

    # converte a imagem para outro espaço de cores
    def convert_color(self, index, color_conversion):
        if 0 <= index < len(self.images):
            self.images[index] = cv2.cvtColor(self.images[index], color_conversion)

    # aplica um filtro à imagem
    def apply_filter(self, index, kernel):
        if 0 <= index < len(self.images):
            self.images[index] = cv2.filter2D(self.images[index], -1, kernel)

    # detecta bordas na imagem em escala de cinza
    def detect_edges(self, index, low_threshold, high_threshold):
        if 0 <= index < len(self.images):
            gray = cv2.cvtColor(self.images[index], cv2.COLOR_BGR2GRAY)
            self.images[index] = cv2.Canny(gray, low_threshold, high_threshold)

    # binarize a imagem em escala de cinza
    def binarize(self, index, threshold):
        if 0 <= index < len(self.images):
            gray = cv2.cvtColor(self.images[index], cv2.COLOR_BGR2GRAY)
            _, binary_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            self.images[index] = binary_img

    # aplica uma operação de morfologia matemática à imagem
    def apply_morphology(self, index, operation, kernel):
        if 0 <= index < len(self.images):
            if operation == 'dilate':
                self.images[index] = cv2.dilate(self.images[index], kernel, iterations=1)
            elif operation == 'erode':
                self.images[index] = cv2.erode(self.images[index], kernel, iterations=1)

    # salve as imagens processadas
    def save_images(self, output_folder):
        for i, img in enumerate(self.images):
            cv2.imwrite(f"{output_folder}/image_{i}.png", img)

# Exemplo de uso
if __name__ == '__main__':
    vec_of_mats = VectorOfMats()

    # Adicione imagens ao vetor
    vec_of_mats.add_image('../Media/Lenna.png')
    vec_of_mats.add_image('../Media/bocha.JPG')
    vec_of_mats.add_image('../Media/galinha.png')
    vec_of_mats.add_image('../Media/borboleta.jpg')
    
    # Converta a primeira imagem para escala de cinza
    vec_of_mats.convert_color(0, cv2.COLOR_BGR2GRAY)

    # Aplique um filtro à segunda imagem
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]], dtype=np.float32)
    vec_of_mats.apply_filter(1, kernel)

    # Detecte bordas na primeira imagem
    vec_of_mats.detect_edges(1, 100, 200)

    # Binarize a quarta imagem
    vec_of_mats.binarize(4, 128)

    # Aplique morfologia matemática de dilatação na segunda imagem
    kernel = np.ones((5, 5), np.uint8)
    vec_of_mats.apply_morphology(2, 'dilate', kernel)

    # Salve as imagens processadas
    vec_of_mats.save_images('../Media')