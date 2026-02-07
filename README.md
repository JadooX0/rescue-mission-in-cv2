# rescue-mission-in-cv2
The project requires you to apply advanced image processing techniques using OpenCV and NumPy to solve a complex resource allocation problem. The Environment (Segmentation)The first step is to partition the image into two primary regions:Ocean: Represented by the blue regions.Land: Represented by the brown or green regions.Output Requirement: You must produce an image for each input that overlays unique colors on these two segments to demonstrate successful partition.2. Feature Detection and ClassificationYou must identify various "areas of interest" (geometric shapes) and categorize them based on their physical appearance and color:Casualties (Passengers):Children: Denoted by star shapes (Priority Score: 3).Elderly: Denoted by triangle shapes (Priority Score: 2).Adults: Denoted by square shapes (Priority Score: 1).Emergency Levels (Color Coding):Red: Severe condition (Score: 3).Yellow: Mild condition (Score: 2).Green: Safe (Score: 1).Rescue Pads: Denoted by circles. There are three in total: two on land and one in the water.
3. The Assignment Algorithm (The "Allocator")The core objective is to assign each casualty to the "best possible" rescue pad while respecting strict capacity limits.+1Camp Capacities: Pink (3 casualties), Blue (4 casualties), and Grey (2 casualties).Scoring Logic: Assignments are based on a formula you devise that considers Priority Score ($Casualty \times Emergency$) and the Distance between the casualty and the camp.Tie-Breaking: If priority scores are equal, the casualty with the higher medical emergency score must be prioritized.4. Evaluation and MetricsBeyond the code itself, project is based on its analytical output for a set of 10 input images:Rescue Ratio ($P_r$): For each image, you must calculate the average priority by summing all camp priorities and dividing by the total number of casualties.Ranking: You must provide a final list of the image names sorted in descending order of their 

HOW TO USE:

1. Prerequisites and Setup
Before running the code, ensure your development environment is ready.
Operating System: While Windows can be used, installing Ubuntu in a disk partition is highly encouraged for future tasks within the society.
Python Installation: Ensure Python 3.10 is installed on your system.
Library Installation: You must install NumPy for numerical computations and OpenCV for image processing tasks.
Install via terminal: pip install opencv-python numpy.

2. Data Preparation
The system is designed to process 10 aerial images of a shipwreck scenario.
Input Folder: Create a folder named inputs (dataset) in your project directory.
Image Format: Place the 10 input images(dataset) in this folder. These images should contain the ocean (blue), land (green/brown), geometric-shaped casualties, and circular rescue pads.

3. Running the MissionExecute your Python script (e.g., python allocation.py) to trigger the autonomous workflow:
 The script will first partition the image into land and ocean segments by overlaying two unique colors.Detection: It will then identify casualties—Stars (Children), Triangles (Elderly), and Squares (Adults)—and their condition based on color (Red: Severe, Yellow: Mild, Green: Safe).Allocation: The system calculates a priority score ($Priority = \text{Casualty Score} \times \text{Emergency Score}$) and assigns casualties to the Pink, Blue, or Grey rescue pads based on proximity and camp capacity.
