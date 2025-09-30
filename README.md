# Reto: Creación del Dataset SAR Despeckling

Este repositorio contiene el desarrollo del reto **“Creación del dataset”**, basado en el artículo:

**Dataset for speckle filter**  
[https://www.sciencedirect.com/science/article/pii/S2352340924000398](https://www.sciencedirect.com/science/article/pii/S2352340924000398)

y su procedimiento para **rescalizado, registro y recorte de imágenes SAR** con ruido *speckle*, siguiendo la metodología planteada por los autores para generar pares de imágenes:  
- **Imagen con ruido (Noisy / SAR)**  
- **Ground Truth (GT)** – obtenida por fusión.

--- 

##  Objetivo del reto
Generar un **dataset propio** de imágenes SAR de **512x512 píxeles** en pares (`Noisy` y `Ground Truth`), mediante el procesamiento de 5 imágenes `.tiff` con ruido *speckle*.

---

##  Metodología aplicada

### 1. **Selección de imágenes**
- Se utilizaron **5 imágenes SAR no filtradas** en formato `.tiff`.
- Todas se encuentran alineadas espacialmente (mismo campo de visión).

### 2. **Selección de imagen base**
- Se elige la **primera imagen** como referencia.
- Esta imagen será la versión **Noisy**, y servirá para alinear las demás.

### 3. **Registro (alineación)**
- Se usa el método de **registro por correlación mejorada** `cv2.findTransformECC()` de OpenCV.
- Se alinean las 4 imágenes restantes respecto a la base.
- Se reduce la escala de procesamiento para optimizar tiempo sin perder precisión.

### 4. **Fusión**
- Se aplica una operación de **media pixel a pixel** sobre las imágenes alineadas.
- Resultado: una imagen con menor ruido, considerada el **Ground Truth (GT)**.

### 5. **Recorte**
- Ambas imágenes (Noisy y GT) se **recortan** al centro con tamaño **512x512 píxeles**, cumpliendo el requisito del dataset.

### 6. **Almacenamiento**
- Los resultados se guardan en:     

output/
├── noisy/
│ └── base_noisy.tif
├── gt/
│ └── base_gt.tif
└── comparacion.png

Resultados obtenidos

Imágenes generadas

- Imagen Noisy (SAR): conserva el ruido speckle característico.
- Imagen Ground Truth: presenta una reducción significativa del ruido, manteniendo detalles estructurales.}

Comparación visual (output/comparacion.png)
Imagen Base(Noisy)	Ground Truth (Media)	Superposición

En la superposición se observa una alineación precisa:
no hay desplazamientos ni doble borde, lo que confirma un registro exitoso.

Análisis del resultado:

- La operación de media suaviza el ruido speckle sin eliminar detalles importantes.
- La alineación previa evita que la fusión genere desenfoques.
- El tamaño estándar de 512x512 facilita el uso en redes neuronales y modelos de filtrado.

Comparación con el artículo original:

| Aspecto            | Artículo original         | Este trabajo              |
| ------------------ | ------------------------- | ------------------------- |
| Número de imágenes | 10                        | 5                         |
| Fusión             | Media (average)           | Media (average)           |
| Registro           | Sí (ECC)                  | Sí (ECC OpenCV)           |
| Tamaño final       | 512x512                   | 512x512                   |
| Resultado          | Dataset alineado y limpio | Dataset alineado y limpio |

Conclusiones:

- Se logró generar un dataset propio con pares Noisy / Ground Truth alineados.
- La fusión por media reduce eficazmente el ruido speckle.
- El recorte estándar de 512x512 permite su uso en tareas de entrenamiento supervisado.
- El uso de OpenCV para registro y procesamiento resultó eficiente y reproducible.
- La comparación visual confirma una alineación precisa y una reducción de ruido satisfactoria
- Al generar imagenes por pixel el consumo es mayor, lento y menos optimo que al hacerlo por el recorte estandar.

Autores:

Jennifer Lotero y Valentin Colorado
Estudiantes de Ingeniería Informática
Politécnico Colombiano Jaime Isaza Cadavid
2025