import os
import cv2
import numpy as np
import glob

# 📂 Directorios
INPUT_DIR = "images"
OUTPUT_DIR = "output"
OUTPUT_NOISY = os.path.join(OUTPUT_DIR, "noisy")
OUTPUT_GT = os.path.join(OUTPUT_DIR, "gt")

# 🛠️ Crear carpetas de salida si no existen
os.makedirs(OUTPUT_NOISY, exist_ok=True)
os.makedirs(OUTPUT_GT, exist_ok=True)

# 🔍 Buscar imágenes .tif y .tiff
image_paths = sorted(glob.glob(os.path.join(INPUT_DIR, "*.tif"))) + \
              sorted(glob.glob(os.path.join(INPUT_DIR, "*.tiff")))

print("📂 Buscando imágenes en:", INPUT_DIR)
print("📄 Archivos encontrados:", image_paths)
print(f"✅ Se cargaron {len(image_paths)} imágenes.\n")

if len(image_paths) == 0:
    raise ValueError("No se encontraron imágenes en la carpeta 'images'.")

# 🖼️ Leer imágenes en escala de grises
images = []
for path in image_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        print(f"✅ Imagen cargada: {os.path.basename(path)} - forma: {img.shape}")
        images.append(img)
    else:
        print(f"⚠️ No se pudo leer la imagen: {path}")

# 🚩 Seleccionar imagen base
base_image = images[0]
h, w = base_image.shape
base_name = os.path.splitext(os.path.basename(image_paths[0]))[0]

# 🔄 Escalar imágenes para registro (más rápido)
scale = 0.5  # usa 0.25 si aún es lento
small_w, small_h = int(w * scale), int(h * scale)
small_base = cv2.resize(base_image, (small_w, small_h))

registered_images = [base_image]

print("\n🔄 Registrando imágenes al tamaño base... (versión rápida)")

criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 500, 1e-5)

for i in range(1, len(images)):
    img = images[i]
    small_img = cv2.resize(img, (small_w, small_h))

    warp_matrix = np.eye(2, 3, dtype=np.float32)
    try:
        cc, warp_matrix = cv2.findTransformECC(small_base, small_img, warp_matrix, cv2.MOTION_EUCLIDEAN, criteria)
        # Aplicar transformación a imagen original completa
        registered = cv2.warpAffine(img, warp_matrix, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        registered_images.append(registered)
        print(f"✅ Imagen {i+1} registrada correctamente.")
    except cv2.error as e:
        print(f"⚠️ Error registrando imagen {i+1}: {e}")
        registered_images.append(img)

# 🧮 Fusionar por media
print("\n🧮 Fusionando imágenes por media...")
stack = np.stack(registered_images, axis=0)
fusion_image = np.mean(stack, axis=0).astype(np.uint8)

# ✂️ Recorte 512x512 (centrado)
crop_size = 512
start_x = (w - crop_size) // 2
start_y = (h - crop_size) // 2

base_cropped = base_image[start_y:start_y + crop_size, start_x:start_x + crop_size]
fusion_cropped = fusion_image[start_y:start_y + crop_size, start_x:start_x + crop_size]

print(f"✂️ Recorte aplicado: {crop_size}x{crop_size}")

# 💾 Guardar resultados
path_noisy = os.path.join(OUTPUT_NOISY, f"{base_name}_noisy.tif")
path_gt = os.path.join(OUTPUT_GT, f"{base_name}_gt.tif")

cv2.imwrite(path_noisy, base_cropped)
cv2.imwrite(path_gt, fusion_cropped)

print(f"\n💾 Guardado:")
print(" -", path_noisy)
print(" -", path_gt)
print("\n✅ Dataset generado con éxito en 'output/' 🎉")

import matplotlib.pyplot as plt

# --- Verificación visual ---
plt.figure(figsize=(12, 4))

# Imagen base (ruidosa)
plt.subplot(1, 3, 1)
plt.imshow(base_cropped, cmap='gray')
plt.title('Imagen Base (Noisy)')
plt.axis('off')

# Imagen fusionada (ground truth)
plt.subplot(1, 3, 2)
plt.imshow(fusion_cropped, cmap='gray')
plt.title('Ground Truth (Media)')
plt.axis('off')

# Superposición para ver alineación
overlay = cv2.addWeighted(
    base_cropped.astype(np.float32) / 255, 0.5,
    fusion_cropped.astype(np.float32) / 255, 0.5, 0
)

plt.subplot(1, 3, 3)
plt.imshow(overlay, cmap='gray')
plt.title('Superposición')
plt.axis('off')

plt.tight_layout()

# Mostrar ventana
plt.show()

# Guardar imagen comparativa
comparison_path = os.path.join(OUTPUT_DIR, "comparacion.png")
plt.savefig(comparison_path, bbox_inches='tight')
print(f"✅ Comparación visual guardada en: {comparison_path}")

