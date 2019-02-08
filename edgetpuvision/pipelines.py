from .gst import *

def decoded_file_src(filename):
    return [
        Source('file', location=filename),
        Filter('decodebin'),
    ]

def v4l2_src(fmt):
    return [
        Source('v4l2', device=fmt.device),
        Caps('video/x-raw', format=fmt.pixel, width=fmt.size.width, height=fmt.size.height,
             framerate='%d/%d' % fmt.framerate),
    ]

def display_sink(fullscreen, sync=False):
    return Sink('kms' if fullscreen else 'wayland', sync=sync),

def h264_sink():
    return Sink('app', name='h264sink', emit_signals=True, max_buffers=1, drop=False, sync=False)

def inference_pipeline(render_size, inference_size):
    size = max_inner_size(render_size, inference_size)
    return [
        Filter('glfilterbin', filter='glcolorscale'),
        Caps('video/x-raw', format='RGBA', width=size.width, height=size.height),
        Filter('videoconvert'),
        Caps('video/x-raw', format='RGB', width=size.width, height=size.height),
        Filter('videobox', autocrop=True),
        Caps('video/x-raw', width=inference_size.width, height=inference_size.height),
        Sink('app', name='appsink', emit_signals=True, max_buffers=1, drop=True, sync=False),
    ]

# Display
def image_display_pipeline(filename, render_size, inference_size, fullscreen):
    size = max_inner_size(render_size, inference_size)
    return (
        [decoded_file_src(filename),
         Tee(name='t')],
        [Pad('t'),
         Queue(),
         Filter('imagefreeze'),
         Filter('videoconvert'),
         Filter('videoscale'),
         Caps('video/x-raw', width=render_size.width, height=render_size.height),
         Filter('rsvgoverlay', name='overlay'),
         display_sink(fullscreen)],
        [Pad('t'),
         Queue(),
         Filter('imagefreeze'),
         Filter('glupload'),
         inference_pipeline(render_size, inference_size)],
    )

def video_display_pipeline(filename, render_size, inference_size, fullscreen):
    return (
        [decoded_file_src(filename),
         Filter('glupload'),
         Tee(name='t')],
        [Pad('t'),
         Queue(max_size_buffers=1),
         Filter('glfilterbin', filter='glcolorscale'),
         Filter('rsvgoverlay', name='overlay'),
         Caps('video/x-raw', width=render_size.width, height=render_size.height),
         display_sink(fullscreen)],
        [Pad('t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         inference_pipeline(render_size, inference_size)],
    )

def camera_display_pipeline(fmt, render_size, inference_size, fullscreen):
    return (
        [v4l2_src(fmt),
         Filter('glupload'),
         Tee(name='t')],
        [Pad(name='t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         Filter('glfilterbin', filter='glcolorscale'),
         Filter('rsvgoverlay', name='overlay'),
         display_sink(fullscreen)],
        [Pad(name='t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         inference_pipeline(render_size, inference_size)],
    )

# Headless
def image_headless_pipeline(filename, render_size, inference_size):
    return (
      [decoded_file_src(filename),
       Filter('imagefreeze'),
       Filter('glupload'),
       inference_pipeline(render_size, inference_size)],
    )

def video_headless_pipeline(filename, render_size, inference_size):
    return (
        [decoded_file_src(filename),
         Filter('glupload'),
         inference_pipeline(render_size, inference_size)],
    )

def camera_headless_pipeline(fmt, render_size, inference_size):
    return (
        [v4l2_src(fmt),
         Filter('glupload'),
         inference_pipeline(render_size, inference_size)],
    )

# Streaming
def video_streaming_pipeline(filename, render_size, inference_size):
    return (
        [Source('file', location=filename),
         Filter('qtdemux'),
         Tee(name='t')],
        [Pad('t'),
         Queue(max_size_buffers=1),
         Filter('h264parse'),
         Caps('video/x-h264', stream_format='byte-stream', alignment='nal'),
         h264_sink()],
        [Pad('t'),
         Queue(max_size_buffers=1),
         Filter('decodebin'),
         inference_pipeline(render_size, inference_size)],
    )

def camera_streaming_pipeline(fmt, profile, bitrate, render_size, inference_size):
    size = max_inner_size(render_size, inference_size)
    return (
        [v4l2_src(fmt), Tee(name='t')],
        [Pad('t'),
         Queue(max_size_buffers=1, leaky='downstream'),
         Filter('videoconvert'),
         Filter('x264enc',
                 speed_preset='ultrafast',
                 tune='zerolatency',
                 threads=4,
                 key_int_max=5,
                 bitrate=int(bitrate / 1000),  # kbit per second.
                 aud=False),
          Caps('video/x-h264', profile=profile),
          Filter('h264parse'),
          Caps('video/x-h264', stream_format='byte-stream', alignment='nal'),
          h264_sink()],
        [Pad('t'),
         Queue(),
         inference_pipeline(render_size, inference_size)],
    )