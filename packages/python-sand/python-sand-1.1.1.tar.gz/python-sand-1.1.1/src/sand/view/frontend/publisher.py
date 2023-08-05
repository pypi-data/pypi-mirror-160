from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Flask, render_template
from overrides import overrides

from sand.config import PublisherConfig, SandConfig
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode


class Publisher(SandNode, ConfigurationManager[PublisherConfig]):
    """
    This is the module, that provides a "Dashboard"-like thing for our video streams. The reason for this is, that our
    cameras have some limit in place for the amount of watchers on a given stream. To circumvent the possibility of one
    just watching the camera-stream and inadvertently blocking SAND from recording/analysing it, we publish the streams
    on one conveniently and customisable site. Here we can also do things, like scale the images down or slow down the
    transfer to be kinder to the network.

    While this module looks like it is "ShutdownAble" in reality it is more complicated than that. While we want to get
    the notification that the system is shutting down, we cannot kill every running thread in this module. This has to
    do with the webserver, as on issue-comment on github put it: "Webservers are not designed to be shutdown". Therefore
    after the shutdown call there is still (at least) one thread running.

    For the implementation this means the following. !Everything! that needs to be shutdown gracefully, needs to be
    handled via ShutdownAble::shutdown. Everything else needs to be able to be killed at any time and point without
    causing problems for the remaining system/system-shutdown.
    """

    def __init__(self, global_config: SandConfig):
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        template_folder = Path(__file__).parent.joinpath("template")
        static_folder = Path(__file__).parent.joinpath("assets")
        self.app = Flask(
            self.config.name,
            template_folder=template_folder.as_posix(),
            static_folder=static_folder.as_posix(),
        )

        self.add_endpoints()

        # daemon necessary for shutdown by disregarding thread
        self.create_thread(
            target=self.start,
            args=(),
            name=self.__class__.__name__,
            daemon=True,
            start=True,
        )

    @overrides
    def select_config(self, global_config: SandConfig) -> PublisherConfig:
        return global_config.publisher

    def start(self) -> None:
        self.set_thread_name("pub_sio")
        # noinspection HttpUrlsUsage
        self.log.i(
            f"Starting webserver: http://{self.config.host}:{self.config.port}", "start"
        )
        self.app.run(host=self.config.host, port=self.config.port)

    @overrides
    def shutdown(self) -> None:
        """
        Publisher is not really ShutdownAble, the thread will never die on its own. This is because of the way socket_io
        and flask work. They don't provide a method to shutdown them cleanly. Therefore we kill the publisher
        server-thread just by ignoring that it is there.
        This method is implemented (with just a pass), to prevent the normal implementation that joins the threads and
        does a graceful shutdown.
        If there is something added in the future that is actually ShutdownAble then you can use this method to do it
        gracefully.
        """

    def add_endpoints(self) -> None:
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/camera/<camera>", "fullscreen", self.fullscreen)
        self.app.add_url_rule("/map", "map", self.map)
        self.app.add_url_rule("/map_video_only", "map_video_only", self.map_video_only)
        self.app.add_url_rule("/error", "error", self.error)
        # pylint: disable=no-member
        self.app.jinja_env.globals["map_config"] = self.config
        self.app.jinja_env.globals["app_name"] = self.config.name
        self.app.jinja_env.globals["camera_configs"] = self.get_camera_configs()
        self.app.jinja_env.globals[
            "is_map_active"
        ] = self._global_config.map_builder.active
        self.app.jinja_env.globals[
            "is_transformer_active"
        ] = self._global_config.transformer.active

    def get_camera_configs(self) -> list[tuple[str, int, int, int]]:
        return list(
            map(
                lambda x: (
                    self.clean_name(x.name),
                    x.serve_port,
                    x.stream_resolution.width,
                    x.stream_resolution.height,
                ),
                self._global_config.cameras,
            )
        )

    def get_camera_config(self, name: str) -> tuple[str, int, int, int] | None:
        for camera in self._global_config.cameras:
            if self.clean_name(camera.name) == name:
                return (
                    self.clean_name(camera.name),
                    camera.serve_port,
                    camera.stream_resolution.width,
                    camera.stream_resolution.height,
                )
        return None

    @staticmethod
    def clean_name(name: str) -> str:
        return name

    @staticmethod
    def index() -> Any:
        return render_template(
            "index.html",
            active_link="/",
        )

    @staticmethod
    def map() -> Any:
        return render_template(
            "map.html",
            port=7998,
            active_link="/map",
            name="Map with all Informations",
        )

    @staticmethod
    def map_video_only() -> Any:
        return render_template(
            "map.html",
            port=7999,
            active_link="/map_video_only",
            name="Map Video Only",
        )

    def fullscreen(
        self,
        camera: str,
    ) -> Any:
        return render_template(
            "fullscreen.html",
            camera_config=self.get_camera_config(camera),
            active_link="/camera/" + camera,
        )

    @staticmethod
    def error() -> Any:
        return render_template(
            "error.html",
            active_link="/error",
        )
