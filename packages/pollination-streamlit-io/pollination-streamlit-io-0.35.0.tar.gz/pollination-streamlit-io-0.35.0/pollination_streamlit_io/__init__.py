import os
from typing import Callable, Dict, Tuple

from streamlit import session_state as _state

import streamlit.components.v1 as components
from streamlit.components.v1 import components as _components

# register callback
# https://gist.github.com/okld/1a2b2fd2cb9f85fc8c4e92e26c6597d5


def _patch_register_widget(register_widget):
    def wrapper_register_widget(*args, **kwargs):
        user_key = kwargs.get("user_key", None)
        callbacks = _state.get("_components_callbacks", None)

        # Check if a callback was registered for that user_key.
        if user_key and callbacks and user_key in callbacks:
            callback = callbacks[user_key]

            # Add callback-specific args for the real register_widget function.
            kwargs["on_change_handler"] = callback[0]
            kwargs["args"] = callback[1]
            kwargs["kwargs"] = callback[2]

        # Call the original function with updated kwargs.
        return register_widget(*args, **kwargs)

    return wrapper_register_widget


# Patch function only once.
if not hasattr(_components.register_widget, "__callbacks_patched__"):
    setattr(_components.register_widget, "__callbacks_patched__", True)
    _components.register_widget = _patch_register_widget(
        _components.register_widget)


def register_callback(element_key, callback, *callback_args, **callback_kwargs):
    # Initialize callbacks store.
    if "_components_callbacks" not in _state:
        _state._components_callbacks = {}

    # Register a callback for a given element_key.
    _state._components_callbacks[element_key] = (
        callback, callback_args, callback_kwargs)
# ----


# get_host
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./get_host/frontend/build")
_get_host = components.declare_component("get_host", path=build_dir)


def get_host(key='foo'):
    """Create a new instance of "get_geometry".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    host: 'web' | 'rhino' | 'revit' | 'sketchup'
    """

    get_host = _get_host(key=key)

    return get_host


# get_geometry
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./get_geometry/frontend/build")
_get_geometry = components.declare_component("get_geometry", path=build_dir)


def get_geometry(key='foo'):
    """Create a new instance of "get_geometry".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        A dictionary with the following structure

        {
            'geometry': List[dict]
        }

        where
            'geometry': List of ladybug geometries as dictionary
    """

    get_geometry = _get_geometry(key=key)

    return get_geometry


# get_hbjson
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./get_hbjson/frontend/build")
_get_hbjson = components.declare_component("get_hbjson", path=build_dir)


def get_hbjson(
    key: str = 'foo', *,
    on_change:  Callable = None,
    args: Tuple = None,
    kwargs: Dict = None,
):
    """Create a new instance of "get_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    on_change: Callable or None
    args: Tuple or None
    kwargs: Dict or None

    Returns
    -------
    dict
        A dictionary with the following structure

        {
            'hbjson': dict
        }

        where
            'hbjson': hbjson model as dictionary
    """

    get_hbjson = _get_hbjson(key=key)

    if on_change is not None:
        args = args or []
        kwargs = kwargs or {}
        register_callback(key, on_change, *args, **kwargs)

    return get_hbjson


# send_geometry
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./send_geometry/frontend/build")
_send_geometry = components.declare_component("send_geometry", path=build_dir)


def send_geometry(key='foo', *, geometry={}, option='preview'):
    """Create a new instance of "send_geometry".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    geometry: dictionary
    option: 'add' | 'preview' | 'clear' | 'subscribe-preview'

    Returns
    -------
    """

    send_geometry = _send_geometry(geometry=geometry, key=key, option=option)

    return send_geometry


# send_hbjson
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./send_hbjson/frontend/build")
_send_hbjson = components.declare_component("send_hbjson", path=build_dir)


def send_hbjson(key='foo', *, hbjson={}, option='preview'):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    hbjson: dictionary
    option: 'add' | 'preview' | 'clear' | 'subscribe-preview'

    Returns
    -------
    """

    send_hbjson = _send_hbjson(hbjson=hbjson, key=key, option=option)

    return send_hbjson


# send_results
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./send_results/frontend/build")
_send_results = components.declare_component("send_results", path=build_dir)


def send_results(key='foo', *, geometry={}):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    geometry: dictionary

    Returns
    -------
    """

    send_results = _send_results(key=key, geometry=geometry)

    return send_results


# auth_user
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./auth_user/frontend/build")
_auth_user = components.declare_component("auth_user", path=build_dir)


def auth_user(key='foo', *, access_token=None):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    access_token: str or None
        jwt to authenticate to pollination api

    Returns
    -------
    """

    auth_user = _auth_user(key=key, access_token=access_token)

    return auth_user


# select_account
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./select_account/frontend/build")
_select_account = components.declare_component(
    "select_account", path=build_dir)


def select_account(key='foo', *, access_token=None):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    access_token: str or None
        jwt to authenticate to pollination api

    Returns
    -------
    """

    select_account = _select_account(key=key, access_token=access_token)

    return select_account


# # select_project
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./select_project/frontend/build")
_select_project = components.declare_component(
    "select_project", path=build_dir)


def select_project(key='foo', *, access_token=None, project_owner=None):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    access_token: str or None
        jwt to authenticate to pollination api
    project_owner: str or None

    Returns
    -------
    """

    select_project = _select_project(
        key=key, access_token=access_token, project_owner=project_owner)

    return select_project


# select_recipe
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./select_recipe/frontend/build")
_select_recipe = components.declare_component(
    "select_recipe", path=build_dir)


def select_recipe(key='foo', *, access_token=None, project_name=None, project_owner=None):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    access_token: str or None
        jwt to authenticate to pollination api
    project_name: str or None
    project_owner: str or None

    Returns
    -------
    """

    select_recipe = _select_recipe(
        key=key,
        access_token=access_token,
        project_name=project_name,
        project_owner=project_owner
    )

    return select_recipe


# select_study
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./select_study/frontend/build")
_select_study = components.declare_component(
    "select_study", path=build_dir)


def select_study(key='foo', *, access_token=None, project_name=None, project_owner=None):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    access_token: str or None
        jwt to authenticate to pollination api
    project_name: str or None
    project_owner: str or None

    Returns
    -------
    """

    select_study = _select_study(
        key=key, access_token=access_token, project_name=project_name, project_owner=project_owner)

    return select_study


# select_run
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "./select_run/frontend/build")
_select_run = components.declare_component(
    "select_run", path=build_dir)


def select_run(key='foo', *, access_token=None, project_name=None, project_owner=None, job_id=None):
    """Create a new instance of "send_hbjson".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    access_token: str or None
        jwt to authenticate to pollination api
    project_owner: str or None
    job_id: str or None

    Returns
    -------
    """

    select_run = _select_run(
        key=key,
        access_token=access_token,
        project_name=project_name,
        project_owner=project_owner,
        job_id=job_id
    )

    return select_run
