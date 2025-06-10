import unittest
from bot.bot_service import DoctorAppointmentBotService
from app.models import SlotModel, SlotDetailsModel, DoctorToSlotMapModel, DoctorInfoModel


class TestIsMessageFormattingCorrectly(unittest.TestCase):

    def test_is_list_of_slots_formats_correct(self):
        method = DoctorAppointmentBotService._get_all_slots_formated
        input_data = [
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

        fmt_string = method(input_data)
        expected_string = (
            "Для записи доступны следующие докторы и даты даты:\n\n"
            "doc0:\n"
            "15.04.2025\n"
            "18.04.2025\n\n"
            "doc1:\n"
            "14.04.2025\n"
        )
        self.assertEqual(expected_string, fmt_string)

if __name__ == '__main__':
    unittest.main()
