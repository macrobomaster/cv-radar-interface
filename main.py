from radar import Radar
import cv2


# Returns the same list of points, but in this order:
# Bottom Right, Bottom Left, Top left, Top right
def order_points(rect: list[list[float]]) -> list[list[int]]:
    points = rect.copy()
    points.sort(key=lambda x: x[1])

    if points[0][0] < points[1][0]:
        bottom_left = points[0]
        bottom_right = points[1]
    else:
        bottom_left = points[1]
        bottom_right = points[0]

    if points[2][0] < points[3][0]:
        top_left = points[2]
        top_right = points[3]
    else:
        top_left = points[3]
        top_right = points[2]

    return [bottom_right, bottom_left, top_left, top_right]


def select_corner(event, x, y, flags, param):
    img = param[0]
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 10, (255, 255, 0), -1)
        param[1].append([x, y])


def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param[1].clear()
        param[1].append(x)
        param[1].append(y)


def main():
    img_path = r"sample_image.jpg"
    window_name = "Sample Image"
    arena_corners = []

    img = cv2.imread(img_path)
    img = cv2.resize(img, (int(img.shape[1] / 3), int(img.shape[0] / 3)))
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, select_corner, [img, arena_corners])

    while len(arena_corners) < 4:
        cv2.imshow(window_name, img)
        print(arena_corners)

        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    arena_corners = order_points(arena_corners)

    cv2.line(img, arena_corners[0], arena_corners[1], (255, 255, 0), 2, -1)
    cv2.line(img, arena_corners[1], arena_corners[2], (255, 255, 0), 2, -1)
    cv2.line(img, arena_corners[2], arena_corners[3], (255, 255, 0), 2, -1)
    cv2.line(img, arena_corners[3], arena_corners[0], (255, 255, 0), 2, -1)

    radar = Radar(arena_corners, 100, 100)

    xy = []

    cv2.setMouseCallback(window_name, select_point, [img, xy])


    while True:
        cv2.imshow(window_name, img)

        #! CAN DELETE LATER
        if xy:
            print(f"Clicked point: {xy}")
            print(f"Transformed point: {radar.transform(xy)}")
            xy.clear()

        if cv2.waitKey(1) == 27: #'Esc' key
            break


    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
