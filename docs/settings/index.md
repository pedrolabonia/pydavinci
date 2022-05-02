## Project vs. Timeline Settings

By default, `Project` settings apply to all `Timeline`s in the project. To change that behavior, you need to use the method [`Timeline.custom_settings(True)`][pydavinci.wrappers.timeline.Timeline.custom_settings]. This will allow timeline settings to be independent from the project settings. You could then have a Project resolution of `1920x1080` for example and a Timeline resolution of `3840x2160`.

<figure markdown>
![Settings Auto completion](../static/settings_autocomplete.gif)
<figcaption>Auto-completion and error catching for settings in the IDE</figcaption>
</figure>


## Literals
Whenever you see `Literal` on the type hints in the documentation, it means that the values listed need to be _literally_ as shown. These literals were gathered by testing which settings are valid on the interface.

!!! note
    Not all settings have been tested. For a fallback, you can still use the regular `get_setting()` and `set_settings()` methods on [`Project`][pydavinci.wrappers.project.Project.get_setting] and [`Timeline`][pydavinci.wrappers.timeline.Timeline.get_setting]

