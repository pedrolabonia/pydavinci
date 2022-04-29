from typing import Optional, Union
from pydavinci.main import resolve_obj


def bool_to_intstr(bool: bool) -> str:
    return str(int(bool))


def super_scale_transform(scale: Union[int, str]) -> Optional[Union[str, int]]:
    if isinstance(scale, int):
        if scale == 0:
            return "auto"
        elif scale == 1:
            return "no_scaling"
        elif scale == 2:
            return "2x"
        elif scale == 3:
            return "3x"
        elif scale == 4:
            return "4x"
    else:
        if scale == "auto":
            return 0
        elif scale == "no_scaling":
            return 1
        elif scale == "2x":
            return 2
        elif scale == "3x":
            return 3
        elif scale == "4x":
            return 4

    return scale


# This is a map that's applied when going from pydantic to the Resolve API.
# Bool to intstr for example gets the bool type from Python, and converts it
# either to a string "1" or "0"

# Superscale has it's own shenanigans

# Also noted are some observations I made while testing out some settings.
# Didn't test them all cause I'm not that masochist.


SETTINGS_MAP = {
    "audioCaptureNumChannels": str,
    "audioOutputHasTimecode": bool_to_intstr,
    "audioPlayoutNumChannels": str,
    "colorAcesGamutCompressType": str,
    "colorAcesIDT": str,
    "colorAcesNodeLUTProcessingSpace": str,
    "colorAcesODT": str,
    "colorGalleryStillsLocation": str,
    "colorGalleryStillsNamingCustomPattern": str,
    "colorGalleryStillsNamingEnabled": bool_to_intstr,
    "colorGalleryStillsNamingPattern": str,
    "colorGalleryStillsNamingWithStillNumber": str,
    "colorKeyframeDynamicsEndProfile": str,
    "colorKeyframeDynamicsStartProfile": str,
    "colorLuminanceMixerDefaultZero": bool_to_intstr,
    "colorScienceMode": str,
    "colorSpaceInput": str,
    "colorSpaceInputGamma": str,
    "colorSpaceOutput": str,
    "colorSpaceOutputGamma": str,
    "colorSpaceOutputGamutMapping": str,
    "colorSpaceOutputGamutSaturationKnee": str,
    "colorSpaceOutputGamutSaturationMax": str,
    "colorSpaceOutputToneLuminanceMax": str,
    "colorSpaceOutputToneMapping": str,
    "colorSpaceTimeline": str,
    "colorSpaceTimelineGamma": str,
    "colorUseBGRPixelOrderForDPX": bool_to_intstr,
    "colorUseContrastSCurve": bool_to_intstr,
    "colorUseLegacyLogGrades": str,
    "colorUseLocalVersionsAsDefault": bool_to_intstr,
    "colorUseStereoConvergenceForEffects": bool_to_intstr,
    "colorVersion10Name": str,
    "colorVersion1Name": str,
    "colorVersion2Name": str,
    "colorVersion3Name": str,
    "colorVersion4Name": str,
    "colorVersion5Name": str,
    "colorVersion6Name": str,
    "colorVersion7Name": str,
    "colorVersion8Name": str,
    "colorVersion9Name": str,
    "graphicsWhiteLevel": str,
    "hdr10PlusControlsOn": bool_to_intstr,
    "hdrDolbyControlsOn": bool_to_intstr,
    "hdrDolbyMasterDisplay": str,
    "hdrDolbyVersion": str,
    "hdrMasteringLuminanceMax": str,
    "hdrMasteringOn": bool_to_intstr,
    "imageDeinterlaceQuality": str,
    "imageEnableFieldProcessing": bool_to_intstr,
    "imageMotionEstimationMode": str,
    "imageMotionEstimationRange": str,
    "imageResizeMode": str,
    "imageResizingGamma": str,
    "imageRetimeInterpolation": str,
    "inputDRT": str,
    "inputDRTSatRolloffLimit": str,
    "inputDRTSatRolloffStart": str,
    "isAutoColorManage": str,
    "limitAudioMeterAlignLevel": str,
    "limitAudioMeterDisplayMode": str,
    "limitAudioMeterHighLevel": str,
    "limitAudioMeterLUFS": str,
    "limitAudioMeterLoudnessScale": str,
    "limitAudioMeterLowLevel": str,
    "limitBroadcastSafeLevels": str,
    "limitBroadcastSafeOn": bool_to_intstr,
    "limitSubtitleCPL": str,
    "limitSubtitleCaptionDurationSec": str,
    "outputDRT": str,
    "outputDRTSatRolloffLimit": str,
    "outputDRTSatRolloffStart": str,
    "perfAutoRenderCacheAfterTime": str,
    "perfAutoRenderCacheComposite": bool_to_intstr,
    "perfAutoRenderCacheEnable": bool_to_intstr,
    "perfAutoRenderCacheFuEffect": bool_to_intstr,
    "perfAutoRenderCacheTransition": str,
    "perfCacheClipsLocation": str,
    "perfOptimisedCodec": str,
    "perfOptimisedMediaOn": bool_to_intstr,  # Menu: Playback -> Use Optimized media if Available
    "perfOptimizedResolutionRatio": str,
    "perfProxyMediaOn": bool_to_intstr,  # Menu: Playback -> Use Proxy Media NOTE: this might change with the new v18 - test
    "perfProxyResolutionRatio": str,  # This is not on the project settings, it's on the menu Playback -> Timeline Proxy Mode
    "perfRenderCacheCodec": str,
    "perfRenderCacheMode": str,  # Menu: Playback -> Render cache mode
    "rcmPresetMode": str,
    "separateColorSpaceAndGamma": bool_to_intstr,
    "superScaleNoiseReduction": str,
    "superScaleSharpness": str,
    "timelineDropFrameTimecode": bool_to_intstr,
    "timelineFrameRate": str,
    "timelineFrameRateMismatchBehavior": str,
    "timelineInputResMismatchBehavior": str,
    "timelineInputResMismatchCustomPreset": str,  # It has to be in Image Scaling -> Resize Filter: Custom, but can't seem to be able to set any custom presets.
    "timelineInputResMismatchUseCustomPreset": str,
    "timelineInterlaceProcessing": bool_to_intstr,
    "timelineOutputPixelAspectRatio": str,
    "timelineOutputResMatchTimelineRes": bool_to_intstr,
    "timelineOutputResMismatchBehavior": str,
    "timelineOutputResMismatchCustomPreset": str,
    "timelineOutputResMismatchUseCustomPreset": bool_to_intstr,
    "timelineOutputResolutionHeight": str,
    "timelineOutputResolutionWidth": str,
    "timelinePixelAspectRatio": str,
    "timelinePlaybackFrameRate": str,
    "timelineResolutionHeight": str,
    "timelineResolutionWidth": str,
    "timelineSaveThumbsInProject": bool_to_intstr,
    "timelineWorkingLuminance": str,  # couldn't find it
    "timelineWorkingLuminanceMode": str,  # couldn't find it
    "useCATransform": bool_to_intstr,
    "useColorSpaceAwareGradingTools": bool_to_intstr,
    "useInverseDRT": bool_to_intstr,
    "videoCaptureCodec": str,
    "videoCaptureFormat": str,
    "videoCaptureIngestHandles": str,
    "videoCaptureLocation": str,
    "videoCaptureMode": str,
    "videoDataLevels": str,  # BUG: Apparently doesn't work.. doesn't change the setting
    "videoDataLevelsRetainSubblockAndSuperWhiteData": bool_to_intstr,
    "videoDeckAdd32Pulldown": bool_to_intstr,
    "videoDeckBitDepth": str,
    "videoDeckFormat": str,
    "videoDeckNonAutoEditFrames": bool_to_intstr,
    "videoDeckOutputSyncSource": str,
    "videoDeckPrerollSec": str,
    "videoDeckSDIConfiguration": str,  # BUG: Only works with single_link, dual and quad link return "none". Cant set it too
    "videoDeckUse444SDI": bool_to_intstr,
    "videoDeckUseAudoEdit": bool_to_intstr,  # BUG: Typo - should be "auto"
    "videoDeckUseStereoSDI": bool_to_intstr,
    "videoMonitorBitDepth": str,
    "videoMonitorFormat": str,
    "videoMonitorMatrixOverrideFor422SDI": str,
    "videoMonitorSDIConfiguration": str,
    "videoMonitorScaling": str,
    "videoMonitorUse444SDI": bool_to_intstr,
    "videoMonitorUseHDROverHDMI": bool_to_intstr,
    "videoMonitorUseLevelA": bool_to_intstr,
    "videoMonitorUseMatrixOverrideFor422SDI": bool_to_intstr,
    "videoMonitorUseStereoSDI": bool_to_intstr,
    "videoPlayoutAudioFramesOffset": int,
    "videoPlayoutBatchHeadDuration": str,
    "videoPlayoutBatchTailDuration": str,
    "videoPlayoutLTCFramesOffset": str,
    "videoPlayoutMode": str,
    "videoPlayoutShowLTC": bool_to_intstr,
    "videoPlayoutShowSourceTimecode": bool_to_intstr,
    "superScale": super_scale_transform,
    "useCustomSettings": bool_to_intstr,
    "selfvalidate": bool,
}
