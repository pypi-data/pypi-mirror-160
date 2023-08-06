import torch as T
import os
import cv2
import numpy as np


class KimEye(T.utils.data.Dataset):
    """KimEye dataset for multi-class Glaucoma grading.  There are three
    classes, and we assigned each a number:

    No Glaucoma: 0,
    Early Glaucoma: 1,
    Advanced Glaucoma: 2

    The fundus images are cropped to the optic disk and have size 240x240.
    """

    CLASS_DISTRIBUTION = [788, 289, 467]
    CLASS_NAMES = ['No_Glaucoma', 'Early_Glaucoma', 'Advanced_Glaucoma']
    CLASS_LABELS = [0, 1, 2]

    def __init__(self, base_dir=os.environ.get('kimeye_dir', './data/kim_eye')):
        """
        """
        super().__init__()
        fps_normal = [(f'{base_dir}/normal_control/{x}.png', 0)
                      for x in range(1, 788+1)]
        fps_early = [(f'{base_dir}/early_glaucoma/{x}.png', 1)
                     for x in range(1, 289+1)]
        fps_adv = [(f'{base_dir}/advanced_glaucoma/{x}.png', 2)
                   for x in range(1, 467+1)]
        self.fps = fps_normal + fps_early + fps_adv
        self.labels = np.array([x[1] for x in self.fps])

    def __len__(self):
        return len(self.fps)

    def __getitem__(self, idx):
        fp, label = self.fps[idx]
        im = cv2.imread(fp, cv2.IMREAD_COLOR)
        assert im is not None, f'Image not found: {fp}'
        im = im[:, :, ::-1].copy()  # bgr to rgb
        return {'image': im, 'fp': fp, 'label': label}


if __name__ == '__main__':
    dset = KimEye()
    assert len(dset) == 1544

    for x in dset:
        print(x['image'].shape) if x['image'].shape != (240,240,3) else None
        pass  # check all images exist
