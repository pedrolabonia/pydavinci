# type: ignore
import time
from collections import defaultdict

from pydavinci import davinci

resolve = davinci.Resolve()

project = resolve.project
project_manager = resolve.project_manager
media_pool = resolve.media_pool
media_storage = resolve.media_storage
ocf_folder = media_pool.add_subfolder("OCF", media_pool.root_folder)
media_pool.set_current_folder(ocf_folder)


def generate_premiere_proxies(input_dir, output_dir, proxyfactor):

    media_pool.import_media(input_dir)

    clips_res = defaultdict(list)

    for media in ocf_folder.clips:
        clips_res[media.properties["Resolution"]].append(media)

    project.set_preset("Proxy_Preset")

    render_ids = []

    for key in clips_res.keys():

        res_x, res_y = key.split("x")

        res_folder = media_pool.add_subfolder(key, ocf_folder)
        clips = clips_res[key]

        media_pool.move_clips(clips, res_folder)
        media_pool.create_timeline_from_clips(res_folder.name, res_folder.clips)

        timeline = project.timeline
        timeline.set_setting(
            "useCustomSettings", "1"
        )  # enable custom timeline size != project settings
        timeline.set_setting("timelineResolutionWidth", res_x)
        timeline.set_setting("timelineResolutionHeight", res_y)

        project.set_render_format_and_codec("mp4", "H264")
        render_settings = {
            "FormatWidth": (int(res_x) // proxyfactor),
            "FormatHeight": (int(res_y) // proxyfactor),
            "TargetDir": output_dir,
        }

        # Set Render Resolution
        project.set_render_settings(render_settings)

        # print(render_id)
        render_id = project.add_renderjob()
        render_ids.append(render_id)
    return render_ids


job_ids = generate_premiere_proxies(
    "A:/media_test2/",
    "A:/media_test2/output",
    2,
)

project.render(job_ids)


for i in len(job_ids):

    render_status = project.render_status(job_ids[i])["JobStatus"]

    while render_status != "Complete":
        time.sleep(3)
        status = project.render_status(job_ids[i])
        try:
            percentage = status["CompletionPercentage"]
            time_left = status["EstimatedTimeRemainingInMs"] / 1000

        except KeyError:
            time.sleep(2)
            break

        print(
            f"Job ID {job_ids[i]} | Rendering time left: {time_left} | Percentage completed: {percentage}%\r",
            end="",
            flush=True,
        )

        render_status = status["JobStatus"]

    time_to_render = project.render_status(job_ids[i])["TimeTakenToRenderInMs"] / 1000
    print("\n")
    print(f"Job ID {job_ids[i]} | Rendering complete. | Total render time: {time_to_render}")
