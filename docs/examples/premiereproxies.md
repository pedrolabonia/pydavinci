# Premiere Proxies {: .examples}
<h5 class='examples'><a target="_blank" href="https://github.com/pedrolabonia/pydavinci/blob/main/examples/premiere_proxies.py">Just show me the code <span class="twemoji lg middle"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4Z"></path></svg></span></a></h5>

We all know about Premieres __particular__ need for proxies.

They have to be:

-   :material-aspect-ratio:{ .lg .middle } Same aspect ratio as the original files

        Otherwise you end up with stretched proxies, and no one likes that.

    ---

-   :material-cast-audio:{ .lg .middle } Same number of audio tracks as the original files

        This doesn't make sense, but that's how it is.

    ---

-   :material-timeline-clock-outline:{ .lg .middle } Ideally same timecode

        Because otherwise you're going to have headaches.

So you end up having to:

-   Create proxies in Premiere and hope you have a nice 16x9 aspect ratio because that's what the default presets use.
-   Realize you have media mixed between DCI 4k and UHD and now you gotta create an individual encoding preset
-   Realize you have to create a Media Encoder encoding preset :face_with_spiral_eyes:

If you ever had to do that at 2am you know that it works so badly it's not even funny. You create the preset and it tries to copy the files, or it can't import the preset into Premiere, or a thousand other weird things.

Then you decide to do just transcode everything in Davinci Resolve, which is probably what you should've done in the first place, but you still need to render everything in the same aspect ratio.

Let's fix that and hopefully come home early :partying_face:

----
## The code

### Importing pydavinci

Assuming we have ``pydavinci`` installed and have a Davinci project open, let's create a ``premiere_proxies.py`` file and import and define the objects we're going to use.

```py title="premiere_proxies.py"
from pydavinci import davinci

resolve = davinci.Resolve()

project = resolve.project
project_manager = resolve.project_manager
media_pool = resolve.media_pool
media_storage = resolve.media_storage
```

!!! tip
    You can also programatically create a project. Check out [``Project``][pydavinci.wrappers.project.Project-attributes]

### Setting up a folder to import to
Now let's create a folder on the media pool root folder, and set it as the current folder.

```py
ocf_folder = media_pool.add_subfolder('OCF', media_pool.root_folder)
media_pool.set_current_folder(ocf_folder)
```

!!! info
    OCF means _Original Camera Format_

### Defining our function

Let's define our function to generate the Premiere proxies:

```py
def generate_premiere_proxies(input_dir, proxyfactor, output_dir):
```
Our function will take as parameters:

- `input_dir`: a path to a folder containing all our media
- `output_dir`: output directory for our proxies
- `proxyfactor`: by how much we will reduce the resolution for the proxies

!!! info
    `proxyfactor` is the number to divide the original resolution to.

    __Example:__
    A `proxyfactor` of `1` on a `1920x1080` resolution will give you a `1920x1080` resolution proxy.

    A `proxyfactor` of `1.5` on a `1920x1080` resolution will give you a `1280x720` resolution proxy.

    A `proxyfactor` of `2` on a `1920x1080` resolution will give you a `960x540` resolution proxy

#### Importing Media
Now we can import the media in our project, and figure out what resolutions they are

```py
def generate_premiere_proxies(input_dir, proxyfactor, output_dir):
    media_pool.import_media(input_dir)
    clips_res = defaultdict(list)

    for media in ocf_folder.clips:
            clips_res[media.properties['Resolution']].append(media)

```

We first import our media using the [`media_pool.import_media()`][pydavinci.wrappers.mediapool.MediaPool.import_media] method, which imports all valid(as judged by Resolve) media files from ``input_dir`` into the media pool on our current folder. We then create a ``defaultdict`` that we will use to store all resolutions from the media.

Then we loop for each [`MediaPoolItem`][pydavinci.wrappers.mediapoolitem.MediaPoolItem-attributes] in the [`ocf_folder.clips`][pydavinci.wrappers.folder.Folder.clips] to grab each clip resolution, and store it in the ``clips_res`` dictionary which will end up looking like this:

```py
clips_res = {
    '1920x1080': [MediaPoolItem1, MediaPoolItem2],
    '3840x2160': [MediaPoolItem3, MediaPoolItem4],
    ...
}
```

!!! tip
    We're using a `defaultdict` to simplify our loop. If we used a regular dict, the first time we find a resolution we would have to first initiate it with a list value and then append to it. This way we don't need to check if we've seen this resolution before or not.

Now while the Resolve API is very powerful, it still lacks a way for us to set the default behavior of exporting audio channels to `Same as Source`, which is what we need for Premiere.. So now let's head to Davinci and create and save a render preset with that option enabled.

<figure markdown>
![Proxy Settings Figure 02](../static/Resolve_02.png)
<figcaption>On the Audio tab, we make sure we're exporting audio and we select Same as source for the audio channels. This ensures that our proxy media can be linked without issue in Premiere. Save the preset as <code>Proxies_Preset</code></figcaption>
</figure>

Now that we created our preset, let's make sure it's activated when we render the clips by using the [`project.set_preset()`][pydavinci.wrappers.project.Project.set_preset] method.

```py
def generate_premiere_proxies(input_dir, output_dir, proxyfactor):

    ...

    project.set_preset("Proxy_Preset")
```

We've imported and grabbed all clips resolutions, and now we can start our main loop.

#### Creating render jobs

First let's create an empty list which will contain our render jobs, then start our main loop and create a folder for each resolution we have and move the correct clips to that folder.


```py
def generate_premiere_proxies(input_dir, output_dir, proxyfactor):

    ...

 render_ids = []

    for key in clips_res.keys():

        res_x, res_y = key.split("x") # (1)

        res_folder = media_pool.add_subfolder(key, ocf_folder)
        clips = clips_res[key] # (2)

        media_pool.move_clips(clips, res_folder)
```


1.  When we grab resolutions from DaVinci, they come as a string, eg: `"1920x1080"`. We split the resolution to get the width and height

2.  We create a new variable containing the list of `MediaPoolItem`s for our current resolution in the loop.

<small>Make sure to click the <span class="twemoji lg middle"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2Z"></path></svg></span> buttons in the code above for more information</small>

Now we need to create a timeline containing all our `MediaPoolItem`s for the current resolution in the loop. We then activate that timeline and set the timeline resolution to be the same as the clip's resolutions, to avoid any letterboxing.

```py
def generate_premiere_proxies(input_dir, output_dir, proxyfactor):

    ...

 render_ids = []

    for key in clips_res.keys():

        ...

        media_pool.create_timeline_from_clips(
        res_folder.name, # (1)
        res_folder.clips
        )

        timeline = project.timeline
        timeline.set_setting("useCustomSettings", "1") # (2)
        timeline.set_setting("timelineResolutionWidth", res_x)
        timeline.set_setting("timelineResolutionHeight", res_y)
```

1.  This is for the created timeline name. We're using the Folder name from before, which is set to be a string representing the resolution.

2.  This allows us to set custom resolutions and framerates for timelines more easily through the Python API, without having to mess with the Project Settings.


For the next step, we need to set our render settings. Let's calculate our desired rendered resolution using our provided `proxyfactor`, set our render format/codec and output directory.

```py
def generate_premiere_proxies(input_dir, output_dir, proxyfactor):

    ...

render_ids = []

    for key in clips_res.keys():

        ...

        project.set_render_format_and_codec("mp4", "H264")
        render_settings = {  # (1)
            "FormatWidth": (int(res_x) // proxyfactor), # (2)
            "FormatHeight": (int(res_y) // proxyfactor),
            "TargetDir": output_dir,
        }
        project.set_render_settings(render_settings)
```

1.  The valid render settings that you can change are available at [Project.set_render_settings()][pydavinci.wrappers.project.Project.set_render_settings]

2.  The `\\` floor operator ensures we get an `int` back and not a `float`


!!! warning
    If for any reason your render resolution ends up being an odd number, DaVinci will throw an error in the GUI and your script won't be able to continue.

Now we're almost done! Just add the current timeline and render settings to the render queue, and append it to our `render_ids` list

```py
def generate_premiere_proxies(input_dir, output_dir, proxyfactor):

    ...

    render_ids = []

    for key in clips_res.keys():

        ...

        render_id = project.add_renderjob()
        render_ids.append(render_id)
    return render_ids

```

### Render time!

Now we can get our `job_ids` and render them out!:

```py
job_ids = generate_premiere_proxies(
    "Path/To/Folder/With/Clips",
    "Path/To/Output/Folder,
    proxyfactor=2,
    )

project.render(job_ids)

```

Resolve will start rendering all our timelines with our clips, and in the end we'll have proxies ready to be edited by Premiere.

[Check out the full code here](https://github.com/pedrolabonia/pydavinci/blob/main/examples/premiere_proxies.py), with some extra functionality at the end which just prints out a nice message on render times left and total render time.
