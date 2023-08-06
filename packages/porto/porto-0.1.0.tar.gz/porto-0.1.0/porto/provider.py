from dataclasses import dataclass, field
from typing import Any, Optional

import pycountry
from moneyed import Money


class Address:
    def __init__(
        self: "Address",
        street: str,
        housenumber: str,
        zip_code: str,
        place: str,
        country: pycountry.db.Data,
        additional: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        salutation: Optional[str] = None,
        title: Optional[str] = None,
        company: Optional[str] = None,
    ) -> None:
        self.street = street
        self.housenumber = housenumber
        self.zip_code = zip_code
        self.place = place
        self.country = country
        self.additional = additional
        self.first_name = first_name
        self.last_name = last_name
        self.salutation = salutation
        self.title = title
        self.company = company


class PersonAddress(Address):
    def __init__(
        self: "PersonAddress",
        first_name: str,
        last_name: str,
        *args: Any,
        **kwargs: Any
    ) -> None:
        kwargs["first_name"] = first_name
        kwargs["last_name"] = last_name
        kwargs["company"] = None
        super().__init__(*args, **kwargs)


class CompanyAddress(Address):
    def __init__(
        self: "CompanyAddress", company: str, *args: Any, **kwargs: Any
    ) -> None:
        kwargs["company"] = company
        super().__init__(*args, **kwargs)


class StampProvider:
    def __init__(self: "StampProvider", *args: Any, **kwargs: Any) -> None:
        pass

    def get_products(self: "StampProvider") -> list["Product"]:
        raise NotImplementedError()

    def get_products_by_id(self: "StampProvider") -> dict[int, "Product"]:
        return {product.product_id: product for product in self.get_products()}

    def get_formats(self: "StampProvider") -> list["StampFormat"]:
        raise NotImplementedError()

    def get_formats_by_id(self: "StampProvider") -> dict[int, "StampFormat"]:
        return {
            stamp_format.format_id: stamp_format for stamp_format in self.get_formats()
        }

    def buy_stamp(
        self: "StampProvider",
        product: "Product",
        stamp_format: "StampFormat",
        sender: Address,
        receiver: Address,
    ) -> "Stamp":
        raise NotImplementedError()


@dataclass
class Stamp:
    """A single stamp."""

    product: "Product"
    stamp_format: "StampFormat"
    sender: Address
    receiver: Address
    pdf: bytes


@dataclass
class Product:
    """A stamp product."""

    provider: StampProvider
    product_id: int
    name: str
    price: Money
    max_weight: Optional[int] = None
    countries: Optional[list[pycountry.db.Data]] = field(
        default_factory=lambda: pycountry.countries
    )


@dataclass
class StampFormat:
    """A paper/label stamp_format."""

    provider: StampProvider
    format_id: int
    name: str
    page_type: str
    width: int
    height: int
    orientation: str
    description: str = ""
    labels_x: int = 1
    labels_y: int = 1
    with_address: bool = False
    with_image: bool = False
