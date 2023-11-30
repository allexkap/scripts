class L:
    def __init__(self, val):
        self.val = bool(val)

    def __or__(self, rhs):
        return L(not self.val or not rhs.val)

    def __str__(self):
        return f'{self.val:0}'


print('a b ! & v ^ > |')
for A in (L(0), L(1)):
    for B in (L(0), L(1)):
        NOT = A | A
        AND = (A | B) | (A | B)
        OR = (A | A) | (B | B)
        XOR = (A | (A | B)) | (B | (A | B))
        IMP = A | (A | B)
        print(f'{A} {B} {NOT} {AND} {OR} {XOR} {IMP} {A | B}')
