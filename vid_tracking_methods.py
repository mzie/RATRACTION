# import necessary packages and modules
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
from collections import deque

def on_mouse(event,x,y,flags,params):

    global rect,startPoint,endPoint

    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:

        if startPoint == True and endPoint == True:
            startPoint = False
            endPoint = False
            rect = (0,0,0,0)
        
        if startPoint == False:
            rect = (x,y,0,0)
            startPoint = True
        elif endPoint == False:
            rect = (rect[0], rect[1], x, y)
            endPoint = True


def live_pixels_to_cm(camera):

    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = frame.array
        
        frame = cv2.resize(frame, (400, 200))

        cv2.namedWindow("Live Camera Feed")
        cv2.setMouseCallback("Live Camera Feed", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Live Camera Feed", frame)

        key = cv2.waitKey(50) & 0xFF

        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = frame.copy()
            if rect[0] < rect[2]:
                if rect[0] > 4:
                    x1 = rect[0]-5
                else:
                    x1 = rect[0]
                if rect[2] < 396:
                    x2 = rect[2]+5
                else:
                    x2 = rect[2]
            elif rect[0] > rect[2]:
                if rect[2] > 4:
                    x1 = rect[2]-5
                else:
                    x1 = rect[2]
                if rect[0] < 396:
                    x2 = rect[0]+5
                else:
                    x2 = rect[0]
            if rect[1] < rect[3]:
                if rect[1] > 4:
                    y1 = rect[1]-5
                else:
                    y1 = rect[1]
                if rect[3] < 196:
                    y2 = rect[3]+5
                else:
                    y2 = rect[3]
            elif rect[1] > rect[3]:
                if rect[3] > 4:
                    y1 = rect[3]-5
                else:
                    y1 = rect[3]
                if rect[1] < 196:
                    y2 = rect[1]+5
                else:
                    y2 = rect[1]
            cropped_arena_pic = uncropped_arena_pic[y1:y2, x1:x2]
            cv2.imshow("Picture of Arena", cropped_arena_pic)
            key = cv2.waitKey(1)
            if key == 27:
                break

        rawCapture.truncate(0)

    cv2.destroyAllWindows()
    return ((rect[0],rect[1]),(rect[2],rect[3]))


def vid_pixels_to_cm(video_name):
    
    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    cap = cv2.VideoCapture('more sample videos.mp4')

    # reading the first frame
    (grabbed, frame) = cap.read()

    while(cap.isOpened()):

        (grabbed, frame) = cap.read()

        if not grabbed:
            break

        frame = cv2.resize(frame, (400,200))

        cv2.namedWindow("Video Feed")
        cv2.setMouseCallback("Video Feed", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Video Feed", frame)

        key = cv2.waitKey(50) & 0xFF

        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = frame.copy()
            if rect[0] < rect[2]:
                if rect[0] > 4:
                    x1 = rect[0]-5
                else:
                    x1 = rect[0]
                if rect[2] < 396:
                    x2 = rect[2]+5
                else:
                    x2 = rect[2]
            elif rect[0] > rect[2]:
                if rect[2] > 4:
                    x1 = rect[2]-5
                else:
                    x1 = rect[2]
                if rect[0] < 396:
                    x2 = rect[0]+5
                else:
                    x2 = rect[0]
            if rect[1] < rect[3]:
                if rect[1] > 4:
                    y1 = rect[1]-5
                else:
                    y1 = rect[1]
                if rect[3] < 196:
                    y2 = rect[3]+5
                else:
                    y2 = rect[3]
            elif rect[1] > rect[3]:
                if rect[3] > 4:
                    y1 = rect[3]-5
                else:
                    y1 = rect[3]
                if rect[1] < 196:
                    y2 = rect[1]+5
                else:
                    y2 = rect[1]
            cropped_arena_pic = uncropped_arena_pic[y1:y2, x1:x2]
            cv2.imshow("Picture of Arena", cropped_arena_pic)
            key = cv2.waitKey(1)
            if key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    return ((rect[0],rect[1]),(rect[2],rect[3]))


def live_cap_arena_pic(camera, arena_pic_name):

    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = frame.array
        
        frame = cv2.resize(frame, (400, 200))

        cv2.namedWindow("Live Camera Feed")
        cv2.setMouseCallback("Live Camera Feed", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Live Camera Feed", frame)

        key = cv2.waitKey(50) & 0xFF

        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = frame.copy()
            if rect[0] < rect[2]:
                    x1 = rect[0]
                    x2 = rect[2]
            elif rect[0] > rect[2]:
                    x1 = rect[2]
                    x2 = rect[0]
            if rect[1] < rect[3]:
                    y1 = rect[1]
                    y2 = rect[3]
            elif rect[1] > rect[3]:
                    y1 = rect[3]
                    y2 = rect[1]
            cropped_arena_pic = uncropped_arena_pic[y1:y2, x1:x2]
            cv2.imshow("Picture of Arena", cropped_arena_pic)
            key = cv2.waitKey(1)
            cv2.imwrite(arena_pic_name, cropped_arena_pic)
            if key == 27:
                break

        rawCapture.truncate(0)

    cv2.destroyAllWindows()
    return None


def vid_cap_arena_pic(video_name, arena_pic_name):
    
    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    cap = cv2.VideoCapture(video_name)

    # reading the first frame
    (grabbed, frame) = cap.read()

    while(cap.isOpened()):

        (grabbed, frame) = cap.read()

        if not grabbed:
            break

        frame = cv2.resize(frame, (400,200))

        cv2.namedWindow("Video Feed")
        cv2.setMouseCallback("Video Feed", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Video Feed", frame)

        key = cv2.waitKey(50) & 0xFF

        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = frame.copy()
            if rect[0] < rect[2]:
                    x1 = rect[0]
                    x2 = rect[2]
            elif rect[0] > rect[2]:
                    x1 = rect[2]
                    x2 = rect[0]
            if rect[1] < rect[3]:
                    y1 = rect[1]
                    y2 = rect[3]
            elif rect[1] > rect[3]:
                    y1 = rect[3]
                    y2 = rect[1]
            cropped_arena_pic = uncropped_arena_pic[y1:y2, x1:x2]
            cv2.imshow("Picture of Arena", cropped_arena_pic)
            key = cv2.waitKey(1)
            cv2.imwrite(arena_pic_name, cropped_arena_pic)
            if key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    return None


##def live_pixels_to_cm(camera):
##    global frame, roiPts, inputMode
##
##    frame = None
##    roiPts = []
##    inputMode = False
##
##    def selectROI(event, x, y, flags, param):
##        global frame, roiPts, inputMode
##
##        if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
##            roiPts.append((x,y))
##            cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
##            cv2.imshow("frame", frame)
##
##    rawCapture = PiRGBArray(camera, size=(640, 480))
##
##    # allow the camera to warmup
##    time.sleep(0.1)
##
##    cv2.namedWindow("frame")
##    cv2.setMouseCallback("frame", selectROI)
##
##    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
##
##        frame = frame.array
##        
##        frame = cv2.resize(frame, (400, 200))
##
##        cv2.imshow("frame", frame)
##        key = cv2.waitKey(1)
##
##        if key == ord("i") and len(roiPts) < 4:
##            inputMode = True
##            orig = frame.copy()
##
##            while len(roiPts) < 4:
##                cv2.imshow("frame", frame)
##                cv2.waitKey(0)
##
##            roiPts = np.array(roiPts)
##            s = roiPts.sum(axis = 1)
##            tl = tuple(roiPts[np.argmin(s)])
##            br = tuple(roiPts[np.argmax(s)])
##
##        rawCapture.truncate(0)
##
##        if key == 27:
##            break
##
##    cv2.destroyAllWindows()
##    return (tl,br)


##def vid_pixels_to_cm(video_name):
##    global frame, roiPts, inputMode
##
##    frame = None
##    roiPts = []
##    inputMode = False
##
##    def selectROI(event, x, y, flags, param):
##        global frame, roiPts, inputMode
##
##        if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
##            roiPts.append((x,y))
##            cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
##            cv2.imshow("frame", frame)
##
##    cap = cv2.VideoCapture(video_name)
##
##    cv2.namedWindow("frame")
##    cv2.setMouseCallback("frame", selectROI)
##
##    while(cap.isOpened()):
##        ret, frame = cap.read()
##
##        if not ret:
##                break
##
##        frame = cv2.resize(frame, (400, 200))
##
##        cv2.imshow("frame", frame)
##        key = cv2.waitKey(1)
##
##        if key == ord("i") and len(roiPts) < 4:
##            inputMode = True
##            orig = frame.copy()
##
##            while len(roiPts) < 4:
##                cv2.imshow("frame", frame)
##                cv2.waitKey(0)
##
##            roiPts = np.array(roiPts)
##            s = roiPts.sum(axis = 1)
##            tl = tuple(roiPts[np.argmin(s)])
##            br = tuple(roiPts[np.argmax(s)])
##
##        if key == 27:
##            break
##
##    cap.release()
##    cv2.destroyAllWindows()
##    return (tl,br)


def live_capture_ref_image(camera, ref_image_name):
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = frame.array
            
        image = cv2.resize(frame, (400, 200))
            
        cv2.imshow("Live Camera Feed", image)
    
        key = cv2.waitKey(1)
        if key == 27:
            break
    
        if key == ord("i"):
            ref_image = image.copy()
            cv2.imshow("Reference Image", ref_image)
            key = cv2.waitKey(1)
            if key == 27:
                break
    
        rawCapture.truncate(0)

    cv2.imwrite(ref_image_name, ref_image)
    cv2.destroyAllWindows()
    return None  


def vid_capture_ref_image(video_name):
    cap = cv2.VideoCapture(video_name)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.resize(frame, (400, 200))
        
        cv2.imshow("Video Feed", image)
        
        k = cv2.waitKey(1)
        if k == 27:
            break

        if k == ord('i'):
            ref_image = image.copy()
            cv2.imshow("Reference Image", ref_image)
            k = cv2.waitKey(1)
            if k == 27:
                break

    cv2.imwrite(ref_image_name, ref_image)
    cap.release()
    cv2.destroyAllWindows()
    return None


def live_colour_calib(camera):
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = frame.array
            
        image = cv2.resize(frame, (400, 200))
            
        cv2.imshow("Live Camera Feed", image)
    
        k = cv2.waitKey(1)
        if k == 27:
                break
    
        if k == ord('i'):
    
            def nothing(x):
                    pass
                    
            cv2.namedWindow("mask")
    
            # create trackbars for color change
            cv2.createTrackbar('Hl', 'mask', 0, 179, nothing)
            cv2.createTrackbar('Hu', 'mask', 179, 179, nothing)
    
            cv2.createTrackbar('Sl', 'mask', 0, 255, nothing)
            cv2.createTrackbar('Su', 'mask', 255, 255, nothing)
    
            cv2.createTrackbar('Vl', 'mask', 0, 255, nothing)
            cv2.createTrackbar('Vu', 'mask', 255, 255, nothing)
    
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            while True:
                hl = cv2.getTrackbarPos('Hl', 'mask')
                sl = cv2.getTrackbarPos('Sl', 'mask')
                vl = cv2.getTrackbarPos('Vl', 'mask')
    
                hu = cv2.getTrackbarPos('Hu', 'mask')
                su = cv2.getTrackbarPos('Su', 'mask')
                vu = cv2.getTrackbarPos('Vu', 'mask')
    
                lower_b = np.array([hl, sl, vl])
                upper_b = np.array([hu, su, vu])
    
                mask = cv2.inRange(hsv, lower_b, upper_b)
                                                    
                cv2.imshow("mask", mask)
                k = cv2.waitKey(1)
                if k == ord('i'):
                    break

        try:
            tracking_preview = image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            live_mask = cv2.inRange(hsv_image, lower_b, upper_b)
            
            _, cnts, _ = cv2.findContours(live_mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

            centre = None
       
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use it to
                # compute the centroid
                c = max(cnts, key=cv2.contourArea)
                M = cv2.moments(c)
                try:
                    centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                    cv2.circle(tracking_preview, centre, 5, (255,0,0), -1)
                except:
                    pass
            
            cv2.imshow("Live Camera Tracking Preview", tracking_preview)
            k = cv2.waitKey(1)
            if k == 27:
                break
        except:
            pass

        rawCapture.truncate(0)
               
    cv2.destroyAllWindows()
    return ([hl,sl,vl],[hu,su,vu])


def vid_colour_calib(video_name):
    cap = cv2.VideoCapture(video_name)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.resize(frame, (400, 200))
        
        cv2.imshow("Video Feed", image)

        k = cv2.waitKey(1)
        if k == 27:
                break

        if k == ord('i'):

            def nothing(x):
                    pass
            
            cv2.namedWindow("mask")

            # create trackbars for color change
            cv2.createTrackbar('Hl', 'mask', 0, 179, nothing)
            cv2.createTrackbar('Hu', 'mask', 179, 179, nothing)

            cv2.createTrackbar('Sl', 'mask', 0, 255, nothing)
            cv2.createTrackbar('Su', 'mask', 255, 255, nothing)

            cv2.createTrackbar('Vl', 'mask', 0, 255, nothing)
            cv2.createTrackbar('Vu', 'mask', 255, 255, nothing)

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            while True:
                hl = cv2.getTrackbarPos('Hl', 'mask')
                sl = cv2.getTrackbarPos('Sl', 'mask')
                vl = cv2.getTrackbarPos('Vl', 'mask')

                hu = cv2.getTrackbarPos('Hu', 'mask')
                su = cv2.getTrackbarPos('Su', 'mask')
                vu = cv2.getTrackbarPos('Vu', 'mask')

                lower_b = np.array([hl, sl, vl])
                upper_b = np.array([hu, su, vu])

                mask = cv2.inRange(hsv, lower_b, upper_b)
                                        
                cv2.imshow("mask", mask)
                k = cv2.waitKey(1)
                if k == ord('i'):
                    break

        try:
            tracking_preview = image.copy()
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            live_mask = cv2.inRange(hsv_image, lower_b, upper_b)
            
            _, cnts, _ = cv2.findContours(live_mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

            centre = None
       
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use it to
                # compute the centroid
                c = max(cnts, key=cv2.contourArea)
                M = cv2.moments(c)
                try:
                    centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                    cv2.circle(tracking_preview, centre, 5, (255,0,0), -1)
                except:
                    pass
            
            cv2.imshow("Video Feed Tracking Preview", tracking_preview)
            k = cv2.waitKey(1)
            if k == 27:
                break
        except:
            pass

    cap.release() 
    cv2.destroyAllWindows()
    return ([hl,sl,vl],[hu,su,vu])


def live_camera_feed(camera, recording=False, record_name=None):
    tme = deque()

    rawCapture = PiRGBArray(camera, size=(640, 480))

    if recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(record_name, fourcc, 30.0, (400, 200))

    # allow the camera to warmup
    time.sleep(0.1)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        if not _isRunning:
            break

        frame = frame.array

        image = cv2.resize(frame, (400, 200))

        if recording:
            # write the frame
            out.write(image)

        millis = float(time.time())
        current_time = millis - start
        tme.append(round(current_time, 2))

        cv2.imshow("Live Camera Feed", image)
        cv2.waitKey(1)

        rawCapture.truncate(0)

        from OneStopTrack import _isRunning

    if recording:
        out.release()
    cv2.destroyAllWindows()
    return (tme)


def video_feed(video_name):
    tme = deque()
        
    cap = cv2.VideoCapture(video_name)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning

    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.resize(frame, (400, 200))

        millis = float(time.time())
        current_time = millis - start
        tme.append(round(current_time, 2))

        cv2.imshow("Video Feed", image)
        cv2.waitKey(1)

        from OneStopTrack import _isRunning

    cap.release()
    cv2.destroyAllWindows()
    return tme


def live_mog_tracking(camera, vidTrack_setup_parameters, recording=False, record_name=None):
    tme = deque()
    pts = deque()
    
    global mod_pts
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']
    
    rawCapture = PiRGBArray(camera, size=(640, 480))

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    if recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(record_name, fourcc, 30.0, (400, 200))

    # allow the camera to warmup
    time.sleep(0.1)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        if not _isRunning:
            break

        frame = frame.array

        image = cv2.resize(frame, (400, 200))

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fgmask = fgbg.apply(mask)

        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

        #opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        _, cnts, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)

        centre = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
                # find the largest contour in the mask, then use it to
                # compute the centroid
                c = max(cnts, key=cv2.contourArea)
                M = cv2.moments(c)
                try:
                    centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                    cv2.circle(image, centre, 5, (255,0,0), -1)
                except:
                    pass

        millis = float(time.time())
        current_time = millis - start

        if centre != None:
            tme.append(round(current_time, 2))

            pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))
    
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)
                                     
        cv2.imshow("Live Camera Tracking", image)
        cv2.waitKey(1)

        if recording:
            # write the frame
            out.write(image)

        rawCapture.truncate(0)

        from OneStopTrack import _isRunning

    if recording:
        out.release()
    cv2.destroyAllWindows()
    return (tme, mod_pts)

        
def vid_mog_tracking(video_name, vidTrack_setup_parameters):
    tme = deque()
    pts = deque()
    
    global mod_pts, mod_pt
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']
    
    cap = cv2.VideoCapture(video_name)

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    start = float(time.time())

    #global _isRunning
    #from OneStopTrack import _isRunning
    import OneStopTrack
    _isRunning = OneStopTrack._isRunning

    #while(cap.isOpened())
    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.resize(frame, (400, 200))

        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                
        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fgmask = fgbg.apply(mask)
    
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    
        #opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    
        _, cnts, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
        centre = None
            
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use it to
            # compute the centroid
            c = max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            try:
                centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
    
                cv2.circle(image, centre, 5, (255,0,0), -1)
            except:
                pass

        millis = float(time.time())
        current_time = millis - start

        if centre != None:
            tme.append(round(current_time, 2))

            pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))

            mod_pt = mod_pts[-1]

        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)
                                         
        cv2.imshow("Video Feed Tracking", image)
        cv2.waitKey(1)

        #from OneStopTrack import _isRunning
        _isRunning = OneStopTrack._isRunning

    cap.release()
    cv2.destroyAllWindows()
    return (tme, mod_pts)


def live_fd_tracking(camera, vidTrack_setup_parameters, recording=False, record_name=None):
    tme = deque()
    pts = deque()
    
    global mod_pts
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']

    ref_image_name = vidTrack_setup_parameters['reference_image_name']
    
    rawCapture = PiRGBArray(camera, size=(640, 480))

    ref_image = cv2.imread(ref_image_name)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    hsv_ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)
    ref_image_mask = cv2.inRange(hsv_ref_image, lower_b, upper_b)

    if recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(record_name, fourcc, 30.0, (400, 200))

    # allow the camera to warmup
    time.sleep(0.1)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        if not _isRunning:
            break

        frame = frame.array

        image = cv2.resize(frame, (400, 200))

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fdmask = cv2.absdiff(mask, ref_image_mask)

        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

        #opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        _, cnts, _ = cv2.findContours(fdmask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)

        centre = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use it to
            # compute the centroid
            c = max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            try:
                centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                cv2.circle(image, centre, 5, (255,0,0), -1)
            except:
                pass

        millis = float(time.time())
        current_time = millis - start

        if centre != None:
            tme.append(round(current_time, 2))

            pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))
    
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)
                                     
        cv2.imshow("Live Camera Tracking", image)
        cv2.waitKey(1)

        if recording:
            # write the frame
            out.write(image)

        rawCapture.truncate(0)

        from OneStopTrack import _isRunning
    
    if recording:
        out.release()
    cv2.destroyAllWindows()
    return (tme, mod_pts)


def vid_fd_tracking(video_name, vidTrack_setup_parameters):
    tme = deque()
    pts = deque()
    
    global mod_pts
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']

    ref_image_name = vidTrack_setup_parameters['reference_image_name']
    
    ref_image = cv2.imread(ref_image_name)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    hsv_ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)

    ref_image_mask = cv2.inRange(hsv_ref_image, lower_b, upper_b)

    cap = cv2.VideoCapture(video_name)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning

    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.resize(frame, (400, 200))

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fdmask = cv2.absdiff(mask, ref_image_mask)

        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

        #opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        _, cnts, _ = cv2.findContours(fdmask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)

        centre = None
       
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use it to
            # compute the centroid
            c = max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            try:
                centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                cv2.circle(image, centre, 5, (255,0,0), -1)
            except:
                pass

        millis = float(time.time())
        current_time = millis - start

        if centre != None:
            tme.append(round(current_time, 2))

            pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))
    
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)
                             
        cv2.imshow("Video Feed Tracking", image)
        cv2.waitKey(1)

        from OneStopTrack import _isRunning
    
    cap.release()
    cv2.destroyAllWindows()
    return (tme, mod_pts)
