from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from service.orm.database import Base


class PiggyBank(Base):
    __tablename__ = "piggybank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    broken = Column(Boolean, default=False, nullable=False)

    wealth = relationship("Wealth")

    def __repr__(self):
        return f"<PiggyBank (id={self.id}, name={self.name}, broken={self.broken})>"


class Change(Base):
    __tablename__ = "change"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String, nullable=False)
    value = Column(Integer)

    def __repr__(self):
        return f"<Change (id={self.id}, kind={self.kind}, value={self.value})>"


class Wealth(Base):
    __tablename__ = "wealth"

    id = Column(Integer, primary_key=True, index=True)
    piggybank_id = Column(Integer, ForeignKey("piggybank.id"), nullable=False)
    change_id = Column(Integer, ForeignKey("change.id"), nullable=False)

    change = relationship("Change")

    def __repr__(self):
        return (
            f"<Wealth (piggybank_id={self.piggybank_id}, change_id={self.change_id})>"
        )
