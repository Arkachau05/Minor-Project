"""
Generate image filters visualization showing various image processing techniques
applied to detect bias in facial/image data.

This script creates a multi-panel visualization similar to academic papers,
demonstrating image processing techniques used in bias detection.
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
from scipy import ndimage

def create_sample_face_image(height=300, width=300):
    """
    Create a synthetic face-like image for demonstration.
    In production, this would be a real image from your dataset.
    """
    image = np.ones((height, width, 3), dtype=np.uint8) * 200
    
    # Create simple face-like features
    cv2.circle(image, (width//2, height//2), 80, (180, 150, 130), -1)  # Face
    cv2.circle(image, (width//2 - 30, height//2 - 20), 8, (50, 50, 50), -1)  # Left eye
    cv2.circle(image, (width//2 + 30, height//2 - 20), 8, (50, 50, 50), -1)  # Right eye
    cv2.ellipse(image, (width//2, height//2 + 30), (40, 20), 0, 0, 180, (150, 100, 80), 2)  # Mouth
    
    return image

def generate_filter_visualizations(input_image=None):
    """
    Apply various image filters to demonstrate bias detection preprocessing.
    
    Filters include:
    - Raw Crop: Original/cropped region of interest
    - Gaussian Blur: Smoothing filter
    - Canny Edges: Edge detection
    - Sobel Magnitude: Gradient magnitude
    - Adaptive Threshold: Local threshold
    - Normalized (z-score): Statistical normalization
    """
    
    # Load or create image
    if input_image is None:
        image = create_sample_face_image(400, 400)
    else:
        image = input_image
    
    # Ensure it's grayscale for processing
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # 1. Raw Crop - just the original
    raw_crop = gray.copy()
    
    # 2. Gaussian Blur
    gaussian = cv2.GaussianBlur(gray, (5, 5), 1.0)
    
    # 3. Canny Edges
    canny = cv2.Canny(gray, 50, 150)
    
    # 4. Sobel Magnitude
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_magnitude = np.sqrt(sobelx**2 + sobely**2)
    sobel_magnitude = np.uint8(255 * sobel_magnitude / np.max(sobel_magnitude))
    
    # 5. Adaptive Threshold
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # 6. Normalized (z-score)
    normalized = (gray.astype(np.float32) - np.mean(gray)) / (np.std(gray) + 1e-8)
    
    return {
        'raw_crop': raw_crop,
        'gaussian_blur': gaussian,
        'canny_edges': canny,
        'sobel_magnitude': sobel_magnitude,
        'adaptive_threshold': adaptive_thresh,
        'normalized': normalized
    }

def plot_filter_visualization(filters_dict, output_path='image_filters_visualization.png'):
    """
    Create a publication-quality multi-panel figure showing all filters.
    """
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle('Image Filters for Bias Detection Analysis', fontsize=16, fontweight='bold')
    
    # Flatten axes for easier iteration
    axes_flat = axes.flatten()
    
    filter_names = ['Raw Crop', 'Gaussian Blur', 'Canny Edges', 
                   'Sobel Magnitude', 'Adaptive Threshold', 'Normalized (z-score)']
    
    for idx, (key, name) in enumerate(zip(filters_dict.keys(), filter_names)):
        ax = axes_flat[idx]
        data = filters_dict[key]
        
        # Use appropriate colormap
        if key == 'canny_edges' or key == 'adaptive_threshold':
            im = ax.imshow(data, cmap='binary', vmin=0, vmax=255)
        elif key == 'sobel_magnitude':
            im = ax.imshow(data, cmap='hot', vmin=0, vmax=255)
        elif key == 'normalized':
            im = ax.imshow(data, cmap='RdBu_r', vmin=-3, vmax=3)
        else:
            im = ax.imshow(data, cmap='gray', vmin=0, vmax=255)
        
        ax.set_title(name, fontweight='bold')
        ax.axis('off')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=8)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_path}")
    plt.close()

def load_or_create_image(image_path=None):
    """
    Load an image from file or create a synthetic one.
    """
    if image_path and os.path.exists(image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not load {image_path}, using synthetic image")
            return create_sample_face_image()
        # Crop to square and resize
        h, w = image.shape[:2]
        size = min(h, w)
        image = image[(h-size)//2:(h-size)//2+size, (w-size)//2:(w-size)//2+size]
        image = cv2.resize(image, (400, 400))
        return image
    else:
        print("No image path provided, generating synthetic face image...")
        return create_sample_face_image()

def main():
    """
    Main function to generate image filter visualization.
    """
    # Configuration
    OUTPUT_DIR = 'outputs/images'
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Try to load a sample image, otherwise create synthetic
    # You can provide a path to a real image here
    sample_image = load_or_create_image()
    
    # Generate filter visualizations
    print("Applying image filters...")
    filters = generate_filter_visualizations(sample_image)
    
    # Create and save visualization
    output_file = os.path.join(OUTPUT_DIR, 'image_filters_roi_analysis.png')
    plot_filter_visualization(filters, output_file)
    
    print("\n✓ Image filter visualization complete!")
    print(f"  Filters applied: Raw Crop, Gaussian Blur, Canny Edges,")
    print(f"                   Sobel Magnitude, Adaptive Threshold, Normalized (z-score)")

if __name__ == '__main__':
    main()
