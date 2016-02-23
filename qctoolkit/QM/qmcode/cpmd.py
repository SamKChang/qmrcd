import qctoolkit as qtk
from qctoolkit.QM.planewave_io import PlanewaveInput
from qctoolkit.QM.planewave_io import PlanewaveOutput
import sys, os, re, copy, shutil
import qctoolkit.QM.qmjob as qmjob
import pkg_resources
import numpy as np
import universal as univ

class inp(PlanewaveInput):
  """
  cpmd input class.
  """
  __doc__ = PlanewaveInput.__doc__ + __doc__
  def __init__(self, molecule, **kwargs):
    PlanewaveInput.__init__(self, molecule, **kwargs)
    self.setting.update(**kwargs)
    if 'ks_states' in kwargs:
      self.setting['ks_states'] = kwargs['ks_states']
    if 'pp_type' not in kwargs:
      self.setting['pp_type'] = 'Goedecker'
    self.backup()

  def run(self, name=None, **kwargs):
    self.setting.update(kwargs)
    return univ.runCode(self, PlanewaveInput, name, **self.setting)

  def write(self, name=None, **kwargs):
    if 'reset' in kwargs and kwargs['reset']:
      self.reset()
    self.setting.update(kwargs)
    def PPString(mol, i, n, outFile):
      ppstr = re.sub('\*', '', mol.string[i])
      if ppstr:
        PPStr = '*' + ppstr
      elif 'vdw' in self.setting\
       and self.setting['vdw'].lower == 'dcacp':
        PPStr = '*'+mol.type_list[i] + '_dcacp_' +\
          self.setting['theory'].lower() + '.psp'
      else:
        nve = qtk.n2ve(mol.type_list[i])
        PPStr = '*'+mol.type_list[i] + '_q%d_' % nve +\
          self.setting['theory'].lower() + '.psp'
      outFile.write(PPStr + '\n')

      if self.setting['pp_type'].title() == 'Goedecker':
        lmax = 'F'
      outFile.write(' LMAX=%s\n %3d\n' % (lmax, n))
      self.pp_files.append(re.sub('\*', '', PPStr))

    inp, molecule = \
      super(PlanewaveInput, self).write(name, **self.setting)

    if molecule.scale:
      molecule.R = molecule.R_scale
      self.setting['scale'] = molecule.scale


    inp.write('&INFO\n')
    inp.write(' ' + self.setting['info'] + '\n')
    inp.write('&END\n\n')

    inp.write('&CPMD\n MIRROR\n')
    if 'save_restart' not in self.setting\
     or not self.setting['save_restart']:
      inp.write(' BENCHMARK\n')
      inp.write('  1 0 0 0 0 0 0 0 0 0\n')
    if 'init_random' in self.setting\
    and self.setting['init_random']:
      inp.write(' INITIALIZE WAVEFUNCTION RANDOM\n')
    if self.setting['mode'].lower() == 'single_point':
      inp.write(' OPTIMIZE WAVEFUNCTION\n')
    elif self.setting['mode'].lower() == 'geopt':
      inp.write(' OPTIMIZE GEOMETRY\n')
    elif self.setting['mode'].lower() == 'kseg':
      if not self.setting['restart']:
        self.setting['restart'] = True
      inp.write(' KOHN-SHAM ENERGIES\n  %d\n'\
        % self.setting['ks_states'])
    elif self.setting['mode'].lower() == 'BOMD':
      inp.write(' MOLECULAR DYNAMICS BO\n')
    if re.match(self.setting['mode'], 'md'):
      inp.write(' TRAJECTORY SAMPLE XYZ\n  %d\n'\
        % self.setting['sample_period'])
      inp.write(' TEMPERATURE\n')
      inp.write('  %.1f\n' % self.setting['T'])
      if self.setting['thermostat'].lower() == 'nose-hoover':
        inp.write(' NOSE IONS\n  %.1f %.1f\n' % \
          (self.setting['T'], self.setting['T_tolerance']))
    if 'geometry_convergence' in self.setting:
      inp.write(' CONVERGENCE GEOMETRY\n  %.2E\n' %\
        self.setting['geometry_convergence'])
    if 'md_step' in self.setting:
      inp.write(' MAXSTEP\n  %d\n' % self.setting['md_step'])
    if 'wf_convergence' in self.setting:
      inp.write(' CONVERGENCE ORBITAL\n  %.2E\n' %\
        self.setting['wf_convergence'])
    if 'scf_step' in self.setting:
      inp.write(' MAXITER\n  %d\n' % self.setting['scf_step'])
    if 'restart' in self.setting and self.setting['restart']:
      inp.write(' RESTART WAVEFUNCTION\n')
    if 'fix_molecule' in self.setting\
     and self.setting['fix_molecule']:
      inp.write(' CENTER MOLECULE OFF\n')
    if 'save_density' in self.setting\
     and self.setting['save_density']:
      inp.write(' RHOOUT\n')
    if molecule.multiplicity != 1:
      inp.write(' LOCAL SPIN DENSITY\n') 
    inp.write('&END\n\n')

    inp.write('&DFT\n FUNCTIONAL %s\n&END\n\n' % \
      self.setting['theory'].upper())

    inp.write('&SYSTEM\n')
    inp.write(' SYMMETRY\n')
    if self.setting['periodic']:
      inp.write('  %s\n' % self.setting['symmetry'].upper())
    else:
      inp.write('  ISOLATED\n')
      if self.setting['isolation'] == 'mt':
        inp.write(' POISSON SOLVER TUCKERMAN\n')
    if self.setting['unit'].lower() == 'angstrom':
      inp.write(' ANGSTROM\n')
    inp.write(' CELL ABSOLUTE\n ')
    for d in self.setting['celldm']:
      inp.write(' %6.3f'% float(d))
    inp.write('\n')
    inp.write(' CUTOFF\n  %.1f\n' % self.setting['cutoff'])
    if 'scale' in self.setting:
      inp.write(' SCALE\n  SX=%d SY=%d SZ=%d\n' %\
        (self.setting['scale'][0],
         self.setting['scale'][1],
         self.setting['scale'][2]))
    if 'kmesh' in self.setting:
      inp.write(' KPOINTS MONKHORST-PACK\n  %d %d %d\n' %\
        (self.setting['kmesh'][0],
         self.setting['kmesh'][1],
         self.setting['kmesh'][2]))
    if 'mesh' in self.setting:
      inp.write(' MESH\n  %d %d %d\n' %\
        (self.setting['mesh'][0],
         self.setting['mesh'][1],
         self.setting['mesh'][2]))
    if molecule.charge != 0:
      inp.write(' CHARGE\n  %d\n' % molecule.charge)
    if molecule.multiplicity != 1:
      inp.write(' MULTIPLICITY\n  %d\n' % molecule.multiplicity)
    inp.write('&END\n\n')

    inp.write('&ATOMS\n')
    molecule.sort()
    type_index = molecule.index
    type_list = molecule.type_list
    # loop through sorted atom type indices
    for atom_type in xrange(0,len(type_index)-1):
      # number of each atom type
      type_n = type_index[atom_type+1] - type_index[atom_type]
      PPString(molecule, type_index[atom_type], type_n, inp)
      for I in\
      xrange(type_index[atom_type],type_index[atom_type+1]):
        inp.write('  ')
        for i in range(3):
          inp.write(' % 8.4f' % molecule.R[I,i])
        inp.write('\n')
    inp.write('&END\n')

    inp.close()

    return univ.writeReturn(inp, name, **self.setting)

class out(PlanewaveOutput):
  def __init__(self, qmout, **kwargs):
    PlanewaveOutput.__init__(self, qmout, **kwargs)
    self.info = ''
    if qmout:
      self.getEt(qmout)

  def getEt(self, name):
    out = sys.stdout if re.match('stdout',name)\
          else open(name, 'r')

    done = False
    finished = False
    converged = True
  
    scf_p = re.compile('^ *[0-9]*  [0-9]\.[0-9]{3}E-[0-9]{2}   .*')
    Et_cpmd = re.compile('.*TOTAL ENERGY = *([-0-9\.]*)')
    convergence = re.compile('.*BUT NO CONVERGENCE.*')
    soft_exit = re.compile('.*SOFT EXIT REQUEST.*')
    done_cpmd = re.compile(' \* *FINAL RESULTS *\*')
    qmInfo = re.compile('.*qmInfo.*')
    info_head = re.compile('.*qmInfo:')
    info_tail = re.compile(' *\*\*.*')

    while True:
      line = out.readline()
      if not line: break

      if (re.match(scf_p, line)):
        try:
          data = [float(x) for x in line.split()]
          self.scf_step = int(data[0])
        except:
          qtk.report("\n\nFailed while reading file:", name,
                    'at line: ', line,
                    '... skipping!! \n', color='yellow')
      elif re.match(convergence, line) and self.scf_step > 5:
        converged = False
      elif re.match(soft_exit, line):
        converged = False
      elif re.match(qmInfo, line):
        tmp1 = re.sub(info_head, '', line)
        tmp2 = re.sub(info_tail, '', tmp1)
        self.info = tmp2
      elif (re.match(done_cpmd,line)):
        done = True,
      elif (re.match(Et_cpmd, line)) and done and converged:
        self.Et = float(Et_cpmd.match(line).group(1))
        finished = True
