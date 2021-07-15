from functools import cached_property
from pydantic import BaseModel

import numpy as np

from .polyline import Polyline
from .position import Position

__all__ = ['Polyline', 'Position', 'BBXCornersClass']


def rot_x(x, y, phi):
    return x * np.cos(phi) - y * np.sin(phi)


def rot_y(x, y, phi):
    return x * np.sin(phi) + y * np.cos(phi)


def rot_point(orig_x, orig_y, x, y, phi):
    return np.array([orig_x + rot_x(x, y, phi), orig_y + rot_y(x, y, phi)])


class BBXCornersClass:

    @cached_property
    def _center2frontcenter2left(self):
        try:
            heading = self.tr.heading / 180 * np.pi
            x = self.tr.pos_x
            y = self.tr.pos_y
        except AttributeError as e:
            try:
                heading = self.heading / 180 * np.pi
                x = self.position.pos_x
                y = self.position.pos_y
            except AttributeError as ee:
                raise AttributeError('Object must either have property Trajectory or position') from (e, ee)
        c2f = self.length / 2
        c2l = self.width / 2
        return x, y, heading, c2f, c2l

    @cached_property
    def front_left(self):
        x, y, heading, c2f, c2l = self._center2frontcenter2left
        return rot_point(x, y, +c2f, +c2l, heading)

    @cached_property
    def front_right(self):
        x, y, heading, c2f, c2l = self._center2frontcenter2left
        return rot_point(x, y, +c2f, -c2l, heading)

    @cached_property
    def back_right(self):
        x, y, heading, c2f, c2l = self._center2frontcenter2left
        return rot_point(x, y, -c2f, -c2l, heading)

    @cached_property
    def back_left(self):
        x, y, heading, c2f, c2l = self._center2frontcenter2left
        return rot_point(x, y, -c2f, +c2l, heading)
