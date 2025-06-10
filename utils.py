from app.models import DoctorToSlotMapModel, DoctorInfoModel, SlotModel, SlotDetailsModel


class DataPacker:

    def get_packed_slots(self, raw_slots: dict[str, dict[str, list[dict]]]):
        formatted_doctors = []

        for doctor_key, doctor_slots in raw_slots.items():
            doctor = self._create_doctor_info(doctor_key)
            slots = self._create_slots_for_doctor(doctor_slots)
            formatted_doctors.append(DoctorToSlotMapModel(doctor=doctor, slots=slots))

        return formatted_doctors

    def _create_doctor_info(self, doctor_key: str) -> DoctorInfoModel:
        code, name = doctor_key.split(':')
        return DoctorInfoModel(code=code, name=name)

    def _create_slots_for_doctor(self, doctor_slots: dict[str, list]) -> list[SlotModel]:
        slots = []

        for date, slot_details_list in doctor_slots.items():
            details = self._create_slot_details(slot_details_list)
            slots.append(SlotModel(date=date, details=details))

        return slots

    def _create_slot_details(self, slot_details_list) -> list[SlotDetailsModel]:
        return [SlotDetailsModel(**detail) for detail in slot_details_list]

    def get_unpacked_slots(self, doctors_slots: list[DoctorToSlotMapModel]) \
            -> dict[str, dict[str, list[dict]]]:
        raw_data = {}
        for doctor_slot in doctors_slots:
            doctor_key = self._create_doctor_key(doctor_slot.doctor)
            raw_data[doctor_key] = self._unpack_doctor_slots(doctor_slot.slots)

        return raw_data

    def _create_doctor_key(self, doctor: DoctorInfoModel) -> str:
        return f"{doctor.code}:{doctor.name}"

    def _unpack_doctor_slots(self, slots: list[SlotModel]) -> dict[str, list[dict]]:
        unpacked_slots = {}

        for slot in slots:
            unpacked_slots[slot.date] = self._unpack_slot_details(slot.details)

        return unpacked_slots

    def _unpack_slot_details(self, details: list[SlotDetailsModel]) -> list[dict]:
        return [detail.model_dump() for detail in details]