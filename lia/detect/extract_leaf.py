"""Extract leaf from an image."""

from .sort_hsv_cnts import sort_hsv_cnts
from .get_center_object import get_center_object
from .get_diff_ellipse import get_diff_ellipse

def extract_leaf(img, thresh=30):
    """Get contours of leaf candidate.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.
    thresh : int, (default: 30)
        Threshold to get contours.

    Returns
    -------
    leaf_candidates: list
        Contours list of leaf candidate.

    Raises
    ------
    ValueError
        If there are no centered contours.
    ValueError
        If leaf shape contours could not be detected.
    """    
    
    # Sort H, S, and V in order of clarity of leaf outline, and find contours from each
    try:
        cnts_list = sort_hsv_cnts(img, thresh)
    except:
        raise
    # Get most centered contour.
    center_cnt_list = []
    for cnts in cnts_list:
        try:
            center_cnt = get_center_object(img, cnts)
        except:
            continue
        else:
            center_cnt_list.append(center_cnt)
    # Whether contour is leaf or not.
    if len(center_cnt_list) == 0:
        raise ValueError('There are no centered contours.')
    leaf_candidates = []
    for cnt in center_cnt_list:
        try:
            diff_ellipse = get_diff_ellipse(img, cnt)
        except:
            continue
        else:
            leaf_candidates.append(cnt)
    if len(leaf_candidates) == 0:
        raise ValueError('Leaf shape contours could not be detected.')
    return leaf_candidates