from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from service.orm.database import Base


class Tirelire(Base):
    __tablename__ = "tirelire"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    broken = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Tirelire (id={self.id}, name={self.name}, broken={self.broken})>"


class Monnaie(Base):
    __tablename__ = "monnaie"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String, nullable=False)
    value = Column(Integer)

    def __repr__(self):
        return f"<Monnaie (id={self.id}, kind={self.kind}, value={self.value})>"


class Richesse(Base):
    __tablename__ = "richesse"

    tirelire_id = Column(Integer, ForeignKey("tirelire.id"), nullable=False)
    monnaie_id = Column(Integer, ForeignKey("monnaie.id"), nullable=False)
    count = Column(Integer, nullable=False)

    __mapper_args__ = {"primary_key": [tirelire_id, monnaie_id]}

    def __repr__(self):
        return f"<Richesse (tirelire_id={self.tirelire_id}, monnaie_id={self.monnaie_id}, count={self.count})>"
