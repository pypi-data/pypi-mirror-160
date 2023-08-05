import os
import cv2
import glob


def addExt(path: str, ext: str) -> str:
    """
    Add ext to path

    :param path: Path to file
    :param ext: Added ext
    :rtype: str
    :return: Path with added ext
    """

    pathExt = os.path.splitext(path)
    return pathExt[0] + '.' + ext + pathExt[1]


def compareFrames(framePath_1: str, framePath_2: str) -> bool:
    """
    Compare 2 frames

    :param framePath_1: Path to frame 1
    :param framePath_2: Path to frame 2
    :return: bool
    """

    # TODO: Check different frames size

    frame_1 = cv2.imread(framePath_1)
    frame_2 = cv2.imread(framePath_2)
    diff = cv2.norm(frame_1, frame_2, cv2.NORM_L2)

    if diff == 0.0:
        return True

    return False


def delExt(path: str, extCount: int = 1) -> str:
    """
    Del ext from path

    :param path: Path to file
    :param extCount: Count of deleted ext
    :rtype: str
    :return: Path without ext
    """

    pathNoExt = path
    for _ in range(extCount):
        pathNoExt = os.path.splitext(pathNoExt)[0]

    return pathNoExt


def templatedRemoveFiles(template: str) -> None:
    """
    Remove files by template

    :param template: Template
    :return: None
    """

    removeFiles = glob.iglob(template)

    for _file in removeFiles:
        os.remove(_file)


def getExt(path: str, extCount: int = 1) -> str:
    """
    Return file extension from path

    :param path: Path to file
    :param extCount: Count of returned extension
    :rtype: str
    :return: Extension
    """

    pathNoExt = path
    lastExt = ''
    for _ in range(extCount):
        splitPath = os.path.splitext(pathNoExt)
        pathNoExt = splitPath[0]
        lastExt = splitPath[1]

    if lastExt != '':
        # Del .
        lastExt = lastExt[1:]

    return lastExt
