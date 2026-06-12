from datetime import date, datetime, time, timedelta
import random

from db.models import (
    Doctor,
    TimeSlot,
    Appointment,
    AppointmentStatus,
)
from db.session import get_db


DOCTORS = [
    {
        "name": "Dr. Ahmed Khan",
        "specialty": "Cardiology",
        "qualification": "MBBS, FCPS Cardiology",
        "languages_spoken": "English, Urdu",
        "bio": "Experienced cardiologist.",
    },
    {
        "name": "Dr. Sara Malik",
        "specialty": "Cardiology",
        "qualification": "MBBS, MD Cardiology",
        "languages_spoken": "English, Urdu",
        "bio": "Heart specialist.",
    },
    {
        "name": "Dr. Ali Hassan",
        "specialty": "Neurology",
        "qualification": "MBBS, FCPS Neurology",
        "languages_spoken": "English, Urdu",
        "bio": "Neurology consultant.",
    },
    {
        "name": "Dr. Fatima Noor",
        "specialty": "Neurology",
        "qualification": "MBBS, MD Neurology",
        "languages_spoken": "English, Urdu",
        "bio": "Brain and nerve specialist.",
    },
    {
        "name": "Dr. John Smith",
        "specialty": "General Practice",
        "qualification": "MBBS",
        "languages_spoken": "English",
        "bio": "General physician.",
    },
    {
        "name": "Dr. Emily Brown",
        "specialty": "General Practice",
        "qualification": "MBBS",
        "languages_spoken": "English",
        "bio": "Family medicine specialist.",
    },
]

def generate_slots_for_doctor(doctor_id: int) -> list[TimeSlot]:
    slots = []

    today = date.today()

    for day_offset in range(7):
        slot_date = today + timedelta(days=day_offset)

        current_time = datetime.combine(
            slot_date,
            time(hour=9, minute=0),
        )

        end_of_day = datetime.combine(
            slot_date,
            time(hour=17, minute=0),
        )

        while current_time < end_of_day:
            start_time = current_time.time()

            end_time = (
                current_time + timedelta(minutes=30)
            ).time()

            slots.append(
                TimeSlot(
                    doctor_id=doctor_id,
                    date=slot_date,
                    start_time=start_time,
                    end_time=end_time,
                    Slot_duration_minutes=30,
                    is_available=True,
                )
            )

            current_time += timedelta(minutes=30)

    return slots

def seed_database() -> None:
    with get_db() as db:

        db.query(Appointment).delete()
        db.query(TimeSlot).delete()
        db.query(Doctor).delete()

        db.commit()

        doctors = []

        for doctor_data in DOCTORS:
            doctor = Doctor(**doctor_data)
            db.add(doctor)
            doctors.append(doctor)

        db.flush()

        all_slots = []

        for doctor in doctors:
            slots = generate_slots_for_doctor(
                doctor.id
            )

            db.add_all(slots)

            all_slots.extend(slots)

        db.flush()

        booked_slots = random.sample(
            all_slots,
            int(len(all_slots) * 0.30)
        )

        for slot in booked_slots:
            slot.is_available = False

            appointment = Appointment(
                doctor_id=slot.doctor_id,
                slot_id=slot.id,
                patient_name="Test Patient",
                patient_contact="03001234567",
                symptoms_summary="Seeded appointment",
                status=AppointmentStatus.confirmed,
            )

            db.add(appointment)

        print("Database seeded successfully.")
        
        

if __name__ == "__main__":
    seed_database()
