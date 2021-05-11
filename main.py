#################################################
# Desain dan Analisis Algoritma                 #
# Quick Hull - Pemecahan masalah Convex Hull    #
# dengan pendekatan Divide and Conquer          #
#                                               #
# github.com/hifra01                            #
# ###############################################

from collections import namedtuple
from operator import attrgetter
from math import atan2
from matplotlib import pyplot as plt
from random import randint
from time import time

Point = namedtuple("Point", 'x y')


class QuickHull:
    points = []
    hull_points = []
    max_x = 0
    max_y = 0

    def __init__(self):
        pass

    def sort_hull_points_by_angle(self, points, hull_points):
        """
        Hull points perlu diurutkan secara melingkar agar garis yang terbentuk juga melingkar seperti semestinya.
        Metode yang digunakan adalah dengan menggunakan fungsi atan2 (https://en.wikipedia.org/wiki/Atan2) dengan
        titik pusat didapat dari rata-rata x dan y.
        """
        x = y = 0
        for point in points:
            x += point[0]
            y += point[1]
        points_length = len(points)
        center = Point(x / points_length, y / points_length)

        hull_points.sort(key=lambda hull_point: (atan2(hull_point[1] - center[1], hull_point[0] - center[0])))
        return hull_points

    def find_determinant(self, leftmost: Point, rightmost: Point, point: Point):
        """
        Jika a(x1, y1), b(x2, y2), dan c(x3, y3) adalah tiga titik arbitrer pada bidang
        Kartesian, maka luas segitiga abc adalah setengah dari determinannya. Hasil determinan akan selalu positif jika
        dan hanya jika c berada di sisi kiri garis ab. Semakin besar determinan, semakin tinggi jarak c dari garis ab.
        Fungsi ini dapat dimanfaatkan untuk mencari letak titik terhadap sebuah garis, sekaligus mencari skor
        ketinggiannya.
        """
        x1, y1 = leftmost
        x2, y2 = rightmost
        x3, y3 = point

        result = (x1 * y2) + (x3 * y1) + (x2 * y3) - (x3 * y2) - (x2 * y1) - (x1 * y3)
        return result

    def add_point(self, point: Point):
        """
        Menambahkan titik pada bidang. Titik harus menggunakan tipe data Point(x, y)
        """
        self.points.append(point)
        self.points.sort(key=attrgetter('x', 'y'))
        self.max_x = max(self.points, key=attrgetter('x'))[0]
        self.max_y = max(self.points, key=attrgetter('y'))[1]

    def find_hull(self, points, leftmost, rightmost):
        # # For visualization purpose, comment to turn off
        # left_x = leftmost[0]
        # left_y = leftmost[1]
        # right_x = rightmost[0]
        # right_y = rightmost[1]
        # line_x = [left_x, right_x]
        # line_y = [left_y, right_y]
        # plt.plot(line_x, line_y, 'gD-')
        # plt.savefig(f'image/{time():.10f}.png', dpi=96)
        # # End of visualization purpose

        if len(points) <= 1:
            return points
        else:
            highest_point = None
            list_of_hull = []
            current_max_determinant = -1
            for point in points:
                point_determinant = self.find_determinant(leftmost, rightmost, point)
                if point_determinant > current_max_determinant:
                    current_max_determinant = point_determinant
                    highest_point = point
                    list_of_hull = [point]
                elif point_determinant == current_max_determinant:
                    list_of_hull.append(point)

            left_points = []
            right_points = []

            for point in points:
                if point not in list_of_hull:
                    left_determinant = self.find_determinant(leftmost, highest_point, point)
                    right_determinant = self.find_determinant(highest_point, rightmost, point)

                    if left_determinant > 0:
                        left_points.append(point)
                    elif right_determinant > 0:
                        right_points.append(point)

            left_hull = self.find_hull(left_points, leftmost, highest_point)
            right_hull = self.find_hull(right_points, highest_point, rightmost)
            result = list_of_hull + left_hull + right_hull

            return result

    def solve(self):
        # For visualization purpose
        start_point_x, start_point_y = [x for x in zip(*self.points)]
        plt.plot(start_point_x, start_point_y, 'ko')
        # plt.savefig(f'image/{time():.10f}.png', dpi=96)
        # End of visualization purpose

        start_time = time()
        print(f"Solving...")
        leftmost = self.points[0]  # Ambil titik paling kiri dari kumpulan titik
        rightmost = self.points[-1]  # Ambil titik paling kanan dari kumpulan titik

        top_points = []  # Siapkan list penampung titik yang berada di atas garis
        bottom_points = []  # Siapkan list penampung titik yang berada di bawah garis

        for point in self.points:
            if point != leftmost or point != rightmost:
                top_determinant = self.find_determinant(leftmost, rightmost,
                                                        point)  # Bernilai > 0 jika titik berada di atas garis
                bottom_determinant = self.find_determinant(rightmost, leftmost,
                                                           point)  # Bernilai > 0 jika titik berada di bawah garis

                # Jika sejajar dengan garis, maka nilai skor = 0

                if top_determinant > 0:
                    top_points.append(point)
                if bottom_determinant > 0:
                    bottom_points.append(point)

        top_hull = self.find_hull(top_points, leftmost, rightmost)  # Titik2 CH yang berada di atas garis
        bottom_hull = self.find_hull(bottom_points, rightmost, leftmost)  # Titik2 CH yang berada di bawah garis

        self.hull_points = [leftmost] + top_hull + bottom_hull + [rightmost]
        self.hull_points = self.sort_hull_points_by_angle(self.points, self.hull_points)

        print()
        print("Convex Hull Points:")
        for point in self.hull_points:
            print(point)

        # For visualization purpose
        self.hull_points.append(self.hull_points[0])

        hull_x, hull_y = [x for x in zip(*self.hull_points)]
        # plt.clf()
        plt.plot(start_point_x, start_point_y, 'ko')
        plt.plot(hull_x, hull_y, 'gD-')
        # plt.savefig(f'image/{time():.10f}.png', dpi=96)
        plt.show()
        # End of visualization purpose

        print(f"Solved in {time() - start_time} seconds.")


if __name__ == '__main__':
    quick_hull = QuickHull()

    # quick_hull.add_point(Point(1, 3))
    # quick_hull.add_point(Point(1, 5))
    # quick_hull.add_point(Point(2, 4))
    # quick_hull.add_point(Point(2, 1))
    # quick_hull.add_point(Point(3, 2))
    # quick_hull.add_point(Point(4, 4))
    # quick_hull.add_point(Point(5, 1))

    for i in range(20):
        x = randint(0, 100)
        y = randint(0, 100)
        quick_hull.add_point(Point(x, y))

    quick_hull.solve()
