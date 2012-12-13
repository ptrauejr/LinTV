class Features:
    def __init__(self, features):
        # Supports Video
        if(features & (1 << 0)):
            self.Video = True
        else:
            self.Video = False

        # Supports Photos
        if(features & (1 << 1)):
            self.Photo = True
        else:
            self.Photo = False

        # Supports Video Fair Play
        if(features & (1<<2)):
            self.VideoFairPlay = True
        else:
            self.VideoFairPlay = False

        # Supports Video Volume Control
        if(features & (1 << 3)):
            self.VideoVolumeControl = True
        else:
            self.VideoVolumeControl = false

        # Supports Video HTTP Live Streams
        if(features & (1 << 4)):
            self.VideoHTTPLiveStreams = True
        else:
            self.VideoHTTPLiveStreams = False

        # Supports Slideshow
        if(features & (1 << 5)):
            self.Slideshot = True
        else:
            self.Slideshot = False

        # Supports Screen
        if(features & (1 << 7)):
            self.Screen = True
        else:
            self.Screen = False

        # Supports ScreenRotate
        if(features & (1 << 8)):
            self.ScreenRotate = True
        else:
            self.ScreenRotate = False

        # Supports Audio
        if(features & (1 << 9)):
            self.Audio = True
        else:
            self.Audio = False

        # Supports Redundant Audio
        if(features & (1 << 11)):
            self.AudioRedundant = True
        else:
            self.AudioRedundant = False

        # Supports FPSAPv2pt5_AES_GCM
        if(features & (1 << 12)):
            self.FPSAPv2pt5_AES_GCM = True
        else:
            self.FPSAPv2pt5_AES_GCM = False

        # Supports Caching of Photos
        if(features & (1 << 13)):
            self.PhotoCaching = True
        else:
            self.PhotoCaching = False
