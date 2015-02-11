import numpy as np


def get_lattice_points(num_dimensions, num_points):
    """ Generates lattice points in multiple dimensions

    """
    z = np.array([1, 182667, 469891, 498753, 110745, 446247, 250185, 118627, 245333, 283199, 408519, 391023, 246327, 126539, 399185, 461527, 300343, 69681, 516695, 436179, 106383, 238523, 413283, 70841, 47719, 300129, 113029, 123925, 410745, 211325, 17489, 511893, 40767, 186077, 519471, 255369, 101819, 243573, 66189, 152143, 503455, 113217, 132603, 463967, 297717, 157383, 224015, 502917, 36237, 94049, 170665, 79397, 123963, 223451, 323871, 303633, 98567, 318855, 494245, 477137, 177975, 64483, 26695, 88779, 94497, 239429, 381007, 110205, 339157, 73397, 407559, 181791, 442675, 301397, 32569, 147737, 189949, 138655, 350241, 63371, 511925, 515861, 434045, 383435, 249187, 492723, 479195, 84589, 99703, 239831, 269423, 182241, 61063, 130789, 143095, 471209, 139019, 172565, 487045, 304803, 45669, 380427, 19547, 425593, 337729, 237863, 428453, 291699, 238587, 110653, 196113, 465711, 141583, 224183, 266671, 169063, 317617, 68143, 291637, 263355, 427191, 200211, 365773, 254701,
                  368663, 248047, 209221, 279201, 323179, 80217, 122791, 316633, 118515, 14253, 129509, 410941, 402601, 511437, 10469, 366469, 463959, 442841, 54641, 44167, 19703, 209585, 69037, 33317, 433373, 55879, 245295, 10905, 468881, 128617, 417919, 45067, 442243, 359529, 51109, 290275, 168691, 212061, 217775, 405485, 313395, 256763, 152537, 326437, 332981, 406755, 423147, 412621, 362019, 279679, 169189, 107405, 251851, 5413, 316095, 247945, 422489, 2555, 282267, 121027, 369319, 204587, 445191, 337315, 322505, 388411, 102961, 506099, 399801, 254381, 452545, 309001, 147013, 507865, 32283, 320511, 264647, 417965, 227069, 341461, 466581, 386241, 494585, 201479, 151243, 481337, 68195, 75401, 58359, 448107, 459499, 9873, 365117, 350845, 181873, 7917, 436695, 43899, 348367, 423927, 437399, 385089, 21693, 268793, 49257, 250211, 125071, 341631, 310163, 94631, 108795, 21175, 142847, 383599, 71105, 65989, 446433, 177457, 107311, 295679, 442763, 40729, 322721, 420175, 430359, 480757])
    z = z[1:num_dimensions + 1].reshape((1, num_dimensions))
    k = np.arange(1, num_points + 1).reshape((1, num_points))

    return np.mod(np.dot(z.T, k), num_points).astype(float) / num_points
