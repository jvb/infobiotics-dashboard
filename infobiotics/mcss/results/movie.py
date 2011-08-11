'''movie class for making a movie from a series of frames (images)

importing module raises EnvironmentError if encoder not found

'''


# default parameters

template = '%012d.png' #MV frame_file_template?
frame_rate = 10#25
default_filename = 'movie'
preferred_extensions = 'mov', 'avi', 'mpeg', 'flv', 'gif'


# check encoder and supported output formats

# ffmpeg
from infobiotics.thirdparty.which import which, WhichError
try:
    ffmpeg = which('ffmpeg')
except WhichError:
    raise EnvironmentError(1, 'ffmpeg not found, aborting.')


import os.path
# helper function
def ext(filename): #MV file_name
    '''Returns the file's extension without the dot.'''
    return os.path.splitext(str(filename))[1].strip('.').strip()


from subprocess import Popen, PIPE, STDOUT
import re
from operator import itemgetter

available_formats = Popen([ffmpeg, '-formats'], stdout=PIPE, stderr=PIPE).communicate()[0]
available_formats = [match for match in re.findall(' .E ([0-9A-Za-z]+)\s*(.*)', available_formats)] 

formats = [ #MV desirable_formats 
    #TODO improve descriptions
    ('asf', 'ASF format'),
    ('avi', 'AVI format'),
    ('dvd', 'MPEG-2 PS format (DVD VOB)'),
    ('flv', 'FLV format'),
#    ('gif', 'GIF Animation'), # Could not write header for output file #0 (incorrect codec parameters ?)
    ('h261', 'raw H.261'),
    ('h263', 'raw H.263'),
    ('h264', 'raw H.264 video format'),
    ('ipod', 'iPod H.264 MP4 format'),
    ('m4v', 'raw MPEG-4 video format'),
    ('matroska', 'Matroska file format'),
    ('mjpeg', 'raw MJPEG video'),
    ('mov', 'MOV format'),
    ('mpeg', 'MPEG-1 System format'),
    ('mpeg1video', 'raw MPEG-1 video'),
    ('mpeg2video', 'raw MPEG-2 video'),
    ('psp', 'PSP MP4 format'),
    ('rm', 'RealMedia format'),
    ('svcd', 'MPEG-2 PS format (VOB)'),
    ('swf', 'Flash format'),
    ('vcd', 'MPEG-1 System format (VCD)'),
    ('vob', 'MPEG-2 PS format (VOB)'),
    ('webm', 'WebM file format'),
#    ('fake', 'Test to see whether the filter below works'), # it does
]

extensions = map(itemgetter(0), formats) 

for i, f in enumerate(available_formats):
    available_formats[i] = ('*.%s' % f[0], f[1])
for i, f in enumerate(formats):
    formats[i] = ('*.%s' % f[0], f[1])

formats = filter(lambda format: format in available_formats, formats)

formats.sort(key=itemgetter(0)) # by extension

# if default_filename has no extension give it one
format = ext(default_filename)
if not format:
    for f in preferred_extensions:
        if f in extensions:
            format = f
            break
    else:
        raise ValueError("Default format not in (%s)" % ', '.join("'%s'" % f for f in preferred_extensions))


def QFileDialog_filter_from_available_formats():
    '''If you want to use multiple filters, separate each one with two semicolons. For example:
    Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)'''
    # formats == [('*.asf', 'ASF format'), ...]
    return ';;'.join(['%s %s (%s)' % (format[1], format[0], format[0]) for format in formats])


#def filename_from_traits_FileDialog():
#    from enthought.etsconfig.api import ETSConfig
#    ETSConfig.toolkit = 'qt4'
#    from enthought.pyface.api import FileDialog, OK
#    fd = FileDialog(
#        action='save as',
#        wildcard=''.join([FileDialog.create_wildcard(f[1], f[0]) for f in formats]), # formats == [('*.asf', 'ASF format'), ...]
#        title='Save movie',
#        default_filename=default_filename,
##        default_directory=os.getcwd(), # default behaviour 
#        wildcard_index=extensions.index(format)
#    )
#    if fd.open() == OK:
#        ext_ = ext(fd.path)
#        if not ext_ or ext_ not in extensions:
#            available_format = extensions[fd.wildcard_index]
#            print "Format '%s (%s)' not available, using '%s' instead." % (dict(available_formats)[ext_], ext_, available_format)
#            fd.path += '.%s' % available_format
#    return fd.path
        

import tempfile
import shutil

class movie(object):
    
    def __init__(self, filename=default_filename, frame_rate=frame_rate, template=template):
        assert filename
        extension = ext(filename)
        if not extension:
            if extension and extension not in extensions:
                print "Format '%s' not available, using '%s' instead." % (dict(available_formats)[extension], extension, format)
            filename += '.%s' % format
        self.filename = filename
        self.frame_rate = frame_rate
        self.template = template
        self.tempdir = tempfile.mkdtemp()
        self.frames = 0

    def next_frame(self, template=None):
        if not template:
            template = self.template
        '''Returns a suitable file name for the next frame, based on template.'''
        self.frames += 1
        return os.path.join(self.tempdir, template % self.frames)
    
    def encode(self, filename=None, frame_rate=None):
        if not filename:
            filename = self.filename
        if not filename:
            print 'Aborted'
            return
        if not frame_rate:
            frame_rate = self.frame_rate
        self.output = ''
        p = Popen(
            [
                ffmpeg,
                '-y',
                '-f',
                'image2',
                '-i',
                '{tempdir}/{template}'.format(**self.__dict__),
                '-r',
                str(frame_rate),
                '-sameq',
                filename,
##                '-pass 2'
#                '-pass'
#                '2',
            ],
            stdout=PIPE,
            stderr=STDOUT
        )
        self.output = p.communicate()[0]
        return p.returncode == 0
    
    def __del__(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
    

def example():
    # setup movie
    m = movie()
    
    # setup example
    from enthought.mayavi import mlab
    mlab.options.offscreen = True
    mlab.test_contour3d()
    f = mlab.gcf() 

    # save frames
    for i in range(36):
        f.scene.camera.azimuth(10) # rotate
        f.scene.render()
        mlab.savefig(m.next_frame(), figure=f)
    
    # encode frames
    encoded = m.encode()

    # remove tempdir
    del m
    
    if not encoded:
        # report error
        exit(m.output)


if __name__ == '__main__':
    example()
#    execfile('spatial_plots.py')
    