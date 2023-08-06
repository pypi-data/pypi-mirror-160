from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from EMCqMRI.core.base import base_likelihood_model
import math
import numpy as np
import torch


class Rician(base_likelihood_model.Likelihood):
    """
        Class for the Rician PDF.
        Methods:
            - logLikelihood
                inputs: signal (measured signal), mu (simulated signal) and sigma (SD of the noise)
                outputs: data consistency loss
            - applyNoise
                inputs: a signal and sigma
                outputs: Noisy signal corrupted by rician noise
    """
    
    def __init__(self, config_object):
        super(Rician, self).__init__(config_object, self)
        self.__name__ = 'Rician'
        if config_object:
            self.args = config_object.args

    def deprec_modif_bessel_0th(self, arg):
        # Based on the implementation in MONAI
        def f_small(x):
            y = torch.divide(x, torch.Tensor([3.75]).to(device=self.args.engine.device))
            y = y*y
            return 1.0+y*(3.5156229+y*(3.0899424+y*(1.2067492+y*(0.2659732+y*(0.360768e-1+y*0.45813e-2)))))

        def f_bigger(ax):
            y = torch.divide(torch.Tensor([3.75]).to(device=self.args.engine.device), ax)
            return (torch.exp(ax)/torch.sqrt(ax))*(0.39894228+y*(0.1328592e-1+y*(0.225319e-2+y*(-0.157565e-2+y*(0.916281e-2+y*(-0.2057706e-1+y*(0.2635537e-1+y*(-0.1647633e-1+y*0.392377e-2))))))))

        ax = torch.abs(arg)
        low_ax_ind = torch.where(ax<3.75)
        high_ax_ind = torch.where(ax>=3.75)

        low_ax = ax[low_ax_ind]
        high_ax = ax[high_ax_ind]

        b_result = ax.clone()
        b_result[low_ax_ind] = f_small(low_ax)
        b_result[high_ax_ind] = f_bigger(high_ax)

        return b_result[0]

    def likelihood(self, signal, modeled_signal, *extra_args):
        modeled_signal = torch.abs(modeled_signal)
        i0_arg = modeled_signal*signal
        besseli = torch.special.i0e(i0_arg) + 0.0001
        p = torch.log(signal) + (-0.5 * (signal - modeled_signal)**2) + torch.log(besseli)
        loss_ = torch.sum(p)
        return loss_

    def apply_noise(self, signal, sigma):
        mean_ = torch.zeros_like(signal)
        real_gaussian_noise = torch.normal(mean_, sigma)
        imag_gaussian_noise = 1j*torch.normal(mean_, sigma)
        noisy_signal = signal + real_gaussian_noise + imag_gaussian_noise
        rice_corr_signal = torch.abs(noisy_signal)
        return rice_corr_signal

    