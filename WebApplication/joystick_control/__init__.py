import os
import streamlit.components.v1 as components


current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "frontend", "build")

#DEV_MODE = True
DEV_MODE = False

if DEV_MODE:
    _component_func = components.declare_component(
        "joystick_control_component",
        url="http://localhost:3001", #npm run start with deploy component here
    )

else:
    _component_func = components.declare_component("joystick_control_component",path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.



def joystick_control_component(max_value_x,min_value_x,default_value_x,increment_x,max_value_y,min_value_y,default_value_y,increment_y,interval_ms, key=None):
    """Create a new instance of "direction_control".

    Parameters
    ----------
    max_value_x: int
        The maximum angle value for the dir controller. (180)
    min_value_x: int
        The minimum angle value for the dir controller. (90)       
    default_value_x: int
        The default angle value for the dir controller. (90) 
    increment_x: int
        The increment value for the dir controller. (10)
    max_value_y: int
        The maximum angle value for the speed controller. (180)
    min_value_y: int
        The minimum angle value for the speed controller. (90)       
    default_value_y: int
        The default angle value for the speed controller. (90) 
    increment_y: int
        The increment value for the speed controller. (10)
    interval_ms: int
        The interval in milliseconds for holding the button to continuously change speed. (100)  
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    speed int
        The speed value selected by the user.
    dir int
        The angle value selected by the user.        
                """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(max_value_x=max_value_x,min_value_x=min_value_x,default_value_x=default_value_x,increment_x=increment_x,max_value_y=max_value_y,min_value_y=min_value_y,default_value_y=default_value_y,increment_y=increment_y,interval_ms=interval_ms,key=key, default={"speed": default_value_y, "dir": default_value_x} )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
        # Ensure default return format even if component_value is None (e.g., on first load)
    if component_value is None:
        return default_value_x, default_value_y
    
    print("default_x:" ,default_value_x)

    # Return x and y values from the component's result
    speed = component_value.get("speed", default_value_y)
    dir = component_value.get("dir", default_value_x)
    return speed, dir
