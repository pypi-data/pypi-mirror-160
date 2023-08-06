import cv2 as cv
import uuid
from datetime import  datetime
import imageio
import os


def get_video_meta_data(file_path):    
        video_instance = cv.VideoCapture(file_path)
        frames = video_instance.get(cv.CAP_PROP_FRAME_COUNT)
        frames_per_second =video_instance.get(cv.CAP_PROP_FPS)
        length_in_second = int(frames/frames_per_second)
        video_instance = None
        return  (frames_per_second,length_in_second,frames)

def _save_an_image(image_name):
    pass

def crop_video(filename,path,output_file_name=None,end_offset_seconds=None,skip_seconds=None,get_file_name=None,frame_rate=None,max_images=None,on_image_save=_save_an_image):


    video = cv.VideoCapture(filename)
    success,image = video.read()

    height,width,*_ = image.shape

    #Frames
    frames = video.get(cv.CAP_PROP_FRAME_COUNT)
    current_video_frame_rate = video.get(cv.CAP_PROP_FPS)
    video_time_in_seconds = int(frames/current_video_frame_rate)
    new_video = imageio.get_writer(output_file_name,"MP4",fps=current_video_frame_rate) if output_file_name else None

    if not frame_rate:
        frame_rate = current_video_frame_rate

    can_save_image_frame = False if skip_seconds else True

    video_seconds = 0
    video_frames_to_count_seconds = 0

    count = 1
    current_frame = 0

    new_video_frames = 0 

    while success:
        current_frame+=1

        if video_time_in_seconds - video_seconds <= end_offset_seconds:
            break

        if max_images and max_images < count:
            break

        video_frames_to_count_seconds+=1

        if video_frames_to_count_seconds >= current_video_frame_rate:
            video_frames_to_count_seconds=0
            video_seconds+=1

            if video_seconds >= skip_seconds:
                can_save_image_frame = True

        

        if current_frame >= frame_rate and can_save_image_frame:
            new_image_file_name = get_file_name(count,filename) if get_file_name else str(count)
            new_image_path = f"{path}/{new_image_file_name}.png"
            cv.imwrite(new_image_path,image)
            on_image_save(new_image_path)
            count+=1
            current_frame = 0

        if can_save_image_frame and new_video:
            new_video_frames+=1
            filename = str(uuid.uuid1())
            _temp_image_name_ = f"./temp-{filename}.png"
            cv.imwrite(_temp_image_name_,image)
            new_video.append_data(imageio.imread(_temp_image_name_))
            os.remove(_temp_image_name_)

        success, image = video.read()
    
    if new_video:
        new_video.close()

    video = None
    return {'saved_images':max_images if max_images else count,'saved_directory':path}


def get_middle_of_the_video(filename,path,output_file_name=None,get_file_name=None,frame_rate=None,max_images=None,on_image_save=_save_an_image):
    fps,length,frames = get_video_meta_data(filename)
    unit = int(length/3)

    return crop_video(filename,
    path,
    skip_seconds=unit,
    end_offset_seconds=unit,
    output_file_name=output_file_name,
    get_file_name=get_file_name,
    frame_rate=frame_rate,
    max_images=max_images,
    on_image_save=on_image_save)

VIDEO_CROP_PART_START = "start"
VIDEO_CROP_PART_MIDDLE = "middle"
VIDEO_CROP_PART_END = "end"

def get_a_unit_of_a_video(filename,
path,video_part,
output_file_name=None,
get_file_name=None,
frame_rate=None,
max_images=None,
on_image_save=_save_an_image):

    _fps,length,*_ = get_video_meta_data(filename)

    unit = int(length/3)

    skip_seconds = unit if video_part == VIDEO_CROP_PART_MIDDLE else 0 if video_part == VIDEO_CROP_PART_START else unit*2
    end_offset = unit if video_part == VIDEO_CROP_PART_MIDDLE else 0 if video_part == VIDEO_CROP_PART_END else unit *2
    return crop_video(filename,
    path,
    output_file_name=output_file_name,
    on_image_save=on_image_save,
    frame_rate=frame_rate,
    max_images=max_images,
    get_file_name=get_file_name,
    skip_seconds=skip_seconds,
    end_offset_seconds=end_offset
    )