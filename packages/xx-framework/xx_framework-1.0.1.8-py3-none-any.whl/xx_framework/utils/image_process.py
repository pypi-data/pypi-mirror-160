from numpy import array as np_array
from numpy import max as np_max
from numpy import uint8 as np_uint8
from PIL import Image
from sklearn.cluster import KMeans


class ImageProcess:
    @classmethod
    def convert_l(cls, image):
        return image.convert("L")

    @classmethod
    def crop_image(cls, image):
        width, height = image.size
        if width == height:
            return image
        elif width > height:
            box = (abs(width - height) // 2, 0, abs(width + height) // 2, height)
        else:
            box = (0, abs(width - height) // 2, width, abs(width + height) // 2)
        return image.crop(box)

    @classmethod
    def resize_image(cls, image):
        return image.resize((99, 99))

    @classmethod
    def reduce_image(cls, image):
        image_array = np_array(image)
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(image_array.reshape((-1, 1)))
        new_image = kmeans.cluster_centers_[kmeans.labels_].reshape(image_array.shape).astype(np_uint8)
        new_image[new_image < np_max(new_image)] = 0
        new_image[new_image != 0] = 255
        return Image.fromarray(new_image)
