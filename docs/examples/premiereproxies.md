# Premiere Proxies

We all know about Premieres __particular__ need for proxies.

They have to be:

-   :material-aspect-ratio:{ .lg .middle } __Same aspect ratio as the original files__
    
        Otherwise you end up with stretched proxies, and no one likes that.
    
    ---

-   :material-cast-audio:{ .lg .middle } __Same number of audio tracks as the original files__
    
        This doesn't make sense, but that's how it is.

    ---

-   :material-timeline-clock-outline:{ .lg .middle } __Ideally same timecode__
    
        Because otherwise you're going to have headaches.

So let's fix that.

## The code

### Importing pydavinci

First, let's import and define the variables we're going to use

```py
from pydavinci.resolve import Resolve

resolve = Resolve()

project = resolve.project
project_manager = resolve.project_manager
media_pool = resolve.media_pool
media_storage = resolve.media_storage
```

### Setting up a folder to import to
Now let's create a folder to import our media, and set it as the current folder

```py
ocf_folder = media_pool.add_subfolder(media_pool.root_folder, 'OCF')
media_pool.set_current_folder(ocf_folder)
```

!!! info
    OCF means _Original Camera Format_, and it's a naming standard we all should use!

### Defining our function

Let's define our function to generate the Premiere proxies:

```py 
def generate_premiere_proxies(input_dir, proxyfactor, output_dir): 
```
Our function will take as parameters:

- `input_dir`: a path to a folder containing all our media
- `proxyfactor`: by how much we will reduce the resolution for the proxies
- `output_dir`: output directory for our proxies

!!! info
    `proxyfactor` is the number to divide the original resolution to.  
    
    __Example:__

    A `proxyfactor` of `1.5` on a `1920x1080` resolution will give you a `1280x720` resolution proxy  
    A `proxyfactor` of `2` on a `1920x1080` resolution will give you a `960x540` resolution proxy

#### Importing Media
Now we can import the media in our project, and figure out what resolutions they are

```py linenums="1" 
def generate_premiere_proxies(input_dir, proxyfactor, output_dir):
    media_pool.import_media(input_dir)
    clips_res = defaultdict(list)
    
    for media in ocf_folder.clips:
            clips_res[media.properties['Resolution']].append(media)
            
```


