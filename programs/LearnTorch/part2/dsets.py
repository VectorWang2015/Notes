import copy
import functools
import glob
import os
import csv

import SimpleITK as sitk
import numpy as np

import torch
import torch.cuda
from torch.utils.data import Dataset

from collections import namedtuple

from util.util import XyzTuple, xyz2irc


data_path = "D:\\LUNA16\\"
csv_path = "D:\\LUNA16\\CSVFILES\\"

CandidateInfoTuple = namedtuple(
        'CandidateInfoTuple',
        'isNodule_bool, diameter_mm, series_uid, center_xyz',
)


# caching params/result
@functools.lru_cache(1)
def getCandidateInfoList(requireOnDisk_bool = True):
    mhd_list = glob.glob(os.path.join(data_path,'subset*/*.mhd'))
    presentOnDisk_set = {os.path.split(p)[-1][:-4] for p in mhd_list}

    diameter_dict = {}
    with open(os.path.join(csv_path, 'annotations.csv'), 'r') as f:
        for row in list(csv.reader(f))[1:]:     # ignore row 0 as is header
            series_uid = row[0]
            annotationCenter_xyz = tuple([float(x) for x in row[1:4]])
            annotationDiameter_mm = float(row[4])
            diameter_dict.setdefault(series_uid, []).append(
                    (annotationCenter_xyz, annotationDiameter_mm)
            )

    CandidateInfo_list = []
    # center xyz may vary in annotation.csv and candidate.csv
    # accept diameter if delta is acceptable (max < diameter/4)
    with open(os.path.join(csv_path, 'candidates.csv'), 'r') as f:
        for row in list(csv.reader(f))[1:]:
            series_uid = row[0]

            if series_uid not in presentOnDisk_set and requireOnDisk_bool:
                continue

            candidateCenter_xyz = tuple([float(x) for x in row[1:4]])
            isNodule_bool = bool(int(row[4]))

            candidateDiameter_mm = 0.0
            for annotation_tup in diameter_dict.get(series_uid, []):
                annotationCenter_xyz, annotationDiameter_mm = annotation_tup
                deltaCenter_xyz = [abs(candidateCenter_xyz[i] - annotationCenter_xyz[i])
                        for i in range(3)]
                if max(deltaCenter_xyz) <= annotationDiameter_mm / 4:
                    candidateDiameter_mm = annotationDiameter_mm
                    break

            CandidateInfo_list.append(CandidateInfoTuple(
                isNodule_bool,
                candidateDiameter_mm,
                series_uid,
                candidateCenter_xyz,
            ))

        CandidateInfo_list.sort(reverse=True)
        return CandidateInfo_list


class Ct:
    def __init__(self, series_uid):
        mhd_path = glob.glob(
                os.path.join(data_path, 'subset*/{}.mhd'.format(series_uid)))[0]
        ct_mhd = sitk.ReadImage(mhd_path)
        ct_a = np.array(sitk.GetArrayFromImage(ct_mhd), dtype=np.float32)

        # min, max, out
        ct_a.clip(-1000, 1000, ct_a)

        self.series_uid = series_uid
        self.hu_a = ct_a

        self.origin_xyz = XyzTuple(*ct_mhd.GetOrigin())
        self.vxSize_xyz = XyzTuple(*ct_mhd.GetSpacing())
        self.direction_a = np.array(ct_mhd.GetDirection()).reshape(3,3)

    def getRawCandidate(self, center_xyz, width_irc):
        center_irc = xyz2irc(
                center_xyz,
                self.origin_xyz,
                self.vxSize_xyz,
                self.direction_a,
        )

        slice_list = []
        for axis, center_val in enumerate(center_irc):
            start_ndx = int(round(center_val - width_irc[axis]/2))
            end_ndx = int(start_ndx + width_irc[axis])

            # exception handling
            assert center_val >= 0 and center_val < self.hu_a.shape[axis]
            if start_ndx < 0:
                start_ndx = 0
                end_ndx = int(width_irc[axis])

            if end_ndx > self.hu_a.shape[axis]:
                end_ndx = self.hu_a.shape[axis]
                start_ndx = int(self.hu_a.shape[axis] - width_irc[axis])

            slice_list.append(slice(start_ndx, end_ndx))

        ct_chunk = self.hu_a[tuple(slice_list)]

        return ct_chunk, center_irc


class LunaDataset(Dataset):
    def __init__(self,
            val_stride=0,
            isValSet_bool=None,
            series_uid=None
            ):
        self.candidateInfo_list = copy.copy(getCandidateInfoList())

        if series_uid:
            self.candidateInfo_list = [
                    x for x in self.candidateInfo_list if x.series_uid == series_uid
            ]

        if isValSet_bool:
            assert val_stride > 0, val_stride
            self.candidateInfo_list = self.candidateInfo_list[::val_stride]
        elif val_stride > 0:
            del self.candidateInfo_list[::val_stride]
            assert self.candidateInfo_list

    def __len__(self):
        return len(self.candidateInfo_list)

    def __getitem__(self, ndx):
        candidateInfo_tup = self.candidateInfo_list[ndx]
        width_irc = (32, 48, 48)

        candidate_a, center_irc = getCtRawCandidate(
                candidateInfo_tup.series_uid,
                candidateInfo_tup.center_xyz,
                width_irc,
            )

        candidate_t = torch.from_numpy(candidate_a)
        candidate_t = candidate_t.to(torch.float32)
        candidate_t = candidate_t.unsqueeze(0)

        pos_t = torch.tensor([
            not candidateInfo_tup.isNodule_bool,
            candidateInfo_tup.isNodule_bool
            ],
            dtype = torch.long
        )

        return (
                candidate_t,
                pos_t,
                candidateInfo_tup.series_uid,
                torch.tensor(center_irc),
        )



@functools.lru_cache(1, typed=True)
def getCt(series_uid):
    return Ct(series_uid)

def getCtRawCandidate(series_uid, center_xyz, width_irc):
    ct = getCt(series_uid)
    ct_chunk, center_irc = ct.getRawCandidate(center_xyz, width_irc)
    return ct_chunk, center_irc


"""
for test
"""
if __name__ == "__main__":
    CandidateInfo_list = getCandidateInfoList(requireOnDisk_bool=False)
    positiveInfo_list = [ x for x in CandidateInfo_list if x[0] ]
    diameter_list = [ x[1] for x in positiveInfo_list ]


    for i in range(0, len(diameter_list), 100):
        print('{:4} {:4.1f} mm'.format(i, diameter_list[i]))
