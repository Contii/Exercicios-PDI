import os
import cv2

class VectorOfMats:
    def __init__(self):
        self.images = []  # Lista para armazenar as imagens
        self.image_names = []  # Lista para armazenar os nomes dos arquivos das imagens

    # Adicione uma imagem à lista de imagens
    def add_image(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            self.images.append(image)
            self.image_names.append(os.path.basename(image_path))  # Armazene o nome do arquivo
            return True
        else:
            return False
    def get_images(self):
        return self.images
    
# Exemplo de uso
if __name__ == '__main__':
    vec_of_mats = VectorOfMats()