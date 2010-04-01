'''
Conclusions
-----------

Best to use Instance(Class) at ABC level because:
 1. no need for editor=InstanceEditor() in Item
 2. can't assign non-instance value to it.
 3. can do default in subclass simply by:
     class ClassName(SuperClass):
         instance_trait = OtherClass(1, kwarg=2)   
 
'''

from enthought.traits.api import HasTraits, Int, Instance
from enthought.traits.ui.api import View, Item, InstanceEditor

class Object(HasTraits):
    i = Int

class ContainsObject(HasTraits):
    a = Object(i=5) # can parse kwargs here
    b = Instance(Object)#, kw={'i':6}) # can pass kwargs in kw parameter
    
    view = View(
        Item('a', editor=InstanceEditor()), # must explicity use InstanceEditor here
        'b'
    )
    
class InheritsFromContainsObject(ContainsObject):
    b = Object()

#c = ContainsObject()
#print c.a
#print c.b
#c.configure_traits()

c = InheritsFromContainsObject()
#print c.a
#print c.b
c.a=5
c.configure_traits()