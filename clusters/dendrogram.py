from PIL import Image, ImageDraw


def get_height(clust):
    # Is this an endpoint? Then the height is just 1
    if not clust.left and not clust.right:
        return 1

    # Otherwise the height is the same of the heights of each branch
    return get_height(clust.left) + get_height(clust.right)


def get_depth(clust):
    # The distance of an endpoint is 0.0
    if not clust.left and not clust.right:
        return 0.0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg="clusters.jpg"):
    # Height and width
    h = get_height(clust) * 20
    w = 1200
    depth = get_depth(clust)

    # width is fixed, so scale distances accordingly
    scaling = float(w - 150) / depth

    # Create a new image with a white background
    img = Image.new("RGB", (w,h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))
    
    # Draw the nodes recursively
    draw_node(draw, clust, 10, (h/2), scaling, labels)
    img.save(jpeg, "JPEG")

    
def draw_node(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = get_height(clust.left) * 20
        h2 = get_height(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        
        # Line length
        ll = clust.distance * scaling

        # Vertical line from this cluster to children
        draw.line((x, top+h1/2, x, bottom - h2/2), fill=(255, 0, 0))

        # Horizontal line to left item
        draw.line((x, top+h1/2, x + ll, top + h1/2), fill=(255, 0, 0))

        # Horizontal line to right item
        draw.line((x, bottom-h2/2, x+ll, bottom-h2/2), fill=(255,0,0))

        # Call the function to draw the left and right nodes
        draw_node(draw, clust.left, x+ll, top+h1/2, scaling, labels)
        draw_node(draw, clust.right, x+ll, bottom-h2/2, scaling, labels)

        # if this is an endpoint, draw the item label
    else:
        draw.text((x+5, y-7), labels[clust.id], (0,0,0))

