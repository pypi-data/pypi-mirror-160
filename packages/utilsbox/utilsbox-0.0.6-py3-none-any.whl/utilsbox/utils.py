from scipy.spatial import distance



def greet(name):
    """This function prints the string saying Hello to the name passed as argument.

    Args:
      name (str): The name of the person.

    Returns:
      None
    """
    print(f'Hello, {name}!')


def get_dist(pt1, pt2):
    """This function returns the distance between two points provided as argument.

    Args:
      pt1 (tuple): The tuple containing x, y coordinates of the first point.
      pt2 (tuple): The tuple containing x, y coordiantes of the second point.

    Returns:
      float: The distance between two points.
    """
    dist = distance.cdist((pt1,), (pt2,), 'euclidean')
    return dist[0][0]


class Rectangle:
    """This class contains the methods and attributes to get the information
    like area, perimeter etc from a rectangle which was created using the 
    height and width arguments passed to the constructor.

    Attributes:
      height (float): The height of the rectangle.
      width (float): The width of the rectangle.
    """
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def area(self):
        """This function returns the area of the rectangle.

        Returns:
          float: The area of the rectangle.
        """
        return self.height*self.width

    def perimeter(self):
        """This function returns the perimeter of the rectangle.

        Returns:
          float: The perimeter of the rectangle.
        """
        return 2*(self.height+self.width)



# def get_arrow_coords(img):
#     _, img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)
#     labels, stats = cv2.connectedComponentsWithStats(img, 8)[1:3]

#     # for label in np.unique(labels)[1:]:
#     arrow = labels == np.unique(labels)[1:][0]
#     indices = np.transpose(np.nonzero(arrow))  # y,x
#     dist = distance.cdist(indices, indices, "euclidean")

#     far_points_index = np.unravel_index(np.argmax(dist), dist.shape)  # y,x

#     far_point_1 = indices[far_points_index[0], :]  # y,x
#     far_point_2 = indices[far_points_index[1], :]  # y,x

#     ### Slope
#     arrow_slope = (far_point_2[0] - far_point_1[0]) / (far_point_2[1] - far_point_1[1])
#     arrow_angle = math.degrees(math.atan(arrow_slope))

#     ### Length
#     arrow_length = distance.cdist(
#         far_point_1.reshape(1, 2),
#         far_point_2.reshape(1, 2),
#         "euclidean",
#     )[0][0]

#     ### Thickness
#     x = np.linspace(far_point_1[1], far_point_2[1], 20)
#     y = np.linspace(far_point_1[0], far_point_2[0], 20)
#     line = np.array([[yy, xx] for yy, xx in zip(y, x)])

#     x1, y1 = tuple(line[-1][::-1].astype(int))
#     x2, y2 = tuple(line[0][::-1].astype(int))

#     return x1, y1, x2, y2
