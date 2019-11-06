# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input
from dash.dependencies import Output
from numpy.fft import fft
from numpy.fft import fftshift
from numpy.fft import ifft
from numpy.fft import ifftshift

from app.app import app
from app.custom_widgets import custom_input_group
from app.custom_widgets import custom_slider

# import csdmpy as


def line_broadening(x, amp, sigma, broadType):
    """
    This function evaluates
    ..math::

    """

    freq = x.coordinates.to("Hz")

    TimeDomain = ifft(ifftshift(amp))
    TimeDomain = np.roll(TimeDomain, int(x.count / 2))
    t = np.arange(x.count) - int(x.count / 2)

    time = t * 1 / (len(freq) * x.increment.to("Hz").value)

    # Lorentzian broadening:
    if broadType == 0 and sigma != 0:
        broadSignal = np.exp(-sigma * np.pi * np.abs(time))
    # Gaussian broadening:
    elif broadType == 1 and sigma != 0:
        broadSignal = np.exp(-((time * sigma * np.pi) ** 2) * 2)
    # No apodization
    else:
        broadSignal = 1

    appodized = np.roll(TimeDomain * broadSignal, -int(x.count / 2))

    return fftshift(fft(appodized))


def post_simulation(function, csdm_object, **kwargs):
    csdm_local = csdm_object.copy()

    x = csdm_local.dimensions[0]
    for datum in csdm_local.dependent_variables:
        y = datum.components[0]
        datum.components[0] = function(x, y, **kwargs)

    return csdm_local
    # return [

    #         function(datum, **kwargs) for datum in local_data if not isinstance(datum, list)
    # ]


# @app.callback(Output("local-computed-data", "data"), [Input("broadening_points-0", "value"),
#         Input("Apodizing_function-0", "value"),])
# def apodizing_function(broadening,
#     apodization,):
#     csdm_object_appodized = post_simulation(
#             line_broadening, csdm_object=csdm_object, sigma=broadening, broadType=apodization
#         )
if __name__ == "__main__":
    import numpy

    line_broadening(numpy.asarray([1, 2]), 2, 0)
