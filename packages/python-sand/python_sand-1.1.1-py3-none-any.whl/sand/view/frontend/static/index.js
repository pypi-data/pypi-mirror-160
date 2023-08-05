$(document).ready(function () {
    const socket = io({reconnection: false});
    const timestamp = $("#timestamp");
    /** @type {string[]} */
    let available_streams = [];

    socket.on("connect", function () {
        console.log("connected");
        socket.emit("send_cameras", {});
        console.log("send_cameras emitted");
    });

    function sendRefresh() {
        const stream_selector = $("#streamSelector");
        const selected_stream = stream_selector.val();

        socket.emit("refresh_cameras", [selected_stream]);
    }

    function saveMoment() {
        socket.emit("save_moment", {})
    }

    /**
     * @param {string} stream
     * @returns {*|Window.jQuery|HTMLElement}
     */
    function createStreamDiv(stream) {
        const stream_div = $("<div></div>");
        const heading = $(`<h4>${stream}</h4>`);
        const img = $(`<img alt="${stream}" id="${stream}" />`);

        stream_div.append(heading);
        stream_div.append(img);

        return stream_div;
    }

    function createCameraNavLi(name){
        return `<li class="nav-item"><a class="nav-link camlink" href="#" >${name}</a></li>`;
    }

    /**
     * @param {string[]} newAvailableStreams
     * @param {string[]} newActiveStreams
     */
    function rebuildAvailableStreams(newAvailableStreams, newActiveStreams) {
        available_streams = newAvailableStreams;

        const settings_div = $("#settings");
        settings_div.empty();

        const navbarUl = $("#navbarNav ul");
        navbarUl.find(".camlink").remove();

        const streams_dropdown = $("<select id='streamSelector'></select>");
        const all_option = $("<option value='all'>all</option>");
        streams_dropdown.append(all_option);

        for (const availableStream of newAvailableStreams) {
            const stream_option = $(`<option value="${availableStream}">${availableStream}</option>`);
            streams_dropdown.append(stream_option);
            navbarUl.append(createCameraNavLi(availableStream));
        }

        if (newAvailableStreams.length === newActiveStreams.length) {
            streams_dropdown.val("all");
        } else {
            streams_dropdown.val(newActiveStreams[0]);
        }

        const refresh_button = $("<button>Refresh</button>");
        refresh_button.click(sendRefresh);

        const save_button = $("<button>Save Moment</button>");
        save_button.click(saveMoment)

        settings_div.append(streams_dropdown);
        settings_div.append(refresh_button);
        settings_div.append(save_button)
    }

    /**
     * @param {string[]} newActiveStreams
     */
    function rebuildActiveStreams(newActiveStreams) {
        const streams_div = $("#streams");
        streams_div.empty();

        for (const stream of newActiveStreams) {
            streams_div.append(createStreamDiv(stream));
        }
    }

    /**
     * @param {{available: string[], active: string[]}} msg
     */
    function onStreamInit(msg) {
        console.log(msg);
        const availableStreamsChanged = msg.available.filter((x) => !available_streams.includes(x)).length !== 0;
        if (availableStreamsChanged) {
            rebuildAvailableStreams(msg.available, msg.active);
        }

        rebuildActiveStreams(msg.active);
    }
    socket.on("stream_init", onStreamInit);

    /**
     * @param {{now: string, f1_l1_v1: string}} msg can have multiple images/keys with encoded images
     */
    function onCameraStream(msg) {
        for (const key of Object.keys(msg)) {
            if (key === "now") {
                timestamp.text(msg[key]);
            } else {
                $(`#${key}`).attr("src", msg[key]);
            }
        }
    }
    socket.on("camera_stream", onCameraStream);

    /**
     * @param {{filename: string}} msg
     */
    function onMomentSaved(msg) {
        console.log(msg)

        download(`/moment/${msg.filename}`)
    }
    socket.on("moment_saved", onMomentSaved)
});
