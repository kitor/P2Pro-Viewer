#!/usr/bin/env python3

import threading
import time
import os
import logging
import keyboard

import P2Pro.video
import P2Pro.P2Pro_cmd as P2Pro_CMD
import P2Pro.recorder

from cv2 import CAP_V4L2
from cv2_enumerate_cameras import enumerate_cameras

indexes = []
print("Found following inputs matching P2 Pro:")
for camera_info in enumerate_cameras(apiPreference = CAP_V4L2):
    if camera_info.vid == P2Pro.video.P2Pro_usb_id[0] \
        and camera_info.pid == P2Pro.video.P2Pro_usb_id[1]:
      indexes.append(camera_info.index)
      print(f'{camera_info.index}: {camera_info.path} "{camera_info.name}" ')

if indexes:
    # Select lower ID. On Linux this is usually the one with video capture
    camera_index = min(indexes)
    print(f"Selected index {camera_index}")
else:
    print("Unable to find P2 pro, aborting...")
    sys.exit(1)


logging.basicConfig()
logging.getLogger('P2Pro.recorder').setLevel(logging.INFO)
logging.getLogger('P2Pro.P2Pro_cmd').setLevel(logging.INFO)

try:
    print ("Hotkeys:")
    print ("[q] close openCV window, then close program using [ctrl]+[c]")
    print ("[s] do NUC")
    print ("[b] do NUC for background")
    print ("[d] read shutter state")
    print ("[l] set low gain (high temperature mode)")
    print ("[h] set high gain (low temperature mode)")
    cam_cmd = P2Pro_CMD.P2Pro()

    vid = P2Pro.video.Video()
    video_thread = threading.Thread(target=vid.open, args=(cam_cmd, camera_index, ))
    video_thread.start()

    while not vid.video_running:
        time.sleep(0.01)

    #rec = P2Pro.recorder.VideoRecorder(vid.frame_queue[1], "test")
    #rec.start()

    # print (cam_cmd._dev)
    # cam_cmd._standard_cmd_write(P2Pro_CMD.CmdCode.sys_reset_to_rom)
    # print(cam_cmd._standard_cmd_read(P2Pro_CMD.CmdCode.cur_vtemp, 0, 2))
    # print(cam_cmd._standard_cmd_read(P2Pro_CMD.CmdCode.shutter_vtemp, 0, 2))

    cam_cmd.pseudo_color_set(0, P2Pro_CMD.PseudoColorTypes.PSEUDO_IRON_RED)

    print(cam_cmd.pseudo_color_get())
    # cam_cmd.set_prop_tpd_params(P2Pro_CMD.PropTpdParams.TPD_PROP_GAIN_SEL, 0)
    print(cam_cmd.get_prop_tpd_params(P2Pro_CMD.PropTpdParams.TPD_PROP_GAIN_SEL))
    print(cam_cmd.get_device_info(P2Pro_CMD.DeviceInfoType.DEV_INFO_GET_PN))

    time.sleep(5)
    #rec.stop()

    while True:
        # print(vid.frame_queue[0].get(True, 2)) # test
        time.sleep(1)

except KeyboardInterrupt:
    print("Killing...")
    time.sleep(5)
    pass
os._exit(0)
