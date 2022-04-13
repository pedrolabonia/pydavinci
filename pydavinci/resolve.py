from typing import Dict, List, Optional, Set, Tuple, Union
from connect import load_fusionscript  # type: ignore
import exceptions
from pydavinci.connect import load_fusionscript
from pyremoteobject import PyRemoteObject



load_fusionscript()
import fusionscript as dvr_script   # type: ignore


def get_resolveobjs(objs: List) -> List[PyRemoteObject]:
    return [x._obj for x in objs]

TRACK_TYPES = ['video', 'audio', 'subtitle']
TRACK_ERROR = "Track type must be: 'video', 'audio', or 'subtitle"
    
class Resolve(object):
    
    resolve = dvr_script.scriptapp("Resolve")
    def __init__(self):
        self.pages = ['media', 'cut', 'edit', 'fusion', 'color', 'fairlight', 'deliver']
        self.project_manager: ProjectManager = ProjectManager()
        self.project: Project = Project()
        self.media_storage: MediaStorage = MediaStorage()
        self.media_pool: MediaPool = MediaPool()
        self.fusion = Resolve.resolve.Fusion()
        self._obj = Resolve.resolve

    @property
    def page(self) -> str:  
        """Page Attribute

        Returns:
            str: Returns page name
        """                
        return self._obj.GetCurrentPage()
    
    @page.setter
    def page(self, page: str) -> None:  
        if page in self.pages:
            return self._obj.OpenPage(page)
        validpages = ' '.join(map(str, self.pages))
        raise ValueError(f'"{page}" is not a valid page. Available pages are: {validpages}')

    @property
    def product_name(self) -> str:
        return self._obj.GetProductName()
    
    @property
    def version(self):
        return self._obj.GetVersionString()
    
    def load_layout(self, layout_name: str) -> bool:
        return self._obj.LoadLayoutPreset(layout_name)
    
    def update_layout(self, layout_name: str) -> bool:
        return self._obj.UpdateLayoutPreset(layout_name)
    
    def save_layout(self, layout_name: str) -> bool:
        return self._obj.SaveLayoutPreset(layout_name)
    
    def import_layout(self, path: str, layout_name: str) -> bool:
        
        return self._obj.ImportLayoutPreset(path, layout_name)
    
    def quit(self):
        return self._obj.Quit()
    
    @property
    def active_timeline(self):
        return Project().timeline

    def __repr__(self) -> str:
        return f'Resolve(Page: "{self.page}")'
                         
class ProjectManager(object):
    _obj = Resolve.resolve.GetProjectManager()
    
    def __init__(self) -> None:
        self.project: Project = Project()
        
    def create_project(self, project_name: str):
        created = ProjectManager._obj.CreateProject(project_name)
        return Project(created)
    
    def load_project(self, project_name:str) -> bool:
        return ProjectManager._obj.LoadProject(project_name)
    
    def create_folder(self, folder_name: str) -> bool:
        return ProjectManager._obj.CreateFolder(folder_name)
        
    def delete_folder(self, folder_name: str) -> bool:
        return ProjectManager._obj.DeleteFolder(folder_name)

    def project_list(self) -> List[str]:
        return ProjectManager._obj.GetProjectListInCurrentFolder()
    
    def folder_list(self) -> List[str]:
        return ProjectManager._obj.GetFolderListInCurrentFolder()
    
    def goto_root_folder(self) -> bool:
        return ProjectManager._obj.GotoRootFolder()
    
    def goto_parent_folder(self) -> bool:
        return ProjectManager._obj.GotoParentFolder()
    
    @property
    def folder(self) -> str:
        return ProjectManager._obj.GetCurrentFolder()
    
    def open_folder(self, folder_name: str) -> bool:
        return ProjectManager._obj.OpenFolder(folder_name)
    
    def import_project(self, path: str) -> bool:
        return ProjectManager._obj.ImportProject(path)
    
    def export_project(self, project_name: str, path: str, stills_and_luts: bool = True) -> bool:
        return ProjectManager._obj.ExportProject(project_name, path, stills_and_luts)
    
    def restore_project(self, path: str) -> bool:
        return ProjectManager._obj.RestoreProject(path)
    
    @property
    def db(self) -> dict:
        return ProjectManager._obj.GetCurrentDatabase()
    
    @db.setter
    def db(self, db_info: dict) -> bool:
        return ProjectManager._obj.SetCurrentDatabase(db_info)
    
    @property
    def db_list(self) -> List[Dict]:
        return ProjectManager._obj.GetDatabaseList()
       
class Project(object):
    """Project class.

    Args:
        object (_type_): _description_

    Returns:
        _type_: Object class
    """    
    _obj = ProjectManager._obj.GetCurrentProject()
    
    def __init__(self, prj = None) -> None:
        if prj:
            self._obj = prj
        else:
            self._obj = Project._obj


    @property
    def mediapool(self) -> 'MediaPool':
        return MediaPool(self._obj.GetMediaPool())
    
    @property
    def timeline_count(self) -> int:
        return self._obj.GetTimelineCount()

    @property
    def name(self):
        return self._obj.GetName()
    
    @name.setter
    def name(self, name: str) -> bool:
        return self._obj.SetName(name)


    @property
    def presets(self) -> list:
        return self._obj.GetPresetList()
    
    def set_preset(self, preset_name: str) -> bool:
        return self._obj.SetPreset(preset_name)
    
    def add_renderjob(self) -> str:
        """Adds current render settings to a render job

        Returns:
            str: returns render job id
        """        
        return self._obj.AddRenderJob()
    
    def delete_renderjob(self, job_id: str) -> bool:
        """Deltes render job

        Args:
            job_id (str): render job ID

        Returns:
            bool: True if ID exists, false otherwise
        """        
        return self._obj.DeleteRenderJob(job_id)
    
    def delete_all_renderjobs(self) -> bool:
        """Deletes all renderjobs

        Returns:
            bool: True if succesfull, false otherwise
        """        
        return self._obj.DeleteAllRenderJobs()
    
    @property
    def render_jobs(self) -> list:
        return self._obj.GetRenderJobList()
        
    @property
    def render_presets(self) -> list:
        return self._obj.GetRenderPresetList()
    
    def render(self, job_ids: List[str] = [''], interactive: bool = False) -> bool:
        if job_ids == ['']:
            return self._obj.StartRendering(isInteractiveMode=interactive)
        else:
            return self._obj.StartRendering(job_ids, isInteractiveMode=interactive)


    def stop_render(self) -> None:
        return self._obj.StopRendering()
    
    def render_status(self, job_id: str) -> dict:
        return self._obj.GetRenderJobStatus(job_id)
    
    @property
    def render_formats(self) -> dict:
        return self._obj.GetRenderFormats()
    
    @property
    def render_codecs(self) -> dict:
        return self._obj.GetRenderCodecs()
    
    @property
    def current_render_format_and_codec(self) -> dict:
        return self._obj.GetCurrentRenderFormatAndCodec()
    
    def set_render_format_and_codec(self, format: str, codec: str) -> bool:
        return self._obj.SetCurrentRenderFormatAndCodec(format, codec)
    
    @property
    def render_mode(self):
        return self._obj.GetCurrentRenderMode()
    
    @render_mode.setter
    def render_mode(self, mode: str) -> bool:
        if 'individual' in mode:
            return self._obj.SetCurrentRenderMode(0)
        elif 'single' in mode:
            return self._obj.SetCurrentRenderMode(1)
        else:
            raise ValueError('Render mode must be "single" or "individual", for single clip and individual clips, respectively.')
    
    def available_resolutions(self, format: str, codec: str) -> dict:
        return self._obj.GetRenderResolutions(format, codec)     
    
    
    @property
    def rendering(self) -> bool:
        return self._obj.IsRenderingInProgress()

    def load_render_preset(self, preset_name: str) -> bool:
        return self._obj.LoadRenderPreset(preset_name)

    def save_render_preset_as(self, preset_name: str) -> bool:
        return self._obj.SaveAsNewRenderPreset(preset_name)
    
    def set_render_settings(self, render_settings: dict) -> bool:
        return self._obj.SetRenderSettings(render_settings)

    def get_setting(self, setting: str) -> dict:
        return self._obj.GetSetting(setting)
    
    def set_setting(self, setting: str, value: str) -> bool:
        return self._obj.SetSetting(setting, value)



    def save(self) -> bool:
        return ProjectManager._obj.SaveProject()
    
    def close(self) -> bool:
        return ProjectManager._obj.CloseProject(self.name)

    def open_timeline(self, name: str) -> bool:
        count = self._obj.GetTimelineCount()
        for i in range(count):
            tl = Timeline(self._obj.GetTimelineByIndex(i+1))
            if tl.name == name:
                return self._obj.SetCurrentTimeline(tl._obj)
            
        raise exceptions.ObjectNotFound("Couldn't find timeline by name.")
        


    @property
    def timeline(self):
        return Timeline(self._obj.GetCurrentTimeline())

    def refresh_luts(self):
        return self._obj.RefreshLUTList()

    def __repr__(self) -> str:
        return f'Project(Name: "{self.name})"'    

class MediaStorage(object):
    _obj = Resolve.resolve.GetMediaStorage()

    @property
    def mounted_volumes(self):
        return MediaStorage._obj.GetMountedVolumeList()

    def get_subfolders(self, folder_path: str) -> List[str]:
        return MediaStorage._obj.GetSubFolderList(folder_path)
    
    def get_file_list(self, folder_path: str) -> List[str]:
        return MediaStorage._obj.GetFileList(folder_path)
    
    def reveal_in_storage(self, path: str) -> None:
        return MediaStorage._obj.RevealInStorage(path)
    
    def add_clip_mattes(self, mediapool_item: 'MediaPoolItem', paths: Union[List[str], str], *args) -> bool:
        return MediaStorage._obj.AddClipMattesToMediaPool(mediapool_item._obj, paths, *args)

    def add_timelilne_mattes(self, paths: Union[List[str], str]) -> List['MediaPoolItem']:
        return MediaStorage._obj.AddTimelineMattesToMediaPool(paths)
    

    def addclips_to_mediapool(self, item: List[str]) -> List['MediaPoolItem']:
        #/TODO Weird bug. Even if doing return type Union[List[MediaPoolItem], MediaPoolItem], 
        # it doesn't identify the case that a single instace of MediaPoolItem might be returned, 
        # and so on the linter it can't access the properties like .name
        
        #Work around is have everything output as a list right now, user should 
        #have to use [0] on the object returned if it's a single clip.
        
        # if type(item) == type([]) and len(item) > 1:
        #     objs_added = [MediaPoolItem(x) for x in MediaStorage._obj.AddItemListToMediaPool(item)]
        #     return objs_added
        # elif type(item) == type([]) and len(item) == 1:
        #     return [MediaPoolItem(MediaStorage._obj.AddItemListToMediaPool(item[0]))]
        # else:
        #     return [MediaPoolItem(MediaStorage._obj.AddItemListToMediaPool(item)[0])]

        objs_added = [MediaPoolItem(x) for x in MediaStorage._obj.AddItemListToMediaPool(item)]
        return objs_added

class MediaPool(object):
    
    def __init__(self, obj = None) -> None:
        self._obj = Project._obj.GetMediaPool()
        
    @property
    def root_folder(self) -> 'Folder':
        return Folder(self._obj.GetRootFolder())
    
    def add_subfolder(self, parent_folder: 'Folder', folder_name: str) -> 'Folder':
        return Folder(self._obj.AddSubFolder(parent_folder._obj, folder_name))
    
    def create_empty_timeline(self, name: str) -> 'Timeline':
        return Timeline(self._obj.CreateEmptyTimeline(name))
    
    def append_to_timeline(self, clips: List['MediaPoolItem']) -> List['TimelineItem']:
        #/ TODO All types: MediaPoolItem, List[Dict], Dict
        appended = self._obj.AppendToTimeline(get_resolveobjs(clips))
        return [TimelineItem(x) for x in appended]
    
    def create_timeline_fromclips(self, name: str, clips: List['MediaPoolItem']) -> 'Timeline':
        return Timeline(self._obj.CreateTimelineFromClips(name, get_resolveobjs(clips)))
    
    def import_timeline_fromfile(self, path: str, options: dict = {}) -> 'Timeline':
        if options == {}:
            return Timeline(self._obj.ImportTimelineFromFile(path, options))
        return Timeline(self._obj.ImportTimelineFromFile(path))
    
    def delete_timelines(self, timelines: List['Timeline']) -> bool:
        return self._obj.DeleteTimelines(get_resolveobjs(timelines))
      
    @property
    def current_folder(self) -> 'Folder':
        return Folder(self._obj.GetCurrentFolder())
        
    def set_current_folder(self, folder: 'Folder') -> bool:
        return self._obj.SetCurrentFolder(folder._obj)
        
    def delete_clips(self, clips: List['MediaPoolItem']) -> bool:
         return self._obj.DeleteClips(get_resolveobjs(clips))
    
    def delete_folders(self, folders: List['Folder']) -> bool:
        return self._obj.DeleteFolders(get_resolveobjs(folders))
    
    def move_clips(self, clips: List['MediaPoolItem'], folder: 'Folder') -> bool:
        return self._obj.MoveClips(get_resolveobjs(clips), folder._obj)
                    
    def move_folders(self, folders: List['Folder'], target_folder: 'Folder') -> bool:
        return self._obj.MoveFolders(get_resolveobjs(folders), target_folder._obj)         
    
    def clip_mattes(self, clip: 'MediaPoolItem') -> List[str]:
        return self._obj.GetClipMatteList(clip._obj)
    
    def timeline_mattes(self, folder: 'Folder') -> List['MediaPoolItem']:
        result = self._obj.GetTimelineMatteList(folder._obj)
        return [MediaPoolItem(x) for x in result]
    
    def delete_mattes_bypath(self, clip: 'MediaPoolItem', path: List[str]) -> bool:
        return self._obj.DeleteClipMattes(clip._obj, path)
    
    def relink_clips(self, clips: List['MediaPoolItem'], parent_folder: str) -> bool:
        return self._obj.RelinkClips(get_resolveobjs(clips), parent_folder)    
        
    def unlink_clips(self, clips: List['MediaPoolItem']) -> bool:
        return self._obj.UnlinkClips(get_resolveobjs(clips))
    
    
    def import_media(self, paths:List[str]) -> List['MediaPoolItem']:
        #/ TODO: Implement image sequence using ImportMedia({ClipInfo})
        
        imported = self._obj.ImportMedia(paths)      
        return [MediaPoolItem(x) for x in imported]     
               
        
    def export_metadata(self, file_name: str, clips: List['MediaPoolItem']) -> bool:
        return self._obj.ExportMetadata(file_name, get_resolveobjs(clips))
    
class MediaPoolItem(object):
#/TODO: Implement a way to acess metadata such as mediapoolitem.metadata['Good Take'] = True 
#       ~ need to mess around with a private dict that uses the SetMetadata() when internal dict updates
    
    def __init__(self, obj):
        self._obj = obj
    
    @property
    def name(self) -> str:
        return self._obj.GetName()

    @property
    def metadata(self) -> dict:
        return self._obj.GetMetadata()
    
    def set_metadata(self, dict) -> bool:
        return self._obj.SetMetadata()
    
    @property
    def mediaid(self) -> str:
        return self._obj.GetMediaId()
    
    def add_marker(self, frameid: int, color: str, name: str, *, note: str = '', duration: int = 1, customdata: str = '') -> bool:
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)

    def get_custom_marker(self, customdata: str) -> dict:
        return self._obj.GetMarkerByCustomData(customdata)
    
    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        return self._obj.UpdateMarkerCustomData(frameid, customdata)
    
    def marker_custom_data(self, frameid: int) -> str:
        return self._obj.GetMarkerCustomData(frameid)
        
    def delete_marker(self, *, frameid: int = 0, color: str = '', customdata: str = '') -> bool:
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)
        if color: 
            return self._obj.DeleteMarkersByColor(color)
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")
    
    @property
    def markers(self) -> dict:
        return self._obj.GetMarkers()

    def add_flag(self, color:str) -> bool:
        return self._obj.AddFlag(color)
    
    @property
    def flags(self) ->  List[str]:
        return self._obj.GetFlagList()
    
    def clear_flags(self, color: str = 'All') -> bool:
        return self._obj.ClearFlags(color)
    
    @property
    def color(self) -> str:
        return self._obj.GetClipColor()
    
    @color.setter
    def color(self, color) -> bool:
        return self._obj.SetClipColor(color)
    
    def clear_color(self) -> bool:
        return self._obj.ClearClipColor()
    
    @property
    def properties(self) -> dict:
        return self._obj.GetClipProperty()
    
    def set_property(self, name: str, value: str) -> bool:
        return self._obj.SetClipProperty(name, value)

    def link_proxy(self, path: str) -> bool:
        return self._obj.LinkProxyMedia(path)
    
    def unlink_proxy(self, path: str) -> bool:
        return self._obj.UnlinkProxyMedia(path)
    
    def replace_clip(self, path: str) -> bool:
        return self._obj.ReplaceClip(path)
    
    
    
    def __repr__(self) -> str:
        return f'MediaPoolItem(Name:"{self.name})"'

class Folder(object):
    def __init__(self, obj) -> None:
        self._obj = obj
        
    @property
    def clips(self) -> List[MediaPoolItem]:
        objs = self._obj.GetClipList()
        return [MediaPoolItem(x) for x in objs]
    
    @property
    def name(self) -> str:
        return self._obj.GetName()
    
    @property
    def subfolders(self) -> List:
        return self._obj.GetSubFolderList()

    def __repr__(self) -> str:
        return f'Folder(Name:"{self.name}"'
      
class Timeline(object):
    def __init__(self, data = None) -> None:
        if data:
            self._obj = data
        else:
            self._obj = Project._obj.GetCurrentTimeline()


    @property
    def name(self) -> str:
        return self._obj.GetName()
    
    @name.setter
    def name(self, name: str) -> bool:
        return self._obj.SetName(name)

    def activate(self):
        return Project._obj.SetCurrentTimeline(self._obj)
    
    @property
    def start_frame(self) -> int:
        return self._obj.GetStartFrame()
    
    @property
    def end_frame(self) -> int:
        return self._obj.GetEndFrame()
    
    def track_count(self, track_type) -> int:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        else:
            return self._obj.GetTrackCount(track_type)

    def items(self, track_type: str, track_index: int) -> List['TimelineItem']:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
            
        return [TimelineItem(x) for x in self._obj.GetItemListInTrack(track_type, track_index)]

    
    ### MARKER STUFF 
    def add_marker(self, frameid: int, color: str, name: str, *, note: str = '', duration: int = 1, customdata: str = '') -> bool:
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)

    def get_custom_marker(self, customdata: str) -> dict:
        return self._obj.GetMarkerByCustomData(customdata)
    
    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        return self._obj.UpdateMarkerCustomData(frameid, customdata)
    
    def marker_custom_data(self, frameid: int) -> str:
        return self._obj.GetMarkerCustomData(frameid)
        
    def delete_marker(self, *, frameid: int = 0, color: str = '', customdata: str = '') -> bool:
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)
        if color: 
            return self._obj.DeleteMarkersByColor(color)
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")
    
    @property
    def markers(self) -> dict:
        return self._obj.GetMarkers()

    ### END MARKER STUFF

    def apply_grade_from_DRX(self, drx_path: str, grade_mode: int, timeline_items: List['TimelineItem']) -> bool:
        if type(timeline_items) == type([]):
            items = get_resolveobjs(timeline_items)
            return self._obj.ApplyGradeFromDRX(drx_path, grade_mode, items)
        else:
            raise ValueError('Timeline Items must be a list of TimelineItems')
            
    @property
    def timecode(self) -> str:
        return self._obj.GetCurrentTimecode()
    
    @property
    def current_video_item(self) -> 'TimelineItem':
        return TimelineItem(self._obj.GetCurrentVideoItem())


    @property
    def current_clip_thumbnail(self) -> dict:
        return self._obj.GetCurrentClipThumbnailImage()
    
    def get_track_name(self, track_type: str, track_index: int) -> str:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        return self._obj.GetTrackName(track_type, track_index)

    def set_track_name(self, track_type: str, track_index:int, new_name: str) -> bool:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        return self._obj.SetTrackName(track_type, track_index, new_name)    
    
    def duplicate_timeline(self, track_name: str = ''):
        if track_name:
            return Timeline(self._obj.DuplicateTimeline(track_name))
        else:
            return Timeline(self._obj.DuplicateTimeline())
    
    def create_compound_clip(self, timeline_items: List['TimelineItem'], clip_info: dict = {}) -> 'TimelineItem':
        if clip_info == {}:
            return TimelineItem(self._obj.CreateCompountClip(get_resolveobjs(timeline_items)))
        
        return TimelineItem(self._obj.CreateCompountClip(get_resolveobjs(timeline_items), clip_info))
    
    def create_fusion_clip(self, timeline_items: List['TimelineItem']) -> 'TimelineItem':
        return TimelineItem(self._obj.CreateFusionClip(get_resolveobjs(timeline_items)))
    
    def import_aaf_into_timeline(self, file_path: str, import_options: dict = {}) -> bool:
        if import_options == {}:
            return self._obj.ImportIntoTimeline(file_path)
        return self._obj.ImportIntoTimeline(file_path, import_options)
    
    def export(self, file_name: str, export_type, export_subtype) -> bool:
        #/ TODO: Do the Enums here. For now we're just passing as-is.
        return self._obj.Export(file_name, export_type, export_subtype)

    def get_setting(self, settingname: str = '') -> str:
        if settingname == '':
            return self._obj.GetSetting()
        return self._obj.GetSetting(settingname)
    
    def set_setting(self, setting_name: str, value: str) -> bool:
        return self._obj.SetSetting(setting_name, value)
    
    def insert_generator(self, generator_name: str) -> 'TimelineItem':
        return TimelineItem(self._obj.InsertGeneratorIntoTimeline(generator_name))
    
    def insert_fusion_generator(self, generator_name: str) -> 'TimelineItem':
        return TimelineItem(self._obj.InsertFusionGeneratorIntoTimeline(generator_name))
    
    def insert_ofx_generator(self, generator_name: str) -> 'TimelineItem':
        return TimelineItem(self._obj.InsertOFXGeneratorIntoTimeline(generator_name))
    
    def insert_title(self, title_name: str) -> 'TimelineItem':
        return TimelineItem(self._obj.InsertTitleIntoTimeline(title_name))
    
    def insert_fusion_title(self, title_name: str) -> 'TimelineItem':
        return TimelineItem(self._obj.InsertFusionTitleIntoTimeline(title_name))
 
class TimelineItem(object):
    def __init__(self, obj):
        self._obj = obj

    @property
    def name(self) -> str:
        return self._obj.GetName()

    @property
    def duration(self) -> int:
        return self._obj.GetDuration()
   
    @property
    def start(self) -> int:
        return self._obj.GetStart()
     
    @property
    def end(self) -> int:
        return self._obj.GetEnd()
    
    @property
    def left_offset(self) -> int:
        return self._obj.GetLeftOffset()
    
    @property
    def right_offset(self) -> int:
        return self._obj.GetRightOffset()
    
    def add_marker(self, frameid: int, color: str, name: str, *, note: str = '', duration: int = 1, customdata: str = '') -> bool:
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)

    def get_custom_marker(self, customdata: str) -> dict:
        return self._obj.GetMarkerByCustomData(customdata)
    
    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        return self._obj.UpdateMarkerCustomData(frameid, customdata)
    
    def marker_custom_data(self, frameid: int) -> str:
        return self._obj.GetMarkerCustomData(frameid)
        
    def delete_marker(self, *, frameid: int = 0, color: str = '', customdata: str = '') -> bool:
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)
        if color: 
            return self._obj.DeleteMarkersByColor(color)
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")
    
    @property
    def markers(self) -> dict:
        return self._obj.GetMarkers()

    def add_flag(self, color:str) -> bool:
        return self._obj.AddFlag(color)
    
    @property
    def flags(self) ->  List[str]:
        return self._obj.GetFlagList()
    
    def clear_flags(self, color: str = 'All') -> bool:
        return self._obj.ClearFlags(color)
    
    @property
    def color(self) -> str:
        return self._obj.GetClipColor()
    
    @color.setter
    def color(self, color) -> bool:
        return self._obj.SetClipColor(color)
    
    def clear_color(self) -> bool:
        return self._obj.ClearClipColor()


    def add_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.AddVersion(name, type)
        
    def delete_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.DeleteVersionByName(name, type)

    def load_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.LoadVersionByName(name, type)

    def rename_version(self, oldname: str, newname: str, type: int = 0) -> bool:
        return self._obj.RenameVersionByName(oldname, newname, type)
    
    @property
    def mediapoolitem(self) -> MediaPoolItem:
        return self._obj.GetMediaPoolItem()

    #/TODO: Add Stero and Fusion wrappers
    
    def set_lut(self, node_index: int, lut_path: str) -> bool:
        return self._obj.SetLUT(node_index, lut_path)

    def set_cdl(self, cdl: dict) -> bool:
        return self._obj.SetCDL(cdl)
    
    def add_take(self, mediapool_item: MediaPoolItem, startframe: int = 0, endframe: int = 0) -> bool:
        return self._obj.AddTake(mediapool_item, startframe, endframe)

    @property
    def take(self) -> int:
        return self._obj.GetSelectedTakeIndex()
    
    @take.setter
    def take(self, takeindex: int) -> bool:
        return self._obj.SelectTakeByIndex(takeindex)

    @property
    def takes(self) -> int:
        return self._obj.GetTakesCount()

    def take_info(self, takeindex:int = 0) -> dict:
        if takeindex:
            return self._obj.GetTakeByIndex(takeindex)
        else:
            return self._obj.GetTakeByIndex(self._obj.GetSelectedTakeIndex())
        
    def delete_take(self, takeindex:int) -> bool:
        return self._obj.DeleteTakeByIndex(takeindex)
    
    def finalize_take(self, takeindex:int = 0) -> bool:
        if takeindex:
            self.take = takeindex
            return self._obj.FinalizeTake()
        else:
            return self._obj.FinalizeTake()
        
    def copy_grade_to(self, timeline_items: list) -> bool:
        return self._obj.CopyGrades(timeline_items)
    
    def __repr__(self) -> str:
        clip_repr = str(self.start) + '{| ' + str(self.duration) + ' |}' + str(self.end)
        return f'TimelineItem(Name:"{self.name}", In/Duration/Out: {clip_repr})'
 