from pyRing.waveform import QNM_fit
import lal

Mf = 70
af = 0.68

l,m,n = 2,2,0

f = QNM_fit(l,m,n).f(Mf, af)
tau = QNM_fit(l,m,n).tau(Mf, af)

print('(l,m,n)     = ({},{},{})'.format(l,m,n))
print('M_f [M_sun] = {:.3f}'.format(Mf))
print('M_f [s]     = {:.3f}'.format(Mf*lal.MTSUN_SI))
print('a_f         = {:.3f}'.format(af))
print('f   [Hz]    = {:.3f}'.format(f))
print('tau [ms]    = {:.3f}'.format(tau*1e3))
print('tau [M]    = {:.3f}'.format(tau/(Mf*lal.MTSUN_SI)))
