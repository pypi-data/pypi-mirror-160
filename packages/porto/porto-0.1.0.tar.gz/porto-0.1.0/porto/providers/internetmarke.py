import pycountry
from inema import Internetmarke, inema
from moneyed import EUR, Money
from zeep.xsd.valueobjects import CompoundValue

from porto.provider import (
    Address,
    CompanyAddress,
    Product,
    Stamp,
    StampFormat,
    StampProvider,
)


class InternetmarkeProvider(StampProvider):
    def __init__(
        self: "InternetmarkeProvider",
        partner_id: str,
        key: str,
        key_phase: str,
        username: str,
        password: str,
    ) -> None:
        self.im = Internetmarke(partner_id, key, key_phase)
        self.im.authenticate(username, password)

    def get_products(self: "InternetmarkeProvider") -> list[Product]:
        """Get all products provided by Internetmarke."""
        products = []
        for product_id, product in self.im.products.items():
            price = Money(float(product["cost_price"]), EUR)
            max_weight = int(product["max_weight"]) or None
            if product["international"]:
                countries = pycountry.countries
            else:
                countries = [pycountry.countries.get(alpha_2="DE")]
            new_product = Product(
                provider=self,
                product_id=int(product_id),
                name=product["name"],
                price=price,
                max_weight=max_weight,
                countries=countries,
            )
            products.append(new_product)

        return products

    def get_formats(self: "InternetmarkeProvider") -> list["StampFormat"]:
        """Get all formats provided by Internetmarke."""
        formats = []
        for stamp_format in inema.formats:
            new_format = StampFormat(
                provider=self,
                format_id=stamp_format["id"],
                name=stamp_format["name"],
                page_type=stamp_format["pageType"],
                width=stamp_format["pageLayout"]["size"]["x"],
                height=stamp_format["pageLayout"]["size"]["y"],
                orientation=stamp_format["pageLayout"]["orientation"],
                description=stamp_format["description"] or "",
                labels_x=stamp_format["pageLayout"]["labelCount"]["labelX"],
                labels_y=stamp_format["pageLayout"]["labelCount"]["labelY"],
                with_address=stamp_format["isAddressPossible"],
                with_image=stamp_format["isImagePossible"],
            )
            formats.append(new_format)
        return formats

    def _build_address(
        self: "InternetmarkeProvider", address: Address
    ) -> CompoundValue:
        """Convert address to a stamp_format compatible with Internetmarke API."""
        address_obj = self.im.build_addr(
            address.street,
            address.housenumber,
            address.zip_code,
            address.place,
            address.country.alpha_3,
            address.additional,
        )
        if isinstance(address, CompanyAddress):
            if address.first_name and address.last_name:
                pers_obj = self.im.build_pers_name(
                    address.first_name,
                    address.last_name,
                    address.salutation,
                    address.title,
                )
            else:
                pers_obj = None
            send_obj = self.im.build_comp_addr(address.company, address_obj, pers_obj)
        else:
            send_obj = self.im.build_pers_addr(
                address.first_name,
                address.last_name,
                address_obj,
                address.salutation,
                address.title,
            )
        return send_obj

    def buy_stamp(
        self: "InternetmarkeProvider",
        product: Product,
        stamp_format: StampFormat,
        sender: Address,
        receiver: Address,
    ) -> Stamp:
        """Buy and create a single stamp using Internetmarke."""
        sender_obj, receiver_obj = self._build_address(sender), self._build_address(
            receiver
        )
        pos = self.im.build_position(
            str(product.product_id), sender=sender_obj, receiver=receiver_obj, pdf=True
        )
        self.im.add_position(pos)
        stamp = self.im.checkoutPDF(stamp_format.format_id)
        return Stamp(
            pdf=stamp.pdf_bin,
            product=product,
            stamp_format=stamp_format,
            sender=sender,
            receiver=receiver,
        )
