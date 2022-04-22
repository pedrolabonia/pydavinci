# type: ignore
import time
from collections import defaultdict

from pydavinci import davinci

resolve = davinci.Resolve()

project = resolve.project
project_manager = resolve.project_manager
media_pool = resolve.media_pool
media_storage = resolve.media_storage
ocf_folder = media_pool.add_subfolder(media_pool.root_folder, "OCF")
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

        res_folder = media_pool.add_subfolder(ocf_folder, key)
        clips = clips_res[key]

        media_pool.move_clips(clips, res_folder)
        media_pool.create_timeline_fromclips(res_folder.name, res_folder.clips)

        timeline = project.timeline
        timeline.set_setting(
            "useCustomSettings", "1"
        )  # enable custom timeline size != project settings
        timeline.set_setting("timelineResolutionWidth", res_x)
        timeline.set_setting("timelineResolutionHeight", res_y)

        render_settings = {
            "FormatWidth": int(int(res_x) / proxyfactor),
            "FormatHeight": int(int(res_y) / proxyfactor),
            "TargetDir": output_dir,
        }

        # Set Render Resolution
        project.set_render_settings(render_settings)
        render_ids.append(project.add_renderjob())

    return render_ids


job_ids = generate_premiere_proxies(
    "/Users/pedrolabonia/Documents/media_tests",
    "/Users/pedrolabonia/Documents/media_tests/output",
    2,
)

project.render(job_ids, interactive=True)


for i, job in enumerate(job_ids):
    render_status = project.render_status(job_ids[i])["JobStatus"]

    while render_status is not "Complete":
        time.sleep(3)
        status = project.render_status(job_ids[i])
        print(status)
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
    print(f"Job ID {job_ids[i]} | Rendering complete. | Total render time: {time_to_render},")
