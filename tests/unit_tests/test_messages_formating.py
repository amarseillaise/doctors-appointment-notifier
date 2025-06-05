import unittest
from bot.bot_service import DoctorAppointmentBotService
from app.models import SlotModel, SlotDetailsModel


class TestIsMessageFormattingCorrectly(unittest.TestCase):

    def test_is_list_of_slots_formats_correct(self):
        method = DoctorAppointmentBotService._get_all_slots_formated
        detail_slots = [
            SlotDetailsModel(rid=0, eid=0, b_dt="09:00", edate="09:30", duration=30),
            SlotDetailsModel(rid=1, eid=1, b_dt="11:00", edate="11:30", duration=30),
            SlotDetailsModel(rid=2, eid=2, b_dt="15:00", edate="15:30", duration=30),
        ]
        slots = [
            SlotModel(date="15.04.2025", details=detail_slots.copy()),
            SlotModel(date="18.04.2025", details=detail_slots.copy()),
            SlotModel(date="21.05.2025", details=detail_slots.copy())
        ]

        fmt_string = method(slots)
        expected_string = (
            "Для записи доступны следующие даты:\n\n"
            "15.04.2025\n"
            "18.04.2025\n"
            "21.05.2025"
        )
        self.assertEqual(expected_string, fmt_string)

if __name__ == '__main__':
    unittest.main()
