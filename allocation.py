import cv2
import numpy as np
import os
import masking


CAMP_CAPS = {'blue': 4, 'pink': 3, 'grey': 2} 
SHAPE_SCORES = {'Star': 3, 'Triangle': 2, 'Square': 1} 
MED_SCORES = {'Severe': 3, 'Mild': 2, 'Safe': 1} 

def process_rescue_mission(image_path):
    img = cv2.imread(image_path)
    if img is None: return None
    
    
    hsv = cv2.cvtColor(cv2.GaussianBlur(img, (5,5), 0), cv2.COLOR_BGR2HSV)
    
    
    ocean_mask = cv2.inRange(hsv, np.array([90, 50, 50]), np.array([130, 255, 255]))
    land_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))

    segmented_img = img.copy()
    segmented_img[ocean_mask > 0] = [255, 0, 0]  
    segmented_img[land_mask > 0] = [0, 255, 255] 

   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    casualties = []
    camps_pos = {'pink': None, 'blue': None, 'grey': None}

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        M = cv2.moments(cnt)
        if M["m00"] == 0: continue
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        
        
        if len(approx) > 8:
            color = img[cy, cx]
            if color[2] > 200 and color[1] < 200: camps_pos['pink'] = (cx, cy)
            elif color[0] > 200: camps_pos['blue'] = (cx, cy)
            elif sum(color)/3 > 150: camps_pos['grey'] = (cx, cy)
            continue

       
        shape = None
        if len(approx) == 3: shape = 'Triangle'
        elif len(approx) == 4: shape = 'Square'
        elif len(approx) > 4: shape = 'Star'

        if shape:
            center_color = img[cy, cx]
            med = 'Safe'
            if center_color[2] > 200: med = 'Severe'
            elif center_color[1] > 200 and center_color[2] > 200: med = 'Mild'

            casualties.append({
                'pos': (cx, cy),
                'details': [shape, med],
                'priority': SHAPE_SCORES[shape] * MED_SCORES[med], # 
                'med_val': MED_SCORES[med]
            })

     
    casualties.sort(key=lambda x: (x['priority'], x['med_val']), reverse=True)
    
    allocation = {'blue': [], 'pink': [], 'grey': []}
    for c in casualties:
        best_camp = None
        min_dist = float('inf')
        for color, pos in camps_pos.items():
            if pos and len(allocation[color]) < CAMP_CAPS[color]:
                dist = np.sqrt((c['pos'][0]-pos[0])**2 + (c['pos'][1]-pos[1])**2)
                if dist < min_dist:
                    min_dist = dist
                    best_camp = color
        if best_camp: allocation[best_camp].append(c)

    return segmented_img, allocation, len(casualties)


input_folder, output_folder = r'C:\Users\scorp\OneDrive\cv based rescue mission\dataset',  r'C:\Users\scorp\OneDrive\cv based rescue mission\masked'
if not os.path.exists(output_folder): os.makedirs(output_folder)

image_ratios = []
for img_name in sorted(os.listdir(input_folder)):
    path = os.path.join(input_folder, img_name)
    res = process_rescue_mission(path)
    if not res: continue
    
    seg_img, alloc, total_count = res
    cv2.imwrite(os.path.join(output_folder, 'seg_' + img_name), seg_img)

   
    blue_p = sum(c['priority'] for c in alloc['blue'])
    pink_p = sum(c['priority'] for c in alloc['pink'])
    grey_p = sum(c['priority'] for c in alloc['grey'])
    pr = (blue_p + pink_p + grey_p) / total_count if total_count > 0 else 0
    image_ratios.append((img_name, pr))

    
    details = [ [c['details'] for c in alloc['blue']], 
                [c['details'] for c in alloc['pink']], 
                [c['details'] for c in alloc['grey']] ]
    
    print(f"{img_name} Details: {details}")
    print(f"Camp Priorities: {[blue_p, pink_p, grey_p]}, Avg Pr: {pr:.3f}\n")


image_ratios.sort(key=lambda x: x[1], reverse=True)
print("Images by Rescue Ratio (Descending):", [x[0] for x in image_ratios])

def generate_final_outputs(all_processed_images):
    

    image_results = []

    for data in all_processed_images:
        name = data['name']
        alloc = data['allocation']
        count = data['total_casualties']

        
        image_n = [
            [[c['age_score'], c['med_score']] for c in alloc['blue']],
            [[c['age_score'], c['med_score']] for c in alloc['pink']],
            [[c['age_score'], c['med_score']] for c in alloc['grey']]
        ]

        
        blue_sum = sum(c['age_score'] * c['med_score'] for c in alloc['blue'])
        pink_sum = sum(c['age_score'] * c['med_score'] for c in alloc['pink'])
        grey_sum = sum(c['age_score'] * c['med_score'] for c in alloc['grey'])
        camp_priority = [blue_sum, pink_sum, grey_sum]

       
        total_priority = sum(camp_priority)
        pr = total_priority / count if count > 0 else 0

        image_results.append({
            'name': name,
            'image_n': image_n,
            'camp_priority': camp_priority,
            'pr': pr
        })

        print(f"{name}_n = {image_n}")
        print(f"Camp_priority = {camp_priority}")
        print(f"Priority_ratio = {total_priority}/{count} = {pr:.3f}\n")

    
    image_results.sort(key=lambda x: x['pr'], reverse=True)
    print(f"image_by_rescue_ratio = {[res['name'] for res in image_results]}")