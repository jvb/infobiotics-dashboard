'''
Correct way to implement has_valid_parameters
'''

#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.#-- Imports --------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, Range, Float, Bool, Str, Property, property_depends_on
    
from enthought.traits.ui.api \
    import View, VGroup, Item

#-- System Class ---------------------------------------------------------------

class System ( HasTraits ):

    # The mass of the system:
    mass = Range( 0.0, 100.0 )
    
    # The velocity of the system:
    velocity = Range( 0.0, 100.0 )
    
    # The kinetic energy of the system:
    kinetic_energy = Property( Float )
    
    # The current error status of the system:
    error = Property( Bool, 
               sync_to_view = 'mass.invalid, velocity.invalid, status.invalid' )
    
    # The current status of the system:
    status = Property( Str )
    
    @property_depends_on( 'mass, velocity' )
    def _get_kinetic_energy ( self ):
        return (self.mass * self.velocity * self.velocity) / 2.0
    
    @property_depends_on( 'kinetic_energy' )
    def _get_error ( self ):
        return (self.kinetic_energy > 50000.0)
    
    @property_depends_on( 'error' )
    def _get_status ( self ):
        if self.error:
            return 'The kinetic energy of the system is too high.'
            
        return ''

    view = View(
        VGroup( 
            VGroup(
                Item( 'mass' ),
                Item( 'velocity' ),
                Item( 'kinetic_energy', 
                      style      = 'readonly',
                      format_str = '%.0f'
                ),
                label       = 'System',
                show_border = True ),
            VGroup(
                Item( 'status',
                      style      = 'readonly',
                      show_label = False
                ),
                label       = 'Status',
                show_border = True
            ),
        )
    )
    
#-- Create and run the demo ----------------------------------------------------

# Create the demo:
demo = System()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()