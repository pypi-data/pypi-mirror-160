import sys, os
import numpy as np
from .utils import formula_parser, get_wt, get_z
from scipy import interpolate
import logging, argparse


class Logg:
    def __init__(self, nom):
        logfmt = logging.Formatter('%(levelname)s::   %(message)s')
        sos = logging.StreamHandler(stream=sys.stdout)
        sos.setFormatter(logfmt)
        self.logger = logging.getLogger(name=nom)
        self.logger.addHandler(sos)
        self.logger.setLevel(20)
    def set_quiet(self):
        self.logger.setLevel(50)
    def set_verbose(self):
        self.logger.setLevel(20)


class Database:
    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__))+'/brencon.dat', 'r') as f:
            l = f.readlines()
        self.lines = [i.strip() for i in l]
        self.slines = [i.strip() for i in self.lines if i.startswith('#S')]
        with open(os.path.dirname(os.path.realpath(__file__))+'/brenconff.dat', 'r') as f:
            l = f.readlines()
        self.ff_lines = [i.strip() for i in l]
        self.ff_slines = [i.strip() for i in self.lines if i.startswith('#S')]
        
    def gimme(self, atom, z, elims):
        # cross sections
        inifin = [0, 0]
        for i in self.slines:
            if i.split()[-1] == atom and i.split()[-2] == z.__str__():
                inifin[0] = self.lines.index(i)
                break
        for i in self.slines:
            if i.split()[-2] == (z+1).__str__():
                inifin[1] = self.lines.index(i)
                break
        self.bren = [i for i in self.lines[inifin[0]:inifin[1]] \
                     if i.startswith('#') == False]
        ene = np.empty(len(self.bren))
        phoe = np.empty(len(self.bren))
        comp = np.empty(len(self.bren))
        elas = np.empty(len(self.bren))
        for i in range(len(self.bren)):
            cols = self.bren[i].strip().split()
            ene[i] = float(cols[0])
            phoe[i] = float(cols[1])
            comp[i] = float(cols[2])
            elas[i] = float(cols[3])
        imin = np.where(ene > elims[0])[0][0]
        imax = np.where(ene < elims[1])[0][-1]
        xsec_out = np.array([ene[imin:imax], phoe[imin:imax]+comp[imin:imax]+elas[imin:imax]])
        phoe_out = np.array([ene[imin:imax], phoe[imin:imax]])
        comp_out = np.array([ene[imin:imax], comp[imin:imax]])
        elas_out = np.array([ene[imin:imax], elas[imin:imax]])

        # fprime
        inifin = [0, 0]
        for i in self.ff_slines:
            if i.split()[-1] == atom and i.split()[-2] == z.__str__():
                inifin[0] = self.ff_lines.index(i)
                break
        for i in self.ff_slines:
            if i.split()[-2] == (z+1).__str__():
                inifin[1] = self.ff_lines.index(i)
                break
        self.ffco = [i for i in self.ff_lines[inifin[0]:inifin[1]] \
                     if i.startswith('#') == False]
        ene = np.empty(len(self.ffco))
        f1p = np.empty(len(self.ffco))
        f2p = np.empty(len(self.ffco))
        for i in range(len(self.ffco)):
            cols = self.ffco[i].strip().split()
            ene[i] = float(cols[0])
            f1p[i] = float(cols[1])
            f2p[i] = float(cols[2])
        imin = np.where(ene > elims[0])[0][0]
        imax = np.where(ene < elims[1])[0][-1]
        fprime_out = np.array([ene[imin:imax], f1p[imin:imax], f2p[imin:imax]])
        
        return xsec_out, phoe_out, comp_out, elas_out, fprime_out


class Atom:
    def __init__(self, name, elims=(1000, 120000)):
        """
        Initialises Atom class. 
        Arguments:
        - name: atom label. Type: string (in quotes).
        - (optional) elims: limits of the energy range in eV to extract from the Brennan-Cowan database
        """
        self.name = name        
        self.z = get_z(self.name)
        self.wt = get_wt(self.name)
        db = Database()
        self.xsec, self.phoe, self.comp, self.rayl, self.fprime = db.gimme(self.name, self.z, elims)
        self.tot_spl = interpolate.splrep(self.xsec[0], self.xsec[1], s=0)
        self.pe_spl = interpolate.splrep(self.phoe[0], self.phoe[1], s=0)
        self.co_spl = interpolate.splrep(self.comp[0], self.comp[1], s=0)
        self.ra_spl = interpolate.splrep(self.rayl[0], self.rayl[1], s=0)
        self.f1_spl = interpolate.splrep(self.fprime[0], self.fprime[1], s=0)
        self.f2_spl = interpolate.splrep(self.fprime[0], self.fprime[2], s=0)
    

    def atom_ff(self, ep):
        """
        Outputs f',f'' for this atom.
        Arguments:
        - ep: energy value in eV. Type: float or numpy array.
        """
        spl = self.f1_spl
        f1 = interpolate.splev(ep, spl, der=0, ext=0)
        spl = self.f2_spl
        f2 = interpolate.splev(ep, spl, der=0, ext=0)
        return f1, f2

    def atom_mu(self, ep):
        """
        Returns f',f'' for this atom.
        Arguments:
        - ep: energy value in eV. Type: float or numpy array.
        Output:
        - sig_el: elastic (Rayleigh-Thomson) cross-section in barns/atom
        - sig_tot: total interaction cross-section in barns/atom
        - sig_tot_ua: total cross-section divided by atom wt = linear attenuation coef divided by density [sig/(uA) = mu/rho in cm2/g]
        """        
        u = 1.660537728 ## 1/avogadro = 1.660537728e-24; 1 barn = 1e-24 cm^2
        barnxs = {}
        cmxs = {}
        for kk in ['tot', 'pe', 'co', 'ra']:
           spline = getattr(self, f'{kk}_spl')
           icurve = interpolate.splev(ep, spline, der=0, ext=0)
           icurve_ua = np.divide(icurve, u*self.wt)
           barnxs[kk] = icurve
           cmxs[kk] = icurve_ua
        return barnxs, cmxs


class Mixture:
    def __init__(self, formula, **kwargs):
        """
        Initialises Mixture class. 
        Arguments:
        - formula: atom labels followed (or not) by coefficients. Type: string (in quotes).
        - d: sample density in g/cm^3. Use in absence of -v and -z. Type: float.
        - v: sample volume in cubic Angstroms. Use together with -z and in absence of -d. Type: float.
        - z: number or formulas per unit cell. Use together with -v and in absence of -d. Type: int.
        """
        logger = logging.getLogger(__name__)
        self.prop = {}
        self.mola = {}  #like stoi but giving molar fractions normalised to 1
        self.weig = {}  #weight fractions normalised to 1
        self.stoi, self.fw = formula_parser(formula) #atom label + stoichio, formula weight
        self.molsum = sum(self.stoi.values()) # n of atoms in formula
        for u in self.stoi.keys():
            self.mola[u] = self.stoi[u]/self.molsum
            self.weig[u] = self.stoi[u]*get_wt(u)/self.fw
        for i in kwargs:
            self.prop[i] = kwargs[i]
        if 'v' in self.prop.keys() and 'z' in self.prop.keys() and 'd' not in self.prop.keys():  # if density is not provided:
             self.prop['d'] = self.prop['z']*self.fw/0.60226/self.prop['v']                      # density = Z*FW/0.60226/Volume
        logger.info('%s formula weight: %.4f g/mol.' % (formula, self.fw))
        logger.info('Input density: %.4f g/cm^3' %(self.prop['d']))

    def mix_mu(self, energy, thickness_cm=0.01, components=0):
        """
        Calculate values for a single energy value. Print output similar to the APS website.
        Arguments:
        - energy: x-ray energy value. Type: float.
        - thickness_cm: sample thickness in cm. Type: float.
        - include_elastic: True=use total cross section (e.g. filters, air)\
                           False=use photoelectric+Compton (e.g. capillary absorption)
        Returns:
        - transmission (type: float)
        - f'. (type: float)
        - f'' (type: float)
        """
        logger = logging.getLogger(__name__)
        self.thick = thickness_cm
        mix_sigma = 0.0
        logger.info('X-ray energy (wavelength): %d eV (%.5f A)'\
                    %(energy, 12398.4/energy))
        logger.info('Sample thickness: %.5f cm' %(self.thick))
        logger.info(f"""{'atom':<8s} {'wt frac':<8s} {"f'":<8s} {"f''":<8s} {'total xs':<15s} {'rayleigh xs':<15s} {'compton xs':<15s} {'photoelectric xs':<15s}""")
        for w in self.stoi.keys():
            u = Atom(w)
            barnxs, cmxs = u.atom_mu(energy)
            if components == 0:
               #label = 'Total'
                sig_ua = cmxs['tot']
            elif components == 1:
               #label = 'Photoelectric+Compton'
                sig_ua = cmxs['pe']+cmxs['co']
            elif components == 2:
               #label = 'Rayleigh'
                sig_ua = cmxs['ra']
            elif components == 3:
               #label = 'Photoelectric'
                sig_ua = cmxs['pe']
            elif components == 4:
               #label = 'Compton'
                sig_ua = cmxs['co']
            mix_sigma += sig_ua*self.weig[u.name]
            f1, f2 = u.atom_ff(energy)
            logger.info('%-8s %-8.3f %-8.3f %-8.3f %-15.3f %-15.3f %-15.3f %-15.3f' \
                 %(u.name, self.weig[u.name], f1, f2,
                   barnxs['tot']*self.stoi[u.name],
                   barnxs['ra']*self.stoi[u.name],
                   barnxs['co']*self.stoi[u.name],
                   barnxs['pe']*self.stoi[u.name]) )
        self.mu = np.multiply(mix_sigma, self.prop['d'])
        self.transm = np.exp(-self.mu*self.thick)
        logger.info('Total mu = %.2f cm^-1' %(self.mu))
        logger.info('Total muR = %.2f' %(self.mu*0.5*self.thick))
        logger.info('Transmission = %.4f %%' %(100*self.transm))
        return self.transm, f1, f2


    def mix_mue(self, energy, thickness_cm=0.01, components=0):
        """
        Calculate values for an array of energy values. No atom-wise print output.
        Arguments:
        - energy: x-ray energy values. Type: numpy array.
        - thickness_cm: sample thickness in cm. Type: float.
        - include_elastic: True=use total cross section (e.g. filters, air. Match Henke website)\n \
                           False=use photoelectric+Compton (e.g. capillary absorption. Match APS website)
        Returns:
        - transmission (type: array)
        - f'. (type: array)
        - f'' (type: array)
        """
        logger = logging.getLogger(__name__)
        self.thick = thickness_cm
        mix_sigma = np.zeros(len(energy))
        f1, f2 = np.zeros(len(energy)), np.zeros(len(energy))
        logger.info('X-ray energy (wavelength): %d-%d eV (%.5f-%.5f A)'\
                    %(energy[0], energy[-1], 12398.4/energy[0], 12398.4/energy[-1]))
        logger.info('Sample thickness: %.5f cm' %(self.thick))
        for w in self.stoi.keys():
            u = Atom(w)
            barnxs, cmxs = u.atom_mu(energy)
            if components == 0:
               #label = 'Total'
                sig_ua = cmxs['tot']
            elif components == 1:
               #label = 'Photoelectric+Compton'
                sig_ua = cmxs['pe']+cmxs['co']
            elif components == 2:
               #label = 'Rayleigh'
                sig_ua = cmxs['ra']
            elif components == 3:
               #label = 'Photoelectric'
                sig_ua = cmxs['pe']
            elif components == 4:
               #label = 'Compton'
                sig_ua = cmxs['co']
            mix_sigma += sig_ua*self.weig[u.name]
            f1_w, f2_w = u.atom_ff(energy)
            f1 += f1_w; f2 += f2_w
        self.mu = np.multiply(mix_sigma, self.prop['d'])
        self.transm = np.exp(-self.mu*self.thick)
        logger.info("""Energy--|-%Transm--|--muR---|---mu---|---f'---|--f''---""")
        for i in range(len(energy)):
            logger.info('%8d|%10.3f|%8.3f|%8.3f|%8.3f|%8.3f' %(energy[i], 
                                             100*self.transm[i], 
                                             self.mu[i]*0.5*self.thick, 
                                             self.mu[i], f1[i], f2[i]))
        return self.transm, f1, f2


def console():
    #thelogger = Logg(__name__)
    thelogger = logging.getLogger(__name__)
    components_help = 'Use total cross section or partial: \
 0 = total; \
 1 = photoelectric + Compton; \
 2 = only Rayleigh (coherent); \
 3 = only photoelectric; \
 4 = only Compton (incoherent)'
     ##--argument parser
    parser = argparse.ArgumentParser(description='X-ray absorption calculation')
    parser.add_argument('-f', type=str,
                        help='Brute formula, e.g. Sr0.85Pr0.15TiO3 or CaO')
    parser.add_argument('-d', type=float,
                        help='Density in g/cm^3. (If not available, use -z and -v)')
    parser.add_argument('-v', type=float,
                        help='Cell volume in AA^3. (Use together with -z instead of density)')
    parser.add_argument('-z', type=int,
                        help='Number of formula units per unit cell, e.g. 1 for Pm-3m. (Use together with -v instead of density)')
    parser.add_argument('-e', type=float,
                        help='X-ray energy in eV. Single value or <start> <step> <end>.', nargs='+')
    parser.add_argument('-t', type=float,
                        help='Sample thickness (diameter) in mm')
    parser.add_argument('-y', type=int, default=0, help=components_help,
                        choices=[0,1,2,3,4])
    parser.add_argument('-l', type=int,
                        help='Display information: 0=OFF, 1=ON (default)',
                        default=1)
    args = parser.parse_args()
     ##--set logger
    if bool(args.l) == False:
        thelogger.setLevel(50)
     ##--initialise mixture 
    if any([args.v, args.z]) == False and not args.d or not args.e or not args.f or not args.t:
        thelogger.error('Not enough arguments. Check options -f, -e, -t, -d (or -v and -z)')
        sys.exit(1)
    elif args.z and args.v and not args.d:
        sk = Mixture(args.f, z=args.z, v=args.v)
    elif args.d:
        sk = Mixture(args.f, d=args.d)
    else:
        sys.exit(1)
     ##--calculate
    t_cm = 0.1*args.t
    if len(args.e) == 1:
        sk.mix_mu(args.e[0], t_cm, int(args.y))
    elif len(args.e) == 2:
        sk.mix_mu(args.e[0], t_cm, int(args.y))
        sk.mix_mu(args.e[1], t_cm, int(args.y))
    elif len(args.e) >=3:
        ene = np.arange(args.e[0], args.e[2]+args.e[1], args.e[1])
        res = sk.mix_mue(ene, t_cm, int(args.y))
     ##--close logger
    logging.shutdown()
    
thelogger = Logg(__name__)