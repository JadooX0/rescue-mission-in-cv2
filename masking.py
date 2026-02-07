import cv2
import numpy as np
import os



path = r'C:\Users\scorp\OneDrive\cv based rescue mission\dataset\datasetimage1.jpeg'

img = cv2.imread(path)

if img is None:
    print("Error: Could not find or open the image at the specified path.")
else:
   
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    ocean_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_land = np.array([35, 40, 40])
    upper_land = np.array([85, 255, 255])
    land_mask = cv2.inRange(hsv, lower_land, upper_land)

   
    segmented_output = img.copy()
    

    segmented_output[land_mask > 0] = [0, 255, 255]   
    segmented_output[ocean_mask > 0] = [255, 0, 0]    

    
    cv2.imshow('Original Image', img)
    cv2.imshow('Ocean Mask', ocean_mask)
    cv2.imshow('Land Mask', land_mask)
    cv2.imshow('Segmented Output', segmented_output)

    
    cv2.imwrite('segmented_result.png', segmented_output)

    print("Image shape:", img.shape)
    print("Masking complete. Segmented image saved.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    output_dir = 'masked'

# 2. Create the directory if it doesn't already exist [cite: 91]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# 3. Define the file names for storage
# We will save the land mask, ocean mask, and the final color overlay [cite: 39]
ocean_filename = os.path.join(output_dir, 'mask_ocean.png')
land_filename = os.path.join(output_dir, 'mask_land.png')
overlay_filename = os.path.join(output_dir, 'segmented_overlay.png')

# 4. Save the images to the directory
cv2.imwrite(ocean_filename, ocean_mask)
cv2.imwrite(land_filename, land_mask)
cv2.imwrite(overlay_filename, segmented_output)

print(f"Successfully stored masks in: {output_dir}")