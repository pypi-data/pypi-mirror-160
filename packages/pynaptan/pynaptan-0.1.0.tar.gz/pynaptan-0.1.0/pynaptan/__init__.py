import csv
import logging
from collections.abc import Iterator
from datetime import datetime
from http import HTTPStatus
from io import StringIO
from pathlib import Path
from typing import Optional, Union

import httpx
from pydantic import BaseModel, Field, ValidationError, validator

NAPTAN_CSV_URL = "https://naptan.api.dft.gov.uk/v1/access-nodes"

logger = logging.getLogger(__name__)


class PyNaptanError(Exception):
    """Base Exception for PyNaptan."""


class Stop(BaseModel):
    """Model for NaPTAN Stops."""

    atco_code: str = Field(..., alias="ATCOCode")
    naptan_code: str = Field(..., alias="NaptanCode")
    plate_code: str = Field(..., alias="PlateCode")
    cleardown_code: str = Field(..., alias="CleardownCode")
    common_name: str = Field(..., alias="CommonName")
    common_name_lang: str = Field(..., alias="CommonNameLang")
    short_common_name: str = Field(..., alias="ShortCommonName")
    short_common_name_lang: str = Field(..., alias="ShortCommonNameLang")
    landmark: str = Field(..., alias="Landmark")
    landmark_lang: str = Field(..., alias="LandmarkLang")
    street: str = Field(..., alias="Street")
    street_lang: str = Field(..., alias="StreetLang")
    crossing: str = Field(..., alias="Crossing")
    crossing_lang: str = Field(..., alias="CrossingLang")
    indicator: str = Field(..., alias="Indicator")
    indicator_lang: str = Field(..., alias="IndicatorLang")
    bearing: str = Field(..., alias="Bearing")
    nptg_locality_code: str = Field(..., alias="NptgLocalityCode")
    nptg_locality_name: str = Field(..., alias="LocalityName")
    parent_locality_name: str = Field(..., alias="ParentLocalityName")
    grand_parent_locality_name: str = Field(..., alias="GrandParentLocalityName")
    town: str = Field(..., alias="Town")
    town_lang: str = Field(..., alias="TownLang")
    suburb: str = Field(..., alias="Suburb")
    suburb_lang: str = Field(..., alias="SuburbLang")
    locality_centre: Optional[bool] = Field(..., alias="LocalityCentre")
    grid_type: str = Field(..., alias="GridType")
    easting: int = Field(..., alias="Easting")
    northing: int = Field(..., alias="Northing")
    longitude: Optional[float] = Field(..., alias="Longitude")
    latitude: Optional[float] = Field(..., alias="Latitude")
    stop_type: str = Field(..., alias="StopType")
    bus_stop_type: str = Field(..., alias="BusStopType")
    timing_status: str = Field(..., alias="TimingStatus")
    default_wait_time: str = Field(..., alias="DefaultWaitTime")
    notes: str = Field(..., alias="Notes")
    notes_lang: str = Field(..., alias="NotesLang")
    administrative_area_code: str = Field(..., alias="AdministrativeAreaCode")
    creation_date_time: datetime = Field(..., alias="CreationDateTime")
    modification_date_time: Optional[datetime] = Field(
        ..., alias="ModificationDateTime"
    )
    revision_number: int = Field(0, alias="RevisionNumber")
    modification: str = Field(..., alias="Modification")
    status: str = Field(..., alias="Status")

    @validator(
        "locality_centre",
        "longitude",
        "latitude",
        "modification_date_time",
        pre=True,
    )
    def handle_empty_string(cls, stop_value: str) -> Optional[str]:
        """Validate empty strings."""
        return None if stop_value == "" else stop_value

    @validator("revision_number", pre=True)
    def validate_revision_number(cls, stop_value: Union[str, int]) -> int:
        """Validate revision numbers."""
        return 0 if stop_value == "" else int(stop_value)


def iload_from_string(csv_str: str) -> Iterator[Stop]:
    """Load NaPTAN Stops from a string representation of a csv."""
    reader = csv.DictReader(StringIO(csv_str), delimiter=",")
    for idx, entry in enumerate(reader):
        try:
            stop = Stop.parse_obj(entry)
        except ValidationError:
            logger.warn("Unable to parse row {0}, skipping.".format(idx))
            continue
        yield stop


def iload_from_filepath(filepath: Path) -> Iterator[Stop]:
    """Load NaPTAN Stops from a filapath to a NaPTAN Stops.csv file."""
    with filepath.open("r") as csvfile:
        return iload_from_string(csvfile.read())


def iload_from_api(url: str) -> Iterator[Stop]:
    """Load NaPTAN Stops from the NaPTAN API."""
    api_params = {"dataFormat": "csv"}
    response = httpx.get(url, params=api_params)
    if response.status_code != HTTPStatus.OK:
        raise PyNaptanError("Unable to load stops.")
    return iload_from_string(response.text)
