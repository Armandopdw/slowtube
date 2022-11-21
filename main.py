import scrapetube
from scenedetect import detect, ContentDetector, FrameTimecode
import pytube
import os
import pandas as pd
import csv


class SlowTube:
    # init method or constructor
    def __init__(self, channels, videos_done):
        self.channels = channels
        self.videos_done = videos_done

    def export_data (self, data):
        # open the file in the write mode
        f = open('new_log.csv', 'a')
        # create the csv writer
        writer = csv.writer(f, delimiter=";")
        # write a row to the csv file
        writer.writerow(data)
        # close the file
        f.close()

    def export_data_channel(self, channel, video_id):
        # open the file in the write mode
        f = open('video_ids.csv', 'a')
        # create the csv writer
        writer = csv.writer(f, delimiter=";")
        # write a row to the csv file
        writer.writerow([channel, video_id])
        # close the file
        f.close()

    def on_downloaded(self, stream, file_handle):
        # get filename of downloaded file (we can't set a output directory) and close the handle
        print("running on downloaded")
        scene_list = detect(file_handle, ContentDetector())
        length = scene_list[-1][-1].get_seconds()
        output = [file_handle, length, round(len(scene_list),0), round(len(scene_list) / length, 2)]
        self.export_data(output)
        print(output)
        # remove original downloaded file
        os.remove(file_handle)

    def download_videos (self):
        for video in self.videos:
            if f"{video['videoId']}" not in self.videos_done:
                print(video['videoId'])
                self.export_data_channel(self.channel, video['videoId'])
                #self.videos_done.append(video['videoId'])
                yt = pytube.YouTube(f"https://www.youtube.com/watch?v={video['videoId']}")
                yt.register_on_complete_callççback(self.on_downloaded)
                stream = yt.streams.filter(file_extension='mp4', res='360p').first()
                try:
                    print('going to download')
                    stream.download(output_path="output", filename=f"video-{video['videoId']}.mp4")
                except Exception as e:
                    print(e)
                    #videos_error.append(video['videoId'])
            else:
                print("video skipped")


    def get_videos (self):
        for channel in self.channels:
            print("looping over channellist")
            self.channel = channel
            self.videos = scrapetube.get_channel(channel_url=channel, limit=30)
            self.download_videos()


df = pd.read_csv("new_log.csv", delimiter=";")
print(df.head(5))
videos_done = df["video_id"]
print(len(videos_done))


channels = [#"https://www.youtube.com/c/KaraandNate",
            #   "https://www.youtube.com/c/devaslife",
            #   "https://www.youtube.com/c/TheActionLab",
            #   "https://www.youtube.com/c/ClarityCoders",
            #   "https://www.youtube.com/channel/UCTvRcHO5jJ_JKcekLacLMuQ",
            #   "https://www.youtube.com/c/CityPlannerPlays",
               "https://www.youtube.com/watch?v=FBB6ku2RlrE",
               "https://www.youtube.com/user/PewDiePie",
               "https://www.youtube.com/@5minutecraftsyoutube",
               "https://www.youtube.com/channel/UCJplp5SjeGSdVdwsfb9Q7lQ/",  # Like Nastya
               "https://www.youtube.com/c/VladandNiki",
               "https://www.youtube.com/c/ChuChuTV"
               ]

slowtube = SlowTube(channels=channels, videos_done=videos_done)
SlowTube.get_videos(slowtube)


