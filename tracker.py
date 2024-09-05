''' This Tracker class is based on the following references, 
https://www.analyticsvidhya.com/blog/2022/04/building-vehicle-counter-system-using-opencv/
https://medium.com/@batuhansenerr/object-tracking-and-counting-for-emergency-situations-with-yolov8-82e2f4c218b6'''

import math


class Tracker:
    def __init__(self):
        # Store the center points of the detected objects
        self.center_points = {}
        # Initialize object count to zero.  This will contain the number of objects being tracked
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Calculate center point of new object from bounding box values
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Check if the object was already detected
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
             
            # Modify value of distance (currently set to 35) based on application
                if dist < 35:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # If new object is detected, assign the next available ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clear the dictionary, using center points of Ids(objects) not in view
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with center points of objects in view
        self.center_points = new_center_points.copy()
        return objects_bbs_ids