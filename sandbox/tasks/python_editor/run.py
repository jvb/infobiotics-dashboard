from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
# Enthought library imports.
from pyface.api import GUI
from pyface.tasks.api import TaskWindow

# Local imports.
from example_task import ExampleTask


def main(argv):
    """ A simple example of using Tasks.
    """
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create a Task and add it to a TaskWindow.
    task = ExampleTask()
    window = TaskWindow(size=(800, 600))
    window.add_task(task)

    # Show the window.
    window.open()

    # Start the GUI event loop.
    gui.start_event_loop()


if __name__ == '__main__':
    import sys
    main(sys.argv)
