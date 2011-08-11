template = '%012d.png'
frame_rate = 25
default_filename = 'movie'
preferred_extensions = 'gif', 'avi', 'mpeg', 'mov', 'flv'

from infobiotics.thirdparty.which import which, WhichError
try:
    ffmpeg = which('ffmpeg')
except WhichError:
    raise EnvironmentError(1, 'ffmpeg not found, aborting.')

from subprocess import Popen, PIPE, STDOUT
import re
from operator import itemgetter
import os.path
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.pyface.api import FileDialog, OK
import shutil
import tempfile

def ext(filename):
    return os.path.splitext(filename)[1].strip('.').strip()

available_formats = Popen([ffmpeg, '-formats'], stdout=PIPE, stderr=PIPE).communicate()[0]
available_formats = [match for match in re.findall(' .E ([0-9A-Za-z]+)\s*(.*)', available_formats)] 

formats = [ #TODO improve descriptions
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
#    else:
#        exit("Default format not in (%s)" % ', '.join("'%s'" % f for f in preferred_extensions))


def start_movie(template='%012d.bmp', frame_rate=10, default_filename='movie'):
    if not ext(default_filename):
        default_filename += '.%s' % format
    fd = FileDialog(
        action='save as',
        # formats[:5] == [('*.asf', 'ASF format'), ('*.avi', 'AVI format'), ('*.dvd', 'MPEG-2 PS format (DVD VOB)'), ('*.flv', 'FLV format'), ('*.h261', 'raw H.261')]
        wildcard=''.join([FileDialog.create_wildcard(f[1], f[0]) for f in formats]),
        title='Save movie',
        default_filename=default_filename,
    #    default_directory=os.getcwd(),
        wildcard_index=extensions.index(format)
    )
    if fd.open() == OK:
        if not ext(fd.path):
            fd.path += '.%s' % extensions[fd.wildcard_index]
        filename = fd.path
        tempdir = tempfile.mkdtemp()
        return dict(
            filename=filename, 
            frame_rate=frame_rate, 
            tempdir=tempdir,
            template=template,
        )
    else:
        return None

output = ''
def finish_movie(movie):
    global output
    output = ''
#    p = Popen(
#        '{ffmpeg} -y -f image2 -i "{tempdir}/{template}" -r {frame_rate} -sameq "{filename}" -pass 2'.format(
#            ffmpeg=which('ffmpeg'), 
#            **movie
#        ),
#        shell=True
#    )
#    p.wait()
    p = Popen(
        [
#            which('ffmpeg'), # in case ffmpeg changed since we import/ran the module?
            ffmpeg,
            '-y',
            '-f',
            'image2',
            '-i',
#            '"{tempdir}/{template}"'.format(**movie),
            '{tempdir}/{template}'.format(**movie),
            '-r',
            str(movie['frame_rate']),
            '-sameq',
#            '"%s"' % movie['filename'],
            '%s' % movie['filename'],
            '-pass 2'
        ],
        stdout=PIPE,
        stderr=STDOUT
    )
    output = p.communicate()[0]
    shutil.rmtree(movie['tempdir'], ignore_errors=True)
    return p.returncode == 0
    
    
def main():
    # setup movie
    movie = start_movie()
    if movie is None:
        exit('Aborted.')
    
    # save some frames
    from enthought.mayavi import mlab
    mlab.options.offscreen = True
    mlab.test_contour3d() #TODO replace with surface
    f = mlab.gcf() 
    for i in range(36): #TODO replace with indices
        f.scene.camera.azimuth(10) #TODO remove
        f.scene.render()
        mlab.savefig(os.path.join(movie['tempdir'], movie['template'] % (i + 1)))
#        arr = mlab.screenshot() #TODO when more than one surface
    
    # process frames
    exit(finish_movie(movie))

if __name__ == '__main__':
#    main()
    execfile('spatial_plots.py')
    