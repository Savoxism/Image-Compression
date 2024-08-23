import numpy as np
from PIL import Image

class ColorAnalyzer:
    def __init__(self, img):
        self.img = img.convert('RGB')
        self.X = np.array(self.img).reshape(-1, 3).astype(float) / 255.0

    def find_closest_centroids(self, centroids):
        K = centroids.shape[0]
        m = self.X.shape[0]
        idx = np.zeros(m, dtype=int)
        for i in range(m):
            distances = np.linalg.norm(self.X[i] - centroids, axis=1)
            idx[i] = np.argmin(distances)
        return idx

    def compute_centroids(self, idx, K):
        centroids = np.zeros((K, self.X.shape[1]))
        for i in range(K):
            centroids[i] = np.mean(self.X[idx == i], axis=0)
        return centroids

    def init_centroids(self, K):
        randidx = np.random.permutation(self.X.shape[0])
        return self.X[randidx[:K]]

    def run_kMeans(self, K, max_iters=10):
        centroids = self.init_centroids(K)
        for i in range(max_iters):
            idx = self.find_closest_centroids(centroids)
            centroids = self.compute_centroids(idx, K)
        return centroids, idx

    def most_common_colors(self, num_colors=10, max_iters=10):
        centroids, _ = self.run_kMeans(num_colors, max_iters)
        # Denormalize the centroids back to 0-255 range
        cluster_centers = (centroids * 255).astype(int)
        cluster_hex_codes = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in cluster_centers]
        return cluster_hex_codes

# Example usage:
# img = Image.open('path_to_your_image.jpg')
# analyzer = ColorAnalyzer(img)
# common_colors = analyzer.most_common_colors()
# print(common_colors)