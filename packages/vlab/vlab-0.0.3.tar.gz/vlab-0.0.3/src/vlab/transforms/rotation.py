import numpy as np
import torch
import torch.nn.functional as F

"""
Reading Materials:

General:
    1. https://thenumbat.github.io/Exponential-Rotations/

Quaternions:
    1. https://eater.net/quaternions

Anxis angle:
    1. https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation
    2. https://people.eecs.berkeley.edu/~ug/slide/pipeline/assignments/as5/rotation.html
    3. http://motion.pratt.duke.edu/RoboticSystems/3DRotations.html#Converting-from-a-rotation-matrix

Acknowledgement:
    Adapted from https://github.com/facebookresearch/pytorch3d/blob/main/pytorch3d/transforms/rotation_conversions.py
"""


def _sqrt_positive_part(x):
    """
    Returns torch.sqrt(torch.max(0, x))
    but with a zero subgradient where x is 0.
    """
    if isinstance(x, np.ndarray):
        ret = np.zeros_like(x)
        positive_mask = x > 0
        ret[positive_mask] = np.sqrt(x[positive_mask])
    elif isinstance(x, torch.Tensor):
        ret = torch.zeros_like(x)
        positive_mask = x > 0
        ret[positive_mask] = torch.sqrt(x[positive_mask])
    else:
        raise TypeError("x should be np.ndarray or torch.Tensor")
    return ret


def split_axis_angle(axis_angle):
    if isinstance(axis_angle, np.ndarray) or isinstance(axis_angle, list) or isinstance(axis_angle, tuple):
        axis_angle = np.asarray(axis_angle)
        angle = np.linalg.norm(axis_angle, axis=-1, keepdims=True)
        axis = axis_angle / angle
    elif isinstance(axis_angle, torch.Tensor):
        angle = torch.norm(axis_angle, p=2, dim=-1, keepdim=True)
        axis = axis_angle / angle
    else:
        raise TypeError(f"axis_angle should be np.ndarray, torch.Tensor, list or tuple, but got {type(axis_angle)}")
    return axis, angle


def compose_axis_angle(axis, angle):
    return axis * angle


def axis_angle_to_quaternion(axis_angle):
    """
    Convert rotations given as axis/angle to quaternions.
    Ref: https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation#Unit_quaternions

    Args:
        axis_angle: Rotations given as a vector in axis angle form,
            as a tensor of shape (..., 3), where the magnitude is
            the angle turned anticlockwise in radians around the
            vector's direction.
    Returns:
        quaternions with real part first, as tensor of shape (..., 4).
    """
    if isinstance(axis_angle, np.ndarray) or isinstance(axis_angle, list) or isinstance(axis_angle, tuple):
        axis_angle = np.asarray(axis_angle)
        angles = np.linalg.norm(axis_angle, axis=-1, keepdims=True)
        half_angles = angles * 0.5
        eps = 1e-6
        small_angles = np.abs(angles) < eps
        sin_half_angles_over_angles = np.empty_like(angles)
        sin_half_angles_over_angles[~small_angles] = np.sin(half_angles[~small_angles]) / angles[~small_angles]
        sin_half_angles_over_angles[small_angles] = 0.5 - (angles[small_angles] * angles[small_angles]) / 48
        quaternions = np.concatenate([np.cos(half_angles), axis_angle * sin_half_angles_over_angles], axis=-1)
    elif isinstance(axis_angle, torch.Tensor):
        angles = torch.norm(axis_angle, p=2, dim=-1, keepdim=True)
        half_angles = angles * 0.5
        eps = 1e-6
        small_angles = angles.abs() < eps
        sin_half_angles_over_angles = torch.empty_like(angles)
        sin_half_angles_over_angles[~small_angles] = torch.sin(half_angles[~small_angles]) / angles[~small_angles]
        # for x small, sin(x/2) is about x/2 - (x/2)^3/6
        # so sin(x/2)/x is about 1/2 - (x*x)/48
        sin_half_angles_over_angles[small_angles] = 0.5 - (angles[small_angles] * angles[small_angles]) / 48
        quaternions = torch.cat([torch.cos(half_angles), axis_angle * sin_half_angles_over_angles], dim=-1)
    else:
        raise TypeError(f"axis_angle should be np.ndarray, torch.Tensor, list or tuple, but got {type(axis_angle)}")
    return quaternions


def quaternion_to_axis_angle(quaternions):
    """
    Convert rotations given as quaternions to axis/angle.
    Ref: https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation#Unit_quaternions

    Args:
        quaternions: quaternions with real part first,
            as tensor of shape (..., 4).
    Returns:
        Rotations given as a vector in axis angle form, as a tensor
            of shape (..., 3), where the magnitude is the angle
            turned anticlockwise in radians around the vector's
            direction.
    """
    if isinstance(quaternions, np.ndarray) or isinstance(quaternions, list) or isinstance(quaternions, tuple):
        quaternions = np.asarray(quaternions)
        norms = np.linalg.norm(quaternions[..., 1:], axis=-1, keepdims=True)
        half_angles = np.arctan2(norms, quaternions[..., :1])
        angles = 2 * half_angles
        eps = 1e-6
        small_angles = np.abs(angles) < eps
        sin_half_angles_over_angles = np.empty_like(angles)
        sin_half_angles_over_angles[~small_angles] = np.sin(half_angles[~small_angles]) / angles[~small_angles]
        sin_half_angles_over_angles[small_angles] = 0.5 - (angles[small_angles] * angles[small_angles]) / 48
        quaternions = quaternions[..., 1:] / sin_half_angles_over_angles
    elif isinstance(quaternions, torch.Tensor):
        norms = torch.norm(quaternions[..., 1:], p=2, dim=-1, keepdim=True)
        half_angles = torch.atan2(norms, quaternions[..., :1])
        angles = 2 * half_angles
        eps = 1e-6
        small_angles = angles.abs() < eps
        sin_half_angles_over_angles = torch.empty_like(angles)
        sin_half_angles_over_angles[~small_angles] = torch.sin(half_angles[~small_angles]) / angles[~small_angles]
        # for x small, sin(x/2) is about x/2 - (x/2)^3/6
        # so sin(x/2)/x is about 1/2 - (x*x)/48
        sin_half_angles_over_angles[small_angles] = 0.5 - (angles[small_angles] * angles[small_angles]) / 48
        quaternions = quaternions[..., 1:] / sin_half_angles_over_angles
    return quaternions


def standardize_quaternion(quaternions):
    """
    Convert a unit quaternion to a standard form: one in which the real
    part is non negative.
    Args:
        quaternions: Quaternions with real part first, as tensor of shape (..., 4).
    Returns:
        Standardized quaternions as tensor of shape (..., 4).
    """
    if isinstance(quaternions, np.ndarray) or isinstance(quaternions, list) or isinstance(quaternions, tuple):
        quat = np.asarray(quaternions)
        quat = np.where(quat[..., 0:1] < 0, -quat, quat)
    elif isinstance(quaternions, torch.Tensor):
        quat = torch.where(quaternions[..., 0:1] < 0, -quaternions, quaternions)
    return quat


def quaternion_real_to_last(quaternions):
    # move the real part in quaternions to last
    return quaternions[..., [1, 2, 3, 0]]


def quaternion_real_to_first(quaternions):
    # move the real part in quaternions to first
    return quaternions[..., [3, 0, 1, 2]]


# Borrow from https://github.com/facebookresearch/pytorch3d/blob/main/pytorch3d/transforms/rotation_conversions.py
def quaternion_to_matrix(quaternions):
    """
    Convert rotations given as quaternions to rotation matrices.
    Ref: https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation

    Args:
        quaternions: quaternions with real part first with shape (..., 4).
    Returns:
        Rotation matrices as tensor of shape (..., 3, 3).
    """
    if isinstance(quaternions, np.ndarray) or isinstance(quaternions, list) or isinstance(quaternions, tuple):
        quaternions = np.asarray(quaternions)
        r, i, j, k = quaternions[..., 0], quaternions[..., 1], quaternions[..., 2], quaternions[..., 3]
        two_s = 2.0 / (quaternions * quaternions).sum(-1)
        matrices = np.stack(
            [
                1 - two_s * (j * j + k * k),
                two_s * (i * j - k * r),
                two_s * (i * k + j * r),
                two_s * (i * j + k * r),
                1 - two_s * (i * i + k * k),
                two_s * (j * k - i * r),
                two_s * (i * k - j * r),
                two_s * (j * k + i * r),
                1 - two_s * (i * i + j * j),
            ],
            axis=-1,
        )
        matrices = matrices.reshape(quaternions.shape[:-1] + (3, 3))
    elif isinstance(quaternions, torch.Tensor):
        r, i, j, k = torch.unbind(quaternions, -1)
        two_s = 2.0 / (quaternions * quaternions).sum(-1)

        matrices = torch.stack(
            [
                1 - two_s * (j * j + k * k),
                two_s * (i * j - k * r),
                two_s * (i * k + j * r),
                two_s * (i * j + k * r),
                1 - two_s * (i * i + k * k),
                two_s * (j * k - i * r),
                two_s * (i * k - j * r),
                two_s * (j * k + i * r),
                1 - two_s * (i * i + j * j),
            ],
            dim=-1,
        )
        matrices = matrices.reshape(quaternions.shape[:-1] + (3, 3))
    else:
        raise TypeError(f"quaternions should be np.ndarray, torch.Tensor, list or tuple, but got {type(quaternions)}")

    return matrices


# Borrow from https://github.com/facebookresearch/pytorch3d/blob/main/pytorch3d/transforms/rotation_conversions.py
def matrix_to_quaternion(matrix):
    """
    Convert rotation matrices to quaternions using Shepperds’s method.
    Ref: http://www.iri.upc.edu/files/scidoc/2068-Accurate-Computation-of-Quaternions-from-Rotation-Matrices.pdf
    Note that the way to determine the best solution is slighly different from the PDF.

    Args:
        matrix: (np.ndarray, torch.Tensor, list, tuple): rotation matrices, the shape could be ...3x3.
    Returns:
        quaternions with real part first, as tensor of shape (..., 4).
    """
    if isinstance(matrix, np.ndarray) or isinstance(matrix, list) or isinstance(matrix, tuple):
        matrix = np.asarray(matrix)
        batch_dim = matrix.shape[:-2]

        m00, m01, m02, m10, m11, m12, m20, m21, m22 = (
            matrix[..., 0, 0],
            matrix[..., 0, 1],
            matrix[..., 0, 2],
            matrix[..., 1, 0],
            matrix[..., 1, 1],
            matrix[..., 1, 2],
            matrix[..., 2, 0],
            matrix[..., 2, 1],
            matrix[..., 2, 2],
        )

        q_abs = _sqrt_positive_part(
            np.stack(
                [
                    1.0 + m00 + m11 + m22,
                    1.0 + m00 - m11 - m22,
                    1.0 - m00 + m11 - m22,
                    1.0 - m00 - m11 + m22,
                ],
                axis=-1,
            )
        )

        quat_by_rijk = np.stack(
            [
                np.stack([q_abs[..., 0] ** 2, m21 - m12, m02 - m20, m10 - m01], axis=-1),
                np.stack([m21 - m12, q_abs[..., 1] ** 2, m10 + m01, m02 + m20], axis=-1),
                np.stack([m02 - m20, m10 + m01, q_abs[..., 2] ** 2, m12 + m21], axis=-1),
                np.stack([m10 - m01, m20 + m02, m21 + m12, q_abs[..., 3] ** 2], axis=-1),
            ],
            axis=-2,
        )
        flr = np.array([0.1])
        quat_candidates = quat_by_rijk / (2.0 * np.maximum(q_abs[..., None], flr))

        quat_candidates = quat_candidates.reshape(-1, 4, 4)
        quat = quat_candidates[np.arange(quat_candidates.shape[0]), np.argmax(q_abs, axis=-1).reshape(-1)]
        quat = quat.reshape(batch_dim + (4,))
    elif isinstance(matrix, torch.Tensor):
        batch_dim = matrix.shape[:-2]
        m00, m01, m02, m10, m11, m12, m20, m21, m22 = torch.unbind(matrix.reshape(batch_dim + (9,)), dim=-1)

        q_abs = _sqrt_positive_part(
            torch.stack(
                [
                    1.0 + m00 + m11 + m22,
                    1.0 + m00 - m11 - m22,
                    1.0 - m00 + m11 - m22,
                    1.0 - m00 - m11 + m22,
                ],
                dim=-1,
            )
        )

        # we produce the desired quaternion multiplied by each of r, i, j, k
        quat_by_rijk = torch.stack(
            [
                torch.stack([q_abs[..., 0] ** 2, m21 - m12, m02 - m20, m10 - m01], dim=-1),
                torch.stack([m21 - m12, q_abs[..., 1] ** 2, m10 + m01, m02 + m20], dim=-1),
                torch.stack([m02 - m20, m10 + m01, q_abs[..., 2] ** 2, m12 + m21], dim=-1),
                torch.stack([m10 - m01, m20 + m02, m21 + m12, q_abs[..., 3] ** 2], dim=-1),
            ],
            dim=-2,
        )

        # We floor here at 0.1 but the exact level is not important; if q_abs is small,
        # the candidate won't be picked.
        flr = torch.tensor(0.1).to(dtype=q_abs.dtype, device=q_abs.device)
        quat_candidates = quat_by_rijk / (2.0 * q_abs[..., None].max(flr))

        # if not for numerical problems, quat_candidates[i] should be same (up to a sign),
        # for all i; we pick the best-conditioned one (with the largest denominator)
        quat = quat_candidates[F.one_hot(q_abs.argmax(dim=-1), num_classes=4) > 0.5, :].reshape(batch_dim + (4,))
    else:
        raise TypeError(f"matrix should be np.ndarray, torch.Tensor, list or tuple, but got {type(matrix)}")

    return quat


def axis_angle_to_matrix(axis_angle):
    """
    Converts axis angles to rotation matrices using Rodrigues formula.

    Args:
        axis_angle (np.ndarray, torch.Tensor, list, tuple): axis_angle, the shape could be ...x3 (including 3).
    Returns:
        Rotation matrices (...x3x3 np.ndarray or torch.Tensor)
    """
    return quaternion_to_matrix(axis_angle_to_quaternion(axis_angle))


def matrix_to_axis_angle(matrix):
    """
    Convert rotations given as rotation matrices to axis/angle.

    Args:
        matrix: Rotation matrices with shape (..., 3, 3).
    Returns:
        Rotations given as a vector in axis angle form, as a tensor
            of shape (..., 3), where the magnitude is the angle
            turned anticlockwise in radians around the vector's
            direction.
    """
    return quaternion_to_axis_angle(matrix_to_quaternion(matrix))


# TODO: check why the Rodrigues formula is not differentiable
def axis_angle_to_matrix_legacy(axis_angle, epsilon=1e-6):
    """
    Converts axis angles to rotation matrices using Rodrigues formula.

    Ref: http://en.wikipedia.org/wiki/Rotation_matrix#Axis_and_angle

    Args:
        axis_angle (np.ndarray, torch.Tensor, list, tuple): axis_angle, the shape could be ...x3 (including 3).
    Returns:
        Rotation matrices (...x3x3 np.ndarray or torch.Tensor)
    """
    if isinstance(axis_angle, np.ndarray) or isinstance(axis_angle, list) or isinstance(axis_angle, tuple):
        axis_angle = np.asarray(axis_angle)

        angle = np.linalg.norm(axis_angle, axis=-1)
        angle = np.where(angle != 0, angle, 1e-12)
        axis = axis_angle / angle[..., None]

        is_angle_small = angle < epsilon

        x, y, z = axis[..., 0], axis[..., 1], axis[..., 2]
        s, c = np.sin(angle), np.cos(angle)
        C = 1 - c

        xs, ys, zs = x * s, y * s, z * s
        xC, yC, zC = x * C, y * C, z * C
        xyC, yzC, zxC = x * yC, y * zC, z * xC

        # Concatenating joins a sequence of tensors along an existing axis,
        # and stacking joins a sequence of tensors along a new axis.
        rot_mat = np.stack(
            [x * xC + c, xyC - zs, zxC + ys, xyC + zs, y * yC + c, yzC - xs, zxC - ys, yzC + xs, z * zC + c],
            axis=-1,
        )
        rot_mat = rot_mat.reshape(angle.shape + (3, 3))

        # For small angles, use a first order approximation
        x, y, z = axis_angle[..., 0], axis_angle[..., 1], axis_angle[..., 2]
        one = np.ones_like(x)
        rot_first_order = np.stack([one, -z, y, z, one, -x, -y, x, one], axis=-1).reshape(angle.shape + (3, 3))
        rot_mat[is_angle_small] = rot_first_order[is_angle_small]
    elif isinstance(axis_angle, torch.Tensor):
        angle = torch.norm(axis_angle, dim=-1)
        axis = axis_angle / angle[..., None]
        is_angle_small = angle < epsilon

        x, y, z = axis[..., 0], axis[..., 1], axis[..., 2]
        s, c = torch.sin(angle), torch.cos(angle)
        C = 1 - c

        xs, ys, zs = x * s, y * s, z * s
        xC, yC, zC = x * C, y * C, z * C
        xyC, yzC, zxC = x * yC, y * zC, z * xC

        rot_mat = torch.stack(
            [x * xC + c, xyC - zs, zxC + ys, xyC + zs, y * yC + c, yzC - xs, zxC - ys, yzC + xs, z * zC + c],
            axis=-1,
        )
        rot_mat = rot_mat.reshape(angle.shape + (3, 3))

        # For small angles, use a first order approximation
        x, y, z = axis_angle[..., 0], axis_angle[..., 1], axis_angle[..., 2]
        one = torch.ones_like(x)
        rot_first_order = torch.stack([one, -z, y, z, one, -x, -y, x, one], dim=-1).reshape(angle.shape + (3, 3))
        rot_mat[is_angle_small] = rot_first_order[is_angle_small]
    else:
        raise TypeError(f"axis_angle should be np.ndarray, torch.Tensor, list or tuple, but got {type(axis_angle)}")

    return rot_mat


def _index_from_letter(letter: str) -> int:
    if letter not in "xyz":
        raise ValueError(f"{letter} is not a valid axis letter")
    return "xyz".index(letter)


def _angle_from_tan(axis, other_axis, data, horizontal, tait_bryan):
    """
    Extract the first or third Euler angle from the two members of
    the matrix which are positive constant times its sine and cosine.

    Args:
        axis: Axis label "x" or "y or "z" for the angle we are finding.
        other_axis: Axis label "x" or "y or "z" for the middle axis in the
            convention.
        data: Rotation matrices as tensor of shape (..., 3, 3).
        horizontal: Whether we are looking for the angle for the third axis,
            which means the relevant entries are in the same row of the
            rotation matrix. If not, they are in the same column.
        tait_bryan: Whether the first and third axes in the convention differ.

    Returns:
        Euler Angles in radians for each matrix in data as a tensor
        of shape (...).
    """
    i1, i2 = {"x": (2, 1), "y": (0, 2), "z": (1, 0)}[axis]
    if horizontal:
        i2, i1 = i1, i2
    even = (axis + other_axis) in ["xy", "yz", "zx"]
    if isinstance(data, np.ndarray):
        if horizontal == even:
            return np.arctan2(data[..., i1], data[..., i2])
        if tait_bryan:
            return np.arctan2(-data[..., i2], data[..., i1])
        return np.arctan2(data[..., i2], -data[..., i1])
    elif isinstance(data, torch.Tensor):
        if horizontal == even:
            return torch.atan2(data[..., i1], data[..., i2])
        if tait_bryan:
            return torch.atan2(-data[..., i2], data[..., i1])
        return torch.atan2(data[..., i2], -data[..., i1])
    else:
        raise TypeError(f"data should be np.ndarray or torch.Tensor, but got {type(data)}")


def matrix_to_euler_angles(matrix, convention="xyz"):
    """
    Convert rotations given as rotation matrices to Euler angles in radians.

    Args:
        matrix: Rotation matrices with shape (..., 3, 3).
        convention: Convention string of 3/4 letters, e.g. "xyz", "sxyz", "rxyz", "exyz".
            If the length is 3, the extrinsic rotation is assumed.
            If the length is 4, the first character is "r/i" (rotating/intrinsic), or "s/e" (static / extrinsic).
            The remaining characters are the axis "x, y, z" in the order.

    Returns:
        Euler angles in radians with shape (..., 3).
    """
    convention = convention.lower()
    extrinsic = True
    if len(convention) != 3 and len(convention) != 4:
        raise ValueError(f"{convention} is not a valid convention")
    if len(convention) == 4:
        if convention[0] not in ["r", "i", "s", "e"]:
            raise ValueError(f"{convention[0]} is not a valid first character for a convention")
        extrinsic = convention[0] in ["s", "e"]
        convention = convention[1:]

    if not extrinsic:  # intrinsic
        convention = convention[::-1]  # reverse order

    i0 = _index_from_letter(convention[0])
    i2 = _index_from_letter(convention[2])
    tait_bryan = i0 != i2

    if isinstance(matrix, np.ndarray) or isinstance(matrix, list) or isinstance(matrix, tuple):
        matrix = np.asarray(matrix)
        if tait_bryan:
            central_angle = np.arcsin(matrix[..., i2, i0] * (-1.0 if i2 - i0 in [-1, 2] else 1.0))
        else:
            central_angle = np.arccos(matrix[..., i2, i2])

        angle3 = _angle_from_tan(convention[2], convention[1], matrix[..., i0], False, tait_bryan)
        angle1 = _angle_from_tan(convention[0], convention[1], matrix[..., i2, :], True, tait_bryan)
        if not extrinsic:
            angle1, angle3 = angle3, angle1
        return np.stack([angle1, central_angle, angle3], axis=-1)
    elif isinstance(matrix, torch.Tensor):
        if tait_bryan:
            central_angle = torch.asin(matrix[..., i2, i0] * (-1.0 if i2 - i0 in [-1, 2] else 1.0))
        else:
            central_angle = torch.acos(matrix[..., i2, i2])

        angle3 = _angle_from_tan(convention[2], convention[1], matrix[..., i0], False, tait_bryan)
        angle1 = _angle_from_tan(convention[0], convention[1], matrix[..., i2, :], True, tait_bryan)
        if not extrinsic:
            angle3, angle1 = angle1, angle3
        return torch.stack([angle1, central_angle, angle3], -1)
    else:
        raise TypeError(f"matrix should be np.ndarray, torch.Tensor, list or tuple, but got {type(matrix)}")


def _axis_angle_rotation(axis, angle):
    """
    Return the rotation matrices for one of the rotations about an axis
    of which Euler angles describe, for each value of the angle given.

    Args:
        axis: Axis label "x" or "y or "z".
        angle: Any shape tensor of Euler angles in radians

    Returns:
        Rotation matrices as tensor of shape (..., 3, 3).
    """
    if isinstance(angle, np.ndarray):
        cos = np.cos(angle)
        sin = np.sin(angle)
        one = np.ones_like(angle)
        zero = np.zeros_like(angle)
        if axis == "x":
            R_flat = (one, zero, zero, zero, cos, -sin, zero, sin, cos)
        elif axis == "y":
            R_flat = (cos, zero, sin, zero, one, zero, -sin, zero, cos)
        elif axis == "z":
            R_flat = (cos, -sin, zero, sin, cos, zero, zero, zero, one)
        else:
            raise ValueError("letter must be either X, Y or Z.")
        return np.stack(R_flat, -1).reshape(angle.shape + (3, 3))
    elif isinstance(angle, torch.Tensor):
        cos = torch.cos(angle)
        sin = torch.sin(angle)
        one = torch.ones_like(angle)
        zero = torch.zeros_like(angle)
        if axis == "x":
            R_flat = (one, zero, zero, zero, cos, -sin, zero, sin, cos)
        elif axis == "y":
            R_flat = (cos, zero, sin, zero, one, zero, -sin, zero, cos)
        elif axis == "z":
            R_flat = (cos, -sin, zero, sin, cos, zero, zero, zero, one)
        else:
            raise ValueError("letter must be either X, Y or Z.")
        return torch.stack(R_flat, -1).reshape(angle.shape + (3, 3))
    else:
        raise TypeError(f"angle should be np.ndarray or torch.Tensor, but got {type(angle)}")


def euler_angles_to_matrix(euler_angles, convention="xyz"):
    """
    Convert rotations given as Euler angles in radians to rotation matrices.

    Args:
        euler_angles: Euler angles in radians as tensor of shape (..., 3).
        convention: Convention string of 3/4 letters, e.g. "xyz", "sxyz", "rxyz", "exyz".
            If the length is 3, the extrinsic rotation is assumed.
            If the length is 4, the first character is "r/i" (rotating/intrinsic), or "s/e" (static / extrinsic).
            The remaining characters are the axis "x, y, z" in the order.

    Returns:
        Rotation matrices as tensor of shape (..., 3, 3).
    """
    convention = convention.lower()
    extrinsic = True
    if len(convention) != 3 and len(convention) != 4:
        raise ValueError(f"{convention} is not a valid convention")
    if len(convention) == 4:
        if convention[0] not in ["r", "i", "s", "e"]:
            raise ValueError(f"{convention[0]} is not a valid first character for a convention")
        extrinsic = convention[0] in ["s", "e"]
        convention = convention[1:]

    if isinstance(euler_angles, np.ndarray) or isinstance(euler_angles, list) or isinstance(euler_angles, tuple):
        euler_angles = np.asarray(euler_angles)
        matrices = [_axis_angle_rotation(c, euler_angles[..., i]) for i, c in enumerate(convention)]
        if extrinsic:
            return np.matmul(np.matmul(matrices[2], matrices[1]), matrices[0])
        else:  # intrinsic
            return np.matmul(np.matmul(matrices[0], matrices[1]), matrices[2])
    elif isinstance(euler_angles, torch.Tensor):
        matrices = [_axis_angle_rotation(c, e) for c, e in zip(convention, torch.unbind(euler_angles, -1))]
        if extrinsic:
            return torch.matmul(torch.matmul(matrices[2], matrices[1]), matrices[0])
        else:
            return torch.matmul(torch.matmul(matrices[0], matrices[1]), matrices[2])
    else:
        raise TypeError(f"euler_angles should be np.ndarray or torch.Tensor, but got {type(euler_angles)}")


def rotation_6d_to_matrix(d6):
    """
    Converts 6D rotation representation by Zhou et al. [1] to rotation matrix
    using Gram--Schmidt orthogonalization per Section B of [1].

    Args:
        d6: 6D rotation representation, of size (*, 6)
    Returns:
        batch of rotation matrices of size (*, 3, 3)
    [1] Zhou, Y., Barnes, C., Lu, J., Yang, J., & Li, H.
    On the Continuity of Rotation Representations in Neural Networks.
    IEEE Conference on Computer Vision and Pattern Recognition, 2019.
    Retrieved from http://arxiv.org/abs/1812.07035
    """
    a1, a2 = d6[..., :3], d6[..., 3:]
    b1 = F.normalize(a1, dim=-1)
    b2 = a2 - (b1 * a2).sum(-1, keepdim=True) * b1
    b2 = F.normalize(b2, dim=-1)
    b3 = torch.cross(b1, b2, dim=-1)
    return torch.stack((b1, b2, b3), dim=-2)


def matrix_to_rotation_6d(matrix):
    """
    Converts rotation matrices to 6D rotation representation by Zhou et al. [1]
    by dropping the last row. Note that 6D representation is not unique.

    Args:
        matrix: batch of rotation matrices of size (*, 3, 3)
    Returns:
        6D rotation representation, of size (*, 6)
    [1] Zhou, Y., Barnes, C., Lu, J., Yang, J., & Li, H.
    On the Continuity of Rotation Representations in Neural Networks.
    IEEE Conference on Computer Vision and Pattern Recognition, 2019.
    Retrieved from http://arxiv.org/abs/1812.07035
    """
    batch_dim = matrix.shape[:-2]
    if isinstance(matrix, np.ndarray):
        return matrix[..., :2, :].copy().reshape(batch_dim + (6,))
    else:
        return matrix[..., :2, :].clone().reshape(batch_dim + (6,))
