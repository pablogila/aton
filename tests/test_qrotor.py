import aton.qrotor as qr
import aton.interface as interface
import aton.txt.extract as extract
import aton.st.file as file


folder = 'tests/samples/'
structure = folder + 'CH3NH3.in'
structure_120 = folder + 'CH3NH3_120.in'


def test_rotate():
    CH3 = [
        '0.100   0.183   0.316',
        '0.151   0.532   0.842',
        '0.118   0.816   0.277'
    ]
    qr.rotate.qe(filepath=structure, positions=CH3, angle=120, precision=2)

    for coord in CH3:
        rotated_coord = interface.qe.get_atom(filepath=structure_120, position=coord, precision=2)
        rotated_coord = extract.coords(rotated_coord)
        coord = extract.coords(coord)
        rotated_coord_rounded = []
        coord_rounded = []
        for i in rotated_coord:
            rotated_coord_rounded.append(round(i, 2))
        for i in coord:
            coord_rounded.append(round(i, 2))
        assert coord_rounded == rotated_coord_rounded
    file.remove(structure_120)

