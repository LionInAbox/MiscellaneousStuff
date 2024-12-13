# Images in IMGUI-bundle SIMPLIFIED!:
import numpy as np
from typing import Any
from numpy.typing import NDArray
from enum import Enum
import cv2  # type: ignore
import math

from imgui_bundle import imgui, immvision, immapp, imgui_md
from imgui_bundle.demos_python import demo_utils


import pygame, moderngl

immvision.use_rgb_color_order()

ImageRgb = NDArray[np.uint8]
ImageFloat = NDArray[np.floating[Any]]


# Create Pygame Image:
pygame.init()

# doublebuf: 2 buffers: one that's on screen, one that you are currently rendering on. That's
# why it's called 'flip' for updating the screen.
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN)
display_surface = pygame.Surface((800, 600)).convert()

img = pygame.image.load("Graphics/lion.png").convert_alpha()


# Context for opengl pipeline and rendering with it, used to convert pygame surface to opengl:
ctx = moderngl.create_context()


# Convert Pygame surface to opengl texture:
def ConvertPygameSurfaceToOpenGl(surface):
    # create a new opengl texture, with 4 color channels:
    tex = ctx.texture(surface.get_size(), 4)
    # texture filtering method (anti-alias/interpolation) NEAREST is pixelperfect. You can use linear and others:
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    # RGBA order to fit between pygame and opengl:
    tex.swizzle = 'BGRA'
    # fill image data into texture, using pygame's data generation function 'get_view':
    tex.write(surface.get_view('1'))
    return tex

def ConvertPygameSurfaceToBinary(surface):
    return surface.get_view('1')

binary_texture = ConvertPygameSurfaceToBinary(img)
gl_texture = ConvertPygameSurfaceToOpenGl(img)


# Our Application State contains:
#     - the original image (image)
#     - parameters to display the images via ImmVision: they share the same zoom key,
#       so that we can move the two image in sync
class AppState:
    image: ImageRgb
    image_sobel: ImageFloat

    immvision_params: immvision.ImageParams
    immvision_params_sobel: immvision.ImageParams

    def __init__(self, image_file: str):
        self.image = demo_utils.imread_pil(image_file)
        # self.image = demo_utils.

        self.immvision_params = immvision.ImageParams()
        self.immvision_params.image_display_size = (int(immapp.em_size(22)), 0)
        self.immvision_params.can_resize = True
        self.immvision_params.show_image_info = False
        self.immvision_params.show_pixel_info = False
        self.immvision_params.show_school_paper_background = True
        self.immvision_params.show_options_button = False
        self.immvision_params.add_watched_pixel_on_double_click = False


# Our GUI function
#    (which instantiates a static app state at startup)
@immapp.static(app_state=None)
def demo_gui():
    static = demo_gui

    if static.app_state is None:
        static.app_state = AppState("Graphics/lion.png")#demo_utils.demos_assets_folder() + "/images/house.jpg")


    immvision.image(
        "", static.app_state.image, static.app_state.immvision_params
    )


def main():
    # demo_utils.set_hello_imgui_demo_assets_folder()
    immapp.run_with_markdown(demo_gui, window_size=(1000, 1000))


# The main entry point will run our GUI function
if __name__ == "__main__":
    main()