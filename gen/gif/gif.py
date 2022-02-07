
import imageio
from PIL import Image
import os
import io
from gen.util import overlay

def build_animation_frames(metadata,animation_path,prefix):
    frames = []
    for i in range(len(os.listdir(animation_path))):
        frame = Image.new('RGBA', (32, 32))
        for key, value in metadata.items():
            overlay(frame, Image.open(value.replace(prefix,animation_path+"/{}/".format(i))))
        frames.append(frame) 
    return frames

def pil_to_imageio(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return imageio.imread(img_byte_arr)

def frames_to_gif(frames,save_name = 'test.gif'):
    imageio.mimsave(save_name, frames)

def create_gif_from_attributes(attributes, animation_path ,prefix, save_path):
        frames_to_gif([pil_to_imageio(x) for x in build_animation_frames(attributes,animation_path,prefix)], save_path)