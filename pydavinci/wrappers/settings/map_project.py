from typing import Optional


def bool_to_intstr(bool: bool) -> str:
    return str(int(bool))


def super_scale_forward(scalestr: str) -> Optional[int]:
    if scalestr == "auto":
        return 0
    elif scalestr == "no_scaling":
        return 1
    elif scalestr == "2x":
        return 2
    elif scalestr == "3x":
        return 3
    elif scalestr == "4x":
        return 4

    return None


def super_scale_reverse(scale: int) -> Optional[str]:
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


SETTINGS_MAP = {
    "audioCaptureNumChannels": str,
    "audioOutputHasTimecode": str,
    "audioPlayoutNumChannels": str,
    "colorAcesGamutCompressType": str,
    "colorAcesIDT": str,
    "colorAcesNodeLUTProcessingSpace": str,
    "colorAcesODT": str,
    "colorGalleryStillsLocation": str,
    "colorGalleryStillsNamingCustomPattern": str,
    "colorGalleryStillsNamingEnabled": str,
    "colorGalleryStillsNamingPattern": str,
    "colorGalleryStillsNamingWithStillNumber": str,
    "colorKeyframeDynamicsEndProfile": str,
    "colorKeyframeDynamicsStartProfile": str,
    "colorLuminanceMixerDefaultZero": str,
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
    "colorUseBGRPixelOrderForDPX": str,
    "colorUseContrastSCurve": str,
    "colorUseLegacyLogGrades": str,
    "colorUseLocalVersionsAsDefault": str,
    "colorUseStereoConvergenceForEffects": str,
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
    "hdr10PlusControlsOn": str,
    "hdrDolbyControlsOn": str,
    "hdrDolbyMasterDisplay": str,
    "hdrDolbyVersion": str,
    "hdrMasteringLuminanceMax": str,
    "hdrMasteringOn": str,
    "imageDeinterlaceQuality": str,
    "imageEnableFieldProcessing": str,
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
    "limitBroadcastSafeOn": int,
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
    "perfOptimisedMediaOn": str,  # Menu: Playback -> Use Optimized media if Available
    "perfOptimizedResolutionRatio": str,
    "perfProxyMediaOn": str,  # Menu: Playback -> Use Proxy Media NOTE: this might change with the new v18 - test
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
    "videoMonitorUseHDROverHDMI": str,
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
    "superScale": super_scale_forward,
    "useCustomSettings": bool_to_intstr,
}
