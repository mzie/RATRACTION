# import necessary packages and modules
import numpy as np
import time
import cv2
from collections import deque
import itertools

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


def live_pixels_to_cm():

    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    cap = cv2.VideoCapture(0)

    # allow the camera to warmup
    time.sleep(0.1)

    while(cap.isOpened()):
        
        ret, frame = cap.read()

        if not ret:
            print("Camera frame not returned. Camera may be missing or damaged")
            break
        
        image = cv2.resize(frame, (400, 225))

        cv2.namedWindow("Live Camera Feed")
        cv2.setMouseCallback("Live Camera Feed", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Live Camera Feed", image)
        key = cv2.waitKey(50) & 0xFF
        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = image.copy()
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


def vid_pixels_to_cm(video_name, vidTrack_setup_parameters):
    
    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    cap = cv2.VideoCapture('more sample videos.mp4')

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    # reading the first frame
    ret, frame = cap.read()

    while(cap.isOpened()):

        ret, frame = cap.read()

        if not ret:
            print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)

        cv2.namedWindow("Recorded Video")
        cv2.setMouseCallback("Recorded Video", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Recorded Video", image)
        key = cv2.waitKey(50) & 0xFF
        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = image.copy()
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


def live_cap_arena_pic(arena_pic_name):

    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    cap = cv2.VideoCapture(0)

    # allow the camera to warmup
    time.sleep(0.1)

    while(cap.isOpened()):

        ret, frame = cap.read()

        if not ret:
            print("Camera frame not returned. Camera may be missing or damaged")
            break
        
        image = cv2.resize(frame, (400, 225))

        cv2.namedWindow("Live Camera Feed")
        cv2.setMouseCallback("Live Camera Feed", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(image (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Live Camera Feed", image)

        key = cv2.waitKey(50) & 0xFF

        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = image.copy()
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


def vid_cap_arena_pic(video_name, vidTrack_setup_parameters, arena_pic_name):
    
    global rect,startPoint,endPoint
    
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False

    cap = cv2.VideoCapture(video_name)

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    # reading the first frame
    ret, frame = cap.read()

    while(cap.isOpened()):

        ret, frame = cap.read()

        if not ret:
            print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)

        cv2.namedWindow("Recorded Video")
        cv2.setMouseCallback("Recorded Video", on_mouse)

        # drawing rectangle
        if startPoint == True and endPoint == True:
            cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 1)

        cv2.imshow("Recorded Video", image)

        key = cv2.waitKey(50) & 0xFF

        if key == 27:
            break

        if key == ord("i"):
            uncropped_arena_pic = image.copy()
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


def live_capture_ref_image(ref_image_name):
    
    cap = cv2.VideoCapture(0)

    # allow the camera to warmup
    time.sleep(0.1)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            print("Camera frame not returned. Camera may be missing or damaged")
            break
            
        image = cv2.resize(frame, (400, 225))
            
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
    
    cv2.imwrite(ref_image_name, ref_image)
    cap.release()
    cv2.destroyAllWindows()
    return None  


def vid_capture_ref_image(video_name, ref_image_name, vidTrack_setup_parameters):

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    cap = cv2.VideoCapture(video_name)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)
        
        cv2.imshow("Recorded Video", image)
        
        k = cv2.waitKey(50) & 0xFF
        
        if k == 27:
            break

        if k == ord('i'):
            ref_image = image.copy()
            cv2.imshow("Reference Image", ref_image)
            k = cv2.waitKey(1)
            cv2.imwrite(ref_image_name, ref_image)
            if k == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    return None


def live_colour_calib(vidTrack_setup_parameters):
    
    cap = cv2.VideoCapture(0)

    video_tracking_algorithm = vidTrack_setup_parameters['video_tracking_algorithm']

    if video_tracking_algorithm == "MOG":
        fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    elif video_tracking_algorithm == "Frame Differencing":
        ref_image_name = vidTrack_setup_parameters['reference_image_name']
        ref_image = cv2.imread(ref_image_name)
        hsv_ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)

    # allow the camera to warmup
    time.sleep(0.1)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            print("Camera frame not returned. Camera may be missing or damaged")
            break
            
        image = cv2.resize(frame, (400, 225))

        try:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            colourmask = cv2.inRange(hsv_image, lower_b, upper_b)
            
            if video_tracking_algorithm == "MOG":
                bsmask = fgbg.apply(colourmask)
            elif video_tracking_algorithm == "Frame Differencing":
                ref_image_mask = cv2.inRange(hsv_ref_image, lower_b, upper_b)
                bsmask = cv2.absdiff(colourmask, ref_image_mask)
            
            _, cnts, _ = cv2.findContours(bsmask.copy(), cv2.RETR_EXTERNAL,
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
            
        except:
            pass
                    
        cv2.imshow("Live Camera Feed", image)
        k = cv2.waitKey(1)
        if k == 27:
            break

        if k == ord('i'):

            def nothing(x):
                    pass
            
            cv2.namedWindow("Colour Mask")

            # create trackbars for color change
            cv2.createTrackbar('Hl', 'Colour Mask', 0, 179, nothing)
            cv2.createTrackbar('Hu', 'Colour Mask', 179, 179, nothing)

            cv2.createTrackbar('Sl', 'Colour Mask', 0, 255, nothing)
            cv2.createTrackbar('Su', 'Colour Mask', 255, 255, nothing)

            cv2.createTrackbar('Vl', 'Colour Mask', 0, 255, nothing)
            cv2.createTrackbar('Vu', 'Colour Mask', 255, 255, nothing)

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            while True:
                hl = cv2.getTrackbarPos('Hl', 'Colour Mask')
                sl = cv2.getTrackbarPos('Sl', 'Colour Mask')
                vl = cv2.getTrackbarPos('Vl', 'Colour Mask')

                hu = cv2.getTrackbarPos('Hu', 'Colour Mask')
                su = cv2.getTrackbarPos('Su', 'Colour Mask')
                vu = cv2.getTrackbarPos('Vu', 'Colour Mask')

                lower_b = np.array([hl, sl, vl])
                upper_b = np.array([hu, su, vu])

                mask = cv2.inRange(hsv, lower_b, upper_b)
                                        
                cv2.imshow("Colour Mask", mask)
                k = cv2.waitKey(1)
                if k == ord('i'):
                    break

    cap.release()
    cv2.destroyAllWindows()
    return ([hl,sl,vl],[hu,su,vu])   

def vid_colour_calib(video_name, vidTrack_setup_parameters):

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    video_tracking_algorithm = vidTrack_setup_parameters['video_tracking_algorithm']

    if video_tracking_algorithm == "MOG":
        fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    elif video_tracking_algorithm == "Frame Differencing":
        ref_image_name = vidTrack_setup_parameters['reference_image_name']
        ref_image = cv2.imread(ref_image_name)
        hsv_ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)

    cap = cv2.VideoCapture(video_name)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)

        try:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            colourmask = cv2.inRange(hsv_image, lower_b, upper_b)

            if video_tracking_algorithm == "MOG":
                bsmask = fgbg.apply(colourmask)
            elif video_tracking_algorithm == "Frame Differencing":
                ref_image_mask = cv2.inRange(hsv_ref_image, lower_b, upper_b)
                bsmask = cv2.absdiff(colourmask, ref_image_mask)
            
            _, cnts, _ = cv2.findContours(bsmask.copy(), cv2.RETR_EXTERNAL,
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
            
        except:
            pass

        cv2.imshow("Recorded Video", image)
        k = cv2.waitKey(1)
        if k == 27:
            break

        if k == ord('i'):

            def nothing(x):
                    pass
            
            cv2.namedWindow("Colour Mask")

            # create trackbars for color change
            cv2.createTrackbar('Hl', 'Colour Mask', 0, 179, nothing)
            cv2.createTrackbar('Hu', 'Colour Mask', 179, 179, nothing)

            cv2.createTrackbar('Sl', 'Colour Mask', 0, 255, nothing)
            cv2.createTrackbar('Su', 'Colour Mask', 255, 255, nothing)

            cv2.createTrackbar('Vl', 'Colour Mask', 0, 255, nothing)
            cv2.createTrackbar('Vu', 'Colour Mask', 255, 255, nothing)

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            while True:
                hl = cv2.getTrackbarPos('Hl', 'Colour Mask')
                sl = cv2.getTrackbarPos('Sl', 'Colour Mask')
                vl = cv2.getTrackbarPos('Vl', 'Colour Mask')

                hu = cv2.getTrackbarPos('Hu', 'Colour Mask')
                su = cv2.getTrackbarPos('Su', 'Colour Mask')
                vu = cv2.getTrackbarPos('Vu', 'Colour Mask')

                lower_b = np.array([hl, sl, vl])
                upper_b = np.array([hu, su, vu])

                mask = cv2.inRange(hsv, lower_b, upper_b)
                                        
                cv2.imshow("Colour Mask", mask)
                k = cv2.waitKey(1)
                if k == ord('i'):
                    break

    cap.release() 
    cv2.destroyAllWindows()
    return ([hl,sl,vl],[hu,su,vu])


def live_camera_feed(recording=False, record_name=None):
    run_tme = deque()

    cap = cv2.VideoCapture(0)

    if recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(record_name, fourcc, 30.0, (400, 225))

    # allow the camera to warmup
    time.sleep(0.1)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning

    while _isRunning:

        ret, frame = cap.read()

        if not ret:
            #print("Camera frame not returned. Camera may be missing or damaged")
            break

        image = cv2.resize(frame, (400,225))

        if recording:
            # write the frame
            out.write(image)

        millis = float(time.time())
        current_time = round(millis - start, 2)
        run_tme.append(current_time)

        cv2.imshow("Live Camera Feed", image)
        cv2.waitKey(1)

        from OneStopTrack import _isRunning

    if recording:
        out.release()
    cap.release()
    cv2.destroyAllWindows()
    return run_tme


def video_feed(video_name, vidTrack_setup_parameters):
    run_tme = deque()

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    cap = cv2.VideoCapture(video_name)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning

    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            #print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)

        millis = float(time.time())
        current_time = round(millis - start, 2)
        run_tme.append(current_time)

        cv2.imshow("Recorded Video", image)
        cv2.waitKey(1)

        from OneStopTrack import _isRunning

    cap.release()
    cv2.destroyAllWindows()
    return run_tme


def live_mog_tracking(vidTrack_setup_parameters, recording=False, record_name=None):
    run_tme = deque()
    pts_tme = deque()
    pts = deque()
    
    global mod_pts, mod_pt
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']

    show_window = vidTrack_setup_parameters['simps']['show_window']
    show_arena_window = vidTrack_setup_parameters['simps']['show_arena_window']
    show_trck_hist = vidTrack_setup_parameters['simps']['show_trck_hist']

    only_sample_arena = vidTrack_setup_parameters['simps']['only_sample_arena']

    x1 = ref_col[0][0]
    x2 = ref_col[1][0]
    y1 = ref_col[0][1]
    y2 = ref_col[1][1]
   
    cap = cv2.VideoCapture(0)

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    if recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(record_name, fourcc, 30.0, (400, 225))

    # allow the camera to warmup
    time.sleep(0.1)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning
    
    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            #print("Camera frame not returned. Camera may be missing or damaged")
            break

        image = cv2.resize(frame, (400, 225))

        if only_sample_arena:
            hsv = cv2.cvtColor(image[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
        else:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        #fgmask = fgbg.apply(mask, learningRate=0)
        fgmask = fgbg.apply(mask)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

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
                    if only_sample_arena:
                        centre = (int(M["m10"]/M["m00"])+x1, int(M["m01"]/M["m00"])+y1)
                    else:
                        centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                    cv2.circle(image, centre, 5, (255,0,0), -1)
                except:
                    pass

        millis = float(time.time())
        current_time = round(millis - start, 2)

        run_tme.append(current_time)

        if centre != None:
            pts_tme.append(current_time)

            if show_trck_hist:
                if len(pts) <= 100:
                    pts.append(centre)
                elif len(pts) > 100:
                    pts = deque(itertools.islice(pts, 1, len(pts)))
                    pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))

            mod_pt = mod_pts[-1]

        if show_trck_hist:
            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)

        if show_window:
            if show_arena_window:
                cv2.imshow("Live Camera Feed Tracking", image[y1:y2, x1:x2])
            else:
                cv2.imshow("Live Camera Feed Tracking", image)
        cv2.waitKey(1)

        if recording:
            # write the frame
            out.write(image)

        from OneStopTrack import _isRunning

    if recording:
        out.release()
    cap.release()
    cv2.destroyAllWindows()
    return (pts_tme, mod_pts, run_tme)

        
def vid_mog_tracking(video_name, vidTrack_setup_parameters):
    run_tme = deque()
    pts_tme = deque()
    pts = deque()
    
    global mod_pts, mod_pt, run_tme_
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    show_window = vidTrack_setup_parameters['simps']['show_window']
    show_arena_window = vidTrack_setup_parameters['simps']['show_arena_window']
    show_trck_hist = vidTrack_setup_parameters['simps']['show_trck_hist']

    only_sample_arena = vidTrack_setup_parameters['simps']['only_sample_arena']

    x1 = ref_col[0][0]
    x2 = ref_col[1][0]
    y1 = ref_col[0][1]
    y2 = ref_col[1][1]

    cap = cv2.VideoCapture(video_name)

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    start = float(time.time())

    import OneStopTrack
    _isRunning = OneStopTrack._isRunning

    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            #print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)

        if only_sample_arena:
            hsv = cv2.cvtColor(image[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
        else:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                
        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fgmask = fgbg.apply(mask)
    
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
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
                if only_sample_arena:
                    centre = (int(M["m10"]/M["m00"])+x1, int(M["m01"]/M["m00"])+y1)
                else:
                    centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                cv2.circle(image, centre, 5, (255,0,0), -1)
            except:
                pass

        millis = float(time.time())        
        current_time = round(millis - start, 2)

        run_tme.append(current_time)

        run_tme_ = run_tme[-1]

        if centre != None:
            pts_tme.append(current_time)

            if show_trck_hist:
                if len(pts) <= 100:
                    pts.append(centre)
                elif len(pts) > 100:
                    pts = deque(itertools.islice(pts, 1, len(pts)))
                    pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))

            mod_pt = mod_pts[-1]

        if show_trck_hist:
            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)

        if show_window:
            if show_arena_window:
                cv2.imshow("Recorded Video Tracking", image[y1:y2, x1:x2])
            else:
                cv2.imshow("Recorded Video Tracking", image)
        cv2.waitKey(1)

        _isRunning = OneStopTrack._isRunning

    cap.release()
    cv2.destroyAllWindows()
    return (pts_tme, mod_pts, run_tme)


def live_fd_tracking(vidTrack_setup_parameters, recording=False, record_name=None):
    run_tme = deque()
    pts_tme = deque()
    pts = deque()
    
    global mod_pts, mod_pt
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']

    ref_image_name = vidTrack_setup_parameters['reference_image_name']

    show_window = vidTrack_setup_parameters['simps']['show_window']
    show_arena_window = vidTrack_setup_parameters['simps']['show_arena_window']
    show_trck_hist = vidTrack_setup_parameters['simps']['show_trck_hist']

    only_sample_arena = vidTrack_setup_parameters['simps']['only_sample_arena']

    x1 = ref_col[0][0]
    x2 = ref_col[1][0]
    y1 = ref_col[0][1]
    y2 = ref_col[1][1]
    
    cap = cv2.VideoCapture(0)

    if only_sample_arena:
        ref_image = cv2.imread(ref_image_name)[y1:y2, x1:x2]
    else:
        ref_image = cv2.imread(ref_image_name)

    lower_b = np.array(calib_col[0])
    upper_b = np.array(calib_col[1])

    hsv_ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2HSV)
    ref_image_mask = cv2.inRange(hsv_ref_image, lower_b, upper_b)

    if recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(record_name, fourcc, 5.0, (400, 225))

    # allow the camera to warmup
    time.sleep(0.1)

    start = float(time.time())

    global _isRunning
    from OneStopTrack import _isRunning
    
    while _isRunning:
        ret, frame = cap.read()

        if not ret:
            #print("Camera frame not returned. Camera may be missing or damaged")
            break

        image = cv2.resize(frame, (400, 225))

        if only_sample_arena:
            hsv = cv2.cvtColor(image[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
        else:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fdmask = cv2.absdiff(mask, ref_image_mask)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

        fdmask = cv2.morphologyEx(fdmask, cv2.MORPH_OPEN, kernel)
        fdmask = cv2.morphologyEx(fdmask, cv2.MORPH_CLOSE, kernel)

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
                if only_sample_arena:
                    centre = (int(M["m10"]/M["m00"])+x1, int(M["m01"]/M["m00"])+y1)
                else:
                    centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                cv2.circle(image, centre, 5, (255,0,0), -1)
            except:
                pass

        millis = float(time.time())
        current_time = round(millis - start, 2)

        run_tme.append(current_time)

        if centre != None:
            pts_tme.append(current_time)

            if show_trck_hist:
                if len(pts) <= 100:
                    pts.append(centre)
                elif len(pts) > 100:
                    pts = deque(itertools.islice(pts, 1, len(pts)))
                    pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))

            mod_pt = mod_pts[-1]
    
        if show_trck_hist:
            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)
                                     
        if show_window:
            if show_arena_window:
                cv2.imshow("Live Camera Feed Tracking", image[y1:y2, x1:x2])
            else:
                cv2.imshow("Live Camera Feed Tracking", image)
        cv2.waitKey(1)

        if recording:
            # write the frame
            out.write(image)

        from OneStopTrack import _isRunning
    
    if recording:
        out.release()
    cap.release()
    cv2.destroyAllWindows()
    return (pts_tme, mod_pts, run_tme)


def vid_fd_tracking(video_name, vidTrack_setup_parameters):
    run_tme = deque()
    pts_tme = deque()
    pts = deque()
    
    global mod_pts, mod_pt
    mod_pts = deque()

    ref_col = vidTrack_setup_parameters['ref_col']
    calib_col = vidTrack_setup_parameters['calib_col']

    ref_image_name = vidTrack_setup_parameters['reference_image_name']

    vid_aspect_ratio = float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[0])/float(vidTrack_setup_parameters['loaded_video_aspect_ratio'].split(":")[1])
    mod_video_resolution = (400, int(400/vid_aspect_ratio))

    show_window = vidTrack_setup_parameters['simps']['show_window']
    show_arena_window = vidTrack_setup_parameters['simps']['show_arena_window']
    show_trck_hist = vidTrack_setup_parameters['simps']['show_trck_hist']

    only_sample_arena = vidTrack_setup_parameters['simps']['only_sample_arena']

    x1 = ref_col[0][0]
    x2 = ref_col[1][0]
    y1 = ref_col[0][1]
    y2 = ref_col[1][1]

    if only_sample_arena:
        ref_image = cv2.imread(ref_image_name)[y1:y2, x1:x2]
    else:
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
            #print("Video recording frame not returned. Video recording may be missing or damaged")
            break

        image = cv2.resize(frame, mod_video_resolution)

        if only_sample_arena:
            hsv = cv2.cvtColor(image[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
        else:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colours
        mask = cv2.inRange(hsv, lower_b, upper_b)

        fdmask = cv2.absdiff(mask, ref_image_mask)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

        fdmask = cv2.morphologyEx(fdmask, cv2.MORPH_OPEN, kernel)
        fdmask = cv2.morphologyEx(fdmask, cv2.MORPH_CLOSE, kernel)

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
                if only_sample_arena:
                    centre = (int(M["m10"]/M["m00"])+x1, int(M["m01"]/M["m00"])+y1)
                else:
                    centre = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

                cv2.circle(image, centre, 5, (255,0,0), -1)
            except:
                pass

        millis = float(time.time())
        current_time = round(millis - start, 2)

        run_tme.append(current_time)

        if centre != None:
            pts_tme.append(current_time)

            if show_trck_hist:
                if len(pts) <= 100:
                    pts.append(centre)
                elif len(pts) > 100:
                    pts = deque(itertools.islice(pts, 1, len(pts)))
                    pts.append(centre)

            mod_pt_x = (centre[0]-ref_col[0][0])*ref_col[4]
            
            mod_pt_y = (centre[1]-ref_col[0][1])*ref_col[5]

            mod_pts.append((mod_pt_x,mod_pt_y))

            mod_pt = mod_pts[-1]

        if show_trck_hist:
            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                cv2.line(image, pts[i-1], pts[i], (0,255,0), 1)
                             
        if show_window:
            if show_arena_window:
                cv2.imshow("Recorded Video Tracking", image[y1:y2, x1:x2])
            else:
                cv2.imshow("Recorded Video Tracking", image)
        cv2.waitKey(1)

        from OneStopTrack import _isRunning
    
    cap.release()
    cv2.destroyAllWindows()
    return (pts_tme, mod_pts, run_tme)
