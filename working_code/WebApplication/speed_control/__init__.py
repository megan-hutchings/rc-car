import os
import streamlit.components.v1 as components


current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "frontend", "build")

#DEV_MODE = True
DEV_MODE = False

if DEV_MODE:
    _component_func = components.declare_component(
        "speed_control_component",
        url="http://localhost:3001", #npm run start with deploy component here
    )

else:
    _component_func = components.declare_component("speed_control_component",path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.



def speed_control_component(max_value,min_value,default_value,increment,interval_ms, key=None):
    """Create a new instance of "speed_control".

    Parameters
    ----------
    max_value: int
        The maximum speed value for the speed controller. (1000-2000)
    min_value: int
        The minimum speed value for the speed controller. (1000-2000)       
    default_value: int
        The default speed value for the speed controller. (1500) 
    increment: int
        The increment value for the speed controller. (10)
    interval_ms: int
        The interval in milliseconds for holding the button to continuously change speed. (100)  
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The speed value selected by the user.

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(max_value=max_value,min_value=min_value,default_value=default_value,increment=increment,interval_ms=interval_ms,key=key, default=1500)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value
