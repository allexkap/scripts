print(
    ''.join(
        '{{+KC_LALT}}{}{{-KC_LALT}}'.format(
            ''.join('{{KC_P{}}}'.format(i) for i in str(ord(ch)))
        )
        for ch in input()
    )
)
