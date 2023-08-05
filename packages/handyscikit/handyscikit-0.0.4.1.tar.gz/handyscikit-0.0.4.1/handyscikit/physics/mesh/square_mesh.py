"""
Make a square mesh topology.
* Index rule.
    (0, H)-------------------(L, H)
      |                         |
      |                         |
      |                         |
      |                         |
      |                         |
    (0, 0)-------------------(L, 0)
"""
from .abstract_mesh import AbstractMesh
import math
import numpy as np
import time
# todo: Check if there is unallocate boundary.


class SquareMeshBase(AbstractMesh):
    def __init__(self, size, segment_num, float_dtype):
        node_num = (segment_num[0] + 1) * (segment_num[1] + 1)
        face_num = segment_num[0] * (segment_num[1] + 1) + segment_num[1] * (segment_num[0] + 1)
        cell_num = segment_num[0] * segment_num[1]
        AbstractMesh.__init__(self, "square", node_num, face_num, cell_num, float_dtype)

        self._segment_num = segment_num
        self._size = size
        self._boundary_condition_setting_list = [0 for i in range(4)]

        self._generate()
        spend_time = time.time() - self._time_start
        self._print_mesh_info("Meshing finished, spend time %fs."%(spend_time))

    def _cal_cell_cell(self):
        index = 0
        for j in range(self._segment_num[1]):
            for i in range(self._segment_num[0]):
                self._cell_cell[index][0] = self.__cell_index(i, j+1)
                self._cell_cell[index][1] = self.__cell_index(i+1, j)
                self._cell_cell[index][2] = self.__cell_index(i, j-1)
                self._cell_cell[index][3] = self.__cell_index(i-1, j)
                index += 1

    def _cal_cell_coord(self):
        for i in range(self._cell_num):
            for j in range(self._node_per_cell):
                self._cell_coord[i] += self._nodes[self._cells[i][j]]
            self._cell_coord[i] /= self._node_per_cell

    def _cal_cell_face(self):
        search = np.zeros([self._node_num, self._node_num], dtype=np.int32)

        for i in range(self._face_num):
            if self._faces[i, 0] < self._faces[i, 1]:
                search[self._faces[i, 0], self._faces[i, 1]] = i
            else:
                search[self._faces[i, 1], self._faces[i, 0]] = i

        for i in range(self._cell_num):
            for j in range(self._face_per_cell):
                tmp = j + 1 if j < self._face_per_cell - 1 else 0
                if self._cells[i, j] < self._cells[i, tmp]:
                    self._cell_face[i, j] = search[self._cells[i, j], self._cells[i, tmp]]
                else:
                    self._cell_face[i, j] = search[self._cells[i, tmp], self._cells[i, j]]

    def _cal_cell_volume(self):
        for i in range(self._cell_num):
            vector_0 = self._nodes[self._cells[i][0]] - self._nodes[self._cells[i][1]]
            vector_1 = self._nodes[self._cells[i][0]] - self._nodes[self._cells[i][3]]
            self._cell_volume[i] = abs(np.cross(vector_0, vector_1))

    def _cal_cells(self):
        index = 0
        for j in range(self._segment_num[1]):
            for i in range(self._segment_num[0]):
                self._cells[index][0] = self.__node_index(i, j)
                self._cells[index][1] = self.__node_index(i, j + 1)
                self._cells[index][2] = self.__node_index(i + 1, j + 1)
                self._cells[index][3] = self.__node_index(i + 1, j)
                index += 1

    def _cal_face_cell(self):
        for i in range(self._cell_num):
            for j in range(self._face_per_cell):
                if self._face_cell[self._cell_face[i, j], 0] == -1:
                    self._face_cell[self._cell_face[i, j], 0] = i
                else:
                    self._face_cell[self._cell_face[i, j], 1] = i

    def _cal_face_center(self):
        for i in range(self._face_num):
            self._face_center[i] = (self._nodes[self._faces[i,0]] + self._nodes[self._faces[i,1]])/2

    def _cal_face_length(self):
        for i in range(self._face_num):
            self._face_length[i] = np.linalg.norm(self._nodes[self._faces[i,0]] - self._nodes[self._faces[i,1]])

    def _cal_face_mark(self):
        """
        Left(1) | Up(2) | Right(3) | Down(4)
        :return:
        """
        for j in range(self._segment_num[1] + 1):
            for i in range(self._segment_num[1]):
                index = self.__horizontal_face_index(i, j)
                if j == 0:
                    self._face_mark[index] = 4
                elif j == self._segment_num[1]:
                    self._face_mark[index] = 2
                else:
                    self._face_mark[index] = 0

        for i in range(self._segment_num[0] + 1):
            for j in range(self._segment_num[1]):
                index = self.__vertical_face_index(i, j)
                if i == 0:
                    self._face_mark[index] = 1
                elif i == self._segment_num[0]:
                    self._face_mark[index] = 3
                else:
                    self._face_mark[index] = 0

    def _cal_face_norm(self):
        for i in range(self._face_num):
            x0 = self._nodes[self._faces[i, 0]][0]
            y0 = self._nodes[self._faces[i, 0]][1]
            x1 = self._nodes[self._faces[i, 1]][0]
            y1 = self._nodes[self._faces[i, 1]][1]

            if abs(x0 - x1) < 1e-15:
                self._face_norm[i][0] = 1
            elif abs(y0 - y1) < 1e-15:
                self._face_norm[i][1] = 1
            else:
                tmp = (x0 - x1)/(y1 - y0)
                self._face_norm[i][0] = 1/(1 + tmp**2)**0.5
                self._face_norm[i][1] = tmp/(1 + tmp**2)**0.5
            vector = self._cell_coord[self._face_cell[i, 0]] - (self._nodes[self._faces[i, 0]] + self._nodes[self._faces[i, 1]])/2
            if np.dot(self._face_norm[i], vector) > 0:
                self._face_norm[i] *= -1

    def _cal_faces(self):
        index = 0
        for j in range(self._segment_num[1] + 1):
            for i in range(self._segment_num[0]):
                self._faces[index][0] = self.__node_index(i, j)
                self._faces[index][1] = self.__node_index(i + 1, j)
                index += 1

        for i in range(self._segment_num[0] + 1):
            for j in range(self._segment_num[1]):
                self._faces[index][0] = self.__node_index(i, j)
                self._faces[index][1] = self.__node_index(i, j + 1)
                index += 1

    def _cal_nodes(self):
        """
        Outer loop change row(j), inner loop change column(i).
        :return:
        """
        delta_x = self._size[0]/self._segment_num[0]
        delta_y = self._size[1]/self._segment_num[1]
        index = 0
        for j in range(self._segment_num[1] + 1):
            for i in range(self._segment_num[0] + 1):
                self._nodes[index][0] = delta_x*i
                self._nodes[index][1] = delta_y*j
                index += 1

    def __cell_index(self, i, j):
        return -1 if i<0 or i>=self._segment_num[0] or j<0 or j>=self._segment_num[1] else self._segment_num[0]*j + i

    def __node_index(self, i, j):
        return (self._segment_num[0] + 1)*j + i

    def __horizontal_face_index(self, i, j):
        return self._segment_num[0]*j + i

    def __vertical_face_index(self, i, j):
        return (self._segment_num[1] + 1)*self._segment_num[0] + i*self._segment_num[1] + j


class SquareMesh(SquareMeshBase):
    def __init__(self, size, segment_num, float_dtype=np.float64):
        SquareMeshBase.__init__(self, size, segment_num, float_dtype)

    @property
    def boundary_down(self):
        return 4

    @property
    def boundary_left(self):
        return 1

    @property
    def boundary_right(self):
        return 3

    @property
    def boundary_up(self):
        return 2

    @property
    def segment_num(self):
        return self._segment_num

    @property
    def size(self):
        return self._size

    def set_dirichlet_boundary(self, boundary_mark, value):
        """
        Set dirichely condition for boundary.
        :param boundary: Boundary mark(Can use prperty function).
        :param value: Boundary value.
        :return:
        """
        # todo: type check.
        for i in range(self._face_num):
            if self._face_mark[i] == boundary_mark:
                self._face_type[i, 0] = 1
                self._face_type[i, 1] = value
                self._face_type[i, 2] = 0

        # Remember this boundary has been set condition.
        self._boundary_condition_setting_list[boundary_mark-1] = 1

    def set_dirichlet_cos_boundary(self, boundary_mark):
        # todo: [Corner condition] Cos boundary is horizontal.
        for i in range(self._face_num):
            if self._face_mark[i] in boundary_mark:
                self._face_type[i, 0] = 1
                self._face_type[i, 1] = math.cos(self._face_center[i, 0]*360/self._size[0]*math.pi/180)
                self._face_type[i, 2] = 0

        # Remember this boundary has been set condition.
        for mark in boundary_mark:
            self._boundary_condition_setting_list[mark-1] = 1

    def set_periodic_boundary(self, boundary_mark_pair):
        """
        Set periodic condition for boundary.
        Param: Boundary type | Adjacent face | Adjacent cell.
        :param boundary_mark_pair: Boundary mark(Can use p_roperty function).
        :return:
        """
        for i in range(self._face_num):
            if self._face_mark[i] == boundary_mark_pair[0]:
                for j in range(self._face_num):
                    if self._face_mark[j] == boundary_mark_pair[1] and abs(self._face_center[j][1] - self._face_center[i][1])<1e-15:
                        self._face_type[i, 0] = 4
                        self._face_type[i, 1] = j
                        self._face_type[i, 2] = self._face_cell[j, 0]
                        self._face_type[j, 0] = 4
                        self._face_type[j, 1] = i
                        self._face_type[j, 2] = self._face_cell[i, 0]

        # Remember this boundary has been set condition.
        self._boundary_condition_setting_list[boundary_mark_pair[0]-1] = 1
        self._boundary_condition_setting_list[boundary_mark_pair[1]-1] = 1
