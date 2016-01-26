#!/usr/bin/python

import qctoolkit as qtk

#path=['../data/qmout/nwchem/H_1g/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_1g-01/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_1g-045/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_1g-08/h.out', 'nwchem']
path=['../data/qmout/nwchem/H_2g/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_2g-rev/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_1a/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_3g/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_1p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_1g1p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_2g1p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_3g1p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_2p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_2g2p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_2a_gaussian_basis/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_aug-cc-pvdz/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H_cc-pvdz_no-p/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_1g/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_1g-4e/h.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_1a/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_3g/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_aug-cc-pvdz/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H2-y_aug-cc-pvdz/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H2-yz_aug-cc-pvdz/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-z/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1a/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-012/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-013/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-023/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-123/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_1g-asym-01/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_1g-asym-02/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H2_1g-asym-12/h2.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_aug-cc-pvdz-2e/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_aug-cc-pvdz-4e/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-asym-012/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-asym-012-2e/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-asym-013/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-asym-023/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-asym-123/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H3_1g-asym/h3.out', 'nwchem']
#path=['../data/qmout/nwchem/H4_1g/h4.out', 'nwchem']
#path=['../data/qmout/nwchem/HHe_1p/hhe.out', 'nwchem']
#path=['../data/qmout/nwchem/HHe_1p-y/hhe.out', 'nwchem']
#path=['../data/qmout/nwchem/HHe_2p/hhe.out', 'nwchem']
#path=['../data/qmout/nwchem/HLi_3g/hli.out', 'nwchem']
#path=['../data/qmout/nwchem/H2He_1p/hhe.out', 'nwchem']
#path=['../data/qmout/nwchem/H2He_3g/h2he.out', 'nwchem']
#path=['../data/qmout/nwchem/H2He_3g-1p/h2he.out', 'nwchem']
#path=['../data/qmout/nwchem/H2O_aug-cc-pvdz/h2o.out', 'nwchem']
#path=['../data/qmout/nwchem/H2O_aug-cc-pvdz_b3lyp/h2o.out', 'nwchem']
#path=['../data/qmout/nwchem/water/anDIR-01_00A.out', 'nwchem']

#path=['../data/qmout/gaussian/H_1g/H.out', 'gaussian']
#path=['../data/qmout/gaussian/H_1p/H.out', 'gaussian']
#path=['../data/qmout/gaussian/H_2g2p/H.out', 'gaussian']
#path=['../data/qmout/gaussian/H_2a/H.out', 'gaussian']
#path=['../data/qmout/gaussian/H2He_3g-1p/H2He.out', 'gaussian']
#path=['../data/qmout/gaussian/H2_3g/H2.out', 'gaussian']
#path=['../data/qmout/gaussian/H2_1s1p/H2.out', 'gaussian']
#path=['../data/qmout/gaussian/H2O_aug-cc-pvdz/H2O.out', 'gaussian']
#path=['../data/qmout/gaussian/OOFCl/OOFCl_0.log', 'gaussian']

qmOut = qtk.QMOut(path[0], program=path[1])
occ = [i for i in range(qmOut.n_ao) if qmOut.occupation[i]==2][-1] + 1
mo = qmOut.mo_vectors
