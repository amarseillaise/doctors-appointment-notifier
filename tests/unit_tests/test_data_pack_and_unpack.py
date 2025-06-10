import unittest

from utils import DataPacker
from app.models import SlotModel, SlotDetailsModel, DoctorInfoModel, DoctorToSlotMapModel


class TestPackDoctorSlotsInfo(unittest.TestCase):

    def test_is_list_of_slots_formats_correct(self):
        method = DataPacker().get_packed_slots
        infos = {
            '0:doc0': {
                '15.04.2025': [
                    {
                        'rid': 0,
                        'eid': 0,
                        'b_dt': '09:00',
                        'edate': '09:30',
                        'duration': 30,
                    },
                    {
                        'rid': 1,
                        'eid': 1,
                        'b_dt': '10:00',
                        'edate': '10:30',
                        'duration': 30,
                    },
                ],
                '18.04.2025': [
                    {
                        'rid': 2,
                        'eid': 2,
                        'b_dt': '09:00',
                        'edate': '09:30',
                        'duration': 30,
                    },
                ],
            },
            '1:doc1': {
                '14.04.2025': [
                    {
                        'rid': 3,
                        'eid': 3,
                        'b_dt': '15:00',
                        'edate': '15:30',
                        'duration': 30,
                    },
                ],
            },
        }

        formated_infos = method(infos)
        expected_infos = [
            DoctorToSlotMapModel(
                doctor=DoctorInfoModel(code='0', name='doc0'),
                slots=[
                    SlotModel(date='15.04.2025',
                              details=[
                                  SlotDetailsModel(rid=0, eid=0, b_dt='09:00', edate='09:30', duration=30),
                                  SlotDetailsModel(rid=1, eid=1, b_dt='10:00', edate='10:30', duration=30),
                              ]
                    ),
                    SlotModel(date='18.04.2025',
                              details=[
                                  SlotDetailsModel(rid=2, eid=2, b_dt='09:00', edate='09:30', duration=30),
                              ]
                    ),
                ]
            ),

            DoctorToSlotMapModel(
                doctor=DoctorInfoModel(code='1', name='doc1'),
                slots=[
                    SlotModel(date='14.04.2025',
                              details=[
                                  SlotDetailsModel(rid=3, eid=3, b_dt='15:00', edate='15:30', duration=30),
                              ]
                    ),
                ]
            ),
        ]
        self.assertEqual(expected_infos, formated_infos)


if __name__ == '__main__':
    unittest.main()

SlotDetailsModel(rid=0, eid=0, b_dt="09:00", edate="09:30", duration=30),
