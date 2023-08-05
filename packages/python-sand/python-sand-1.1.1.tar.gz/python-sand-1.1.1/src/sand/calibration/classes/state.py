from __future__ import annotations

from ast import literal_eval

from sand.calibration.classes.camera import Cam
from sand.calibration.classes.lidar import Lidar
from sand.config import CameraConfig, SandConfig
from sand.config.config import _to_points
from sand.datatypes import CalPoints, LidarPoints, LidarTransformation, Point
from sand.util.camera import get_path_from_camera_name


class State:
    point_id: int
    cam_list: list[Cam] = []
    active_point_index: int = 0
    active_lidar_index: int = 0
    points2d_list: list[LidarPoints] = []
    lidar_list: list[Lidar] = []

    def __init__(self, config: SandConfig) -> None:
        self.config = config
        for camera_config in self.config.cameras:
            cam = Cam(
                name=camera_config.name,
                calibration_points=self._calibration_points(camera_config),
                corner_calibration_points=self._calibration_points(camera_config),
                image_path=get_path_from_camera_name(camera_config.name),
                focal=camera_config.focal,
                dimension=camera_config.transformation_source_resolution,
            )
            self.cam_list.append(cam)
        for lidar_config in self.config.lidars:
            lidar = Lidar(lidar_config)
            self.lidar_list.append(lidar)
        self.active_cam = self.cam_list[0]

    def camera_names(self) -> list[str]:
        names = []
        for cam in self.cam_list:
            names.append(cam.name)
        return names

    def read_lidars(self) -> None:
        for lidar in self.lidar_list:
            lidar.read_cloud()

    def next_lidar(self) -> None:
        index = self.active_lidar_index
        self.active_lidar_index = index + 1 if index < len(self.lidar_list) - 1 else 0

    def prev_lidar(self) -> None:
        index = self.active_lidar_index
        self.active_lidar_index = index - 1 if index > 0 else len(self.lidar_list) - 1

    def next_camera(self) -> Cam:
        index = self.cam_list.index(self.active_cam)
        self.active_cam = (
            self.cam_list[index + 1]
            if index + 1 < len(self.cam_list)
            else self.cam_list[0]
        )
        return self.active_cam

    def prev_camera(self) -> Cam:
        index = self.cam_list.index(self.active_cam)
        self.active_cam = (
            self.cam_list[index - 1]
            if index - 1 > 0
            else self.cam_list[len(self.cam_list) - 1]
        )
        return self.active_cam

    def next_point(self) -> None:
        index = self.active_point_index
        self.active_point_index = index + 1 if index < 3 else 0

    def prev_point(self) -> None:
        index = self.active_point_index
        self.active_point_index = index - 1 if index > 0 else 3

    def move_lidar(self, move_x: float, move_y: float) -> None:
        trans = self.lidar_list[self.active_lidar_index].vlp_cloud.transformation
        new_trans = LidarTransformation(
            z=trans.z, x=trans.x + move_x, y=trans.y + move_y, angle=trans.angle
        )
        self.lidar_list[self.active_lidar_index].vlp_cloud.set_transformation(new_trans)
        print(trans, new_trans)

    def rotate_lidar(self, angle: float) -> None:
        trans = self.lidar_list[self.active_lidar_index].vlp_cloud.transformation
        new_trans = LidarTransformation(
            z=trans.z, x=trans.x, y=trans.y, angle=trans.angle + angle
        )
        self.lidar_list[self.active_lidar_index].vlp_cloud.set_transformation(new_trans)
        print(trans, new_trans)

    def move_point(self, move_x: int, move_y: int) -> None:
        try:
            point = self.active_cam.corner_calibration_points.target_points[
                self.active_point_index
            ]
            self.active_cam.corner_calibration_points.target_points[
                self.active_point_index
            ] = Point(point.x + move_x, point.y + move_y)
        except IndexError as error:
            print("active_point_index:", self.active_point_index)
            print(
                "len(target_points):",
                len(self.active_cam.corner_calibration_points.target_points),
            )
            print(error)

    def change_focal(self, focal: int) -> None:
        self.active_cam.focal = self.active_cam.focal + focal

    def active_point(self) -> Point:
        return self.active_cam.corner_calibration_points.target_points[
            self.active_point_index
        ]

    @staticmethod
    def _calibration_points(cam_config: CameraConfig) -> CalPoints:
        return CalPoints(
            source_points=_to_points(
                literal_eval(cam_config.transformation_source_points)
            ),
            target_points=_to_points(
                literal_eval(cam_config.transformation_target_points)
            ),
        )
