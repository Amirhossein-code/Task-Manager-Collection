from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225), nullable=False)

    # Time Stamps
    time_created = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc))

    # Task Model Relationship | A category can have many tasks (1 to Many relationship)
    tasks = relationship(
        "Task", back_populates="category", cascade="all, delete-orphan"
    )

    # User model relation ships | Users can create many categories (1 to Many relationship)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="categories")

    def __repr__(self):
        return f"<Category(title='{self.title}'>"
