from tiny_tf.tf import Transform
from threeviz.api import plot_pose, delete, clear_all, plot_plane_tex, plot_cube_cloud, move_camera
from threeviz.helpers import image_to_uri
import time
import cv2
from cv_pre import *
from cv_common.maps import get_map_data_and_image
from cv_pipeline.utilities.relocalization import meta_to_LocalizedRangeScan

unit_xform = Transform.from_position_euler(0, 0, 0, 0, 0, 0)

job = get_job("31af6ec3-0cad-4074-b794-bf3976581308")

data, im = get_map_data_and_image(job.locale, job.metas[0].map_name)

h, w = im.shape

res = data["resolution"]
dx, dy, _ = data["origin"]
dx = dx + w*res / 2
dy = dy + h*res / 2

plot_plane_tex(Transform.from_position_euler(0, 0, 0, 0, 0, 0), "map", im, scale=(w*res, h*res))

for meta in [m for m in job.metas if m.image_source == "laser"]:
    plot_pose(Transform.from_xyt(meta.robot_pos_x - dx, meta.robot_pos_y - dy, np.deg2rad(meta.robot_yaw_deg)), label=meta.image_name + "pose", size=0.5)
    x, y = meta_to_LocalizedRangeScan(meta).points()
    plot_cube_cloud(x - dx, y - dy, x*0, meta.image_name + "laser", size=0.1)

for meta in job.rgb_metas:
    xform = Transform.from_xyt(meta.robot_pos_x - dx, meta.robot_pos_y - dy, np.deg2rad(meta.robot_yaw_deg)) + Transform.from_position_euler(0, 0.5, meta.stitch_y*(2.3/8), 0, 0, 0) + Transform.from_position_euler(0, 0, 0, np.pi/2, 0, 0)
    plot_plane_tex(xform, meta.image_name, meta.image_thumbnail, scale=(0.45, 0.25))

# move_camera(xform + Transform.from_position_euler(1, 1, 1, 0, 0, 0), xform)