from typing import Annotated

from fastapi import FastAPI, Depends

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit = False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database",
          tags = ["Database"],
          summary = "Setup database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True, "message": "Database setup"}

class BookPostSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookPostSchema):
    id: int
@app.post("/books",
          tags = ["Books"],
          summary = "Create a book")
async def add_book(data: BookPostSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {"success": True, "message": "Book created"}

@app.get("/books",
         tags = ["Books"],
         summary = "Get all books")
async def get_books(session: SessionDep):
    query = select(BookModel)
    results = await session.execute(query)
    return results.scalars().all()
