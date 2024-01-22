from radar import Radar
import cv2


#! Click points in this order:
#! Top Left, Top Right, Bottom Right, Bottom Left
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
    img_path = r"sample_images\keyboard\keyboard1.jpg"
    ref_img_path = r"sample_images\keyboard\keyboard0.jpg"

    window_name = "Sample Image"
    ref_window_name = "Reference Image"

    arena_corners = []
    ref_arena_corners = []

    img = cv2.imread(img_path)
    ref_img = cv2.imread(ref_img_path)
    img = cv2.resize(img, (int(img.shape[1] / 3), int(img.shape[0] / 3)))
    ref_img = cv2.resize(
        ref_img, (int(ref_img.shape[1] / 3), int(ref_img.shape[0] / 3))
    )

    cv2.namedWindow(window_name)
    cv2.namedWindow(ref_window_name)
    cv2.setMouseCallback(window_name, select_corner, [img, arena_corners])
    cv2.setMouseCallback(ref_window_name, select_corner, [ref_img, ref_arena_corners])

    while len(arena_corners) < 4:
        cv2.imshow(window_name, img)

        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    print(
        f"TL: {arena_corners[0]} \nTR: {arena_corners[1]} \nBR: {arena_corners[2]} \nBL: {arena_corners[3]}"
    )

    cv2.line(img, arena_corners[0], arena_corners[1], (255, 255, 0), 2, -1)
    cv2.line(img, arena_corners[1], arena_corners[2], (255, 255, 0), 2, -1)
    cv2.line(img, arena_corners[2], arena_corners[3], (255, 255, 0), 2, -1)
    cv2.line(img, arena_corners[3], arena_corners[0], (255, 255, 0), 2, -1)
    cv2.imshow(window_name, img)

    while len(ref_arena_corners) < 4:
        cv2.imshow(ref_window_name, ref_img)

        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    print(
        f"TL: {ref_arena_corners[0]} \nTR: {ref_arena_corners[1]} \nBR: {ref_arena_corners[2]} \nBL: {ref_arena_corners[3]}"
    )

    cv2.line(ref_img, ref_arena_corners[0], ref_arena_corners[1], (255, 255, 0), 2, -1)
    cv2.line(ref_img, ref_arena_corners[1], ref_arena_corners[2], (255, 255, 0), 2, -1)
    cv2.line(ref_img, ref_arena_corners[2], ref_arena_corners[3], (255, 255, 0), 2, -1)
    cv2.line(ref_img, ref_arena_corners[3], ref_arena_corners[0], (255, 255, 0), 2, -1)
    radar = Radar(arena_corners, ref_arena_corners)

    xy = []

    cv2.setMouseCallback(window_name, select_point, [img, xy])
    cv2.setMouseCallback(ref_window_name, lambda *args: None)

    while True:
        cv2.imshow(window_name, img)
        cv2.imshow(ref_window_name, ref_img)

        #! Data display
        if xy:
            print(f"Clicked point: {xy}")
            transform = radar.transform(xy)
            print(f"Transformed point: {transform}")
            cv2.circle(img, (xy[0], xy[1]), 3, (255, 255, 0), -1)
            cv2.circle(
                ref_img,
                (int(transform[0][0][0]), int(transform[0][0][1])),
                3,
                (255, 255, 0),
                -1,
            )
            xy.clear()

        if cv2.waitKey(1) == 27:  #'Esc' key
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
