from sqlalchemy import(
    Column,
    Integer,
    String,
    Date,
    Time,
    Boolean,
    ForeignKey,
    Enum,
    DateTime,
    Text,
    UniqueConstraint,
    func,
    
)

from sqlalchemy.orm import declarative_base , relationship

Base = declarative_base()

import enum

# ------  Enums  ------

class AppointmentStatus(str , enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    
    
# -----  Doctor Model ------ 

class Doctor(Base):
    
    __tablename__= "doctors"
    
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String, nullable=False, index=True)
    specialty = Column(String, nullable=False, index=True)
    qualification = Column(String, nullable=True)
    languages_spoken = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    time_slots = relationship("TimeSlot", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    
    
# ------  Time Slot Model ------

class TimeSlot(Base):
    
    __tablename__ = "time_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id= Column(Integer, ForeignKey("doctors.id"), nullable=False)
    
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False) 
    end_time = Column(Time, nullable=False) 
    
    Slot_duration_minutes= Column(Integer, default=30)
    is_available = Column(Boolean, default=True, index=True)
    
    doctor = relationship("Doctor", back_populates="time_slots")
    appointment = relationship("Appointment", back_populates="slot", uselist=False)
    
    
    __table_args__ = (
    UniqueConstraint(
        "doctor_id",
        "date",
        "start_time",
        name="uq_doctor_slot"
    ),
)
    
    
# ------ Appointment Model -------

class Appointment(Base):
    
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)

    patient_name = Column(String, nullable=False)
    patient_contact = Column(String, nullable=False)
    symptoms_summary = Column(Text, nullable=True)
    
    booked_at = Column(DateTime(timezone=True),server_default=func.now())
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    
    doctor = relationship("Doctor", back_populates="appointments")
    slot = relationship("TimeSlot", back_populates="appointment")