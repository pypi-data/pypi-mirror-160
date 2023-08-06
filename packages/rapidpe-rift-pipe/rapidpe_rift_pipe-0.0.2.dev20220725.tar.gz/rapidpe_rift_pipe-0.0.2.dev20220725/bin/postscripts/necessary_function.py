import numpy
import lal

def mass1_from_mchirp_eta(mchirp,eta):
    return(0.5*mchirp*(eta**(-3./5.))*(1.+numpy.sqrt(1.-4.*eta)))

def mass2_from_mchirp_eta(mchirp,eta):
    return(0.5*mchirp*(eta**(-3./5.))*(1.-numpy.sqrt(1.-4.*eta)))

def mchirp_from_mass1_mass2(m1,m2):
    return(((m1*m2)**(3./5.))*((m1+m2)**(-1./5.)))

def eta_from_mass1_mass2(m1,m2):
    return((m1*m2)*((m1+m2)**(-2.)))

def mass1_from_mtotal_eta(mtotal, eta):
    """Returns the primary mass from the total mass and symmetric mass
    ratio.
    """
    return 0.5 * mtotal * (1.0 + (1.0 - 4.0 * eta)**0.5)



def mass2_from_mtotal_eta(mtotal, eta):
    """Returns the secondary mass from the total mass and symmetric mass
    ratio.
    """
    return 0.5 * mtotal * (1.0 - (1.0 - 4.0 * eta)**0.5)

def _a0(f_lower):
    """Used in calculating chirp times: see Cokelaer, arxiv.org:0706.4437
       appendix 1, also lalinspiral/python/sbank/tau0tau3.py.
    """
    return 5. / (256. * (numpy.pi * f_lower)**(8./3.))

def _a3(f_lower):
    """Another parameter used for chirp times"""
    return numpy.pi / (8. * (numpy.pi * f_lower)**(5./3.))


def tau0_from_mtotal_eta(mtotal, eta, f_lower):
    r"""Returns :math:`\tau_0` from the total mass, symmetric mass ratio, and
    the given frequency.
    """
    # convert to seconds
    mtotal = mtotal * lal.MTSUN_SI
    # formulae from arxiv.org:0706.4437
    return _a0(f_lower) / (mtotal**(5./3.) * eta)



def tau3_from_mtotal_eta(mtotal, eta, f_lower):
    r"""Returns :math:`\tau_0` from the total mass, symmetric mass ratio, and
    the given frequency.
    """
    # convert to seconds
    mtotal = mtotal * lal.MTSUN_SI
    # formulae from arxiv.org:0706.4437
    return _a3(f_lower) / (mtotal**(2./3.) * eta)



def tau0_from_mass1_mass2(mass1, mass2, f_lower):
    r"""Returns :math:`\tau_0` from the component masses and given frequency.
    """
    mtotal = mass1 + mass2
    eta = eta_from_mass1_mass2(mass1, mass2)
    return tau0_from_mtotal_eta(mtotal, eta, f_lower)



def tau3_from_mass1_mass2(mass1, mass2, f_lower):
    r"""Returns :math:`\tau_3` from the component masses and given frequency.
    """
    mtotal = mass1 + mass2
    eta = eta_from_mass1_mass2(mass1, mass2)
    return tau3_from_mtotal_eta(mtotal, eta, f_lower)



def mtotal_from_tau0_tau3(tau0, tau3, f_lower,
                          in_seconds=False):
    r"""Returns total mass from :math:`\tau_0, \tau_3`."""
    mtotal = (tau3 / _a3(f_lower)) / (tau0 / _a0(f_lower))
    if not in_seconds:
        # convert back to solar mass units
        mtotal /= lal.MTSUN_SI
    return mtotal


def eta_from_tau0_tau3(tau0, tau3, f_lower):
    r"""Returns symmetric mass ratio from :math:`\tau_0, \tau_3`."""
    mtotal = mtotal_from_tau0_tau3(tau0, tau3, f_lower,
                                   in_seconds=True)
    eta = mtotal**(-2./3.) * (_a3(f_lower) / tau3)
    return eta



def mass1_from_tau0_tau3(tau0, tau3, f_lower):
    r"""Returns the primary mass from the given :math:`\tau_0, \tau_3`."""
    mtotal = mtotal_from_tau0_tau3(tau0, tau3, f_lower)
    eta = eta_from_tau0_tau3(tau0, tau3, f_lower)
    return mass1_from_mtotal_eta(mtotal, eta)



def mass2_from_tau0_tau3(tau0, tau3, f_lower):
    r"""Returns the secondary mass from the given :math:`\tau_0, \tau_3`."""
    mtotal = mtotal_from_tau0_tau3(tau0, tau3, f_lower)
    eta = eta_from_tau0_tau3(tau0, tau3, f_lower)
    return mass2_from_mtotal_eta(mtotal, eta)



def prior_mchirp_eta(mchirp,eta):
    return(numpy.abs(mchirp*numpy.power(eta,-6./5.)*(1./numpy.sqrt(1.-4.*eta)))/(0.4**2.))


def prior_tau0_tau3(tau0,tau3,f_lower):
	m1 = mass1_from_tau0_tau3(tau0, tau3, f_lower)
	m2 = mass2_from_tau0_tau3(tau0, tau3, f_lower)
	num = 165888.*f_lower**(13./3.)*m1**3.*(m1 - m2)*m2**3.*(m1 + m2)*(4./3.)*numpy.pi**(10./3.)
	den = 5.*(m1-3*m2)*(3.*m1-m2)*(3.*m1+2.*m2)*(2.*m1+3.*m2)
	p = numpy.abs((1./(1.6-1.2)**2.)*(num/den))
	return p

