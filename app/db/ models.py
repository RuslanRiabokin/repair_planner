# app/db/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    Numeric,
    ForeignKey,
    DateTime,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    # Первичный ключ пользователя
    id = Column(Integer, primary_key=True, index=True)

    # Полное имя (опционально)
    full_name = Column(String(255), nullable=True)

    # Номер телефона — уникален, nullable (может быть только email)
    phone = Column(String(32), unique=True, nullable=True)

    # Email — уникален, nullable (может быть только телефон)
    email = Column(String(255), unique=True, nullable=True, index=True)

    # Дата/время создания записи (на стороне сервера)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Ограничение: хотя бы phone или email должны быть заполнены
    __table_args__ = (
        CheckConstraint("phone IS NOT NULL OR email IS NOT NULL", name="ck_user_phone_or_email_not_null"),
    )

    # Связь к проектам (если планируем связывать проект с владельцем)
    projects = relationship("Project", back_populates="owner", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} phone={self.phone!r}>"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(512), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    comments = Column(Text, nullable=True)

    # Владелец проекта — nullable, чтобы проект мог быть без владельца
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    owner = relationship("User", back_populates="projects", lazy="selectin")

    rooms = relationship(
        "Room",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    planned_materials = relationship("PlannedMaterial", back_populates="project", lazy="selectin")
    expenses = relationship("Expense", back_populates="project", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name!r}>"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    area = Column(Numeric(10, 2), nullable=True)

    project = relationship("Project", back_populates="rooms", lazy="selectin")
    planned_materials = relationship("PlannedMaterial", back_populates="room", lazy="selectin")
    expenses = relationship("Expense", back_populates="room", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Room id={self.id} name={self.name!r} project_id={self.project_id}>"
