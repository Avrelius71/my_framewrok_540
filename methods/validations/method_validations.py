from pydantic import BaseModel, RootModel
from datetime import date
from typing import Optional
from typing import List


class RequestPostAuth(BaseModel):
    username: str
    password: str


class ResponsePostAuth(BaseModel):
    token: str


class BokingDates(BaseModel):
    checkin: date
    checkout: date


class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BokingDates
    additionalneeds: Optional[str] = None


class RequestCreateBooking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BokingDates
    additionalneeds: Optional[str] = None


class ResponseCreateBooking(BaseModel):
    bookingid: int
    booking: Booking


class BookingSummary(BaseModel):
    bookingid: int


class BookingIdsResponse(RootModel[List[BookingSummary]]):
    root: List[BookingSummary]


class PatchRequest(BaseModel):
    firstname: str
    lastname: str
    totalprice: Optional[int] = None
    depositpaid: Optional[bool] = None
    bookingdates: Optional[BokingDates] = None
    additionalneeds: Optional[str] = None