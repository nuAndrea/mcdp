# -*- coding: utf-8 -*-
import itertools

from contracts.utils import indent, raise_wrapped
from mcdp_posets import (NotBelongs, PosetProduct,
    lowerset_product, upperset_product)
from mcdp_posets.uppersets import lowerset_product_good
from mcdp.development import do_extra_checks

from .dp_series import get_product_compact
from .primitive import PrimitiveDP
from .repr_strings import repr_h_map_parallel


__all__ = [
    'Parallel',
]


class Parallel(PrimitiveDP):

    def __init__(self, dp1, dp2):
        self.dp1 = dp1
        self.dp2 = dp2

        F1 = self.dp1.get_fun_space()
        F2 = self.dp2.get_fun_space()
        F = PosetProduct((F1, F2))
        R1 = self.dp1.get_res_space()
        R2 = self.dp2.get_res_space()

        R = PosetProduct((R1, R2))

        M1 = self.dp1.get_imp_space()
        M2 = self.dp2.get_imp_space()


        self.M1 = M1
        self.M2 = M2

        M, _, _ = self._get_product()

        PrimitiveDP.__init__(self, F=F, R=R, I=M)

    def __getstate__(self):
        state = dict(**self.__dict__)
        state.pop('prod', None)
        return state

    def _get_product(self):
        if not hasattr(self, 'prod'):
            self.prod = _, _, _ = get_product_compact(self.M1, self.M2)
        return self.prod

    def get_implementations_f_r(self, f, r):
        f1, f2 = f
        r1, r2 = r
        _, pack, _ = self._get_product()

        m1s = self.dp1.get_implementations_f_r(f1, r1)
        m2s = self.dp2.get_implementations_f_r(f2, r2)
        options = set()

        if do_extra_checks():
            for m1 in m1s:
                self.M1.belongs(m1)

            try:
                for m2 in m2s:
                    self.M2.belongs(m2)
            except NotBelongs as e:
                msg = ' Invalid result from dp2'
                raise_wrapped(NotBelongs, e, msg, dp2=self.dp2.repr_long())

        for m1 in m1s:
            for m2 in m2s:
                m = pack(m1, m2)
                options.add(m)

        if do_extra_checks():
            for _ in options:
                self.I.belongs(_)

        return options
        
    def _split_m(self, m):
        _, _, unpack = self._get_product()

        m1, m2 = unpack(m)
        return m1, m2

    def evaluate(self, i):
        m1, m2 = self._split_m(i)

        fs1, rs1 = self.dp1.evaluate(m1)
        fs2, rs2 = self.dp2.evaluate(m2)

        fs = lowerset_product(fs1, fs2)
        rs = upperset_product(rs1, rs2)

        return fs, rs

#     def evaluate_f_m(self, f, m):
#         """ Returns the resources needed
#             by the particular implementation m """
#         f1, f2 = f
#         m1, m2 = self._split_m(m)
#         r1 = self.dp1.evaluate_f_m(f1, m1)
#         r2 = self.dp2.evaluate_f_m(f2, m2)
#         return (r1, r2)


    def solve(self, f):
        if do_extra_checks():
            F = self.get_fun_space()
            F.belongs(f)

        f1, f2 = f

        r1 = self.dp1.solve(f1)
        r2 = self.dp2.solve(f2)
        
        R = self.get_res_space()
        s = []
        for m1, m2 in itertools.product(r1.minimals, r2.minimals):
            s.append((m1, m2))

        res = R.Us(set(s))

        return res

    def solve_r(self, r):
        r1, r2 = r
        lf1 = self.dp1.solve_r(r1)
        lf2 = self.dp2.solve_r(r2)
        return lowerset_product_good(lf1, lf2)

    def __repr__(self):
        return 'Parallel(%r, %r)' % (self.dp1, self.dp2)

    def repr_long(self):
        r1 = self.dp1.repr_long()
        r2 = self.dp2.repr_long()
        s = 'Parallel2  %% %s ⇸ %s' % (self.get_fun_space(), self.get_res_space())
        s += '\n' + indent(r1, '. ', first='\ ')
        s += '\n' + indent(r2, '. ', first='\ ') 
        return s
    
    def repr_h_map(self):
        return repr_h_map_parallel('f', 2, 'h')
    
    def repr_hd_map(self):
        return repr_h_map_parallel('r', 2, 'h*')

# 
# def upperset_project_two(P, u):
#     """ u = upperset in P
#         P = Product(P1, P2) 
#         returns u1, u2
#     """
#     m1 = set()
#     m2 = set()
#     for a,b in u.minimals:
#         m1.add(a)
#         m2.add(b)
#     
#     P1 = P[0]
#     P2 = P[1]
#     m1m = poset_minima(m1, P1.leq)
#     m2m = poset_minima(m2, P2.leq)
#     
#     u1 = UpperSet(m1m, P1)
#     u2 = UpperSet(m2m, P2)
#     return u1, u2
#         
