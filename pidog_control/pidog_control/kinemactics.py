import numpy as np
from math import sin, cos, atan2, asin, pi, floor
import math
import copy

L1 = 0.047  # meters
L2 = 0.064
W = 0.0095

OUTER_RADIUS = L1**2 + L2**2
INNER_RADIUS = L1**2 - L2**2
if INNER_RADIUS < 0:
    INNER_RADIUS = -INNER_RADIUS

def abs(x):
    if x >= 0:
        return x
    else:
        return -x


def norm_ang(angle):

    if -pi < angle < pi: return angle

    theta = (angle + np.pi) % (2*np.pi) - np.pi

    return theta


def leg_forward_kin(angle1, angle2, left=True):

    sign = 1 if left else -1

    x = -(sign) * L1 * sin(angle1) + L2 * cos(angle1 + angle2)
    y = sign * L1 * cos(angle1) + L2 * sin(angle1 + angle2)
    z = W

    return x, y, z


def leg_inverse_kin(x, y, left=True):

    if not left:
        y = -y

    radius2 = x**2 + y**2

    sign = 1 if left else -1

    b = (radius2 - L1**2 - L2**2) / (2 * L1 * L2)

    if b > 1 or b < -1:
        raise ValueError("Coordinates out of domian with b =", b)

    angle2 = [norm_ang(asin(sign * b)), norm_ang(pi - asin(sign * b))]

    angles = []

    for a2 in angle2:

        k1 = L2 * cos(a2)
        k2 = L2 * sin(a2) + (sign) * L1

        a1 = norm_ang(atan2(k1, k2) - atan2(x, y))

        angles.append([a1, a2])

    found_angle = False
    for angs in angles:

        if (-pi / 2 < angs[0] < pi / 2) and (-pi / 2 < angs[1] < pi / 2):
            angle1 = angs[0]
            angle2 = angs[1]
            found_angle = True
            break

    if not found_angle:
        raise ValueError(f"No solution in range {angles} for (x,y) --> ({x},{y}) (left leg -> {left})")

    return angle1, angle2


def jacobian(angle1, angle2, left=True) -> np.ndarray:

    sign = 1 if left else -1

    J = np.array(
        [
            [
                -sign * L1 * cos(angle1) - L2 * sin(angle1 + angle2),
                -L2 * sin(angle1 + angle2),
            ],
            [
                -sign * L1 * sin(angle1) + L2 * cos(angle1 + angle2),
                L2 * cos(angle1 + angle2),
            ],
        ]
    )

    return J


def jacobian_inv(angle1, angle2, left=True):

    J = jacobian(angle1, angle2, left)

    return np.linalg.inv(J)


def equal_four_legs_inverse_kin(x : float, y : float):

    left_legs = leg_inverse_kin(x, y, True)
    right_legs = leg_inverse_kin(x, y, False)

    angles = []

    angles.extend(left_legs)
    angles.extend(right_legs)
    angles.extend(left_legs)
    angles.extend(right_legs)

    return angles


def four_legs_inverse_kin(x : np.ndarray, y : np.ndarray, left: np.ndarray = None):

    if isinstance(x, float):
        x = np.array([x])

    if isinstance(y, float):
        y = np.array([y])

    if left is None:
        left = np.array([True])
    
    if isinstance(left, bool):
        left = np.array([left])

    if x.shape != y.shape:
        raise ValueError(f"X and Y have different shapes {x.shape} != {y.shape}")
    
    if len(x.shape) != 1 or len(y.shape) != 1 or len(left.shape) != 1:
        raise ValueError("All numpy arrays must have 1 dimension") 

    angles = []
    for i in range(0, x.shape[0]):
        leg_angles = leg_inverse_kin(x[i], y[i], left[i])
        angles.extend(leg_angles)

    return angles


def leg_circle_path(angle1, angle2, N, r, left=True):

    angle = np.linspace(0, 2 * pi, N)

    x0, y0, _ = leg_forward_kin(angle1, angle2, left)

    x = (x0 - r) + r * np.cos(angle)
    y = y0 + r * np.sin(angle)

    delta_x = x[1:] - x[:-1]
    delta_y = y[1:] - y[:-1]

    ang = [angle1, angle2]

    planned_angles = []
    planned_angles.append(ang)

    for i in range(0, delta_x.shape[0]):

        J_inv = jacobian_inv(ang[0], ang[1], left)

        delta_angles = np.matmul(J_inv, np.array([[delta_x[i]], [delta_y[i]]]))
        delta_angles.flatten()

        ang[0] += float(delta_angles[0])
        ang[1] += float(delta_angles[1])

        planned_angles.append(copy.deepcopy(ang))

    return planned_angles



def straight_walk_planner(x_offset, height):

    walk_order = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],  
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ])

    walk_dist = 0.06
    delta_x = walk_dist / 5
    foot_height = 0.015
    
    leg_sides = np.array([True, False, True, False])

    x = np.array([0.01, 0.01, -0.01, -0.01]) + x_offset
    y = np.ones((4, 8)) * height
    
    planned_angles = []

    for i in range(0, 8):

        if i >= 3:
            x -= delta_x  
        
        if i % 2 == 0:
            for j in range(0, 3):
                
                if j % 3 == 0: y[:, i] = np.subtract(y[:, i], walk_order[:, i] * foot_height)
                if j % 3 == 1: y[:, i] = np.add(y[:, i], walk_order[:, i] * foot_height)
                if j % 3 != 2: x += walk_order[:, i] * (walk_dist / 2)

                angles = four_legs_inverse_kin(x, y[:, i], leg_sides)
                angles.extend([0.0, 0.0, 0.0, 0.0])

                planned_angles.append(angles)
        else:
            x += walk_order[:, i] * walk_dist
            angles = four_legs_inverse_kin(x, y[:, i], leg_sides)
            angles.extend([0.0, 0.0, 0.0, 0.0])

            planned_angles.append(angles)
    
    print("Planned angles:", len(planned_angles))
    return planned_angles

def pivot_planner(x_offset, height):

    walk_order = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],  
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ])

    walk_dist = 0.06
    delta_x = walk_dist / 5
    foot_height = 0.015
    
    leg_sides = np.array([True, False, True, False])

    x = np.array([0.01, 0.01, -0.01, -0.01]) + x_offset
    y = np.ones((4, 8)) * height
    
    planned_angles = []

    for i in range(0, 8):

        if i >= 3:
            x -= delta_x  
        
        if i % 2 == 0:
            for j in range(0, 3):
                
                if j % 3 == 0: y[:, i] = np.subtract(y[:, i], walk_order[:, i] * foot_height)
                if j % 3 == 1: y[:, i] = np.add(y[:, i], walk_order[:, i] * foot_height)
                if j % 3 != 2: x += walk_order[:, i] * (walk_dist / 2)

                angles = four_legs_inverse_kin(x, y[:, i], leg_sides)
                angles.extend([0.0, 0.0, 0.0, 0.0])

                planned_angles.append(angles)
        else:
            x += walk_order[:, i] * walk_dist
            angles = four_legs_inverse_kin(x, y[:, i], leg_sides)
            angles.extend([0.0, 0.0, 0.0, 0.0])

            planned_angles.append(angles)
    
    print("Planned angles:", len(planned_angles))
    return planned_angles