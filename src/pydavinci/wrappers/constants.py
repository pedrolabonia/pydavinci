"""
Enumerated values (constants) of the DaVinci Resolve scripting API, e.g. ``AUDIO_SYNC_TIMECODE``.

Resolve publishes its enumerations as attributes of the ``resolve`` object (``resolve.AUDIO_SYNC_TIMECODE``). Their values
are only known at runtime, so this module looks them up on first access (and caches them):

```python
from pydavinci.wrappers import constants

constants.AUDIO_SYNC_TIMECODE                # 1.0
constants.get("AUDIO_SYNC_TIMECODE")         # 1.0
constants.lookup("AUDIO_SYNC_", "timecode")  # 1.0 - a string maps to a constant, a number is passed through
```

The names declared below are the constants of DaVinci Resolve 21.1.2, typed for autocompletion - any other constant of
the running Resolve works as well. Unknown names raise an ``AttributeError`` (Resolve itself answers them with ``None``).

Wrapper methods that take an enumerated value (e.g.
[``MediaPool.auto_sync_audio``][pydavinci.wrappers.mediapool.MediaPool.auto_sync_audio]) accept the constant or the
name without its prefix (``"timecode"``).
"""
from typing import Dict, Union

import pydavinci.main

_cache: Dict[str, float] = {}


def get(name: str) -> float:
    """
    Returns the value of the Resolve constant ``name``.

    Args:
        name (str): constant name, e.g. ``"AUDIO_SYNC_TIMECODE"``

    Raises:
        AttributeError: Resolve has no constant ``name``

    Returns:
        float: constant value
    """
    if name in _cache:
        return _cache[name]
    value = getattr(pydavinci.main.resolve_obj, name, None) if name.isupper() else None
    if value is None:
        raise AttributeError(f"DaVinci Resolve has no constant {name!r}")
    _cache[name] = value
    return value  # type: ignore[no-any-return]


def lookup(prefix: str, value: Union[str, float, int]) -> Union[float, int]:
    """
    Maps a name to the Resolve constant ``prefix + NAME``, numbers (e.g. constants) are returned unchanged.

    The name is case-insensitive, spaces and dashes count as underscores:
    ``lookup("AUDIO_SYNC_", "waveform")`` returns ``AUDIO_SYNC_WAVEFORM``.

    Args:
        prefix (str): constant prefix, e.g. ``"AUDIO_SYNC_"``
        value (Union[str, float, int]): name without prefix, or a value

    Raises:
        AttributeError: Resolve has no such constant

    Returns:
        Union[float, int]: constant value
    """
    if isinstance(value, str):
        return get(prefix + value.strip().upper().replace(" ", "_").replace("-", "_"))
    return value


def __getattr__(name: str) -> float:
    if not name.isupper() or name.startswith("_"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return get(name)


# Constants of DaVinci Resolve 21.1.2, grouped by the type alias of DaVinciResolveScript.pyi.
# Declared only - the values are looked up in the running Resolve by __getattr__.

# KeyframeMode
KEYFRAME_MODE_ALL: float
KEYFRAME_MODE_COLOR: float
KEYFRAME_MODE_SIZING: float

# CloudSettingKey
CLOUD_SETTING_PROJECT_NAME: float
CLOUD_SETTING_PROJECT_MEDIA_PATH: float
CLOUD_SETTING_IS_COLLAB: float
CLOUD_SETTING_SYNC_MODE: float
CLOUD_SETTING_IS_CAMERA_ACCESS: float

# CloudSyncMode
CLOUD_SYNC_NONE: float
CLOUD_SYNC_PROXY_ONLY: float
CLOUD_SYNC_PROXY_AND_ORIG: float

# PhotoExportFormat
PHOTO_FORMAT_JPEG: float
PHOTO_FORMAT_PNG: float
PHOTO_FORMAT_HEIC: float
PHOTO_FORMAT_TIFF: float

# PhotoAutoQuality
PHOTO_AUTO_QUALITY_LEAST: float
PHOTO_AUTO_QUALITY_LOW: float
PHOTO_AUTO_QUALITY_MEDIUM: float
PHOTO_AUTO_QUALITY_HIGH: float
PHOTO_AUTO_QUALITY_BEST: float

# PhotoTiffCompressionType
PHOTO_TIFF_COMPRESSION_NONE: float
PHOTO_TIFF_COMPRESSION_LZW: float
PHOTO_TIFF_COMPRESSION_ZIP: float

# PhotoScaleMode
PHOTO_SCALE_ORIGINAL: float
PHOTO_SCALE_DIMENSIONS: float
PHOTO_SCALE_SHORT_SIDE: float
PHOTO_SCALE_LONG_SIDE: float
PHOTO_SCALE_PERCENT: float
PHOTO_SCALE_MEGAPIXELS: float

# PhotoResolutionUnit
PHOTO_RESOLUTION_UNIT_PPI: float
PHOTO_RESOLUTION_UNIT_PPCM: float

# AudioSyncSettingKey
AUDIO_SYNC_MODE: float
AUDIO_SYNC_CHANNEL_NUMBER: float
AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO: float
AUDIO_SYNC_RETAIN_VIDEO_METADATA: float

# AudioSyncMode
AUDIO_SYNC_WAVEFORM: float
AUDIO_SYNC_TIMECODE: float
AUDIO_SYNC_IN: float
AUDIO_SYNC_OUT: float
AUDIO_SYNC_MARKER: float

# AudioSyncChannel
AUDIO_SYNC_CHANNEL_AUTOMATIC: float
AUDIO_SYNC_CHANNEL_MIX: float

# MulticamAngleSyncMode
MULTICAM_ANGLE_SYNC_IN: float
MULTICAM_ANGLE_SYNC_OUT: float
MULTICAM_ANGLE_SYNC_TIMECODE: float
MULTICAM_ANGLE_SYNC_AUDIO: float
MULTICAM_ANGLE_SYNC_MARKER: float

# MulticamAngleNameMode
MULTICAM_ANGLE_NAME_SEQUENTIAL: float
MULTICAM_ANGLE_NAME_ANGLE: float
MULTICAM_ANGLE_NAME_CAMERA: float
MULTICAM_ANGLE_NAME_CLIP: float
MULTICAM_ANGLE_NAME_FILE: float

# MulticamDetectMode
MULTICAM_DETECT_BY_CAMERA_NUMBER: float
MULTICAM_DETECT_BY_ANGLE: float
MULTICAM_DETECT_BY_REEL_NUMBER: float
MULTICAM_DETECT_BY_REEL_NAME: float
MULTICAM_DETECT_BY_ROLL_CARD: float
MULTICAM_DETECT_NONE: float

# MulticamAudioMode
MULTICAM_AUDIO_ADAPTIVE: float
MULTICAM_AUDIO_SOURCE: float
MULTICAM_AUDIO_REFERENCE: float
MULTICAM_AUDIO_ALL: float

# CloudSyncStatus
CLOUD_SYNC_DEFAULT: float
CLOUD_SYNC_DOWNLOAD_IN_QUEUE: float
CLOUD_SYNC_DOWNLOAD_IN_PROGRESS: float
CLOUD_SYNC_DOWNLOAD_SUCCESS: float
CLOUD_SYNC_DOWNLOAD_FAIL: float
CLOUD_SYNC_DOWNLOAD_NOT_FOUND: float
CLOUD_SYNC_UPLOAD_IN_QUEUE: float
CLOUD_SYNC_UPLOAD_IN_PROGRESS: float
CLOUD_SYNC_UPLOAD_SUCCESS: float
CLOUD_SYNC_UPLOAD_FAIL: float
CLOUD_SYNC_UPLOAD_NOT_FOUND: float
CLOUD_SYNC_SUCCESS: float

# SlateMarkerColor
MARKER_NONE: float
MARKER_BLUE: float
MARKER_CYAN: float
MARKER_GREEN: float
MARKER_YELLOW: float
MARKER_RED: float
MARKER_PINK: float
MARKER_PURPLE: float
MARKER_FUCHSIA: float
MARKER_ROSE: float
MARKER_LAVENDER: float
MARKER_SKY: float
MARKER_MINT: float
MARKER_LEMON: float
MARKER_SAND: float
MARKER_COCOA: float
MARKER_CREAM: float

# NormalizeAudioSetLevelMode
NORMALIZE_AUDIO_SET_LEVEL_RELATIVE: float
NORMALIZE_AUDIO_SET_LEVEL_INDEPENDENT: float

# AutoAlignSyncUsing
AUTO_ALIGN_CLIPS_USING_WAVEFORM: float
AUTO_ALIGN_CLIPS_USING_TIMECODE: float

# AutoAlignUseTrack
AUTO_ALIGN_CLIPS_WAVEFORM_TRACK_MIX: float
AUTO_ALIGN_CLIPS_WAVEFORM_TRACK_AUTOMATIC: float

# TimelineExportType
EXPORT_AAF: float
EXPORT_DRT: float
EXPORT_EDL: float
EXPORT_FCP_7_XML: float
EXPORT_FCPXML_1_8: float
EXPORT_FCPXML_1_9: float
EXPORT_FCPXML_1_10: float
EXPORT_HDR_10_PROFILE_A: float
EXPORT_HDR_10_PROFILE_B: float
EXPORT_TEXT_CSV: float
EXPORT_TEXT_TAB: float
EXPORT_DOLBY_VISION_VER_2_9: float
EXPORT_DOLBY_VISION_VER_4_0: float
EXPORT_DOLBY_VISION_VER_5_1: float
EXPORT_OTIO: float
EXPORT_ALE: float
EXPORT_ALE_CDL: float

# TimelineExportSubtype
EXPORT_NONE: float
EXPORT_AAF_NEW: float
EXPORT_AAF_EXISTING: float
EXPORT_CDL: float
EXPORT_SDL: float
EXPORT_MISSING_CLIPS: float

# SubtitleSettingKey
SUBTITLE_LANGUAGE: float
SUBTITLE_CAPTION_PRESET: float
SUBTITLE_CHARS_PER_LINE: float
SUBTITLE_LINE_BREAK: float
SUBTITLE_GAP: float
SUBTITLE_EXTENDED_LANGUAGE_SUPPORT: float

# AutoCaptionLanguage
AUTO_CAPTION_AUTO: float
AUTO_CAPTION_MANDARIN_SIMPLIFIED: float
AUTO_CAPTION_DUTCH: float
AUTO_CAPTION_ENGLISH: float
AUTO_CAPTION_FINNISH: float
AUTO_CAPTION_FRENCH: float
AUTO_CAPTION_GERMAN: float
AUTO_CAPTION_HINDI: float
AUTO_CAPTION_INDONESIAN: float
AUTO_CAPTION_ITALIAN: float
AUTO_CAPTION_JAPANESE: float
AUTO_CAPTION_KOREAN: float
AUTO_CAPTION_MALAY: float
AUTO_CAPTION_NORWEGIAN: float
AUTO_CAPTION_POLISH: float
AUTO_CAPTION_PORTUGUESE: float
AUTO_CAPTION_ROMANIAN: float
AUTO_CAPTION_RUSSIAN: float
AUTO_CAPTION_SPANISH: float
AUTO_CAPTION_SWEDISH: float
AUTO_CAPTION_TURKISH: float
AUTO_CAPTION_VIETNAMESE: float
AUTO_CAPTION_TAMIL: float
AUTO_CAPTION_THAI: float
AUTO_CAPTION_DANISH: float
AUTO_CAPTION_MANDARIN_TRADITIONAL: float
AUTO_CAPTION_AFRIKAANS: float
AUTO_CAPTION_ARABIC: float
AUTO_CAPTION_ARMENIAN: float
AUTO_CAPTION_AZERBAIJANI: float
AUTO_CAPTION_BELARUSIAN: float
AUTO_CAPTION_BOSNIAN: float
AUTO_CAPTION_BULGARIAN: float
AUTO_CAPTION_CANTONESE: float
AUTO_CAPTION_CATALAN: float
AUTO_CAPTION_CROATIAN: float
AUTO_CAPTION_CZECH: float
AUTO_CAPTION_ESTONIAN: float
AUTO_CAPTION_GALICIAN: float
AUTO_CAPTION_GREEK: float
AUTO_CAPTION_HEBREW: float
AUTO_CAPTION_HUNGARIAN: float
AUTO_CAPTION_ICELANDIC: float
AUTO_CAPTION_KANNADA: float
AUTO_CAPTION_KAZAKH: float
AUTO_CAPTION_LATVIAN: float
AUTO_CAPTION_LITHUANIAN: float
AUTO_CAPTION_MACEDONIAN: float
AUTO_CAPTION_MAORI: float
AUTO_CAPTION_MARATHI: float
AUTO_CAPTION_MYANMAR: float
AUTO_CAPTION_NEPALI: float
AUTO_CAPTION_PERSIAN: float
AUTO_CAPTION_SERBIAN: float
AUTO_CAPTION_SLOVAK: float
AUTO_CAPTION_SLOVENIAN: float
AUTO_CAPTION_SWAHILI: float
AUTO_CAPTION_TAGALOG: float
AUTO_CAPTION_UKRAINIAN: float
AUTO_CAPTION_URDU: float
AUTO_CAPTION_WELSH: float

# AutoCaptionPreset
AUTO_CAPTION_SUBTITLE_DEFAULT: float
AUTO_CAPTION_TELETEXT: float
AUTO_CAPTION_NETFLIX: float

# AutoCaptionLineBreak
AUTO_CAPTION_LINE_SINGLE: float
AUTO_CAPTION_LINE_DOUBLE: float

# DolbyVisionAnalysisType
DLB_BLEND_SHOTS: float

# DynamicZoomEase
DYNAMIC_ZOOM_EASE_LINEAR: float
DYNAMIC_ZOOM_EASE_IN: float
DYNAMIC_ZOOM_EASE_OUT: float
DYNAMIC_ZOOM_EASE_IN_AND_OUT: float

# CompositeMode
COMPOSITE_NORMAL: float
COMPOSITE_ADD: float
COMPOSITE_SUBTRACT: float
COMPOSITE_DIFF: float
COMPOSITE_MULTIPLY: float
COMPOSITE_SCREEN: float
COMPOSITE_OVERLAY: float
COMPOSITE_HARDLIGHT: float
COMPOSITE_SOFTLIGHT: float
COMPOSITE_DARKEN: float
COMPOSITE_LIGHTEN: float
COMPOSITE_COLOR_DODGE: float
COMPOSITE_COLOR_BURN: float
COMPOSITE_EXCLUSION: float
COMPOSITE_HUE: float
COMPOSITE_SATURATE: float
COMPOSITE_COLORIZE: float
COMPOSITE_LUMA_MASK: float
COMPOSITE_DIVIDE: float
COMPOSITE_LINEAR_DODGE: float
COMPOSITE_LINEAR_BURN: float
COMPOSITE_LINEAR_LIGHT: float
COMPOSITE_VIVID_LIGHT: float
COMPOSITE_PIN_LIGHT: float
COMPOSITE_HARD_MIX: float
COMPOSITE_LIGHTER_COLOR: float
COMPOSITE_DARKER_COLOR: float
COMPOSITE_FOREGROUND: float
COMPOSITE_ALPHA: float
COMPOSITE_INVERTED_ALPHA: float
COMPOSITE_LUM: float
COMPOSITE_INVERTED_LUM: float

# KeyframeTiming
KEYFRAME_TIMING_MAINTAIN: float
KEYFRAME_TIMING_STRETCH_TO_FIT: float

# RetimeProcess
RETIME_USE_PROJECT: float
RETIME_NEAREST: float
RETIME_FRAME_BLEND: float
RETIME_OPTICAL_FLOW: float

# MotionEstimation
MOTION_EST_USE_PROJECT: float
MOTION_EST_STANDARD_FASTER: float
MOTION_EST_STANDARD_BETTER: float
MOTION_EST_ENHANCED_FASTER: float
MOTION_EST_ENHANCED_BETTER: float
MOTION_EST_SPEED_WARP_FASTER: float
MOTION_EST_SPEED_WARP_BETTER: float
MOTION_EST_METAL: float

# Scaling
SCALE_USE_PROJECT: float
SCALE_CROP: float
SCALE_FIT: float
SCALE_FILL: float
SCALE_STRETCH: float

# ResizeFilter
RESIZE_FILTER_USE_PROJECT: float
RESIZE_FILTER_SHARPER: float
RESIZE_FILTER_SMOOTHER: float
RESIZE_FILTER_BICUBIC: float
RESIZE_FILTER_BILINEAR: float
RESIZE_FILTER_BESSEL: float
RESIZE_FILTER_BOX: float
RESIZE_FILTER_CATMULL_ROM: float
RESIZE_FILTER_CUBIC: float
RESIZE_FILTER_GAUSSIAN: float
RESIZE_FILTER_LANCZOS: float
RESIZE_FILTER_MITCHELL: float
RESIZE_FILTER_NEAREST_NEIGHBOR: float
RESIZE_FILTER_QUADRATIC: float
RESIZE_FILTER_SINC: float
RESIZE_FILTER_LINEAR: float

# CacheMode
CACHE_AUTO_ENABLED: float
CACHE_DISABLED: float
CACHE_ENABLED: float

# DialogueLevelerMode
DIALOGUE_LEVELER_MODE_ALLOW_WIDER_DYNAMICS: float
DIALOGUE_LEVELER_MODE_OPTIMIZE_MODERATE_LEVELS: float
DIALOGUE_LEVELER_MODE_MORE_LIFT_FOR_LOW_LEVELS: float
DIALOGUE_LEVELER_MODE_LIFT_SOFT_WHISPERY_SOURCES: float

# FlattenMulticamGrade
FLATTEN_MULTICAM_COPY_GRADE: float
FLATTEN_MULTICAM_RETAIN_GRADE_FROM_ANGLE: float

# ExportLutType
EXPORT_LUT_17PTCUBE: float
EXPORT_LUT_33PTCUBE: float
EXPORT_LUT_65PTCUBE: float
EXPORT_LUT_PANASONICVLUT: float

# SmartSwitchQuality
SMART_SWITCH_QUALITY_FASTER: float
SMART_SWITCH_QUALITY_BETTER: float

# SmartSwitchWideAngleFrequency
SMART_SWITCH_WIDE_ANGLE_FREQ_LOW: float
SMART_SWITCH_WIDE_ANGLE_FREQ_MEDIUM: float
SMART_SWITCH_WIDE_ANGLE_FREQ_HIGH: float

# SmartSwitchAnalysisMode
SMART_SWITCH_ANALYSIS_MODE_NONE: float
SMART_SWITCH_ANALYSIS_MODE_DETECT_WIDE_ANGLE: float
SMART_SWITCH_ANALYSIS_MODE_AUDIO_ONLY: float

# CloneChecksumType
CLONE_CHECKSUM_TYPE_NONE: float
CLONE_CHECKSUM_TYPE_FILESIZE: float
CLONE_CHECKSUM_TYPE_CRC32: float
CLONE_CHECKSUM_TYPE_MD5: float
CLONE_CHECKSUM_TYPE_SHA256: float
CLONE_CHECKSUM_TYPE_SHA512: float
CLONE_CHECKSUM_TYPE_XXH_64: float

# PhotoImageOrientation
PHOTO_ORIENTATION_0_DEG: float
PHOTO_ORIENTATION_90_DEG_RIGHT: float
PHOTO_ORIENTATION_180_DEG: float
PHOTO_ORIENTATION_90_DEG_LEFT: float

# PhotoCropRatio
PHOTO_CROP_RATIO_AS_SHOT: float
PHOTO_CROP_RATIO_CUSTOM: float
PHOTO_CROP_RATIO_16X9: float
PHOTO_CROP_RATIO_1X1: float
PHOTO_CROP_RATIO_4X5: float
PHOTO_CROP_RATIO_2X3: float
PHOTO_CROP_RATIO_4X3: float

# PhotoLookType
PHOTO_LOOK_DEFAULT: float
PHOTO_LOOK_BW: float
PHOTO_LOOK_BRIGHT: float
PHOTO_LOOK_COOL: float
PHOTO_LOOK_DRAMATIC: float
PHOTO_LOOK_GOLD: float
PHOTO_LOOK_NATURAL: float
PHOTO_LOOK_RICH_CONTRAST: float
PHOTO_LOOK_ROSE: float
PHOTO_LOOK_VIBRANT: float
PHOTO_LOOK_WARM: float
