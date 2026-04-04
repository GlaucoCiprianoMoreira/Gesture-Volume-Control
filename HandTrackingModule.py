import cv2
import mediapipe as mp
import time
import numpy as np
from mediapipe.tasks.python.vision import drawing_utils, drawing_styles
from mediapipe.tasks.python.components.containers import NormalizedLandmark

class handDetector():
    """
    A modernized Hand Tracking module operating natively on the MediaPipe Tasks Vision API.
    Specifically designed as a drop-in replacement for deprecated mp.solutions frameworks.
    """
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        
        # In the modern Tasks API, confidence thresholds are strictly evaluated as pure floating-point metrics.
        self.detectionCon = float(detectionCon)
        self.trackCon = float(trackCon)
        
        # MediaPipe Tasks API Base Initialization
        BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Configuring the core options object.
        # The 'hand_landmarker.task' bundle must reside in the local execution directory.
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=self.maxHands,
            min_hand_detection_confidence=self.detectionCon,
            min_hand_presence_confidence=self.trackCon,
            min_tracking_confidence=self.trackCon
        )
        
        # Instantiate the landmarker pipeline securely using the factory pattern
        self.landmarker = self.HandLandmarker.create_from_options(options)
        
        # Initialize rendering utilities natively adapted for the new data structures
        self.mp_drawing = drawing_utils
        self.mp_drawing_styles = drawing_styles
        self.mp_hands = mp.tasks.vision.HandLandmarksConnections
        
        self.results = None

    def findHands(self, img, draw=True):
        """
        Ingests a raw BGR image matrix, processes the topological hand mapping, 
        and optionally renders annotated spatial nodes onto the visual canvas.
        """
        # Hardware optical arrays must be actively transformed to SRGB compliance
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Matrix data must be encapsulated into the proprietary MediaPipe Image protocol
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        
        # The VIDEO running mode requires a strictly monotonic chronological marker
        timestamp_ms = int(time.time() * 1000)
        
        # Execute the C++ inference backend, blocking the current execution thread safely
        self.results = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        # Parse the structured detection_result and execute node rendering
        if self.results and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                if draw:
                                         
                    self.mp_drawing.draw_landmarks(
                        img, 
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Translates the normalized floating-point coordinate space into a discrete 
        two-dimensional pixel space required for absolute geometric analysis.
        """
        lmList = []
        bbox = []
        xList = []
        yList = []
        
        if self.results and self.results.hand_landmarks:
            # Structurally prevent sequence index out-of-bounds exceptions
            if handNo < len(self.results.hand_landmarks):
                myHand = self.results.hand_landmarks[handNo]
                h, w, c = img.shape
                
                # Iterate through the 21 unique topological nodes
                for id, lm in enumerate(myHand):
                    # Projection execution from the [0.0, 1.0] fractional domain to exact integer pixel dimensions
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    lmList.append([id, cx, cy])
                    
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                
                # Derive dynamic tracking bounding box parameters based on spatial extrema
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
                
                if draw:
                    cv2.rectangle(
                        img, 
                        (bbox[0] - 20, bbox[1] - 20),
                        (bbox[2] + 20, bbox[3] + 20), 
                        (0, 255, 0), 2
                    )
        
        return lmList, bbox